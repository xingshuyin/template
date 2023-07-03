<!--
 * @Filename     : spider.vue
 * @Description  : wjt-前端-爬虫管理
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-10-30 10:31:33
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-19 22:15:04
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<template>
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
            <el-button @click="attrs.adding = true; attrs.add_form = {}; attrs.submit_type = 'add'" icon="Plus" circle />
            <f-columns-edit v-if="attrs.columns" v-model="attrs.columns" :base_url="attrs.base_url"></f-columns-edit>
            <el-button icon="Download" circle
                @click="export_data_(attrs.base_url, { create_start: special_form.range[0], create_end: special_form.range[1], ...form })" />
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
    <el-dialog v-model="attrs.adding" :title="attrs.submit_type == 'add' ? '新增' : '编辑'" width="50%" top="0" :modal="false"
        style="scrollbar-width: 0;">
        <el-form :model="attrs.add_form" label-width="220px" :rules="rules" ref="form_dom">
            <el-form-item label="名称">
                <el-input v-model="attrs.add_form.name" />
            </el-form-item>
            <el-form-item label="地区等级">
                <el-select v-model="attrs.add_form.level" class="m-2" placeholder="" clearable collapse-tags
                    collapse-tags-tooltip style="width: 150px;float: left; margin-right: 20px;">
                    <el-option v-for="v, k in area_level" :key="parseInt(k)" :label="v" :value="parseInt(k)" />
                </el-select>
            </el-form-item>
            <el-form-item label="父级地区" prop="area">
                <el-cascader v-model="attrs.add_form.parent" :options="attrs.areas_tree"
                    :props="{ emitPath: false, value: 'code', label: 'name', checkStrictly: true }" />
            </el-form-item>
            <el-form-item label="地区编码">
                <el-input v-model="attrs.add_form.code" placeholder="地区编码" />
            </el-form-item>
            <el-form-item label="纬度">
                <el-input v-model="attrs.add_form.lat" placeholder="纬度" />
            </el-form-item>
            <el-form-item label="经度">
                <el-input v-model="attrs.add_form.lng" placeholder="经度" />
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
import { get_data_, select_, mult_delete_, sort_, submit_, export_data_ } from '../../hooks/table_common'
import { area_level, Tree } from '../../utils/data';
import r from '../../utils/request';
import store from "../../store/index";
const attrs = reactive({
    columns: [
        { type: 'text', label: '名称', prop: 'name', width: 250, align: "left", show: true, sortable: true },
        { type: 'text', label: '地区编码', prop: 'code', width: 150, align: "center", show: true },
        { type: 'select', label: '地区等级', prop: 'level', width: 200, align: "center", show: true, option: area_level },
        { type: 'text', label: '纬度', prop: 'lat', width: 115, align: "center", show: true },
        { type: 'text', label: '经度', prop: 'lng', width: 135, align: "center", show: true },
        { type: 'text', label: '父地区', prop: 'parent_name', width: 150, align: "center", show: true },
        { type: 'text', label: '父地区编码', prop: 'parent', width: 150, align: "center", show: true },

    ],
    base_url: 'area',
    selects: [],
    data: [],
    total: 0,
    loading: true,
    submit_type: null,
    update_item_id: null,
    adding: false,
    background: true,
    expandedRowKeys: [],
    add_form: {},
})
const special_form = reactive({
    range: [undefined, undefined],
})
const form = reactive({
    page: 1,
    limit: 100,
    // defer: ['code'],  //排除字段
    // values: ['name', 'code'] //选择字段
})
watch([form, special_form], () => {
    console.log(form)
    if (special_form.range == null) {
        special_form.range = [undefined, undefined]
    }
    get_data()
})
const form_dom = ref()
const rules = reactive({  //https://element-plus.gitee.io/zh-CN/component/form.html#%E8%87%AA%E5%AE%9A%E4%B9%89%E6%A0%A1%E9%AA%8C%E8%A7%84%E5%88%99
    name: [
        { required: true, message: '请填写名称', trigger: 'blur' },
    ],
    code: [
        { required: true, message: '请填写编码', trigger: 'blur' },
    ],
})
const validate = () => {
    form_dom.value.validate((valid, fields) => {
        if (valid) {
            submit_(attrs.base_url, attrs.add_form, attrs.submit_type, submit_success); attrs.adding = false
        }
    })
}
const submit_success = (res) => {
    if (attrs.submit_type == 'add') {
        attrs.data.shift(res.data)
        attrs.add_form = {};
    }

    get_data()
}
const get_data = async () => {
    attrs.areas_tree = await store().get_areas_tree();
    get_data_(`/${attrs.base_url}/`, { create_start: special_form.range[0], create_end: special_form.range[1], ...form }, attrs)
}

get_data()
</script>

<style scoped lang="scss">
.detail {
    margin-left: 60px;
    margin-right: 10px;
    box-shadow: 0 0 2px 0 black;
}

:deep(.sub-table) {
    width: 100%;
    height: 200px;
}
</style>
