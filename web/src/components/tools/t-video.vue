<template>
    <vue3VideoPlay v-if="attrs.show" ref="player_ref" v-element-visibility="video_pause" v-bind="attrs.video" />
</template>
<script setup>
// https://xdlumia.github.io/guide/install.html
// https://vueuse.org/shared/createGlobalState/  //TODO:vueuse
import { vElementVisibility } from '@vueuse/components'   // npm i @vueuse/core @vueuse/components
import { onMounted } from 'vue';
const props = defineProps(['data']); //子向父传数据
const player_ref = ref();
const attrs = reactive({
    video: {},
    show: false,
});
const video_pause = (state) => {
    if (state) {
        player_ref.value.pause(); // 超出屏幕停止
    }
}
onMounted(() => {
    init(props.data.url)
})
const init = (src) => {
    attrs.show = true
    console.log(src);
    attrs.video = { //TODO:视频播放
        width: '100%', //播放器高度
        height: '100%', //播放器高度
        color: "#fff", //主题色
        title: '', //视频名称
        src: src, //视频源
        muted: false, //静音
        webFullScreen: false,
        speedRate: ["0.75", "1.0", "1.25", "1.5", "2.0"], //播放倍速
        autoPlay: false, //自动播放
        loop: false, //循环播放
        mirror: false, //镜像画面
        ligthOff: false,  //关灯模式
        volume: 0.3, //默认音量大小
        control: true, //是否显示控制
        preload: 'meta',
        controlBtns: ['audioTrack', 'quality', 'speedRate', 'volume', 'setting', 'pip', 'pageFullScreen', 'fullScreen'] //显示所有按钮,
    }
}

</script>
<style scoped lang='scss'></style>