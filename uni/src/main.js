import { createSSRApp } from "vue";
import * as Pinia from "pinia"; // https://uniapp.dcloud.net.cn/tutorial/vue3-pinia.html#%E7%8A%B6%E6%80%81%E7%AE%A1%E7%90%86-pinia
import uView from "./uni_modules/vk-uview-ui"; // https://ext.dcloud.net.cn/plugin?name=vk-uview-ui
// https://ext.dcloud.net.cn/plugin?id=55
import App from "./App.vue";
export function createApp() {
  const app = createSSRApp(App);
  app.use(Pinia.createPinia());
  app.use(uView);
  return {
    app,
  };
}
