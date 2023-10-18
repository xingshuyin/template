export const TreeMenu = (data, parent) => {
  //TODO:生成树状结构
  let d = [];
  data.forEach((item) => {
    if (item.parent == parent) {
      d.push({
        name: item.name,
        path: item.path,
        icon: item.icon,
        component: item.component,
        children: TreeMenu(data, item.id, item.name),
      });
    }
  });
  return d;
};
export const Tree = (data, key, parent_key, parent) => {
  // console.log("parent", parent);
  key = key ? key : "id";
  parent_key = parent_key ? parent_key : "parent";
  parent = parent ? parent : null;
  let r = [];
  data.forEach((item) => {
    if (item[parent_key] == parent) {
      let t = item;
      t.children = Tree(data, key, parent_key, item[key]);
      r.push(t);
    }
  });
  return r;
};

export const methods = {
  0: "GET",
  1: "POST",
  2: "PUT",
  3: "DELETE",
};
export const style_type = {
  0: "success",
  1: "info",
  2: "danger",
  3: "warning",
};
export const permission_type = {
  0: "仅本人数据权限",
  1: "本部门及以下数据权限",
  2: "本部门数据权限",
  3: "全部数据权限",
  4: "自定数据权限",
};

export const area_level = {
  0: "省份",
  1: "城市",
  2: "区县",
  3: "乡镇",
};

export const spider_type = {
  1: "分页爬虫",
  2: "json分页爬虫",
};
