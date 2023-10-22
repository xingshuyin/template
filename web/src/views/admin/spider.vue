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
            <el-button type="primary" v-if="attrs.can_create"
                @click="attrs.adding = true; attrs.add_form = {}; attrs.submit_type = 'add'" icon="Plus" circle />
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
            <el-form-item label="规则名称">
                <el-input v-model="attrs.add_form.name" />
            </el-form-item>
            <el-form-item label="类型">
                <el-select v-model="attrs.add_form.type" class="m-2" placeholder="" clearable collapse-tags
                    collapse-tags-tooltip style="width: 150px;float: left; margin-right: 20px;">
                    <el-option v-for="v, k in spider_type" :key="k" :label="v" :value="k" />
                </el-select>
            </el-form-item>
            <el-form-item label="域名列表">
                <el-input v-model="attrs.add_form.allowed_domains" placeholder="能够访问的域名范围可用逗号分割多个" />
            </el-form-item>
            <el-form-item label="开始页">
                <el-input v-model="attrs.add_form.start_urls" placeholder="开始爬取页的链接(逗号分隔)" />
            </el-form-item>
            <el-divider />
            <el-form-item label="页数最小值">
                <el-input v-model="attrs.add_form.page_min" placeholder="分页页数起始值" />
            </el-form-item>
            <el-form-item label="页数最大值">
                <el-input v-model="attrs.add_form.page_max" placeholder="分页页数起始值" />
            </el-form-item>
            <el-form-item label="页码转换">
                <el-input v-model="attrs.add_form.page_shift"
                    placeholder="页码转换->  '_'+str(num) if num > 0 else '' -> num 就是传入的页数 " />
            </el-form-item>
            <el-divider />
            <el-form-item label="分页提取">
                <el-input v-model="attrs.add_form.get_page" placeholder="分页提取" />
            </el-form-item>
            <el-form-item label="内容提取">
                <el-input v-model="attrs.add_form.get_item" placeholder="内容提取" />
            </el-form-item>
            <el-form-item label="分页过滤">
                <el-input v-model="attrs.add_form.re_page" placeholder="分页过滤" />
            </el-form-item>
            <el-form-item label="内容过滤">
                <el-input v-model="attrs.add_form.re_item" placeholder="内容过滤" />
            </el-form-item>

            <el-divider />
            <el-form-item label="标题获取">
                <el-input v-model="attrs.add_form.path_name" placeholder="标题获取" />
            </el-form-item>
            <el-form-item label="时间获取">
                <el-input v-model="attrs.add_form.path_time" placeholder="时间获取" />
            </el-form-item>
            <el-form-item label="来源获取">
                <el-input v-model="attrs.add_form.path_source" placeholder="来源获取" />
            </el-form-item>
            <el-form-item label="文章获取">
                <el-input v-model="attrs.add_form.path_content" placeholder="文章获取" />
            </el-form-item>
            <el-form-item label="时间提取">
                <el-input v-model="attrs.add_form.re_time" placeholder="时间提取" />
            </el-form-item>
            <el-form-item label="来源提取">
                <el-input v-model="attrs.add_form.re_source" placeholder="来源提取" />
            </el-form-item>
            <el-form-item label="是否生效">
                <el-switch v-model="attrs.add_form.enable" inline-prompt active-text="是" inactive-text="否" />
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
import r from '../../utils/request';
import { spider_type } from '../../utils/data';
import store from '../../store';
store().get_userinfo().then((res) => {
    if (res.interfaces.indexOf(attrs.base_url + '-mult_update') != -1) {
        attrs.can_mult_update = true
    }
    if (res.interfaces.indexOf(attrs.base_url + '-create') != -1) {
        attrs.can_create = true
    }
})
const attrs = reactive({
    columns: [
        { type: 'text', label: '规则名称', prop: 'name', align: "left", show: true },
        { type: 'text', label: '域名列表', prop: 'allowed_domains', align: "center", show: true },
        { type: 'link', label: '开始页', prop: 'start_urls', width: 200, align: "center", show: true },
        { type: 'select', label: '类型', prop: 'type', width: 200, align: "center", show: true, option: spider_type },

        { type: 'text', label: '页数最小值', prop: 'page_min', width: 115, align: "center", show: true },
        { type: 'text', label: '页数最大值', prop: 'page_max', width: 135, align: "center", show: true },
        { type: 'text', label: '页码转换', prop: 'page_shift', width: 150, align: "center", show: true },

        { type: 'text', label: '分页过滤', prop: 're_page', width: 115, align: "center", show: true },
        { type: 'text', label: '内容过滤', prop: 're_item', width: 115, align: "center", show: true },
        { type: 'text', label: '分页提取', prop: 'get_page', width: 180, align: "center", show: true },
        { type: 'text', label: '内容提取', prop: 'get_item', width: 180, align: "center", show: true },

        { type: 'text', label: '标题获取', prop: 'path_name', width: 100, align: "center", show: true },
        { type: 'text', label: '时间获取', prop: 'path_time', width: 100, align: "center", show: true },
        { type: 'text', label: '来源获取', prop: 'path_source', width: 100, align: "center", show: true },
        { type: 'text', label: '文本获取', prop: 'path_content', width: 100, align: "center", show: true },
        { type: 'text', label: '时间提取', prop: 're_time', width: 100, align: "center", show: true },
        { type: 'text', label: '来源提取', prop: 're_source', width: 100, align: "center", show: true },
        { type: 'text', label: '创建时间', prop: 'create_time', width: 100, align: "center", show: true },
    ],
    base_url: 'spider',
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
    can_create: false,
    can_mult_update: false,
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
const get_data = () => {
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
