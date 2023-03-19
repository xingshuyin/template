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
            <el-form-item label="规则名称">
                <el-input v-model="attrs.add_form.name" />
            </el-form-item>
            <el-form-item label="域名列表(逗号分隔)">
                <el-input v-model="attrs.add_form.allowed_domains" placeholder="能够访问的域名范围可用逗号分割多个" />
            </el-form-item>
            <el-form-item label="开始页(逗号分隔)">
                <el-input v-model="attrs.add_form.start_urls" placeholder="开始爬取页的链接" />
            </el-form-item>
            <el-divider />
            <el-form-item label="分页页数开头">
                <el-input v-model="attrs.add_form.start_page_num" placeholder="分页页数起始值" />
            </el-form-item>
            <el-form-item label="分页页数正则">
                <el-input v-model="attrs.add_form.re_page_num" placeholder="分页是动态生成的时侯可以用正则匹配(第一个组为所需要的值)" />
            </el-form-item>
            <el-form-item label="分页链接格式化字符">
                <el-input v-model="attrs.add_form.page_format" placeholder="页数相关字符会替换链接中的{}  (只能有一个{})" />
            </el-form-item>
            <el-form-item label="分页链接页码转换">
                <el-input v-model="attrs.add_form.page_format_shift"
                    placeholder="页码格式转换->  '_'+str(num) if num > 0 else '' -> num 就是传入的页数 " />
            </el-form-item>
            <el-divider>
                上下紧邻两个取一个方法
            </el-divider>
            <el-form-item label="分页链接提取区域xpath">
                <el-input v-model="attrs.add_form.xpath_page_restrict" placeholder="分页链接所在元素的xpath(减少链接搜索范围)" />
            </el-form-item>
            <el-form-item label="分页链接正则">
                <el-input v-model="attrs.add_form.re_page" placeholder="不用分页页数正则时就会使用它, 正则匹配需要的分页链接链接" />
            </el-form-item>
            <el-divider />
            <el-form-item label="内容链接正则">
                <el-input v-model="attrs.add_form.re_item" placeholder="文章链接正则匹配" />
            </el-form-item>
            <el-form-item label="内容链接提取区域xpath">
                <el-input v-model="attrs.add_form.xpath_item_restrict" placeholder="文章链接所在元素xpath(减少链接搜索范围)" />
            </el-form-item>
            <el-divider />
            <el-form-item label="标题xpath">
                <el-input v-model="attrs.add_form.xpath_name" placeholder="文章标题xpath" />
            </el-form-item>
            <el-form-item label="时间xpath">
                <el-input v-model="attrs.add_form.xpath_time" placeholder="时间xpath" />
            </el-form-item>
            <el-form-item label="时间正则">
                <el-input v-model="attrs.add_form.re_time" placeholder="包含时间的元素不止包含时间时,正则匹配的第一个组为时间" />
            </el-form-item>
            <el-form-item label="封面xpath">
                <el-input v-model="attrs.add_form.xpath_cover" placeholder="查找封面图片的范围" />
            </el-form-item>
            <el-form-item label="内容xpath">
                <el-input v-model="attrs.add_form.xpath_content" placeholder="包含所有文章内容的元素的xpath (到元素即至止,不要text())" />
            </el-form-item>
            <el-form-item label="来源xpath">
                <el-input v-model="attrs.add_form.xpath_source" placeholder="来源xpath" />
            </el-form-item>
            <el-form-item label="来源正则">
                <el-input v-model="attrs.add_form.re_source" placeholder="包含来源的元素不止包含来源时,正则匹配的第一个组为来源" />
            </el-form-item>
            <el-form-item label="是否生效">
                <el-switch v-model="attrs.add_form.enable" inline-prompt active-text="是" inactive-text="否" />
            </el-form-item>
            <el-form-item label="类型">
                <el-select v-model="attrs.add_form.category_id" class="m-2" placeholder="" clearable collapse-tags
                    collapse-tags-tooltip style="width: 150px;float: left; margin-right: 20px;">
                    <el-option v-for="item in attrs.categorys" :key="item.id" :label="item.name" :value="item.id" />
                </el-select>
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
import store from "../../store/index";
const attrs = reactive({
    columns: [
        { type: 'text', label: '规则名称', prop: 'name', align: "left", show: true },
        { type: 'text', label: '域名列表', prop: 'allowed_domains', align: "center", show: true },
        { type: 'link', label: '开始页', prop: 'start_urls', width: 200, align: "center", show: true },
        { type: 'text', label: '分页页数开头', prop: 'start_page_num', width: 115, align: "center", show: true },
        { type: 'text', label: '分页页数正则', prop: 're_page_num', width: 115, align: "center", show: true },
        { type: 'text', label: '分页链接格式化字符', prop: 'page_format', width: 155, align: "center", show: true },
        { type: 'text', label: '分页链接页码转换', prop: 'page_format_shift', width: 150, align: "center", show: true },
        { type: 'text', label: '分页链接正则', prop: 're_page', width: 115, align: "center", show: true },
        { type: 'text', label: '内容链接正则', prop: 're_item', width: 115, align: "center", show: true },
        { type: 'text', label: '分页链接提取区域xpath', prop: 'xpath_page_restrict', width: 180, align: "center", show: true },
        { type: 'text', label: '内容链接提取区域xpath', prop: 'xpath_item_restrict', width: 180, align: "center", show: true },
        { type: 'text', label: '标题xpath', prop: 'xpath_name', width: 100, align: "center", show: true },
        { type: 'text', label: '时间xpath', prop: 'xpath_time', width: 100, align: "center", show: true },
        { type: 'text', label: '时间正则', prop: 're_time', align: "center", show: true },
        { type: 'text', label: '封面xpath', prop: 'xpath_cover', width: 100, align: "center", show: true },
        { type: 'text', label: '内容xpath', prop: 'xpath_content', width: 100, align: "center", show: true },
        { type: 'text', label: '来源xpath', prop: 'xpath_source', width: 100, align: "center", show: true },
        { type: 'text', label: '来源正则', prop: 're_source', align: "center", show: true },
        { type: 'text', label: '创建时间', prop: 'create_time', align: "center", show: true },
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
