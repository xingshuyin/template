<!--
 * @Filename     : scroll.vue
 * @Description  : wjt-前端-无限滚动
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-10-22 19:32:53
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-17 14:47:19
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
// 注意:  父组件必须有宽高
import { ref, onMounted, onUpdated } from 'vue';
const props = defineProps({}); // defineProps的参数, 可以直接使用
const scroll_item_a = ref(null)
const scroll_item_b = ref(null)
const scroll = ref(null)
const scroll_body = ref(null)
var height = ref('')
var ScrollTime = ref('')
onMounted(() => {
    ScrollTime.value = parseInt(scroll_item_a.value.offsetHeight / 30) + 's' //获取滚动时间
    height.value = '-' + scroll_item_a.value.offsetHeight + 'px'  //获取滚动目标的高度
    if (scroll_item_a.value.offsetHeight < scroll.value.offsetHeight) {
        scroll_item_b.value.style.display = 'none'
        scroll_body.value.style.animationPlayState = 'paused'
    }
})
onUpdated(() => {
    ScrollTime.value = parseInt(scroll_item_a.value.offsetHeight / 30) + 's' //获取滚动时间
    height.value = '-' + scroll_item_a.value.offsetHeight + 'px'  //获取滚动目标的高度
    if (scroll_item_a.value.offsetHeight < scroll.value.offsetHeight) {
        scroll_item_b.value.style.display = 'none'
        ScrollTime.value = '0'
    } else {
        scroll_item_b.value.style.display = 'block'
        scroll_body.value.style.animationPlayState = 'running'
        // scroll_body.value.style.animationPlayState = 'paused'

    }

})
// TODO:动画-无限滚动
</script>
<template>
    <div class="scroll" ref="scroll">
        <div class="scroll-body" ref="scroll_body">
            <div ref="scroll_item_a" class="scroll-item">
                <slot></slot>
            </div>
            <div ref="scroll_item_b" class="scroll-item">
                <slot></slot>
            </div>
        </div>
    </div>
</template>
<style scoped lang="scss">
.scroll {
    width: 100%;
    height: 100%;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.scroll-body {
    height: 100%;
    width: 100%;
    animation: v-bind(ScrollTime) rowup linear infinite normal;
}

.scroll-body:hover {
    animation-play-state: paused !important;
}

.scroll-item {
    width: 100%;
    height: fit-content;
}


@keyframes rowup {
    0% {
        // -webkit-transform: translate3d(0, 0, 0);
        // transform: translate3d(0, 0, 0);
    }

    100% {
        // TODO:样式-使用js变量
        -webkit-transform: translate3d(0, v-bind(height), 0);
        transform: translate3d(0, v-bind(height), 0);
        display: none;
    }
}
</style>
