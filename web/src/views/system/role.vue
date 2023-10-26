<template>
    <div class="main-top">
        <div class="search">
            <f-input v-model="form.label" label="名称" />
            <f-timerange v-model="special_form.range" />
        </div>
        <div class="tool">
            <el-button size="small" type="danger"
                @click="mult_delete_(`/${attrs.base_url}/mult_destroy/`, attrs.selects, get_data)"
                v-if="attrs.selects.length > 0">批量删除
            </el-button>
            <el-button type="primary" v-if="attrs.can_create" icon="Plus" circle
                @click="attrs.adding = true; attrs.add_form = {}; attrs.submit_type = 'add'; attrs.submit_type = 'add'" />
            <f-columns-edit v-if="attrs.columns" v-model="attrs.columns" :base_url="attrs.base_url"></f-columns-edit>
        </div>
    </div>


    <div class="main-table">
        <el-table :data="attrs.data" v-loading.fullscreen:false="attrs.loading" stripe border size="small"
            :expand-row-keys="attrs.expandedRowKeys" :row-key="(row) => { return row.id }"
            @selection-change="(d) => { select_(d, attrs) }" @sort-change="(d) => { sort_(d, form) }"
            :cell-style="() => { return { 'text-align': 'center' } }">
            <f-columns v-if="attrs.columns" v-model="attrs.columns" v-model:attrs="attrs" :callback_delete="get_data"
                :opt_width="250">
                <template #opt="{ scope }">
                    <el-button size="small" type="primary"
                        @click="attrs.show_permissions = true; attrs.role_id = scope.row.id; GetRolePermision()">
                        权限管理
                    </el-button>
                </template>
            </f-columns>
        </el-table>
        <t-page v-model:page="form.page" v-model:limit="form.limit" :total="attrs.total"></t-page>
    </div>


    <el-dialog v-model="attrs.adding" class="add_form" :title="attrs.submit_type == 'add' ? '新增' : '编辑'" width="50%"
        :modal="false">
        <el-form :model="attrs.add_form" label-width="120px" :rules="rules" ref="form_dom">
            <el-form-item label="角色名称" prop="name">
                <el-input v-model="attrs.add_form.name" />
            </el-form-item>
            <el-form-item label="角色标识" prop="key">
                <el-input v-model="attrs.add_form.key" />
            </el-form-item>
            <el-form-item label="是否管理员" prop="is_admin">
                <!-- <el-input v-model="attrs.add_form.is_admin" /> -->
                <el-switch v-model="attrs.add_form.is_admin" style="margin-left: 24px" inline-prompt active-text="是"
                    inactive-text="否" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="attrs.adding = false">取消</el-button>
                <el-button type="primary" @click="validate">
                    提交
                </el-button>
            </span>
        </template>
    </el-dialog>

    <el-drawer v-model="attrs.show_permissions" title="角色权限" size="50%" center close-on-click-modal>
        <el-select v-model="permission" placeholder="权限范围">
            <el-option v-for="v, k in permission_type" :key="parseInt(k)" :label="v" :value="parseInt(k)" />
        </el-select>
        <el-cascader v-if="permission == 4" v-model="custom_dept" :options="attrs.all_dept" clearable
            :show-all-levels="false"
            :props="{ emitPath: false, multiple: true, checkStrictly: true, value: 'id', label: 'name', }" />
        <h3 style="margin-top: 20px;">接口权限</h3>
        <div class="permissions-body common-scroll">
            <el-tree ref="interface_tree" :data="attrs.interfaces_tree" node-key="id" show-checkbox check-strictly
                default-expand-all @check="check">
                <template #default="{ node, data }">
                    <div class="permission-item">
                        <div class="permission-item-label">{{ data.name }}</div>
                        <div class="permission-item-gap">|</div>
                        <div class="permission-item-interface">
                            <el-checkbox-group v-model="interface_">
                                <el-checkbox v-for="i in data.childrens" :key="i.id" :label="i.id">
                                    {{ i.name }}
                                </el-checkbox>
                            </el-checkbox-group>
                        </div>
                    </div>
                </template>
            </el-tree>
        </div>
        <el-divider />
        <h3>菜单权限</h3>
        <el-tree ref="menu_tree" :data="attrs.menus" node-key="id" show-checkbox check-strictly default-expand-all>
            <template #default="{ node, data }">
                <div class="permission-item">
                    <div class="permission-item-label">{{ data.label }}</div>
                </div>
            </template>
        </el-tree>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="attrs.show_permissions = false">取消</el-button>
                <el-button type="primary" @click="SetRolePermision">
                    提交
                </el-button>
            </span>
        </template>
    </el-drawer>
</template>
  
<script setup>

