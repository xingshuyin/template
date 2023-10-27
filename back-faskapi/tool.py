from base64 import b32encode
from hashlib import sha3_224
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Type

from pydantic import ConfigDict, Field, computed_field, create_model
from pydantic._internal._decorators import PydanticDescriptorProxy
from tortoise.contrib.pydantic.creator import PydanticMeta, _br_it, _cleandoc, _pydantic_recursion_protector
from tortoise.contrib.pydantic.base import PydanticModel
from tortoise.contrib.pydantic.utils import get_annotations
from tortoise.fields import JSONField, relational
if TYPE_CHECKING:  # pragma: nocoverage
    from tortoise.models import Model
_MODEL_INDEX: Dict[str, Type[PydanticModel]] = {}


def pydantic_model_creator(
    cls: "Type[Model]",
    *,
    name=None,
    exclude: Tuple[str, ...] = (),
    include: Tuple[str, ...] = (),
    computed: Tuple[str, ...] = (),
    optional: Tuple[str, ...] = (),
    allow_cycles: Optional[bool] = None,
    sort_alphabetically: Optional[bool] = None,
    _stack: tuple = (),
    exclude_readonly: bool = False,
    meta_override: Optional[Type] = None,
    model_config: Optional[ConfigDict] = None,
) -> Type[PydanticModel]:
    """
    Function to build `Pydantic Model <https://pydantic-docs.helpmanual.io/usage/models/>`__ off Tortoise Model.

    :param _stack: Internal parameter to track recursion
    :param cls: The Tortoise Model
    :param name: Specify a custom name explicitly, instead of a generated name.
    :param exclude: Extra fields to exclude from the provided model.
    :param include: Extra fields to include from the provided model.
    :param computed: Extra computed fields to include from the provided model.
    :param optional: Extra optional fields for the provided model.
    :param allow_cycles: Do we allow any cycles in the generated model?
        This is only useful for recursive/self-referential models.

        A value of ``False`` (the default) will prevent any and all backtracking.
    :param sort_alphabetically: Sort the parameters alphabetically instead of Field-definition order.

        The default order would be:

            * Field definition order +
            * order of reverse relations (as discovered) +
            * order of computed functions (as provided).
    :param exclude_readonly: Build a subset model that excludes any readonly fields
    :param meta_override: A PydanticMeta class to override model's values.
    :param model_config: A custom config to use as pydantic config.

        Note: Created pydantic model uses config_class parameter and PydanticMeta's
            config_class as its Config class's bases(Only if provided!), but it
            ignores ``fields`` config. pydantic_model_creator will generate fields by
            include/exclude/computed parameters automatically.
    """

    # Fully qualified class name
    fqname = cls.__module__ + "." + cls.__qualname__
    postfix = ""

    def get_name() -> str:
        # If arguments are specified (different from the defaults), we append a hash to the
        # class name, to make it unique
        # We don't check by stack, as cycles get explicitly renamed.
        # When called later, include is explicitly set, so fence passes.
        nonlocal postfix
        is_default = (
            exclude == ()
            and include == ()
            and computed == ()
            and sort_alphabetically is None
            and allow_cycles is None
        )
        hashval = (
            f"{fqname};{exclude};{include};{computed};{_stack}:{sort_alphabetically}:{allow_cycles}"
        )
        postfix = (
            "." + b32encode(sha3_224(hashval.encode("utf-8")).digest()).decode("utf-8").lower()[:6]
            if not is_default
            else ""
        )
        return fqname + postfix

    # We need separate model class for different exclude, include and computed parameters
    _name = name or get_name()
    has_submodel = False

    # Get settings and defaults
    meta = getattr(cls, "PydanticMeta", PydanticMeta)

    def get_param(attr: str) -> Any:
        if meta_override:
            return getattr(meta_override, attr, getattr(meta, attr, getattr(PydanticMeta, attr)))
        return getattr(meta, attr, getattr(PydanticMeta, attr))

    default_include: Tuple[str, ...] = tuple(get_param("include"))
    default_exclude: Tuple[str, ...] = tuple(get_param("exclude"))
    default_computed: Tuple[str, ...] = tuple(get_param("computed"))
    default_config: Optional[ConfigDict] = get_param("model_config")

    backward_relations: bool = bool(get_param("backward_relations"))

    max_recursion: int = int(get_param("max_recursion"))
    exclude_raw_fields: bool = bool(get_param("exclude_raw_fields"))
    _sort_fields: bool = (
        bool(get_param("sort_alphabetically"))
        if sort_alphabetically is None
        else sort_alphabetically
    )
    _allow_cycles: bool = bool(get_param("allow_cycles") if allow_cycles is None else allow_cycles)

    # Update parameters with defaults
    include = tuple(include) + default_include
    exclude = tuple(exclude) + default_exclude
    computed = tuple(computed) + default_computed

    annotations = get_annotations(cls)

    pconfig = PydanticModel.model_config.copy()
    if default_config:
        pconfig.update(default_config)
    if model_config:
        pconfig.update(model_config)
    if "title" not in pconfig:
        pconfig["title"] = name or cls.__name__
    if "extra" not in pconfig:
        pconfig["extra"] = "forbid"

    properties: Dict[str, Any] = {}

    # Get model description
    model_description = cls.describe(serializable=False)

    # Field map we use
    field_map: Dict[str, dict] = {}
    pk_raw_field: str = ""

    def field_map_update(keys: tuple, is_relation=True) -> None:
        nonlocal pk_raw_field

        for key in keys:
            fds = model_description[key]
            if isinstance(fds, dict):
                fds = [fds]
            for fd in fds:
                n = fd["name"]
                if key == "pk_field":
                    pk_raw_field = n
                # Include or exclude field
                if (include and n not in include) or n in exclude:
                    continue
                # Remove raw fields
                raw_field = fd.get("raw_field", None)
                if raw_field is not None and exclude_raw_fields and raw_field != pk_raw_field:
                    del field_map[raw_field]
                field_map[n] = fd

    # Update field definitions from description
    if not exclude_readonly:
        field_map_update(("pk_field",), is_relation=False)
    field_map_update(("data_fields",), is_relation=False)
    if not exclude_readonly:
        included_fields: tuple = (
            "fk_fields",
            "o2o_fields",
            "m2m_fields",
        )
        if backward_relations:
            included_fields = (
                *included_fields,
                "backward_fk_fields",
                "backward_o2o_fields",
            )

        field_map_update(included_fields)
        # Add possible computed fields
        field_map.update(
            {
                k: {"field_type": callable, "function": getattr(cls, k), "description": None}
                for k in computed
            }
        )

    # Sort field map (Python 3.7+ has guaranteed ordered dictionary keys)
    if _sort_fields:
        # Sort Alphabetically
        field_map = {k: field_map[k] for k in sorted(field_map)}
    else:
        # Sort to definition order
        field_map = {
            k: field_map[k] for k in tuple(cls._meta.fields_map.keys()) + computed if k in field_map
        }
    # Process fields
    for fname, fdesc in field_map.items():
        comment = ""
        json_schema_extra: Dict[str, Any] = {}
        fconfig: Dict[str, Any] = {
            "json_schema_extra": json_schema_extra,
        }
        field_type = fdesc["field_type"]
        field_default = fdesc.get("default")

        def get_submodel(_model: "Type[Model]") -> Optional[Type[PydanticModel]]:
            """Get Pydantic model for the submodel"""
            nonlocal exclude, _name, has_submodel

            if _model:
                new_stack = _stack + ((cls, fname, max_recursion),)

                # Get pydantic schema for the submodel
                prefix_len = len(fname) + 1
                pmodel = _pydantic_recursion_protector(
                    _model,
                    exclude=tuple(
                        str(v[prefix_len:]) for v in exclude if v.startswith(fname + ".")
                    ),
                    include=tuple(
                        str(v[prefix_len:]) for v in include if v.startswith(fname + ".")
                    ),
                    computed=tuple(
                        str(v[prefix_len:]) for v in computed if v.startswith(fname + ".")
                    ),
                    stack=new_stack,
                    allow_cycles=_allow_cycles,
                    sort_alphabetically=sort_alphabetically,
                )
            else:
                pmodel = None

            # If the result is None it has been excluded and we need to exclude the field
            if pmodel is None:
                exclude += (fname,)
            else:
                has_submodel = True
            # We need to rename if there are duplicate instances of this model
            if cls in (c[0] for c in _stack):
                _name = name or get_name()

            return pmodel

        # Foreign keys and OneToOne fields are embedded schemas
        if (
            field_type is relational.ForeignKeyFieldInstance
            or field_type is relational.OneToOneFieldInstance
            or field_type is relational.BackwardOneToOneRelation
        ):
            model = get_submodel(fdesc["python_type"])
            if model:
                if fdesc.get("nullable"):
                    json_schema_extra["nullable"] = True
                if fdesc.get("nullable") or field_default is not None:
                    model = Optional[model]  # type: ignore

                properties[fname] = model

        # Backward FK and ManyToMany fields are list of embedded schemas
        elif (
            field_type is relational.BackwardFKRelation
            or field_type is relational.ManyToManyFieldInstance
        ):
            model = get_submodel(fdesc["python_type"])
            if model:
                properties[fname] = List[model]  # type: ignore

        # Computed fields as methods
        elif field_type is callable:
            func = fdesc["function"]
            annotation = get_annotations(cls, func).get("return", None)
            comment = _cleandoc(func)
            if annotation is not None:
                properties[fname] = computed_field(return_type=annotation, description=comment)(
                    func
                )

        # Json fields
        elif field_type is JSONField:
            properties[fname] = Any
        # Any other tortoise fields
        else:
            annotation = annotations.get(fname, None)
            if "readOnly" in fdesc["constraints"]:
                json_schema_extra["readOnly"] = fdesc["constraints"]["readOnly"]
                del fdesc["constraints"]["readOnly"]
            fconfig.update(fdesc["constraints"])
            ptype = fdesc["python_type"]
            if fdesc.get("nullable"):
                json_schema_extra["nullable"] = True
            if fdesc.get("nullable") or field_default is not None or fname in optional:
                ptype = Optional[ptype]
            if not (exclude_readonly and fdesc["constraints"].get("readOnly") is True):
                properties[fname] = annotation or ptype

        if fname in properties and not isinstance(properties[fname], tuple):
            fconfig["title"] = fname.replace("_", " ").title()
            description = comment or _br_it(fdesc.get("docstring") or fdesc["description"] or "")
            if description:
                fconfig["description"] = description
            ftype = properties[fname]
            if isinstance(ftype, PydanticDescriptorProxy):
                continue
            if field_default is not None and not callable(field_default):
                properties[fname] = (ftype, Field(default=field_default, **fconfig))
            else:
                properties[fname] = (ftype, Field(**fconfig, default=None))

    # Here we endure that the name is unique, but complete objects are still labeled verbatim
    if not has_submodel:
        _name = name or f"{fqname}.leaf"
    elif has_submodel:
        _name = name or get_name()

    # Here we de-dup to ensure that a uniquely named object is a unique object
    # This fixes some Pydantic constraints.
    if _name in _MODEL_INDEX:
        return _MODEL_INDEX[_name]

    # Creating Pydantic class for the properties generated before
    properties["model_config"] = pconfig
    model = create_model(
        _name,
        __base__=PydanticModel,
        **properties,
    )
    # Copy the Model docstring over
    model.__doc__ = _cleandoc(cls)
    # Store the base class
    model.model_config["orig_model"] = cls  # type: ignore
    # Store model reference so we can de-dup it later on if needed.
    _MODEL_INDEX[_name] = model
    return model


if __name__ == "__main__":
    a = 'sssss'
    print("{} \\{\\}". format(a))
