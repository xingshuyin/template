<template>
    <el-config-provider :locale="zhCn">
        <el-pagination class="pager" v-model:currentPage="page" v-model:page-size="limit" :background="true"
            :page-sizes="[50, 100, 200, 300, 400]" layout="total, sizes, prev, pager, next, jumper" :total="total"
            :pager-count="11">
        </el-pagination>
    </el-config-provider>
</template>
<script setup>
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
const props = defineProps(['page', 'limit', 'total']); // defineProps的参数, 可以直接使用
const emits = defineEmits(['update:page', 'update:limit']); // emits 触发父组件函数
watch(() => props.page, () => {
    emits('update:page', props.page)
})
watch(() => props.limit, () => {
    emits('update:limit', props.limit)
})
</script>
<style scoped lang='scss'>
</style>
