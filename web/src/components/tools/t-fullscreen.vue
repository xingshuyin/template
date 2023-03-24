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
