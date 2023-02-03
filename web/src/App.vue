<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import { ElLoading } from 'element-plus'
import { onBeforeMount } from 'vue';
const loading = ref(null)
onBeforeMount(() => { //TODO:刷新加载动画
  loading.value = ElLoading.service({
    lock: true,
    text: '加载中',
    background: '#2da4dc',
  })
})

onMounted(() => {
  loading.value.close()
})
</script>

<template>
  <router-view></router-view>
</template>

<style scoped lang="scss">
.el-loading-spinner {
  .circular {
    .path {
      stroke: aqua !important;
    }

  }
}
</style>
