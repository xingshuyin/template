<template>
    <el-config-provider :locale="zhCn">
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
                <el-button icon="Plus" circle
                    @click="attrs.adding = true; attrs.add_form = {}; attrs.submit_type = 'add'; attrs.submit_type = 'add'" />
                <f-columns-edit v-if="attrs.columns" v-model="attrs.columns" :base_url="attrs.base_url"></f-columns-edit>
            </div>
        </div>


        <div class="main-table">
            <el-table :data="attrs.data" v-loading.fullscreen:false="attrs.loading" stripe border size="small"
                :expand-row-keys="attrs.expandedRowKeys" :row-key="(row) => { return row.id }"
                @selection-change="(d) => { select_(d, attrs) }" @sort-change="(d) => { sort_(d, form) }">
                <f-columns v-model="attrs.columns"></f-columns>
                <el-table-column label="操作" fixed="right" width="150">
                    <template #default="scope">
                        <el-button size="small" type="primary" @click="edit(scope)">编辑
                        </el-button>
                        <!-- <el-button size="small" type="primary" @click="handleDelete(scope.$index, scope.row)">屏蔽</el-button> -->
                        <el-popconfirm title="确定删除吗?" v-if="scope.row.is_delete != 1"
                            @confirm="delete_item_(`/${attrs.base_url}/${scope.row.id}/`, get_data)">
                            <template #reference>
                                <el-button size="small" type="primary">删除
                                </el-button>
                            </template>
                        </el-popconfirm>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" v-model:currentPage="form.page" v-model:page-size="form.limit" :background="true"
                :page-sizes="[100, 200, 300, 400]" layout="total, sizes, prev, pager, next, jumper" :total="attrs.total"
                :pager-count="11">
            </el-pagination>
        </div>


        <el-dialog v-model="attrs.adding" class="add_form" :title="attrs.submit_type == 'add' ? '新增' : '编辑'" width="50%"
            :modal="false">
            <el-form :model="attrs.add_form" label-width="120px" :rules="rules" ref="form_dom">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="attrs.add_form.name" />
                </el-form-item>
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
    </el-config-provider>
</template>
  
<script setup>
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { get_data_, select_, mult_delete_, delete_item_, sort_, submit_, get_all_role_, get_all_role_dict_, get_all_dept_tree_ } from '../../hooks/table_common'
const form_dom = ref()
const attrs = reactive({
    columns: [
        { prop: 'name', type: 'text', label: '名称', size: 'small', align: "left", show: true },
        { prop: 'username', type: 'text', label: '账号', size: 'small', align: "center", show: true },
        { prop: 'role', type: 'list', label: '角色', option: {}, show: true },
        { prop: 'dept_name', type: 'text', width: 150, label: '部门', size: 'small', align: "center", show: true },
        { prop: 'type', type: 'select', label: '用户类型', option: { 1: '前端用户', 2: '后台用户' }, show: true },
        { prop: 'is_super', type: 'select', width: 150, label: '是否超级用户', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
        { prop: 'createAt', type: 'text', width: 160, label: '创建时间', size: 'small', align: "center", show: true },
    ],
    base_url: 'user',
    selects: [],
    data: [],
    total: 0,
    loading: true,
    adding: false,

    expandedRowKeys: [],
    add_form: {},
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
    get_data_(`/${attrs.base_url}/`, { create_start: special_form.range[0], create_end: special_form.range[1], ...form }, attrs)
}
get_data()
const validate = () => {
    form_dom.value.validate((valid, fields) => {
        if (valid) {
            submit_(attrs.base_url, attrs.add_form, attrs.submit_type, get_data);
            attrs.adding = false
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
    attrs.columns[2].option = res //确保索引对
})

// attrs.columns = [
//     { type: 'text', label: '名称', prop: 'name', size: 'small', align: "left", show: true },
//     { type: 'text', label: '账号', prop: 'username', size: 'small', align: "center", show: true },
//     { type: 'list', label: '角色', prop: 'role', option: await get_all_role_dict_(), show: true },
//     { type: 'text', width: 150, label: '部门', prop: 'dept_name', size: 'small', align: "center", show: true },
//     { type: 'select', label: '用户类型', prop: 'type', option: { 1: '前端用户', 2: '后台用户' }, show: true },
//     { type: 'select', width: 150, label: '是否超级用户', prop: 'is_super', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
//     { type: 'text', width: 160, label: '创建时间', prop: 'createAt', size: 'small', align: "center", show: true },
// ]

</script>

<style scoped lang="scss">
</style>
