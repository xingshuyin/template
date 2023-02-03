<!--
 * @Filename     : full_screen.vue
 * @Description  : wjt-前端-全屏按钮
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-11-04 13:10:35
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-17 14:30:43
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
import { api as fullscreen } from 'vue-fullscreen'
const full = ref(false)
</script>
<template>
    <el-button @click="fullscreen.toggle(); full = !full" circle size="small">
        <mdi:fullscreen v-if="!full"></mdi:fullscreen>
        <mdi:fullscreen-exit v-else></mdi:fullscreen-exit>
    </el-button>
</template>
<style scoped lang='scss'>

</style>
