import { defineStore } from "pinia";
import r from "../utils/request";
import rest from "../utils/rest";
export const GlobalStore = defineStore("counter", {
  state: () => ({
    all_menu: null,
    current_menu: "enterprise",
    menu_width: "200px",
    menu_tab: [],
    menu: [],
    userinfo: null,
    hasmenu: false,
    toggle_side: false,
    // detail_show: false,
    // detail_type: null,
    // detail_data: null,
  }),
  getters: {
    get_userinfo: state => {
      return async not_cache => {
        if (!not_cache) {
          if (state.userinfo) {
            return state.userinfo;
          }
        }
        let a = await r().get("/data/get_userinfo/");
        if (a) {
          state.userinfo = a.data;
          return a.data;
        } else {
          localStorage.clear();
          window.location = "/#/login/";
        }
      };
    },
    get_areas_tree: state => {
      return async not_cache => {
        if (!not_cache) {
          if (state.areas_tree) {
            return state.areas_tree;
          }
        }
        let a = await r().get("/Area/", { params: { page: 1, limit: 99999 } });
        if (a) {
          state.areas_tree = a.data;
          return a.data;
        } else {
          localStorage.clear();
          window.location = "/#/login/";
        }
      };
    },
  },
  actions: {},
});

export default defineStore("counter", {
  state: () => ({
    all_menu: null,
    current_menu: "enterprise",
    menu_tab: [],
    menu: [],
    userinfo: null,
    hasmenu: false,
    toggle_side: false,
    // detail_show: false,
    // detail_type: null,
    // detail_data: null,
  }),
  getters: {
    get_userinfo: state => {
      return async not_cache => {
        if (!not_cache) {
          if (state.userinfo) {
            return state.userinfo;
          }
        }
        let a = await r().get("/data/get_userinfo/");
        if (a) {
          state.userinfo = a.data;
          return a.data;
        } else {
          localStorage.clear();
          window.location = "/#/login/";
        }
      };
    },
  },
  actions: {},
});
