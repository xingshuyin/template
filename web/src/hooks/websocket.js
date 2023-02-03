import store from "../store";
export default async () => {
  let userinfo = await store().get_userinfo();
  console.log(userinfo);
  const websocket = new WebSocket("ws://" + "127.0.0.1:8002/" + "/ws/group/" + 1 + "/" + 12 + "/");
  websocket.onmessage = function (e) {
    //接收消息
    let data = JSON.parse(e.data); // {'type':'message', 'key':'value'}, 根据不同的type做不同的处理
    console.log("接到消息", data);
  };
  websocket.onclose = function (e) {
    //socket关闭后的提示
    console.error("Chat socket closed unexpectedly");
  };
  return websocket;
};
