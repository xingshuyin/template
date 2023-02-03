<!--
 * @Filename     : player.vue
 * @Description  : wjt-前端-视频播放器
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-10-16 07:58:52
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-17 15:01:11
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
//import { ref } from 'vue';
//import {useRoute, useRouter} from 'vue-router';
//const route = useRoute() //当前路由
//const router = useRouter() //全局路由对象
//const props = defineProps({ data: Object, title: String}); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['onclick']); // emits 触发父组件函数
//const map = ref(null); //获取ref值为map的元素
//defineExpose({ map,}); //暴露组件的内容, 父组件通过组件对象(如ref)的value获取暴露的对象
import { onMounted, watch } from "vue";
import store from "../store/index";
//通过store.video传递信息
const get_url = ref(false)
const video_options = reactive({
    width: '100%', //播放器高度
    height: '700px', //播放器高度
    color: "#409eff", //主题色
    title: null, //视频名称
    src: '', //视频源
    muted: false, //静音
    webFullScreen: false,
    speedRate: ["0.75", "1.0", "1.25", "1.5", "2.0"], //播放倍速
    autoPlay: false, //自动播放
    loop: false, //循环播放
    mirror: false, //镜像画面
    ligthOff: false,  //关灯模式
    volume: 0.3, //默认音量大小
    control: true, //是否显示控制器
})
onMounted(() => {
    video_options.src = store().video.url
    get_url.value = true
    console.log('play video', video_options)
})
</script>
<template>
    <el-dialog v-if="get_url" :title="store().video.title" v-model="store().video.show" center align-center width="70%"
        destroy-on-close style="height: fit-content;" @closed="store().video.url = null; get_url = false">
        <template #header="{ close, titleId, titleClass }">
        </template>
        <div style="width: 100%;height: 100%;display: flex; justify-content: center;align-items: center;">
            <vue3VideoPlay v-bind="video_options" :poster='store?.video?.cover' />
        </div>
    </el-dialog>
</template>
<style scoped lang='scss'>

</style>
