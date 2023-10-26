export default async (group, user, onmessage, onclose, onopen) => {
  var loc = window.location,
    new_uri;
  if (loc.protocol === "https:") {
    new_uri = "wss:";
  } else {
    new_uri = "ws:";
  }
  console.log(loc);
  const websocket = new WebSocket(
    "ws://" + "127.0.0.1:8000" + "/ws/websocket/" + group + "/" + user + "/"
  );
  websocket.onmessage = function (e) {
    //接收消息
    // let data = JSON.parse(e.data); // {'type':'message', 'key':'value'}, 根据不同的type做不同的处理
    if (onmessage) onmessage(e.data);
  };
  websocket.onclose = function (e) {
    //socket关闭后的提示
    if (onclose) onclose(e);
  };

  websocket.onopen = function (event) {
    console.log(event);
    if (onopen) onopen(event);
  };

  return websocket;
};
