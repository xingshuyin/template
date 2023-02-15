// TODO:tool-对象数组去重
import r from "./request";
export const DuplicateObject = (arr, key) => Array.from(new Set(arr.map(e => e[key]))).map(e => arr.find(x => x[key] == e));
export const randomColor = () => {
  //随机颜色
  var col = "#";
  for (var i = 0; i < 6; i++) col += parseInt(Math.random() * 16).toString(16);
  return col;
};
export const parse_token = () => {
  //TODO:tool-解析token
  var token = localStorage.getItem("token"); //在请求头中获取token
  let strings = token.split("."); //截取token，获取载体
  let r = JSON.parse(decodeURIComponent(decodeURI(window.atob(strings[1].replace(/-/g, "+").replace(/_/g, "/"))))); //解析，需要吧‘_’,'-'进行转换否则会无法解析
  let d = new Date();
  if (r.exp - d.getTime() / 1000 < 500) {
    refresh_token();
  }
  return r;
};

const refresh_token = () => {
  r()
    .post("/refresh/", { refresh: localStorage.getItem("refresh") })
    .then(response => {
      if (response.status == 200) {
        console.log("refresh_token");
        localStorage.setItem("token", response.data.access);
      } else {
        localStorage.clear();
        window.location = "/#/login/";
      }
    })
    .catch(err => {
      localStorage.clear();
      window.location = "/#/login/";
    });
};
// TODO:tool-嵌套字典列表搜索
// [{ name: a, childern: [{ name: b, childern: [] }] }];   value->name
export const deep_search = (list, key, value) => {
  for (let index = 0; index < list.length; index++) {
    const i = list[index];
    if (i[key != undefined ? key : "name"] == value) return i;
    else if (i?.children?.length > 0) {
      let c = deep_search(i.children, value);
      if (c) return c;
    }
  }
  return false;
};
