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
            @expand-change="async (row, rows) => { await get_devices_(row, rows, attrs) }"
            @selection-change="(d) => { select_(d, attrs) }" @sort-change="(d) => { sort_(d, form) }">
            <!-- 动态列 -->
            <f-columns v-if="attrs.columns" v-model="attrs.columns" v-model:attrs="attrs" :callback_delete="get_data">
            </f-columns>
        </el-table>
        <t-page v-model:page="form.page" v-model:limit="form.limit" :total="attrs.total"></t-page>
    </div>


    <el-dialog v-model="attrs.adding" class="add_form" :title="attrs.submit_type == 'add' ? '新增' : '编辑'" width="80%"
        :modal="false" fullscreen append-to-body>
        <el-form :model="attrs.add_form" label-width="60px" :rules="rules" ref="form_dom">
            <el-form-item label="名称" prop="name">
                <el-input v-model="attrs.add_form.name" />
            </el-form-item>
            <el-form-item label="标签" prop="tag">
                <el-input v-model="attrs.add_form.tag" />
            </el-form-item>
            <el-form-item label="文件" prop="file">
                <f-jfile v-model="attrs.add_form.file" :limit="10" :size="3" />
            </el-form-item>
            <el-form-item label="链接" prop="link">
                <el-input v-model="attrs.add_form.link" />
            </el-form-item>
            <el-form-item label="" prop="content">
                <v-md-editor v-model="attrs.add_form.content" height="550px" :disabled-menus="[]"
                    @upload-image="upload_image"></v-md-editor>
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
        { type: 'text', label: '名称', prop: 'name', align: "left", show: true },
        { type: 'link', width: 150, label: '链接', prop: 'url', align: "center", show: true },
        { type: 'text', width: 160, label: '发布时间', prop: 'pub_time', align: "center", show: true, sortable: true },
        { type: 'text', label: '标签', prop: 'tag', align: "left", show: true },
        { type: 'jfile', width: 150, label: '文件', prop: 'file', align: "center", show: true },
        { type: 'text', width: 160, label: '创建时间', prop: 'create_time', align: "center", show: true, sortable: true },
    ],
    base_url: 'article',
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
    // defer: ['code'],  //排除字段
    // values: ['name', 'code'] //选择字段
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
watch([form, special_form], () => {
    if (special_form.range == null) {
        special_form.range = [undefined, undefined]
    }
    get_data()
})
const upload_image = (event, insertImage, files) => {
    console.log(files)
    r().post('/data/upload/', { file: files[0] }, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then((res) => {
        insertImage({
            url:
                window.location.protocol + "//" + window.location.host + '/' + res.data.url,
            desc: res.data.name,
            id: res.data.id,
            // width: 'auto',
            // height: 'auto',
        });
    })
}
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
