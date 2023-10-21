// export const base_url = "http://121.89.199.142:59978/api";
export const base_url =
  process.env.NODE_ENV === "development"
    ? "http://127.0.0.1:8000"
    : "http://121.89.199.142/api";
const base = base_url.replace(/[\s\t\n\r\\/]+$/, "");
export default {
  get_: (url, data) => {
    return uni.request({
      url: url,
      method: "GET",
      data: data,
      header: {
        "content-type": "application/json",
      },
    });
  },
  get: (url, data, force = true) => {
    console.log(base + "/" + url.replace(/^[\s\t\n\r\\/]+/, ""));
    return uni.request({
      url: base + "/" + url.replace(/^[\s\t\n\r\\/]+/, ""),
      method: "GET",
      data: data,
      header: {
        "content-type": "application/json",
        "http-force": force ? "true" : "false",
        Authorization: uni.getStorageSync("access")
          ? "Bearer  " + uni.getStorageSync("access")
          : null,
      },
    });
  },
  post: (url, data) => {
    return uni.request({
      url: base + "/" + url.replace(/^[\s\t\n\r\\/]+/, ""),
      method: "POST",
      data: data,
      header: {
        "content-type": "application/json",
        Authorization: uni.getStorageSync("access")
          ? "Bearer  " + uni.getStorageSync("access")
          : null,
      },
    });
  },
  form: (url, data) => {
    return uni.request({
      url: base + "/" + url.replace(/^[\s\t\n\r\\/]+/, ""),
      method: "POST",
      data: data,
      header: {
        "content-type": "application/x-www-form-urlencoded",
        Authorization: uni.getStorageSync("access")
          ? "Bearer  " + uni.getStorageSync("access")
          : null,
      },
    });
  },
  delete: (url) => {
    return uni.request({
      url: base + "/" + url.replace(/^[\s\t\n\r\\/]+/, ""),
      method: "DELETE",
      header: {
        "content-type": "application/json",
        Authorization: uni.getStorageSync("access")
          ? "Bearer  " + uni.getStorageSync("access")
          : null,
      },
    });
  },
  put: (url, data) => {
    return uni.request({
      url: base + "/" + url.replace(/^[\s\t\n\r\\/]+/, ""),
      method: "PUT",
      data: data,
      header: {
        "content-type": "application/json",
        Authorization: uni.getStorageSync("access")
          ? "Bearer  " + uni.getStorageSync("access")
          : null,
      },
    });
  },
};
