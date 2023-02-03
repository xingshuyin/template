/*
 * @Filename     : index.js
 * @Description  :wjt-前端-全局路由文件
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-09-30 17:43:42
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-20 11:00:15
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
 */
import { createRouter, createWebHashHistory } from "vue-router";
const router = createRouter({
  // npm install vue-router@4
  //TODO:router-创建router
  // 路由模式  https://www.bilibili.com/video/BV1dS4y1y7vd?p=77&spm_id_from=pageDriver&vd_source=5a8d3b99ea863352520bda5fad9b504d
  //TODO:router-history记录历史方式
  history: createWebHashHistory(),
  routes: [
    { path: "/login", name: "login", component: () => import("../views/login/index.vue"), meta: { title: import.meta.env.title, animate: "animate__fadeIn" } },
    {
      path: "/admin",
      name: "layout",
      // redirect: "index",
      component: () => import("../layout/index.vue"),
      meta: { title: import.meta.env.title, animate: "animate__fadeIn" },
      children: [],
    },
    {
      path: "/",
      name: "front",
      component: () => import("../views/front/index.vue"),
      meta: { title: import.meta.env.title, animate: "animate__fadeIn" },
      children: [],
    },
  ],
});
export default router;
