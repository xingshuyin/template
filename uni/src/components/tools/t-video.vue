<template>
    <view>
        <video ref="player_ref" :id="`video${data.id}`" v-if="attrs.show"
            :src="attrs.video.includes('http') ? attrs.video : base_url + '/' + attrs.video"
            @timeupdate="(e) => { check_show(e, `video${data.id}`) }" controls>
        </video>
    </view>
</template>
<script setup>
import { onMounted, reactive, ref, getCurrentInstance } from 'vue';
import { base_url } from '../../utils/request';
const player_ref = ref(null);
const props = defineProps(['data']); //子向父传数据
const attrs = reactive({
    video: '',
    show: false,
});
const instance = getCurrentInstance()
onMounted(() => {
    console.log(instance);
    init(props.data.url)
})

const init = (src) => {
    attrs.show = true
    attrs.video = src
}

const check_show = async (e, id) => {

}
</script>
<style scoped lang='scss'></style>