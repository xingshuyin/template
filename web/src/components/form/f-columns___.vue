
<script setup>
//TODO:动态列
const props = defineProps(['modelValue']); // defineProps的参数, 可以直接使用
// modelValue = [
//     { type: ['text','select','jimage','jfile'], width: 180, label: '名称', prop: 'name', align: "center", show: true , [option]: { false: '否', true: '是' }},
// ]

</script>
<template>
    <template v-for="i, index in modelValue">
        <!-- 普通文本 -->
        <el-table-column v-if="i.type == 'text' && i.show" :align="i.align" :label="i.label" :prop="index"
            :sortable="i.sortable" :width="i.width">
        </el-table-column>
        <!-- 单选用标签 -->
        <el-table-column v-else-if="i.type == 'select' && i.show" :align="i.align" :label="i.label" :prop="index"
            :width="i.width">
            <template #default="scope">
                <el-tag effect="dark">
                    {{ i.option[scope.row[index]] }}
                </el-tag>
            </template>
        </el-table-column>
        <!-- 多选 -->
        <el-table-column v-else-if="i.type == 'list' && i.show" :align="i.align" :label="i.label" :prop="index"
            :width="i.width">
            <template #default="scope">
                <el-tag effect="dark" v-for="v in scope.row[index]">
                    {{ i.option[v]?.name }}
                </el-tag>
            </template>
        </el-table-column>
        <!-- 文件 -->
        <el-table-column v-else-if="i.type == 'jfile' && i.show" :align="i.align" :label="i.label" :prop="index"
            :width="i.width">
            <template #default="scope">
                <div class="form-files">
                    <div v-for="i in scope.row[index]">
                        <a :href="i.url" target="_blank">
                            {{ i.name }}
                        </a>
                    </div>
                </div>
            </template>
        </el-table-column>
        <!-- 图片 -->
        <el-table-column v-else-if="i.type == 'jimage' && i.show" :align="i.align" :label="i.label" :prop="index"
            :width="i.width">
            <template #default="scope">
                <el-image v-if="scope.row[index][0]" style="width: 70px; height: 70px" fit="cover" :z-index="30"
                    :src="`/api/data/${scope.row[index][0]?.id}/zip_img/`"
                    :preview-src-list="scope.row[index].reduce((pre, cur) => { pre.push(cur.url); return pre; }, [])"
                    preview-teleported hide-on-click-modal />
                <div v-else></div>
            </template>
        </el-table-column>
        <!-- 链接 -->
        <el-table-column v-else-if="i.type == 'link' && i.show" :align="i.align" :label="i.label" :prop="index"
            :width="i.width">
            <template #default="scope">
                <a :href="scope.row[index]" target="_blank">{{ scope.row[index] }}</a>
            </template>
        </el-table-column>
        <!-- 多选框 -->
        <el-table-column v-else-if="i.type == 'selection' && i.show" type="selection" :width="i.width" />
    </template>
</template>
<style scoped lang='scss'>
</style>
