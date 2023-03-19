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
            <el-button icon="Plus" circle @click="attrs.adding = true; attrs.add_form = {}; attrs.submit_type = 'add'" />
            <f-columns-edit v-if="attrs.columns" v-model="attrs.columns" :base_url="attrs.base_url"></f-columns-edit>
        </div>
    </div>


    <div class="main-table">
        <el-table :data="attrs.data" v-loading.fullscreen:false="attrs.loading" stripe border size="small"
            :expand-row-keys="attrs.expandedRowKeys" :row-key="(row) => { return row.id }"
            @expand-change="async (row, rows) => { await get_devices_(row, rows, attrs) }"
            @selection-change="(d) => { select_(d, attrs) }" @sort-change="(d) => { sort_(d, form) }"
            :cell-style="() => { return { 'text-align': 'center' } }">
            <!-- 动态列 -->
            <f-columns v-if="attrs.columns" v-model="attrs.columns" v-model:attrs="attrs" :callback_delete="get_data">
            </f-columns>
        </el-table>

        <t-page v-model:page="form.page" v-model:limit="form.limit" :total="attrs.total"></t-page>
    </div>


    <el-dialog v-model="attrs.adding" class="add_form" :title="attrs.submit_type == 'add' ? '新增' : '编辑'" width="50%"
        :modal="false">
        <el-form :model="attrs.add_form" label-width="120px">
            <el-form-item label="登录用户名" prop="username"> <el-input v-model="attrs.add_form.username" />
            </el-form-item>
            <el-form-item label="登录ip" prop="ip"> <el-input v-model="attrs.add_form.ip" /> </el-form-item>
            <el-form-item label="agent信息" prop="agent"> <el-input v-model="attrs.add_form.agent" /> </el-form-item>
            <el-form-item label="浏览器名" prop="browser"> <el-input v-model="attrs.add_form.browser" /> </el-form-item>
            <el-form-item label="操作系统" prop="os"> <el-input v-model="attrs.add_form.os" /> </el-form-item>
            <el-form-item label="州" prop="continent"> <el-input v-model="attrs.add_form.continent" />
            </el-form-item>
            <el-form-item label="国家" prop="country"> <el-input v-model="attrs.add_form.country" /> </el-form-item>
            <el-form-item label="省份" prop="province"> <el-input v-model="attrs.add_form.province" />
            </el-form-item>
            <el-form-item label="城市" prop="city"> <el-input v-model="attrs.add_form.city" /> </el-form-item>
            <el-form-item label="县区" prop="district"> <el-input v-model="attrs.add_form.district" />
            </el-form-item>
            <el-form-item label="运营商" prop="isp"> <el-input v-model="attrs.add_form.isp" /> </el-form-item>
            <el-form-item label="区域代码" prop="area_code"> <el-input v-model="attrs.add_form.area_code" />
            </el-form-item>
            <el-form-item label="英文全称" prop="country_english"> <el-input v-model="attrs.add_form.country_english" />
            </el-form-item>
            <el-form-item label="简称" prop="country_code"> <el-input v-model="attrs.add_form.country_code" />
            </el-form-item>
            <el-form-item label="经度" prop="longitude"> <el-input v-model="attrs.add_form.longitude" />
            </el-form-item>
            <el-form-item label="纬度" prop="latitude"> <el-input v-model="attrs.add_form.latitude" />
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
</template>
  
<script setup>

import { Tree } from '../../utils/data';
import { get_data_, select_, mult_delete_, delete_item_, sort_, submit_ } from '../../hooks/table_common'
const attrs = reactive({
    columns: [
        { prop: 'username', type: 'text', label: '登录用户名', width: 100, size: 'small', align: "left", show: true },
        { prop: 'ip', type: 'text', label: '登录ip', size: 'small', align: "left", show: true },
        { prop: 'agent', type: 'text', label: 'agent信息', width: 300, size: 'small', align: "left", show: true },
        { prop: 'browser', type: 'text', label: '浏览器名', width: 300, size: 'small', align: "left", show: true },
        { prop: 'os', type: 'text', label: '操作系统', size: 'small', align: "left", show: true },
        { prop: 'continent', type: 'text', label: '州', size: 'small', align: "left", show: true },
        { prop: 'country', type: 'text', label: '国家', size: 'small', align: "left", show: true },
        { prop: 'province', type: 'text', label: '省份', size: 'small', align: "left", show: true },
        { prop: 'city', type: 'text', label: '城市', size: 'small', align: "left", show: true },
        { prop: 'district', type: 'text', label: '县区', size: 'small', align: "left", show: true },
        { prop: 'isp', type: 'text', label: '运营商', size: 'small', align: "left", show: true },
        { prop: 'area_code', type: 'text', label: '区域代码', size: 'small', align: "left", show: true },
        { prop: 'country_english', type: 'text', label: '英文全称', size: 'small', align: "left", show: true },
        { prop: 'country_code', type: 'text', label: '简称', size: 'small', align: "left", show: true },
        { prop: 'longitude', type: 'text', label: '经度', size: 'small', align: "left", show: true },
        { prop: 'latitude', type: 'text', label: '纬度', size: 'small', align: "left", show: true },
        { prop: 'create_time', type: 'text', width: 160, label: '创建时间', size: 'small', align: "center", show: true },
    ],
    base_url: 'log',
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
    limit: 100,
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