import { get_data_, select_, mult_delete_, sort_, submit_, get_all_menu_tree_, get_all_dept_tree_ } from '../../hooks/table_common'
import { Tree, permission_type } from '../../utils/data';
import r from '../../utils/request';
import rest from '../../utils/rest';
import store from '../../store';
store().get_userinfo().then((res) => {
    if (res.interfaces.indexOf(attrs.base_url + '-mult_update') != -1) {
        attrs.can_mult_update = true
    }
    if (res.interfaces.indexOf(attrs.base_url + '-create') != -1) {
        attrs.can_create = true
    }
})
const form_dom = ref()
const attrs = reactive({
    columns: [
        { prop: 'name', type: 'text', label: '角色名称', size: 'small', align: "left", show: true },
        { prop: 'key', type: 'text', label: '角色标识', size: 'small', align: "center", show: true },
        { prop: 'is_admin', type: 'select', width: 150, label: '是否管理员', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
        { prop: 'create_time', type: 'text', width: 160, label: '创建时间', size: 'small', align: "center", show: true },
    ],
    base_url: 'role',
    selects: [],
    data: [],
    total: 0,
    loading: true,
    adding: false,
    show_permissions: false,


    expandedRowKeys: [],
    add_form: {},
    can_create: false,
    can_mult_update: false,
    interfaces_tree: [],
})
const special_form = reactive({
    range: [undefined, undefined],
})
const form = reactive({
    name: undefined,
    status: undefined,
    synthetic: undefined,
    page: 1,
    limit: 100,
})
const rules = reactive({
    name: [
        { required: true, message: '请填写角色名称', trigger: 'blur' },
    ],
})
watch([form, special_form], () => {
    if (special_form.range == null) {
        special_form.range = [undefined, undefined]
    }
    get_data()
})

const get_data = () => {
    get_data_(`/${attrs.base_url}/`, { create_start: special_form.range[0], create_end: special_form.range[1], ...form }, attrs, (a) => { a.data = Tree(a.data) })
}
get_data()

const validate = () => {
    form_dom.value.validate((valid, fields) => {
        if (valid) {
            submit_(attrs.base_url, attrs.add_form, attrs.submit_type, get_data);
            attrs.adding = false
        } else {
            ElMessage({
                showClose: true,
                message: Object.values(fields)[0][0]['message'],
                center: true,
            });
        }
    })
}
rest.list('interface', { page: 1, limit: 999999 }, null, null, (res) => {
    let d = res.data.data
    let menus = {}
    for (let i = 0; i < d.length; i++) {
        if (Object.keys(menus).indexOf(d[i].model) == -1) {
            menus[d[i].model] = { id: d[i].model, name: d[i].model_name }
        }
    }
    menus = Object.values(menus)
    let r = []
    for (let i = 0; i < menus.length; i++) {
        let menu = {
            id: menus[i].id,
            name: menus[i].name,
            childrens: [],
        }
        for (let j = 0; j < d.length; j++) {
            if (d[j].model == menu.id) {
                menu.childrens.push({
                    id: d[j].id,
                    name: d[j].name,
                    checked: false,
                    disabled: false,
                })
            }
        }
        r.push(menu)
    }
    attrs.interfaces_tree = r
    console.log(r);
})

const interface_tree = ref()
const menu_tree = ref()
const interface_ = ref([])
const permission = ref()
const custom_dept = ref()
const GetRolePermision = () => {
    r().get('/data/GetRolePermision/', { params: { role_id: attrs.role_id } }).then((res) => {
        console.log('setCheckedKeys')
        menu_tree.value.setCheckedKeys(res.data.menus, true)
        interface_.value = res.data.interfaces
        permission.value = res.data.permission
    })
}

const SetRolePermision = () => {
    r().post('/data/SetRolePermision/', { custom_dept: custom_dept.value, menus: menu_tree.value.getCheckedKeys(), interfaces: interface_.value, role_id: attrs.role_id, permission: permission.value }).then((res) => {
        attrs.show_permissions = false
        if (res.status == 200) {
            ElMessage({
                message: '权限设置成功',
                type: 'success',
            })
        }

    })
}

const check = (node) => {
    let checked = interface_tree.value.getCheckedKeys()
    console.log(node, checked, interface_)
    if (checked.indexOf(node.id) != -1) {
        node.childrens.forEach(i => {
            if (interface_.value.indexOf(i.id) == -1) {
                interface_.value.push(i.id)
            }
        });
    } else {
        node.childrens.forEach(i => {
            interface_.value.splice(interface_.value.indexOf(i.id), 1)
        });
    }
    // console.log(interface_);

}
// get_all_dept_tree_(attrs)
get_all_menu_tree_(attrs)


</script>

<style scoped lang="scss">
:deep(.el-tree-node__content) {
    min-height: 50px;
    height: fit-content;

    .el-checkbox {
        // align-items: flex-start;
    }
}

.permissions-body {
    // height: 100%;
    width: 100%;
    overflow: auto;

    .permission-item {
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: space-around;
        align-items: left;

        .permission-item-label {
            display: flex;
            align-items: center;
            padding-right: 10px;
        }

        .permission-item-gap {
            display: flex;
            align-items: center;
            padding-right: 10px;
        }

        .permission-item-interface {
            :deep(.el-checkbox-group) {
                display: flex;
                flex-direction: row;
                // align-items: center;
                // justify-content: center;
                flex-wrap: wrap;
            }

        }
    }
}
</style>
