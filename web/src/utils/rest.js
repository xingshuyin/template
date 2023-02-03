import r from "./request";
export default {
  list: (url, params, attrs, key, callback) => {
    if (!params) {
      params = { page: 1, limit: 9999999 };
    }
    r()
      .get(`/${url}/`, { params: params })
      .then(res => {
        if (attrs) {
          attrs[key ? key : "list"] = res?.data?.data;
        }

        if (callback) {
          callback(res);
        }
      });
  },
  item: (url, id, attrs, key, callback) => {
    r()
      .get(`/${url}/${id}/`)
      .then(res => {
        if (attrs) {
          attrs[key ? key : "item"] = res?.data;
        }

        if (callback) {
          callback(res);
        }
      });
  },
  post: (url, data, callback) => {
    r()
      .post(`/${url}/`, { ...data })
      .then(res => {
        if (callback) {
          callback(res);
        }
      });
  },
  put: (url, id, data, callback) => {
    r()
      .put(`/${url}/${id}/`, { ...data })
      .then(res => {
        res?.data?.data;
        if (callback) {
          callback(res);
        }
      });
  },
  delete: (url, id, callback) => {
    r()
      .delete(`/${url}/${id}/`)
      .then(res => {
        if (callback) {
          callback(res);
        }
      });
  },
};
