
<script setup>
import { delete_item_ } from '../../hooks/table_common'
import store from '../../store';
//TODO:动态列
const props = defineProps(['modelValue', 'attrs', 'callback_delete', 'opt_width']); // defineProps的参数, 可以直接使用
const emits = defineEmits(['update:attrs']); // emits 触发父组件函数
watch(() => props.attrs, () => {
    emits('update:attrs', props.attrs)
})
const attrs_ = reactive({
    can_delete: false,
    can_put: false,
})
store().get_userinfo().then((res) => {
    if (res.interfaces.indexOf(props.attrs.base_url + '-destroy') != -1) {
        attrs_.can_delete = true
    }
    if (res.interfaces.indexOf(props.attrs.base_url + '-update') != -1) {
        attrs_.can_put = true
    }
})
// modelValue = [
//     { type: ['text','select','jimage','jfile'], width: 180, label: '名称', prop: 'name', align: "center", show: true , [option]: { false: '否', true: '是' }},
// ]

</script>
<template>
    <template v-for="i in attrs.columns">
        <!-- 普通文本 -->
        <el-table-column v-if="i.type == 'text' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
            :sortable="i.sortable" :width="i.width">
        </el-table-column>
        <!-- 单选用标签 -->
        <el-table-column v-else-if="i.type == 'select' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
            :sortable="i.sortable" :width="i.width">
            <template #default="scope">
                <el-tag effect="dark">
                    {{ i.option[scope.row[i.prop]] }}
                </el-tag>
            </template>
        </el-table-column>
        <!-- 多选 -->
        <el-table-column v-else-if="i.type == 'list' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
            :sortable="i.sortable" :width="i.width">
            <template #default="scope">
                <el-tag effect="dark" v-for="v in scope.row[i.prop]">
                    {{ i.option[v].name }}
                </el-tag>
            </template>
        </el-table-column>
        <!-- 文件 -->
        <el-table-column v-else-if="i.type == 'jfile' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
            :sortable="i.sortable" :width="i.width">
            <template #default="scope">
                <div class="form-files">
                    <div v-for="i in scope.row[i.prop]">
                        <a :href="i.url" target="_blank">
                            {{ i.name }}
                        </a>
                    </div>
                </div>
            </template>
        </el-table-column>
        <!-- 图片 -->
        <el-table-column v-else-if="i.type == 'jimage' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
            :sortable="i.sortable" :width="i.width">
            <template #default="scope">
                <el-image v-if="scope.row[i.prop][0]" style="width: 70px; height: 70px" fit="cover" :z-index="30"
                    :src="`/api/data/${scope.row[i.prop][0]?.id}/zip_img/`"
                    :preview-src-list="scope.row[i.prop].reduce((pre, cur) => { pre.push(cur.url); return pre; }, [])"
                    preview-teleported hide-on-click-modal />
                <div v-else></div>
            </template>
        </el-table-column>
        <!-- 链接 -->
        <el-table-column v-else-if="i.type == 'link' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
            :sortable="i.sortable" :width="i.width">
            <template #default="scope">
                <a :href="scope.row[i.prop]" target="_blank">{{ scope.row[i.prop] }}</a>
            </template>
        </el-table-column>
        <!-- JSON -->
        <el-table-column v-else-if="i.type == 'json' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
            :width="i.width">
            <template #default="scope">
                {{ JSON.stringify(scope.row[i.prop]) }}
            </template>
        </el-table-column>
    </template>
    <el-table-column label="操作" fixed="right" :width="opt_width ? opt_width : 150" align="center">
        <template #default="scope">
            <slot name="opt" :scope="scope"></slot>
            <el-button size="small" type="primary" v-if="attrs_.can_put"
                @click="attrs.adding = true; attrs.add_form = scope.row; attrs.submit_type = 'update'">编辑
            </el-button>
            <!-- <el-button size="small" type="primary" @click="handleDelete(scope.$index, scope.row)">屏蔽</el-button> -->
            <el-popconfirm title="确定删除吗?" v-if="attrs_.can_delete"
                @confirm="delete_item_(`/${attrs.base_url}/${scope.row.id}/`, callback_delete)">
                <template #reference>
                    <el-button size="small" type="primary">删除
                    </el-button>
                </template>
            </el-popconfirm>
        </template>
    </el-table-column>
</template>
<style scoped lang='scss'></style>
