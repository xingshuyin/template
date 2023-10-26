<template>
    <div class="image-wall">
        <image class="image" mode="aspectFill" v-for="img in data" :key="img.url"
            :src="img.url.includes('http') ? img.url : base_url + '/' + img.url" alt=""
            @click="show(img.url.includes('http') ? img.url : base_url + '/' + img.url)">
        </image>
    </div>
</template>
<script setup>
import { reactive } from 'vue';
import { base_url } from '../../utils/request';
const props = defineProps(['data']); //子向父传数据
const attrs = reactive({
    view_url: null,
    view_show: false,
});

const show = (url) => {
    uni.previewImage({
        urls: [url],
    })
}
</script>
<style scoped lang='scss'>
.image-wall {
    display: flex;
    flex-direction: row;
    // align-items: center;
    // justify-content: space-around;
    gap: 10px;
    flex-wrap: wrap;

    .image {
        width: 280rpx;
        height: 280rpx;
    }

    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
}
</style>