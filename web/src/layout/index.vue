<script setup>
import Side from './side.vue'
import Head from './head.vue'
const router = useRouter()
const route = useRoute()
</script>
<template>
  <!-- TODO:整体框架 -->
  <!-- <processLine></processLine> -->
  <div class="layout">
    <div class="layout-top">

      <Head></Head>
    </div>
    <div class="layout-bottom">
      <div class="layout-bottom-left">
        <Side></Side>
      </div>
      <div class="layout-bottom-right">
        <t-menu-tabs></t-menu-tabs>
        <div class="layout-bottom-main">

          <router-view #default="{ route, Component }">
            <!-- TODO:router-添加animate动画 -->
            <!-- animate动画   https://www.jq22.com/yanshi819 =>  animate__animated animate__动画名 -->
            <!-- 通过路由源信息可以给每个路由添加一个animate的动画类名;渲染视图时用transition 接受这个类名;并用component渲染组件-->
            <transition :enter-active-class="`animate__animated ${route.meta.animate}`" appear
              leave-to-class="router-leave-to" leave-from-class="router-leave-from">
              <!-- TODO:动画 -->
              <!-- https://cn.vuejs.org/guide/built-ins/transition.html#css-based-transitions -->
              <!-- TODO:动态组件 -->
              <!-- Component为组件的实例,不能直接使用字符串,想使用字符串=>全局组件,用选项式api声明组件 -->
              <div style="height: 100%;width: 100%;">
                <component :is='Component'></component>
              </div>
            </transition>
          </router-view>
        </div>
      </div>


    </div>
  </div>
</template>
<style scoped lang="scss">
.layout {
  position: absolute;
  left: 0;
  top: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: aliceblue;

  .layout-top {
    width: 100vw;
    height: 42px;
    overflow: hidden;
    box-shadow: 0px 0px 1px 0px black;
  }

  .layout-bottom {
    width: 100vw;
    height: calc(100vh - 40px);
    display: flex;
    flex-direction: row;
    overflow: auto;

    .layout-bottom-left {
      width: max-content;
      height: 100%;
      overflow-y: visible;
      overflow: visible;
      position: relative;
      z-index: 6;
      box-shadow: 0px 0px 1px 0px black;

    }

    .layout-bottom-right {
      flex: 1;
      // width: 500px;
      height: 100%;
      display: flex;
      overflow: auto;
      flex-direction: column;

      .layout-bottom-main {
        // width: 100%;
        flex: 1;
        // height: 100%;
        overflow: auto;
        z-index: 5;
        position: relative;
      }
    }

  }
}
</style>
