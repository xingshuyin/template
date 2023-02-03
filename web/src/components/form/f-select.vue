<script setup>
const props = defineProps(['modelValue', 'data', 'key', 'label', 'value', 'placeholder']); // defineProps的参数, 可以直接使用
const emits = defineEmits(['update:modelValue']);
const temp = ref([undefined, undefined])
const update_value = () => {
    emits('update:modelValue', temp.value)
}
</script>
<template>
    <el-select v-model="temp" placeholder="placeholder" @change="update_value">
        <el-option v-for="item in data" :key="item[key]" :label="item[label]" :value="item[value]" />
    </el-select>
</template>
<style scoped lang='scss'>

</style>
