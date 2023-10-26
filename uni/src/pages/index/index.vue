<template>
  <view
    style="height: var(--status-bar-height);position: fixed;top: 0;z-index: 1; background-color: antiquewhite;width: 100vw;">
    <!-- 这里是状态栏 -->
  </view>
  <view style="height: var(--status-bar-height);z-index: 1;">
    <!-- 这里是状态栏 -->
  </view>
  <articleL ref="articleLRef" :data="attrs.data" username="user__name" icon="user__icon"></articleL>
</template>
<script setup>
import articleL from '../../components/list/articleL'
import r from '../../utils/request'
import rest from '../../utils/rest'
import { onMounted, reactive, ref } from 'vue'
import { onLoad, onReady, onShow, onHide, onUnload, onPullDownRefresh, onReachBottom, onPageScroll, onShareAppMessage } from '@dcloudio/uni-app';
const articleLRef = ref();
const attrs = reactive({
  url: 'article',
  form: {
    page: 1,
    limit: 10,
    sort: '-create_time',
    'extra[]': ['user__name', 'user__icon'],
  },
  end: false,
  data: [],
  loading: false,
});



const get_data = (replace) => {
  attrs.loading = true
  if (replace) attrs.form.page = 1;
  rest.list(attrs.url, attrs.form, null, null, (res) => {
    attrs.loading = false
    if (replace) { attrs.data = res.data.data; articleLRef.value.check(0) }
    else {
      if (res.data.data.length === 0) { attrs.end = true }
      else {
        let l = attrs.data.length
        attrs.data.push(...res.data.data); attrs.form.page++; articleLRef.value.check(l)
      }
    }
  })
}

onMounted(() => {
  get_data()
})
onReachBottom(() => {
  get_data()
})
onPullDownRefresh(() => {
  get_data(true)
})
</script>
<style scoped lang='scss'></style>