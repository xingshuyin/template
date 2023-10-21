import { defineStore } from "pinia";
import r from "../utils/request";

export default defineStore("counter", {
  state: () => ({
    is_login: false,
    userinfo: null,
  }),
  getters: {},
  actions: {
    async get_userinfo(cache) {
      if (cache && this.userinfo != null) return this.userinfo;
      let a = await r.get("/data/get_userinfo/");
      if (a.statusCode >= 400) {
        uni.reLaunch({
          url: "/pages/login/index",
          success(res) {
            localStorage.clear();
          },
          fail(res) {
            localStorage.clear();
          },
        });
      } else {
        this.userinfo = a.data;
        return a.data;
      }
    },
  },
});
