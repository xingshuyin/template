import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";

//TODO:自动导入-图标
import Icons from "unplugin-icons/vite"; // npm i -D unplugin-icons              npm i -D @iconify/json
import IconsResolver from "unplugin-icons/resolver";

// import Unocss from "@unocss/vite";
// import UnocssConfig from "./unocss.config";

// import Inspect from "vite-plugin-inspect"; //https://github.com/antfu/vite-plugin-inspect
//TODO:自动导入
import AutoImport from "unplugin-auto-import/vite"; // npm install -D unplugin-vue-components unplugin-auto-import
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";
import { visualizer } from "rollup-plugin-visualizer"; //项目文件结构分析 npm install rollup-plugin-visualizer

// https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [vue(), Unocss(UnocssConfig)],
// });
//性能优化 https://xiaoman.blog.csdn.net/article/details/126811832
export default ({ mode }) => {
  // console.log(mode); //development     //TODO:全局-vite配置文件中获取运行环境
  // console.log(loadEnv(mode, process.cwd())); //TODO:全局-vite配置文件中获取自定义环境变量
  return defineConfig({
    // css: {
    //   preprocessorOptions: {
    //     scss: {
    //       additionalData: `@use "~/src/element.scss" as *;`,
    //     },
    //   },
    // },
    // base: "./",
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            echarts: ["echarts"],
          },
        },
      },
    },

    server: {
      proxy: {
        //TODO:跨域设置
        "/api": {
          target: "http://127.0.0.1:8002/",
          changeOrigin: true,
          rewrite: path => path.replace(/\/api/, ""),
        },
        "/media": {
          //TODO:图片路径转发
          target: "http://127.0.0.1:8002/",
          changeOrigin: true,
          rewrite: path => path,
        },
      },
      open: "http://localhost:5173/", //dev后打开链接
    },
    plugins: [
      vue(),
      // Unocss(UnocssConfig), //TODO:unocss-安装unocss
      AutoImport({
        // 自动导入 Vue,vue-router  相关函数，如：ref, reactive, toRef, useRoute, useRouter 等
        imports: ["vue", "vue-router"],

        resolvers: [
          //TODO:自动导入-自动导入element-ui组件
          ElementPlusResolver(),
          //TODO:自动导入图标-自动导入图标组件

          IconsResolver({
            prefix: "icon",
          }),
        ],
      }),
      Components({
        resolvers: [
          // 自动注册图标组件<span class="iconify" data-icon="material-symbols:10k" data-inline="false"></span>
          IconsResolver({
            prefix: false, //关闭i 的前缀 <ep-edit />    关闭了之后 就可以直接在用在icones网站复制的图标名   如 ep:avatar, 使用前得把  ep加入到enabledCollections中
            //TODO:自动导入图标-自动注册图标组件
            //使用方法 //<i-ep-edit />       ep就是elementplus的图标组的名字   edit为图标名称   只是好像不能与动态组件一块用
            //图标组网站  https://icones.netlify.app/collection/ep
            enabledCollections: ["ion", "ph", "material-symbols", "ep", "mdi", "iconoir", "ic", "uil", "teenyicons", "ooui", "carbon", "fa6-solid", "ri"],
          }),
          //TODO:自动导入-自动导入element-ui方法
          ElementPlusResolver(),
        ],
      }),
      Icons({
        autoInstall: true,
      }),
      visualizer({
        //TODO:全局-项目结构分析
        open: true, //为true时,会生成项目分析图并自动打开浏览器查看
      }),
      // Inspect(),
    ],
  });
};
