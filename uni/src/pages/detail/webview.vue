<template>
    <view>
        <!-- #ifdef MP-WEIXIN -->
        <u-navbar back-text="返回"></u-navbar>
        <!-- #endif -->
        <web-view :src="attrs.url" :fullscreen="false" :webview-styles="{
            width: '100%',
            height: '710',
            top: '70'
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
    if (option.url != null) {
        attrs.url = option.url;
    } else {
        attrs.url = 'https://www.baidu.com';
    }
})
</script>
<style scoped lang='scss'></style>