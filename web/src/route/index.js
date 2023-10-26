import { createRouter, createWebHashHistory } from "vue-router";
const router = createRouter({
  // npm install vue-router@4
  //TODO:router-创建router
  // 路由模式  https://www.bilibili.com/video/BV1dS4y1y7vd?p=77&spm_id_from=pageDriver&vd_source=5a8d3b99ea863352520bda5fad9b504d
  //TODO:router-history记录历史方式
  history: createWebHashHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("../views/login/index.vue"),
      meta: { title: import.meta.env.title, animate: "animate__fadeIn" },
    },
    {
      path: "/admin",
      name: "layout",
      redirect: "/admin/article",
      component: () => import("../layout/index.vue"),
      meta: { title: import.meta.env.title, animate: "animate__fadeIn" },
      children: [
        {
          path: "userinfo",
          name: "userinfo",
          component: () => import("../views/system/user_message.vue"),
          meta: { title: "个人信息", animate: "animate__fadeIn" },
          children: [],
        },
      ],
    },
    {
      path: "/",
      name: "front",
      component: () => import("../views/front/index.vue"),
      meta: { title: "首页", animate: "animate__fadeIn" },
      children: [],
    },
    {
      path: "/article/:id",
      name: "article_detail",
      component: () => import("../views/front/article.vue"),
      meta: { title: "文章", animate: "animate__fadeIn" },
      children: [],
    },
  ],
});
export default router;
