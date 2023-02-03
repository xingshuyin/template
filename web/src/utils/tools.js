// TODO:tool-对象数组去重
export const DuplicateObject = (arr, key) => Array.from(new Set(arr.map(e => e[key]))).map(e => arr.find(x => x[key] == e));
export const randomColor = () => {
  //随机颜色
  var col = "#";
  for (var i = 0; i < 6; i++) col += parseInt(Math.random() * 16).toString(16);
  return col;
};
export const get_token = () => {
  //TODO:tool-解析token
  var token = localStorage.getItem("token"); //在请求头中获取token
  let strings = token.split("."); //截取token，获取载体
  return JSON.parse(decodeURIComponent(decodeURI(window.atob(strings[1].replace(/-/g, "+").replace(/_/g, "/"))))); //解析，需要吧‘_’,'-'进行转换否则会无法解析
};
