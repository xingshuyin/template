<!--
 * @Filename     : side.vue
 * @Description  : wjt-前端-后台管理菜单
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-09-30 18:13:42
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-12-14 11:19:29
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
// import { ref, reactive, watch } from 'vue';
import MenuTree from './MenuTree.vue';
// import { useRoute, useRouter } from 'vue-router';
import store from "../store/index";
const route = useRoute() //当前路由
const router = useRouter() //全局路由对象
// const items = JSON.parse(sessionStorage.getItem('menu'))
const items = store().menu

const collapse = ref(false)
const menu_width = ref('200px')
// https://blog.csdn.net/qq_34465338/article/details/124949520
//     系统框架->左侧菜单栏
</script>
<template>

    <div :style="`height: 100%;overflow: visible;width: ${menu_width};position: relative;`">
        <div style="height: 100%;" class="side common-scroll">
            <el-menu class="menu" router :collapse="store().toggle_side" background-color="rgba(0,0,0,0)"
                active-text-color="yellow" :collapse-transition="true" text-color="white"
                :default-active="route.fullPath" unique-opened>
                <MenuTree :data="items" :parent_path="'/admin'"></MenuTree>
            </el-menu>



            <div class="collapse-btn"
                @click="store().toggle_side = !store().toggle_side; store().toggle_side ? menu_width = '50px' : menu_width = '200px'">
                <ep:arrow-left v-if="!store().toggle_side" style="font-size: 10px;color: black;" />
                <ep:arrow-right v-else style="font-size: 10px;color: black;" />
            </div>
            <!-- <el-button :icon="'Search'" class="collapse-btn" circle @click="collapse=!collapse" /> -->
        </div>

    </div>


</template>
 

<style scoped lang="scss">
.side {
    // background-color: burlywood;
    // position: relative;
    // background: linear-gradient(to bottom, rgb(31 104 84) 0%, #8d8678 100%); // 绿色渐变
    // background: linear-gradient(to bottom, rgb(12 205 255) 0%, #5f57d4 100%);
    background: rgb(100 100 100);
    overflow-y: auto;
    overflow-x: hidden;
    width: v-bind(menu_width);
    transition: 400ms;
    // padding-right: 5px;

}

.side:hover>.collapse-btn {
    // collapse-btn必须在menu下边

    width: 10px;

}

.collapse-btn {
    // display: none;
    display: flex !important;
    align-items: center;
    position: absolute;
    overflow: hidden;
    right: 0;
    top: 0;
    width: 0px;
    // top: 50%;
    height: 100%;
    // transition-delay: 400ms;
    // transition: 1000ms;
    background-color: rgba(255, 255, 255, 0.281);

    // transform: translateY(-50%);
}

.menu {
    // width: v-bind(menu_width);
    border: 0;

    .el-menu-item,
    .el-sub-menu {
        width: 100%;
        padding-right: 0;
    }

}

// TODO:自定义滚动条 

:deep(.el-menu) {

    .el-menu-item,
    .el-sub-menu {
        width: 100%;
        padding-right: 0;
    }

}

:deep(.el-menu--collapse) {
    width: 50px;

    .el-menu-item,
    .el-sub-menu {
        width: 100%;
        padding: 0;

        .el-tooltip__trigger {
            padding: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
    }
}
</style>
