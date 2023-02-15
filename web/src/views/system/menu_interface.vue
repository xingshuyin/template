<!--
 * @Filename     : menu_interface.vue
 * @Description  : wjt-前端-角色管理
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-10-18 09:45:18
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-19 11:48:42
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<template>
    <el-config-provider :locale="zhCn">
        <div class="main-top">
            <div class="search">
                <f-input v-model="form.name" label="名称" />
                <f-timerange v-model="special_form.range" />
            </div>
            <div class="tool">
                <el-button size="small" type="danger"
                    @click="mult_delete_(`/${attrs.base_url}/mult_destroy/`, attrs.selects, get_data)"
                    v-if="attrs.selects.length > 0">批量删除
                </el-button>
                <el-button icon="Plus" circle
                    @click="attrs.adding = true; attrs.add_form = {}; attrs.submit_type = 'add'; attrs.submit_type = 'add'" />
                <f-columns-edit v-if="attrs.columns" v-model="attrs.columns"
                    :base_url="attrs.base_url"></f-columns-edit>
            </div>
        </div>


        <div class="main-table">
            <el-table :data="attrs.data" v-loading.fullscreen:false="attrs.loading" stripe border size="small"
                :expand-row-keys="attrs.expandedRowKeys" :row-key="(row) => { return row.id }"
                @selection-change="(d) => { select_(d, attrs) }" @sort-change="(d) => { sort_(d, form) }"
                :cell-style="() => { return { 'text-align': 'center' } }">
                <f-columns v-if="attrs.columns" v-model="attrs.columns"></f-columns>
                <el-table-column label="操作" fixed="right" width="150">
                    <template #default="scope">
                        <el-button size="small" type="primary" @click="edit(scope)">编辑
                        </el-button>
                        <!-- <el-button size="small" type="primary" @click="handleDelete(scope.$index, scope.row)">屏蔽</el-button> -->
                        <el-popconfirm title="确定删除吗?"
                            @confirm="delete_item_(`/${attrs.base_url}/${scope.row.id}/`, get_data)">
                            <template #reference>
                                <el-button size="small" type="primary">删除
                                </el-button>
                            </template>
                        </el-popconfirm>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" v-model:currentPage="form.page" v-model:page-size="form.limit"
                :background="true" :page-sizes="[100, 200, 300, 400]" layout="total, sizes, prev, pager, next, jumper"
                :total="attrs.total" :pager-count="11">
            </el-pagination>
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
    </el-config-provider>


</template>

<script setup>
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { get_data_, select_, mult_delete_, delete_item_, sort_, submit_, get_all_role_, get_all_menu_tree_, get_all_interface_ } from '../../hooks/table_common'
import store from "../../store/index";
const form_dom = ref()
const attrs = reactive({
    columns: null,
    base_url: 'MenuInterface',
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
get_all_role_(attrs)
get_all_menu_tree_(attrs)
get_all_interface_(attrs)



//动态列
attrs.columns = [
    { type: 'text', label: '接口名称', prop: 'name', size: 'small', align: "center", show: true },
    { type: 'text', label: '标识符', prop: 'key', size: 'small', align: "center", show: true },
    {
        type: 'select', label: '请求方式', prop: 'method', size: 'small', align: "center", show: true, option: {
            0: "GET",
            1: "POST",
            2: "PUT",
            3: "DELETE",
        }
    },
    { type: 'text', width: 180, label: '接口地址', prop: 'path', size: 'small', align: "center", show: true },
    { type: 'text', width: 150, label: '菜单', prop: 'menu_label', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
    { type: 'text', width: 160, label: '创建时间', prop: 'createAt', size: 'small', align: "center", show: true },
]
</script>

<style scoped lang="scss">

</style>
