<script setup>
//const props = defineProps(['modelValue']); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['update:modelValue']); // emits 触发父组件函数
import { onBeforeMount, reactive } from 'vue';
import store from '../../store';
const attrs = reactive({
    userinfo: {}
})
const rules = reactive({
    username: [
        { required: true, message: '请填写角色名称', trigger: 'blur' },
    ],
})
onBeforeMount(() => {
    store().get_userinfo(true).then((res) => {
        attrs.userinfo = res
        console.log(attrs.userinfo)
    })
})

</script>
<template>
    <div class="con">
        <el-form :model="attrs.userinfo" label-width="120px" :rules="rules" ref="form_dom">
            <el-form-item label="名称" prop="name">
                <el-input v-model="attrs.userinfo.name" />
            </el-form-item>
            <el-form-item label="账号" prop="username">
                <el-input v-model="attrs.userinfo.username" />
            </el-form-item>
        </el-form>
        <el-button type="primary">Primary</el-button>
    </div>
</template>
<style scoped lang='scss'>
.con {
    width: 50%;
    margin: auto;
    display: flex;
    align-items: center;
    flex-direction: column;

    .el-form {
        width: 100%;
    }
}
</style>