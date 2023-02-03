from email.policy import default
import hashlib
import os
from random import choices
from secrets import choice
from typing import Any, Dict, Tuple
import uuid
from attr import fields
from django.apps import apps
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField, ForeignKey
from itertools import chain
from django.forms import ModelForm
import datetime
import time
from django.core.files.storage import FileSystemStorage
from root.settings import BASE_DIR
from django.utils._os import safe_join
from django.utils.encoding import filepath_to_uri
from urllib.parse import urljoin


class BaseModel(models.Model):
    createAt = models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)
    updateAt = models.DateTimeField(auto_now=True, help_text='更新时间', null=True)
    dept_belong_id = models.IntegerField(help_text='所属部门id', null=True, blank=True)
    creator_id = models.IntegerField(help_text='创建人id', null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = '基础模型'
        verbose_name_plural = verbose_name
        ordering = ('-createAt', )

    def model_to_dict(self, fields=None, exclude=None, deep=2):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            # if not getattr(f, "editable", False):
            #     continue
            # if fields is not None and f.name not in fields:
            #     continue
            # if exclude and f.name in exclude:
            #     continue
            v = f.value_from_object(self)
            if isinstance(f, ManyToManyField):  # 外键序列化,使用它必须继承本模型
                if deep > 0:
                    v = [i.model_to_dict(deep=deep - 1) for i in v] if v else []
                else:
                    v = [i.id for i in v] if v else []
            elif isinstance(f, ForeignKey):  # 外键序列化,使用它必须继承本模型
                if deep > 0:
                    v = f.related_model.objects.get(pk=v).model_to_dict(deep=deep - 1) if v else None
                else:
                    pass
            if isinstance(f, DateTimeField):
                v = v.strftime('%Y-%m-%d %H:%M:%S') if v else None
            data[f.name] = v

        return data


def make_file_name(instance, filename):
    today = datetime.date.today()
    return f"upload/{today.year}/{today.month}/{today.day}/{str(time.time())+'_'+filename}"


class storage(FileSystemStorage):

    def __init__(self):
        super().__init__()
        # self._location = os.path.join(BASE_DIR, "media")  # 自定义文件的路径或者使用settings中的MEDIA_ROOT
        # self._base_url = '/media/'

    def _save(self, name, content):
        name = super()._save(name, content)
        print('_save', self.base_url.lstrip('/'), name)
        return self.base_url.lstrip('/') + name  #TODO:文件上传- 保存文件的路径拼接上base_url

    def path(self, name):  #构造文件的路径 删除拼接上的base_url
        print('path', safe_join(self.location, name.lstrip(self.base_url.lstrip('/'))))
        return safe_join(self.location, name.lstrip(self.base_url.lstrip('/')))

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        url = filepath_to_uri(name)
        if url is not None:
            url = url.lstrip("/")
        print(url)
        return url

    def delete(self, name):
        if not name:
            raise ValueError("The name must be given to delete().")
        name = self.path(name)
        # If the file or directory exists, delete it from the filesystem.
        try:
            if os.path.isdir(name):
                os.rmdir(name)
            else:
                os.remove(name)
        except FileNotFoundError:
            # FileNotFoundError is raised if the file or directory was removed
            # concurrently.
            pass


fs = storage()


# TODO:文件上传-模型/表单
class File(BaseModel):
    file = models.FileField(upload_to=make_file_name, max_length=200, storage=fs)
    name = models.CharField(max_length=100)

    def delete(self, using: Any = ..., keep_parents: bool = ...) -> Tuple[int, Dict[str, int]]:
        self.file.delete()
        return super().delete()

    class Meta:
        db_table = "File"
        verbose_name = "文件"


class FileForm(ModelForm):

    class Meta:
        model = File
        fields = '__all__'


class Dept(BaseModel):
    name = models.CharField(max_length=20, help_text='部门名称')
    key = models.CharField(max_length=50, help_text="标识符", null=True)
    parent = models.ForeignKey(to='self', on_delete=models.PROTECT, null=True, blank=True)
    sort = models.IntegerField(default=1, help_text="排序")
    owner = models.CharField(max_length=32, null=True, blank=True, help_text="负责人")

    class Meta:
        db_table = "Dept"
        verbose_name = "部门"
        verbose_name_plural = verbose_name
        ordering = ("sort", )


class Menu(BaseModel):
    parent = models.ForeignKey(
        to="Menu",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_constraint=False,
        help_text="上级菜单",
    )
    icon = models.CharField(max_length=64, null=True, blank=True, help_text="菜单图标")
    label = models.CharField(max_length=64, help_text="菜单名称")
    sort = models.IntegerField(default=1, null=True, blank=True, help_text="显示排序")
    ISLINK_CHOICES = (
        (0, "否"),
        (1, "是"),
    )
    is_link = models.BooleanField(default=False, help_text="是否外链")
    is_catalog = models.BooleanField(default=False, help_text="是否目录")
    path = models.CharField(max_length=128, null=True, blank=True, help_text="路由地址")
    component = models.CharField(max_length=128, null=True, blank=True, help_text="组件地址")
    name = models.CharField(max_length=50, null=True, blank=True, help_text="路由名称")
    disable = models.BooleanField(default=False, null=True, blank=True, help_text="禁用状态")
    cache = models.BooleanField(default=False, null=True, blank=True, help_text="是否页面缓存")

    class Meta:
        db_table = "Menu"
        verbose_name = "菜单表"
        verbose_name_plural = verbose_name
        ordering = ("sort", )


class MenuInterface(BaseModel):
    name = models.CharField(max_length=50, help_text='接口名称')
    key = models.CharField(max_length=50, help_text="标识符", null=True)
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(choices=METHOD_CHOICES, help_text='请求方式')
    path = models.CharField(max_length=100, help_text="接口地址")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = "MenuInterface"
        verbose_name = "菜单接口"
        verbose_name_plural = verbose_name


class Role(BaseModel):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50, help_text="标识符", null=True)
    PERMISSION_CHOICES = (
        (0, "仅本人数据权限"),
        (1, "本部门及以下数据权限"),
        (2, "本部门数据权限"),
        (3, "全部数据权限"),
        (4, "自定数据权限"),
    )
    permission = models.IntegerField(choices=PERMISSION_CHOICES, help_text="数据权限范围", default=0)
    # dept = models.ManyToManyField(Dept)
    menu = models.ManyToManyField(Menu, blank=True)
    menu_interface = models.ManyToManyField(MenuInterface, blank=True)
    is_admin = models.BooleanField(default=False, help_text='是否为管理员')

    class Meta:
        db_table = "Role"
        verbose_name = "角色"
        verbose_name_plural = verbose_name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, BaseModel):
    name = models.CharField(max_length=100, help_text='名称', null=True)
    openid = models.CharField(max_length=100, help_text='微信openid', unique=True, null=True)
    username = models.CharField(max_length=100, help_text='用户名', unique=True)
    role = models.JSONField(default=list, help_text='用户角色')
    type = models.IntegerField(choices=((1, '前端'), (2, '后端')), default=1, help_text='用户类型')
    dept = models.ForeignKey(Dept, on_delete=models.PROTECT, null=True, help_text="所属部门")
    email = models.EmailField(help_text="邮箱", null=True)
    phone = models.CharField(max_length=12, help_text="电话", null=True)
    USERNAME_FIELD = 'username'
    objects = UserManager()
    is_super = models.BooleanField(default=False, help_text='是否为超级管理员')

    def set_password(self, raw_password):  # TODO:model-用户表-设置密码方式
        # encode(encoding="UTF-8")  之后 通过索引获取的值为unciode编码值
        super().set_password(hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest())

    # def save(self, *args, **kwargs) -> None:
    #     self.set_password(self.password)
    #     super().save(*args, **kwargs)

    class Meta:
        db_table = "User"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name


