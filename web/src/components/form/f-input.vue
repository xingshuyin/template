<script setup>
//import { ref } from 'vue';
//import {useRoute, useRouter} from 'vue-router';
//const route = useRoute() //当前路由


//const router = useRouter() //全局路由对象
const props = defineProps(['modelValue', 'label']); // defineProps的参数, 可以直接使用
const emits = defineEmits(['update:modelValue']);
//const map = ref(null); //获取ref值为map的元素
//defineExpose({ map,}); //暴露组件的内容, 父组件通过组件对象(如ref)的value获取暴露的对象
// 防抖输入框
const temp = ref(undefined)
const update_value = () => {
    emits('update:modelValue', temp.value)
}
</script>
<template>
    <el-form-item :label="label">
        <el-input v-model="temp" placeholder="" clearable style="width: 100px;" @blur="update_value()"
            @keyup.enter="update_value()" @clear="temp = undefined ; update_value()">
        </el-input>
    </el-form-item>
    <!-- <el-input v-model="temp" placeholder="" clearable style="width: 150px;" @blur="update_value()"
        @keyup.enter="update_value()" @clear="temp = undefined ; update_value()">
        <template #prepend>{{ label }}</template>
    </el-input> -->
</template>
<style scoped lang='scss'>

</style>
