<!--
 * @Filename     : img.vue
 * @Description  : wjt-前端-图片上传组件
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-11-01 22:35:25
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-29 18:11:38
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
// 上传文件 ; 返回文件 id列表(modelValue)
import { reactive } from 'vue';
import { upload_file_, remove_file_ } from '../../hooks/table_common'
//const router = useRouter() //全局路由对象
const props = defineProps(['modelValue', 'limit', 'size']); // limit数量限制   size大小限制(mb)
//  <Uimg v-model="attrs.add_form.door_img" :limit="1" :size="3" :file-list="attrs.add_form.door_img ? [{ url: attrs.add_form.door_img }] : []">
//  </Uimg>
//  :file-list为文件列表,需要传入由{name:'img',  value: 'url'}  组成的的列表, name可以不传
//  modelValue 与图片显示无关,它只关联字段值    :file-list才关系到图片的展示

const emits = defineEmits(['update:modelValue']);
//const map = ref(null); //获取ref值为map的元素
//defineExpose({ map,}); //暴露组件的内容, 父组件通过组件对象(如ref)的value获取暴露的对象
const attrs = reactive({
    file_list: [],
    headers: {},
})
const sucess = (res, file, files) => { //返回数据构造
    if (props.limit == 1) {  //一张图片时直接返回第一张图片链接
        // console.log('update:modelValue', res, file, files[0].url)
        emits('update:modelValue', res.url)
    } else {
        let f = []
        files.forEach(item => {
            if (item.response) {  //新上传的
                f.push(item.response.url)
            } else if (item.url) { //v-model带来的值
                f.push(item.url)
            }
        })
        console.log('upload sucess', f, files, attrs.file_list)
        emits('update:modelValue', f.join(","))
    }

}
const remove = (file, files) => { //返回数据构造
    if (props.limit == 1) {  //一张图片时直接返回第一张图片链接
        emits('update:modelValue', null)
    } else {
        let f = []
        files.forEach(item => {
            f.push(item.url)
        })
        emits('update:modelValue', f.join(","))
    }
}
const before_remove = async (file, files) => { //返回数据构造
    let res = await remove_file_(file)
    if (res.data.code == 200) {
        return true
    } else {
        return false
    }


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
        let values = props.modelValue.split(',')
        values.forEach(element => {
            attrs.file_list.push({ name: element.substr(element.lastIndexOf('_') + 1), url: element })
        });
    }
})
</script>
<template>
    <el-upload v-model:file-list="attrs.file_list" :limit="limit" action="/api/data/upload/" @on-progress="upload_file_"
        :on-remove="remove" :before-remove="before_remove" :on-success="sucess" :before-upload="before_upload"
        :headers="attrs.headers" :on-exceed="exceed">
        <el-button type="primary">选择文件</el-button>
    </el-upload>
</template>
<style scoped lang='scss'>

</style>
