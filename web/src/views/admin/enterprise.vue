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
                <!-- <f-input v-model="form.label" label="名称" /> -->
                <f-input v-model="form.name" label="名称" />
                <f-timerange v-model="special_form.range" />
            </div>
            <div class="tool">
                <el-button size="small" type="danger"
                    @click="mult_delete_(`/${attrs.base_url}/mult_destroy/`, attrs?.selects, get_data)"
                    v-if="attrs?.selects?.length > 0">批量删除
                </el-button>
                <el-button @click="attrs.adding = true; attrs.add_form = {}; attrs.submit_type = 'add'" icon="Plus"
                    circle />
                <f-columns-edit v-if="attrs.columns" v-model="attrs.columns"
                    :base_url="attrs.base_url"></f-columns-edit>
                <el-button icon="Download" circle
                    @click="export_data_(attrs.base_url, { create_start: special_form.range[0], create_end: special_form.range[1], ...form })" />
            </div>
        </div>


        <div class="main-table">
            <el-table :data="attrs.data" v-loading.fullscreen:false="attrs.loading" stripe border size="small"
                :expand-row-keys="attrs.expandedRowKeys" :row-key="(row) => { return row.id }"
                @expand-change="async (row, rows) => { await get_devices_(row, rows, attrs) }"
                @selection-change="(d) => { select_(d, attrs) }" @sort-change="(d) => { sort_(d, form) }">
                <!-- 动态列 -->
                <f-columns v-if="attrs.columns" v-model="attrs.columns"></f-columns>
                <el-table-column label="操作" fixed="right" width="150" align="center">
                    <template #default="scope">
                        <el-button size="small" type="primary"
                            @click="attrs.adding = true; attrs.add_form = scope.row; attrs.submit_type = 'update' ">编辑
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

            <el-pagination class="pager" v-model:currentPage="form.page" v-model:page-size="form.limit"
                :background="true" :page-sizes="[50, 100, 200, 300, 400]"
                layout="total, sizes, prev, pager, next, jumper" :total="attrs.total" :pager-count="11">
            </el-pagination>
        </div>


        <el-dialog v-model="attrs.adding" class="add_form" :title="attrs.submit_type == 'add' ? '新增' : '编辑'" width="50%"
            :modal="false">
            <el-form :model="attrs.add_form" label-width="120px">
                <el-form-item label="名称">
                    <el-input v-model="attrs.add_form.name" />
                </el-form-item>
                <el-form-item label="地址" prop="area">
                    <el-cascader v-model="attrs.add_form.area" :options="attrs.areas_tree"
                        :props="{ emitPath: false, value: 'code', label: 'name' }" />
                </el-form-item>
                <el-form-item label="文件" prop="file">
                    <f-jfile v-model="attrs.add_form.file" :limit="10" :size="3" />
                </el-form-item>
                <el-form-item label="图片" prop="image">
                    <f-jimage v-model="attrs.add_form.image" :limit="10" :size="3" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="attrs.adding = false">取消</el-button>
                    <el-button type="primary"
                        @click="submit_(attrs.base_url, attrs.add_form, attrs.submit_type, submit_success); attrs.adding = false">
                        提交
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </el-config-provider>


</template>
  
<script setup>
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { get_data_, select_, mult_delete_, delete_item_, sort_, submit_, export_data_ } from '../../hooks/table_common'
import store from "../../store/index";
const attrs = reactive({
    columns: null,
    base_url: 'Enterprise',
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
    page: 1,
    limit: 50,
})
watch([form, special_form], () => {
    if (special_form.range == null) {
        special_form.range = [undefined, undefined]
    }
    get_data()
})
const get_data = async () => {
    attrs.areas_tree = await store().get_areas_tree();
    get_data_(`/${attrs.base_url}/`, { create_start: special_form.range[0], create_end: special_form.range[1], ...form }, attrs)
}
get_data()
const submit_success = (res) => {
    if (attrs.submit_type == 'add') {
        attrs.data.shift(res.data)
    }
}



attrs.columns = [
    { type: 'text', label: '名称', prop: 'name', align: "left", show: true },
    { type: 'text', width: 150, label: '行政区域', prop: 'area_name', align: "center", show: true },
    { type: 'jfile', width: 150, label: '文件', prop: 'file', align: "center", show: true },
    { type: 'jimage', width: 150, label: '图片', prop: 'image', align: "center", show: true },
    { type: 'text', width: 160, label: '创建时间', prop: 'createAt', align: "center", show: true, sortable: true },
]
</script>

<style scoped lang="scss">
.devices-tab {
    width: 1000px;
    margin-left: 100px;

    :deep(.el-tabs__item) {
        color: #080000;
        font-size: 16px;
    }

    :deep(.is-active) {
        color: #028a3b !important;
    }
}
</style>
