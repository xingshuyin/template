<!--
 * @Filename     : scroll_step.vue
 * @Description  : wjt-前端-逐步滚动  line_count->行数
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-10-24 09:53:23
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-17 14:32:07
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
// 注意:  父组件必须有宽高
import { ref, onMounted, onUpdated, onBeforeUnmount } from 'vue';
const props = defineProps(['line_count']); // defineProps的参数, 可以直接使用
const scroll_item_a = ref(null)
const scroll = ref(null)
const scroll_body = ref(null)
var scroll_height = ref(0)
var scroll_top = ref('')
var scroll_duration = ref('1000ms')
var scrolling = ref(true)
const step = ref(null)
const line = ref(0)
const start = () => {
    step.value = setInterval(() => {
        if (scrolling.value) {
            scroll_height.value = scroll_body.value.offsetHeight / 2 / props.line_count  //获取滚动目标的高度
            if (line.value < props.line_count + 1) {
                scroll_duration.value = '1000ms'
                scroll_top.value = '-' + scroll_height.value * line.value + 'px'
                line.value += 1
            }
            else {
                line.value = 0
                scroll_duration.value = '0'
                scroll_top.value = 0
            }
        }

    }, 4000)
}
onMounted(() => {
    start()
})
onBeforeUnmount(() => {
    clearInterval(step.value)
})
// TODO:动画-无限滚动
</script>
<template>
    <div class="scroll" ref="scroll" :style="{ height: '100%' }" @onmouseover="scrolling = false"
        @onmouseleave="scrolling = true">
        <div class="scroll-body" ref="scroll_body">
            <slot></slot>
            <slot></slot>
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
    // height: fi;
    transition-duration: v-bind(scroll_duration);
    top: v-bind(scroll_top);
    position: relative;
    width: 100%;
}
</style>
