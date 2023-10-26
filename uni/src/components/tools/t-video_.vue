<template>
    <view style="width: 100%;">
        <video style="width: 100%;" ref="player_ref" :id="`video${data.id}`" v-if="show"
            :src="video.includes('http') ? video : base_url + '/' + video" controls>
        </video>
    </view>
</template>
<script>
import { base_url } from '../../utils/request'
export default {
    // data() 返回的属性将会成为响应式的状态
    // 并且暴露在 `this` 上
    data() {
        return {
            show: false,
            base_url: base_url,
            scrollTop: 0
        }
    },
    onPageScroll(e) {
        console.log(e);
        this.$u.getRect(this.$refs['player_ref']).then(res => {
            console.log(res) // 输出 vnode 的位置和尺寸信息
        })
        this.check_position()
    },
    props: ['data'],
    // methods 是一些用来更改状态与触发更新的函数
    // 它们可以在模板中作为事件处理器绑定
    methods: {

        check_position() {
            console.log(player_ref.value, instance.vnode);
            // let a = await instance.proxy.$u.getRect('#video1')
            // console.log('aaaaaaa', a);
        },
        init(src) {
            this.show = true
            this.video = src
        }
    },

    // 生命周期钩子会在组件生命周期的各个不同阶段被调用
    // 例如这个函数就会在组件挂载完成后被调用
    mounted() {
        this.init(this.data.url)
    },
}
</script>
<style scoped lang='scss'></style>