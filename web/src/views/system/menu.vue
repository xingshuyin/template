<!--
 * @Filename     : menu.vue
 * @Description  : wjt-前端-菜单管理
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-10-18 09:45:18
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-30 19:14:14
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<template>
    <el-config-provider :locale="zhCn">
        <div class="main-top">
            <div class="search">
                <f-input v-model="form.label" label="菜单名称" />
                <f-input v-model="form.name" label="路由名称" />
                <f-timerange v-model="special_form.range" />
            </div>
            <div class="tool">
                <el-button size="small" type="danger"
                    @click="mult_delete_(`/${attrs.base_url}/mult_destroy/`, attrs?.selects, get_data)"
                    v-if="attrs?.selects?.length > 0">批量删除
                </el-button>
                <el-button icon="Plus" circle
                    @click="attrs.adding = true; attrs.add_form = {}; attrs.submit_type = 'add'" />
                <f-columns-edit v-if="attrs.columns" v-model="attrs.columns"
                    :base_url="attrs.base_url"></f-columns-edit>
            </div>
        </div>


        <div class="main-table">
            <el-table :data="attrs.data" v-loading.fullscreen:false="attrs.loading" stripe border size="small"
                :expand-row-keys="attrs.expandedRowKeys" :row-key="(row) => { return row.id }"
                @selection-change="(d) => { select_(d, attrs) }" @sort-change="(d) => { sort_(d, form) }">

                <!-- 动态列 -->
                <f-columns v-if="attrs.columns" v-model="attrs.columns"></f-columns>

                <el-table-column label="操作" fixed="right" width="150">
                    <template #default="scope">
                        <el-button size="small" type="primary"
                            @click="attrs.adding = true; attrs.add_form = scope.row; attrs.submit_type = 'update' ">编辑
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
            <el-form :model="attrs.add_form" label-width="120px">
                <el-form-item label="父级菜单">
                    <el-cascader :options="attrs.data" v-model="attrs.add_form.parent"
                        :props="{ checkStrictly: true, value: 'id', label: 'label' }" checkStrictly clearable
                        :show-all-levels="false" :getCheckedNodes="true"
                        @change="(value) => { attrs.add_form.parent = value.slice(-1)[0] }" />
                </el-form-item>
                <el-form-item label="路由名称">
                    <el-input v-model="attrs.add_form.name" />
                </el-form-item>
                <el-form-item label="路由地址">
                    <el-input v-model="attrs.add_form.path" />
                </el-form-item>
                <el-form-item label="菜单名称">
                    <el-input v-model="attrs.add_form.label" />
                </el-form-item>
                <el-form-item label="菜单图标">
                    <el-input v-model="attrs.add_form.icon" />
                </el-form-item>
                <el-form-item label="显示排序">
                    <el-input-number v-model="attrs.add_form.sort" class="mx-4" :min="1" :max="100"
                        controls-position="right" />
                </el-form-item>
                <el-form-item label="组件地址">
                    <el-select v-model="attrs.add_form.component" filterable placeholder="Select">
                        <el-option v-for="item in components" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
                <el-form-item label="是否外链">
                    <el-switch v-model="attrs.add_form.is_link" inline-prompt />
                </el-form-item>
                <el-form-item label="是否目录">
                    <el-switch v-model="attrs.add_form.is_catalog" inline-prompt />
                </el-form-item>
                <el-form-item label="是否禁用">
                    <el-switch v-model="attrs.add_form.disable" inline-prompt />
                </el-form-item>
                <el-form-item label="是否缓存">
                    <el-switch v-model="attrs.add_form.cache" inline-prompt />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="attrs.adding = false">取消</el-button>
                    <el-button type="primary"
                        @click="submit_(attrs.base_url, attrs.add_form, attrs.submit_type, get_data); attrs.adding = false">
                        提交
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </el-config-provider>


</template>
  
<script setup>
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { get_data_, select_, mult_delete_, delete_item_, sort_, submit_ } from '../../hooks/table_common'
import { Tree } from '../../utils/data';
;
const views = import.meta.glob("/src/views/**/**.vue");
const components = []
Object.keys(views).forEach(i => {
    components.push(i.slice(11))
});
const attrs = reactive({
    columns: null,
    base_url: 'Menu',
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
    name: undefined,
    status: undefined,
    synthetic: undefined,
    page: 1,
    limit: 100,
    sort: 'sort',
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


//动态列--------------------------
attrs.columns = [
    { type: 'text', width: 180, label: '菜单名称', prop: 'label', size: 'small', align: "left", show: true },
    { type: 'text', width: 150, label: '菜单图标', prop: 'icon', size: 'small', align: "center", show: true },
    { type: 'text', width: 130, label: '父级菜单', prop: 'parent_name', size: 'small', align: "center", show: true },
    { type: 'text', width: 100, label: '路由名称', prop: 'name', size: 'small', align: "center", show: true },
    { type: 'text', width: 100, label: '排序', prop: 'sort', size: 'small', align: "center", show: true },
    { type: 'select', width: 150, label: '是否外链', prop: 'is_link', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
    { type: 'select', width: 100, label: '是否目录', prop: 'is_catalog', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
    { type: 'text', width: 100, label: '组件地址', prop: 'component', size: 'small', align: "center", show: true },
    { type: 'select', width: 100, label: '是否禁用', prop: 'disable', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
    { type: 'select', width: 150, label: '是否缓存', prop: 'cache', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
    { type: 'text', width: 160, label: '创建时间', prop: 'createAt', size: 'small', align: "center", show: true },
]
</script>

<style scoped lang="scss">

</style>
