<template>
    <view>
        <!-- #ifdef MP-WEIXIN -->
        <u-navbar back-text="返回"></u-navbar>
        <!-- #endif -->
        <web-view :src="'https://blog.csdn.net/allway2/article/details/116568687'" :fullscreen="false" :webview-styles="{
            width: '100%',
            height: '100%',
        }"></web-view>
    </view>
</template>
<script setup>
import { onLoad } from '@dcloudio/uni-app';
import { reactive } from 'vue';
const attrs = reactive({
    url: null
});
onLoad((option) => {
    attrs.url = option.url;
})
</script>
<style scoped lang='scss'></style>