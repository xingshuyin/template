<template>
    <div class="main-top">
        <div class="search">
            <f-input v-model="form.name" label="名称" />
            <f-timerange v-model="special_form.range" />
            <el-cascader v-model="form.menu" :options="attrs.menus" :filter-method="filter_method" :show-all-levels="false"
                :getCheckedNodes="true" placeholder="菜单"
                :props="{ emitPath: false, checkStrictly: true, value: 'id', label: 'label', }" filterable clearable />
        </div>
        <div class="tool">
            <el-button size="small" type="danger"
                @click="mult_delete_(`/${attrs.base_url}/mult_destroy/`, attrs.selects, get_data)"
                v-if="attrs.selects.length > 0">批量删除
            </el-button>
            <el-button icon="Refresh" circle @click="init_permision" />
            <el-button icon="Plus" circle
                @click="attrs.adding = true; attrs.add_form = {}; attrs.submit_type = 'add'; attrs.submit_type = 'add'" />
            <f-columns-edit v-if="attrs.columns" v-model="attrs.columns" :base_url="attrs.base_url"></f-columns-edit>
        </div>
    </div>


    <div class="main-table">
        <el-table :data="attrs.data" v-loading.fullscreen:false="attrs.loading" stripe border size="small"
            :expand-row-keys="attrs.expandedRowKeys" :row-key="(row) => { return row.id }"
            @selection-change="(d) => { select_(d, attrs) }" @sort-change="(d) => { sort_(d, form) }"
            :cell-style="() => { return { 'text-align': 'center' } }">
            <f-columns v-if="attrs.columns" v-model="attrs.columns" v-model:attrs="attrs" :callback_delete="get_data">
            </f-columns>
        </el-table>
        <t-page v-model:page="form.page" v-model:limit="form.limit" :total="attrs.total"></t-page>
    </div>


    <el-dialog v-model="attrs.adding" class="add_form" :title="attrs.submit_type == 'add' ? '新增' : '编辑'" width="50%"
        :modal="false">
        <el-form :model="attrs.add_form" label-width="120px" :rules="rules" ref="form_dom">
            <el-form-item label="接口名称" prop="name">
                <el-input v-model="attrs.add_form.name" />
            </el-form-item>
            <el-form-item label="接口标识符" prop="key">
                <el-input v-model="attrs.add_form.key" />
            </el-form-item>
            <el-form-item label="请求方式" prop="method">
                <el-select v-model="attrs.add_form.method" placeholder="" clearable>
                    <el-option key="0" label="GET" :value="0" />
                    <el-option key="1" label="POST" :value="1" />
                    <el-option key="2" label="PUT" :value="2" />
                    <el-option key="3" label="DELETE" :value="3" />
                </el-select>
            </el-form-item>
            <el-form-item label="接口地址" prop="path">
                <el-select v-model="attrs.add_form.path" placeholder="" clearable>
                    <el-option v-for="v, k in attrs.all_interface" :key="k" :label="k" :value="k" />
                </el-select>
            </el-form-item>
            <el-form-item label="菜单">
                <el-cascader :options="attrs.menus" v-model="attrs.add_form.menu"
                    :props="{ checkStrictly: true, value: 'id', label: 'label' }" checkStrictly clearable
                    :show-all-levels="false" :getCheckedNodes="true"
                    @change="(value) => { attrs.add_form.menu = value.slice(-1)[0] }" />
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
import store from '../../store';
import r from '../../utils/request';
import { get_data_, select_, mult_delete_, sort_, submit_, get_all_role_, get_all_menu_tree_, get_all_interface_ } from '../../hooks/table_common'
const form_dom = ref()
const attrs = reactive({
    columns: [
        { prop: 'name', type: 'text', label: '接口名称', size: 'small', align: "center", show: true },
        { prop: 'key', type: 'text', label: '标识符', size: 'small', align: "center", show: true },
        {
            prop: 'method',
            type: 'select', label: '请求方式', size: 'small', align: "center", show: true, option: {
                0: "GET",
                1: "POST",
                2: "PUT",
                3: "DELETE",
            }
        },
        { prop: 'path', type: 'text', width: 180, label: '接口地址', size: 'small', align: "center", show: true },
        { prop: 'menu_label', type: 'text', width: 150, label: '菜单', size: 'small', align: "center", show: true },
        { prop: 'create_time', type: 'text', width: 160, label: '创建时间', size: 'small', align: "center", show: true },
    ],
    base_url: 'menu_interface',
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
const init_permision = () => {
    r().get('/data/init_permision/').then((res) => {
        ElMessage({
            showClose: true,
            message: res.data.detail,
            center: true,
        });
    })
}
get_all_role_(attrs)
get_all_menu_tree_(attrs)
get_all_interface_(attrs)


</script>

<style scoped lang="scss"></style>
