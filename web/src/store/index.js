import { defineStore } from "pinia";
import r from "../utils/request";
import rest from "../utils/rest";
import { Tree } from "../utils/data";

export default defineStore("counter", {
  state: () => ({
    all_menu: null,
    current_menu: "enterprise",
    menu_width: "200px",
    menu_tab: [],
    menu: [],
    userinfo: null,
    hasmenu: false,
    toggle_side: false,
    is_login: false,
  }),
  getters: {
    // get_userinfo: (state) => {
    //   return async (not_cache) => {
    //     if (!not_cache) {
    //       if (state.userinfo) {
    //         return state.userinfo;
    //       }
    //     }
    //     let a = await r().get("/data/get_userinfo/");
    //     if (a) {
    //       state.userinfo = a.data;
    //       return a.data;
    //     } else {
    //       localStorage.clear();
    //       window.location = "/#/login/";
    //     }
    //   };
    // },
    // get_areas_tree: (state) => {
    //   return async (not_cache) => {
    //     if (!not_cache) {
    //       if (state.areas_tree) {
    //         return state.areas_tree;
    //       }
    //     }
    //     let a = await r().get("/area/", { params: { page: 1, limit: 99999 } });
    //     if (a) {
    //       state.areas_tree = Tree(a.data.data, "code", "parent", null);
    //       return state.areas_tree;
    //     } else {
    //       localStorage.clear();
    //       window.location = "/#/login/";
    //     }
    //   };
    // },
  },
  actions: {
    async get_userinfo(cache) {
      if (cache && this.userinfo != null) return this.userinfo;
      let a = await r().get("/data/get_userinfo/");
      if (a.statusCode >= 400) {
        localStorage.clear();
        window.location = "/#/login/";
      } else {
        this.userinfo = a.data;
        return a.data;
      }
    },
    async get_areas_tree(cache = true) {
      if (cache) {
        if (this.areas_tree) {
          return this.areas_tree;
        }
      }
      let a = await r().get("/area/", { params: { page: 1, limit: 99999 } });
      if (a) {
        this.areas_tree = Tree(a.data.data, "code", "parent", null);
        return this.areas_tree;
      } else {
        localStorage.clear();
        window.location = "/#/login/";
      }
    },
  },
});
