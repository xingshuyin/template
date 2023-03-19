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
            <el-form-item label="父级部门" prop="parent">
                <el-cascader v-model="attrs.add_form.parent" :options="attrs.data" clearable
                    :props="{ emitPath: false, checkStrictly: true, value: 'id', label: 'name', }" />
            </el-form-item>
            <el-form-item label="部门名称" prop="name">
                <el-input v-model="attrs.add_form.name" />
            </el-form-item>
            <el-form-item label="标识符" prop="key">
                <el-input v-model="attrs.add_form.key" />
            </el-form-item>
            <el-form-item label="排序" prop="sort">
                <el-input-number v-model="attrs.add_form.sort" :min="1" :max="500" />
            </el-form-item>
            <el-form-item label="负责人" prop="owner">
                <el-input v-model="attrs.add_form.owner" />
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
import rest from '../../utils/rest';
const attrs = reactive({
    columns: [
        { prop: 'name', type: 'text', label: '部门名称', size: 'small', align: "left", show: true },
        { prop: 'key', type: 'text', label: '标识符', size: 'small', align: "left", show: true },
        { prop: 'parent_name', type: 'text', label: '父级部门', size: 'small', align: "center", show: true },
        { prop: 'sort', type: 'text', width: 180, label: '排序', size: 'small', align: "center", show: true },
        { prop: 'owner', type: 'text', width: 150, label: '负责人', size: 'small', align: "center", show: true },
        { prop: 'create_time', type: 'text', width: 160, label: '创建时间', size: 'small', align: "center", show: true },
    ],
    base_url: 'dept',
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
rest.list("dept", { page: 1, limit: 99999 }, null, null, res => {
    attrs.dept_tree = Tree(res.data.data, "id", "parent");
});
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
