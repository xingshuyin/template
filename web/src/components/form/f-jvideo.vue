<!--
 * @Filename     : img.vue
 * @Description  : 前端-文件上传组件(json保存文件信息)
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-11-01 22:35:25
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-29 18:11:38
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
// 上传文件 ; 返回文件 id列表(modelValue)
import { get_token } from '../../utils/request'
import { reactive, watch } from 'vue';
import { upload_file_, remove_file_, remove_jfile_ } from '../../hooks/table_common'
//const router = useRouter() //全局路由对象
const props = defineProps(['modelValue', 'limit', 'size']); // limit数量限制   size大小限制(mb)
//  <Uimg v-model="attrs.add_form.door_img" :limit="1" :size="3" :file-list="attrs.add_form.door_img ? [{ url: attrs.add_form.door_img }] : []">
//  </Uimg>
//  :file-list为文件列表,需要传入由{name:'img',  value: 'url'}  组成的的列表, name可以不传
//  modelValue 与图片显示无关,它只关联字段值    :file-list才关系到图片的展示
// 假定 modelValue  => [{name:'img',  url: 'url', id: 1}]

const emits = defineEmits(['update:modelValue']);
//const map = ref(null); //获取ref值为map的元素
//defineExpose({ map,}); //暴露组件的内容, 父组件通过组件对象(如ref)的value获取暴露的对象
const attrs = reactive({
    file_list: [],
    headers: { Authorization: get_token(), },
})
const sucess = (res, file, files) => { //返回数据构造
    let f = []
    files.forEach(item => {
        if (item.response) {  //新上传的
            f.push(item.response)
        } else if (item.url) { //v-model带来的值
            f.push(item)
        }
    })
    emits('update:modelValue', f)
}
const remove = (file, files) => { //返回数据构造
    let f = []
    files.forEach(item => {
        if (item.response) {  //新上传的
            f.push(item.response)
        } else if (item.url) { //v-model带来的值
            f.push(item)
        }
    })
    emits('update:modelValue', f)
}
const before_remove = async (file, files) => { //返回数据构造
    if (file?.id || file?.response?.id) {
        let res = await remove_jfile_(file)
        if (res.status == 200) {
            return true
        } else {
            return false
        }
    }
    return true
}
const before_upload = (file) => {
    if (props.size) {
        if (file.size > props.size * 1024 * 1024) {
            ElMessage({
                message: `文件大小超出${props.size}mb限制`,
                type: 'warning',
            })
            return false
        }
    }
}
const exceed = (files, file) => {
    ElMessage({
        message: `文件数量超出${props.limit}个限制`,
        type: 'warning',
    })
}
onBeforeMount(() => {
    if (props.modelValue != null) { //初始化值
        attrs.file_list = props.modelValue
    }
})
watch(() => { return attrs.file_list }, () => {
    console.log(attrs.file_list)
})
watch(() => { return props.modelValue }, () => {
    attrs.file_list = props.modelValue
})
</script>
<template>
    <el-upload class="video-upload" v-model:file-list="attrs.file_list" :limit="limit" drag action="/api/data/upload/"
        @on-progress="upload_file_" :on-remove="remove" :before-remove="before_remove" :on-success="sucess"
        :before-upload="before_upload" accept="video/*" :headers="attrs.headers" :on-exceed="exceed">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
            拖拽或点击上传
        </div>
        <template #tip>
            <div class="el-upload__tip">
                文件大小不能超过 {{ props.size }} mb
            </div>
        </template>
    </el-upload>
</template>
<style scoped lang='scss'>
.video-upload {
    :deep(.el-upload-dragger) {
        --el-upload-dragger-padding-horizontal: 10px;
    }
}
</style>
