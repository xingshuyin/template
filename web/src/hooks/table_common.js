/*
 * @Filename     : table_common.js
 * @Description  :wjt-前端-菜单通用接口
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-10-14 15:20:49
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-12-01 21:49:10
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
 */
import { Tree } from "../utils/data";
import { DuplicateObject } from "../utils/tools";
import r from "../utils/request";
import store from "../store/index";
import rest from "../utils/rest";
// ALTER
export const update_item_ = (url, params, callback) => {
  r()
    .put(url, params)
    .then(res => {
      if (res.status == 200) {
        ElMessage({
          showClose: true,
          message: "修改成功",
          center: true,
        });
        if (callback != undefined) {
          callback(res);
        }
      }
    });
};
export const delete_item_ = (url, callback) => {
  r()
    .delete(url)
    .then(res => {
      if (res?.status == 200) {
        ElMessage({
          showClose: true,
          message: "删除成功",
          center: true,
        });
        if (callback != undefined) {
          callback(res);
        }
      }
    });
};
export const mult_delete_ = (url, id, callback) => {
  //多项删除
  r()
    .delete(url, { params: { id: id } })
    .then(res => {
      if (callback != undefined) callback(res);
    });
};
export const mult_update_ = (url, id, querys, callback) => {
  //多项修改
  r()
    .delete(url, { params: { id: id }, ...querys })
    .then(res => {
      if (callback != undefined) callback(res);
    });
};

//GET LIST

var request_time = 0;
export const get_data_ = (url, params, attrs, callback) => {
  //获取菜单数据
  let now = new Date().getTime();
  if (now - request_time > 500) {
    request_time = now;
    attrs.loading = true;
    r()
      .get(url, { params: params })
      .then(res => {
        attrs.loading = false;
        attrs.data = res.data.data;
        attrs.total = res.data.total;
        if (callback != undefined) callback(attrs);
      });
  }
};

export const get_detail_ = async (url, row, rows, attrs) => {
  console.log(row, rows);
  //获取详细信息
  let keys = [];
  rows.forEach(element => {
    keys.push(element.id);
  });
  if (!row.opened && url) {
    row.opened = true;
  }
  attrs.expandedRowKeys = keys; //修改数据后会自动关闭expand, 通过在 expand-row-keys添加row-key来重新打开
};

export const get_list_ = async (url, params, attrs, key, callback) => {
  //获取列表
  r()
    .get(url, { params: params })
    .then(res => {
      attrs[key] = res.data.data;
      attrs[key + "_total"] = res.data.total;
      if (callback != undefined) callback(attrs);
    });
};

export const get_all_menu_tree_ = attrs => {
  if (store().all_menu) {
    attrs.menus = store().all_menu;
  } else {
    r()
      .get("/data/GetAllMenu/")
      .then(res => {
        attrs.menus = Tree(res.data);
        store().all_menu = attrs.menus;
      });
  }
};
export const get_all_dept_tree_ = attrs => {
  if (store().all_dept) {
    attrs.all_dept = store().all_dept;
  } else {
    rest.list("dept", null, null, null, res => {
      console.log(res);
      attrs.all_dept = Tree(res.data.data);
      store().all_dept = attrs.all_dept;
    });
  }
};
export const get_all_interface_ = attrs => {
  if (store().all_interface) {
    attrs.all_interface = store().all_interface;
  } else {
    r()
      .get("/")
      .then(res => {
        attrs.all_interface = res.data.paths;
        store().all_interface = attrs.all_interface;
      });
  }
};
export const get_all_role_ = async (attrs, params) => {
  if (store().all_role) {
    attrs.all_role = store().all_role;
  } else {
    rest.list("role", params, null, null, res => {
      console.log(res);
      attrs.all_role = res.data.data;
      store().all_role = res.data.data;
    });
  }
};
export const get_all_role_dict_ = async params => {
  console.log("get_all_role_dict_");
  if (store().all_role_dict) {
    return store().all_role_dict;
  } else {
    let res = await r().get("/data/GetAllRoleDict/", { params: params });
    store().all_role_dict = res.data;
    return store().all_role_dict;
  }
};
export const get_all_users_ = async (attrs, params) => {
  //获取所有用户
  await r()
    .get("/data/users/", { params: params })
    .then(res => {
      console.log("users", res);
      attrs.users = res.data;
    });
};
export const get_all_area_tree_ = () => {
  rest.list("area", { page: 1, limit: 99999 }, null, null, res => {
    attrs.areas_tree = Tree(res.data.data, "code", "pcode");
    // resolve(nodes)
  });
};
export const get_all_area_ = () => {
  rest.list("area", { page: 1, limit: 99999 }, null, null, res => {
    attrs.areas = res.data.data;
    // resolve(nodes)
  });
};
//GET ITEM

//FORM
export const add_ = async (url, form, callback) => {
  //添加对象
  console.log(form);
  r()
    .post(url, form)
    .then(res => {
      if (res.status == 201) {
        ElMessage({
          showClose: true,
          message: "添加成功",
          center: true,
        });
        if (callback != undefined) {
          callback(res);
        }
      }
    });
};
export const submit_ = async (base_url, form, type, callback) => {
  //提交; 修改或新增
  let url = type == "add" ? `/${base_url}/` : `/${base_url}/${form.id}/`;
  if (type == "add") {
    add_(url, form, callback);
  } else if (type == "update") {
    update_item_(url, form, callback);
  }
};

//FILE
export const remove_file_ = async file => {
  //删除文件
  console.log("remove", file);
  if (file.response) return r().post(`/data/remove/`, { file: file.response.url });
  else return r().post(`/data/remove/`, { file: file.url });
};
export const remove_jfile_ = async file => {
  //删除json类型文件, 针对elementplus  新上传的文件和原有值的数据格式不同
  console.log("remove jfile", file);
  if (file.response) return r().delete(`/file/${file.response.id}/`);
  else return r().delete(`/file/${file.id}/`);
};
export const upload_file_ = (event, file, files) => {
  //手动上传文件
  console.log("upload", file);
};

//TINY TOOL
export const select_ = (data, v) => {
  //获取多选结果
  let r = [];
  data.forEach(element => {
    r().push(element.id);
  });
  v.selects = r;
};
export const sort_ = (d, form) => {
  //排序
  //d -> {column: Proxy, prop: 'create_time', order: 'ascending'}
  //form -> 需要提交的表单(reactive)
  console.log(d);
  if (d.order == "ascending") {
    form.sort = d.prop;
  } else if (d.order == "descending") {
    form.sort = "-" + d.prop;
  } else {
    form.sort = undefined;
  }
};

export const add_menu_tab_ = item => {
  if (item.name != "enterprise") {
    store().menu_tab.push({ label: item.label, name: item.name });
    store().menu_tab = DuplicateObject(store().menu_tab, "name");
  }
  store().current_menu = item.name;
};

export const export_data_ = (base_url, params) => {
  r()
    .post(`/${base_url}/export/`, { columns: JSON.parse(localStorage.getItem(`columns_${base_url}`)), ...params })
    .then(res => {
      console.log(res.data.url);
      window.location.href = res.data.url;
    });
};