class Area(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称", help_text="名称")
    code = models.CharField(max_length=20, verbose_name="地区编码", help_text="地区编码", unique=True, db_index=True)
    level = models.BigIntegerField(verbose_name="地区层级(0省份 1城市 2区县 3乡级)", help_text="地区层级(0省份 1城市 2区县 3乡级)")
    lat = models.CharField(max_length=10, help_text='', null=True, blank=True)
    lng = models.CharField(max_length=10, help_text='', null=True, blank=True)
    pcode = models.ForeignKey(
        to="self",
        verbose_name="父地区编码",
        to_field="code",
        on_delete=models.CASCADE,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="父地区编码",
    )

    class Meta:
        db_table = "Area"
        verbose_name = "地区表"
        verbose_name_plural = verbose_name
        ordering = ("code", )

    def __str__(self):
        return f"{self.name}"


class LoginLog(BaseModel):
    LOGIN_TYPE_CHOICES = ((1, "普通登录"), )
    username = models.CharField(max_length=32, verbose_name="登录用户名", null=True, blank=True, help_text="登录用户名")
    ip = models.CharField(max_length=32, verbose_name="登录ip", null=True, blank=True, help_text="登录ip")
    agent = models.TextField(verbose_name="agent信息", null=True, blank=True, help_text="agent信息")
    browser = models.CharField(max_length=200, verbose_name="浏览器名", null=True, blank=True, help_text="浏览器名")
    os = models.CharField(max_length=200, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    continent = models.CharField(max_length=50, verbose_name="州", null=True, blank=True, help_text="州")
    country = models.CharField(max_length=50, verbose_name="国家", null=True, blank=True, help_text="国家")
    province = models.CharField(max_length=50, verbose_name="省份", null=True, blank=True, help_text="省份")
    city = models.CharField(max_length=50, verbose_name="城市", null=True, blank=True, help_text="城市")
    district = models.CharField(max_length=50, verbose_name="县区", null=True, blank=True, help_text="县区")
    isp = models.CharField(max_length=50, verbose_name="运营商", null=True, blank=True, help_text="运营商")
    area_code = models.CharField(max_length=50, verbose_name="区域代码", null=True, blank=True, help_text="区域代码")
    country_english = models.CharField(max_length=50, verbose_name="英文全称", null=True, blank=True, help_text="英文全称")
    country_code = models.CharField(max_length=50, verbose_name="简称", null=True, blank=True, help_text="简称")
    longitude = models.CharField(max_length=50, verbose_name="经度", null=True, blank=True, help_text="经度")
    latitude = models.CharField(max_length=50, verbose_name="纬度", null=True, blank=True, help_text="纬度")
    login_type = models.IntegerField(default=1, choices=LOGIN_TYPE_CHOICES, verbose_name="登录类型", help_text="登录类型")

    class Meta:
        db_table = "LoginLog"
        verbose_name = "登录日志"
        verbose_name_plural = verbose_name
        ordering = ("-createAt", )


class Enterprise(BaseModel):
    name = models.CharField(max_length=100, verbose_name="名称", help_text="名称", null=True)
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING, null=True, to_field="code")
    file = models.JSONField(default=list, help_text="文件")
    image = models.JSONField(default=list, help_text="图片")  # JSON类型前端直接传列表就可以,不需要JSON化, 前端axios接收后也不用解析直接使用

    class Meta:
        db_table = "Enterprise"
        verbose_name = "企业信息"
        verbose_name_plural = verbose_name
