/*
 * @Filename     : request.js
 * @Description  :wjt-前端-全局请求组件
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-09-30 18:46:21
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-21 22:06:16
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
 */
import axios from "axios";
// const router = useRouter(); //全局路由对象
const get_token = () => {
  return "Bearer " + localStorage.getItem("token");
};
export default () => {
  let r_ = axios.create({
    baseURL: import.meta.env.VITE_BASE_API,
    timeout: 15000,
    headers: {
      Authorization: get_token(), //业务需要的设备编号 或者可以当成是token来理解
    },
  });
  r_.interceptors.request.use(
    config => {
      return config; //必须返回
    },
    error => {
      if (error.response.data?.code == "token_not_valid") {
        localStorage.removeItem("token"); //token无效了必须删除token
        window.location = "/#/login"; //token失效跳转登录页
      }
      return Promise.reject("interceptors.request.error", error);
    }
  );
  r_.interceptors.response.use(
    res => {
      // console.log("interceptors.response", res.config.url, res);
      return res; //必须返回
    },
    error => {
      // console.log("interceptors.response.error", error);

      if (error.response.status == 401) {
        ElMessage({
          showClose: true,
          message: error.response.data.detail,
          center: true,
        });
        localStorage.clear();
        window.location = "/#/login/";
      } else if (error.response.status == 500) {
        ElMessage({
          showClose: true,
          message: "服务器错误",
          center: true,
        });
      } else if (error.response?.data?.detail) {
        ElMessage({
          showClose: true,
          message: error.response.data.detail,
          center: true,
        });
      } else {
        ElMessage({
          showClose: true,
          message: error.response.data,
          center: true,
        });
      }
      // return Promise.reject("interceptors.request.error", error);
    }
  );
  return r_;
};

//TODO:axios-拦截器

// export default r;
export const r_sync = async (url, query) => {
  return await r.get(url, query);
};
