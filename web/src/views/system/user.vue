<template>
    <div class="main-top">
        <div class="search">
            <f-input v-model="form.username" label="名称" />
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
            @selection-change="(d) => { select_(d, attrs) }" @sort-change="(d) => { sort_(d, form) }">
            <f-columns v-if="attrs.columns" v-model="attrs.columns" v-model:attrs="attrs" :callback_delete="get_data">
            </f-columns>
        </el-table>
        <t-page v-model:page="form.page" v-model:limit="form.limit" :total="attrs.total"></t-page>
    </div>


    <el-dialog v-model="attrs.adding" class="add_form" :title="attrs.submit_type == 'add' ? '新增' : '编辑'" width="50%"
        :modal="false">
        <el-form :model="attrs.add_form" label-width="120px" :rules="rules" ref="form_dom">
            <!-- <el-form-item label="名称" prop="name">
                <el-input v-model="attrs.add_form.name" />
            </el-form-item> -->
            <el-form-item label="账号" prop="username">
                <el-input v-model="attrs.add_form.username" />
            </el-form-item>
            <el-form-item label="密码" prop="password" v-if="attrs.submit_type == 'add'">
                <el-input v-model="attrs.add_form.password" />
            </el-form-item>
            <el-form-item label="用户类型" prop="type">
                <el-select v-model="attrs.add_form.type" placeholder="" clearable>
                    <el-option :key="1" label="前端用户" :value="1" />
                    <el-option :key="2" label="后台用户" :value="2" />
                </el-select>
            </el-form-item>
            <el-form-item label="超级用户" prop="password">
                <el-switch v-model="attrs.add_form.is_super" />
            </el-form-item>
            <el-form-item label="角色" prop="role">
                <el-select v-model="attrs.add_form.role" placeholder="" multiple clearable collapse-tags
                    collapse-tags-tooltip>
                    <el-option v-for="item in attrs.all_role" :key="item.id" :label="item.name" :value="item.id" />
                </el-select>
            </el-form-item>
            <el-form-item label="部门" prop="dept">
                <el-cascader v-model="attrs.add_form.dept" :options="attrs.all_dept"
                    :props="{ checkStrictly: true, emitPath: false, value: 'id', label: 'name' }" />
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
</template>

<script setup>

import { get_data_, select_, mult_delete_, sort_, submit_, get_all_role_, get_all_role_dict_, get_all_dept_tree_ } from '../../hooks/table_common'
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
        { prop: 'username', type: 'text', label: '账号', size: 'small', align: "center", show: true },
        { prop: 'role', type: 'list_dict', label: '角色', option: {}, show: true },
        { prop: 'dept_name', type: 'text', width: 150, label: '部门', size: 'small', align: "center", show: true },
        { prop: 'type', type: 'select', label: '用户类型', option: { 1: '前端用户', 2: '后台用户' }, show: true },
        { prop: 'is_super', type: 'select', width: 150, label: '是否超级用户', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
        { prop: 'create_time', type: 'text', width: 160, label: '创建时间', size: 'small', align: "center", show: true },
    ],
    base_url: 'user',
    selects: [],
    data: [],
    total: 0,
    loading: true,
    adding: false,

    expandedRowKeys: [],
    add_form: {},
    can_create: false,
    can_mult_update: false,
})
const special_form = reactive({
    range: [undefined, undefined],
})
const form = reactive({
    username: undefined,
    status: undefined,
    synthetic: undefined,
    page: 1,
    limit: 100,
})
const rules = reactive({
    username: [
        { required: true, message: '请填写账号', trigger: 'blur' },
    ],
})
watch([form, special_form], () => {
    if (special_form.range == null) {
        special_form.range = [undefined, undefined]
    }
    get_data()
})
const get_data = () => {
    get_data_(`/${attrs.base_url}/`, { create_start: special_form.range[0], create_end: special_form.range[1], ...form }, attrs)
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
const edit = (scope) => {
    attrs.adding = true;
    const temp = {}
    for (let key in scope.row) { //拷贝对象
        temp[key] = scope.row[key];
    }
    attrs.add_form = temp;
    attrs.submit_type = 'update';
}

get_all_role_(attrs)
get_all_dept_tree_(attrs)
get_all_role_dict_().then((res) => {
    attrs.columns[1].option = res //确保索引对
})
</script>

<style scoped lang="scss"></style>
