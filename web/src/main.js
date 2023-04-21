import { createApp } from "vue";
import "./style.scss";
import "./element.scss";
import "./initial.css";
import "./assets/css/quill.snow.css";
// import "uno.css"; // npm i -D @unocss/vite (无预设安装)   还需要在vite.config.ts中配置  具体看->  https://github.com/unocss/unocss/tree/main/packages/vite
import "animate.css";
import "element-plus/dist/index.css"; //导入element样式文件
import r from "./utils/request";

// import BaiduMap from "vue-baidu-map-3x"; //npm install vue-baidu-map-3x --save

import * as ElementPlusIconsVue from "@element-plus/icons-vue"; //引入所有element图标

import { createPinia } from "pinia"; //引入pinia   npm install pinia
import store from "./store/index";
const pinia = createPinia();

import App from "./App.vue";
import vue3videoPlay from "vue3-video-play"; // 引入组件  npm i vue3-video-play --save
import "vue3-video-play/dist/style.css"; // 引入css    npm i vue3-video-play --save

const views = import.meta.glob("./views/*/*.vue"); //TODO:动态路由-引入所有菜单路径,然后才能动态引入
import route from "./route"; //引入路由组件

// import VMdEditor from "@kangc/v-md-editor"; //pnpm i @kangc/v-md-editor@next -S
// import "@kangc/v-md-editor/lib/style/base-editor.css";
// import vuepressTheme from "@kangc/v-md-editor/lib/theme/vuepress.js";

// import VMdPreview from "@kangc/v-md-editor/lib/preview";
// import "@kangc/v-md-editor/lib/style/preview.css";
// import githubTheme from "@kangc/v-md-editor/lib/theme/github.js";
// import "@kangc/v-md-editor/lib/theme/style/github.css";
// // highlightjs
// import Prism from "prismjs";
// import hljs from "highlight.js";
// VMdEditor.use(vuepressTheme, {
//   Prism,
// });
// VMdPreview.use(githubTheme, {
//   Hljs: hljs,
// });

const app = createApp(App);
app.use(route); //使用路由组件
app.use(pinia);
// app.use(BaiduMap, { ak: "ium5InHYNhRUBiSlGWeak9i6ufZ5jdf3" });
app.use(vue3videoPlay);
// app.use(VMdEditor);
// app.use(VMdPreview);

app.mount("#app");
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  //注册所有element图标    <el-button icon="Search"/>   <el-icon :size="20"> <Edit /> </el-icon>
  app.component(key, component);
}

//------------------------router开始-----------------------------
const RoutesTree = (data, parent) => {
  //TODO:生成树状结构
  let d = [];
  data.forEach(item => {
    if (item.parent == parent && item.disable == 0) {
      d.push({
        id: item.id,
        name: item.name,
        path: item.path,
        label: item.label,
        is_link: item.is_link,
        icon: item.icon,
        sort: item.sort,
        is_catalog: item.is_catalog,
        component: views["./views/" + item.component],
        meta: { title: item.label, animate: "animate__fadeIn" },
        children: RoutesTree(data, item.id, item.name),
      });
    }
  });
  return d;
};

const set_menu = () => {
  store().menu.forEach(element => {
    route.addRoute("layout", element);
  });
  store().hasmenu = true;
};

const get_menu = (to, next) => {
  r()
    .get("/data/GetMenu/", { params: { disable: false } })
    .then(res => {
      if (res) {
        let routestree = RoutesTree(res.data, null);
        // routestree.forEach(element => {
        //   // console.log("添加路由", element)
        //   route.addRoute("layout", element);
        // });
        store().hasmenu = true;
        store().menu = routestree;
        set_menu();
        next({ ...to, replace: true }); //必须要用这个,不然就刷新空白
      } else {
        localStorage.clear();
        next("/login");
      }
    });
};
const whiteList = ["/login"]; //前置守卫白名单
route.beforeEach((to, from, next) => {
  console.log("进入", to.path);
  if (to.meta.title != undefined) window.document.title = to.meta.title;
  //TODO:router-前置守卫
  if (localStorage.getItem("token") && localStorage.getItem("refresh")) {
    store()
      .get_userinfo()
      .then(res => {
        if (!res) {
          localStorage.clear();
          next("/login");
        }
        if (res.is_super || res.type == 2) {
          if (to.path.startsWith("/admin")) {
            if (store().menu.length > 0) {
              //判断store中是否有菜单数据
              if (!store().hasmenu) set_menu(); //判断是否已经添加路由
              if (to.matched.length === 0) next("/admin/article"); //未知页面跳到首页
              // if (to.meta.title != undefined) window.document.title = to.meta.title; //TODO:设置标题
              next(); // 进入页面, 其他带参数都是跳转路由
            } else get_menu(to, next); //没有菜单数据获取数据
          } else {
            // if (to.path === "/login") next("/admin"); //TODO:router-有token登录页跳转首页
            // next("/admin/enterprise");
            next(); //必须要用这个,不然就刷新空白
          }
        } else {
          if (to.path === "/login") next("/");
          // refresh_token(to, next);
          next();
        }
      });
  } else {
    if (whiteList.includes(to.path)) next(); //白名单中路由直接进入
    else if (to.path.startsWith("/admin")) next("/login");
    else next(); //不在白名单进入登录页
  }
});
route.afterEach((to, from, next) => {
  // TODO:router-后置守卫
});
//------------------------router结束---------------------------
