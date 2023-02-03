/*
 * @Filename     : unocss.config.js
 * @Description  :unocss 通过类名配置样式
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-09-30 17:47:44
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-18 10:58:12
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
 */
export default {
  presets: [],
  rules: [
    //TODO:unocss-自定义样式类名
    [/flex(\d+)/, ([, num]) => ({ flex: num })],
    //()=>({}) 自调用,返回{}, 传入第一个参数为待匹配的字符串,后面的参数皆为按顺序匹配到的组
    [/^bg_((#|rgb).*)/, ([, color]) => ({ background: color })], //TODO:unocss-正则动态样式
    ["bg-center", { "background-position": "center", "background-repeat": "no-repeat", "background-size": "cover" }],
    [/flex_(r|c)_jc-(.*?)_ai-(.*)/, ([, direction, jc, ai]) => ({ display: "flex", "justify-content": jc, "align-items": ai, "flex-direction": direction == "c" ? "column" : "row" })],
    [/^m(\d+)/, ([, num]) => ({ margin: `${num}px` })],
    [/^p(\d+)/, ([, num]) => ({ padding: `${num}px` })],
    [/^w(\d+%|\d+px|\d+vw)/, ([, num]) => ({ width: `${num}` })],
    [/^h(\d+%|\d+px|\d+vh)/, ([, num]) => ({ height: `${num}` })],
    [/^z(\d+)/, ([, num]) => ({ "z-index": `${num}` })],
    [/trans_x(.*?)_y(.*)/, ([, x, y]) => ({ transform: `translate(${x}, ${y})` })],
    [/pos_(a|r)_(l|r)(.*?)_(t|b)(.*)/, ([, position, x, x_num, y, y_num]) => ({ position: position == "a" ? "absolute" : "relative", [x == "l" ? "left" : "right"]: x_num, [y == "t" ? "top" : "bottom"]: y_num })],
    [/pos_(a|r)_(t|b)(.*?)_(l|r)(.*)/, ([, position, y, y_num, x, x_num]) => ({ position: position == "a" ? "absolute" : "relative", [x == "l" ? "left" : "right"]: x_num, [y == "t" ? "top" : "bottom"]: y_num })],
  ],
  // 组合rules中的样式
  shortcuts: {
    // c: ["bg-center", "flex-center"],
  },
};
