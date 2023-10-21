import r from "./request";

export default {
  list: (base, params, attrs, key, callback, push) => {
    r.get(`/${base}/`, params, true).then((res) => {
      if (attrs != null) {
        if (push) {
          attrs[key ? key : "data"] = attrs[key ? key : "data"].concat(
            res.data.data
          );
        } else {
          attrs[key ? key : "data"] = [...res.data.data];
        }
      }
      if (callback) {
        callback(res);
      }
    });
  },
  post: (base, params, callback) => {
    r.post(`/${base}/`, params).then((res) => {
      if (callback) {
        callback(res);
      }
    });
  },
  get: (base, id, attrs, key, callback) => {
    r.get(`/${base}/${id}/`, {}).then((res) => {
      attrs[key ? key : "item"] = res.data;
      if (callback) {
        callback(res);
      }
    });
  },
  update: (base, id, params, callback) => {
    r.put(`/${base}/${id}/`, params).then((res) => {
      if (callback) {
        callback(res);
      }
    });
  },
  delete: (base, id, callback) => {
    r.delete(`/${base}/${id}/`).then((res) => {
      if (callback) {
        callback(res);
      }
    });
  },
};
