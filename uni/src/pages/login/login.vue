<template>
  <view class="login">
    <view class="header">
      <img src="@/static/logo.png" style="width: 200rpx;height: 200rpx;">
      <view>
        欢迎登陆软件
      </view>
    </view>
    <view class="form">
      <view class="line">
        <view class="title">账号</view>
        <view class="input"><input placeholder="请输入账号" class="input-editor" type="text" v-model="form.username"></view>
      </view>
      <view class="line">
        <view class="title">密码</view>
        <view class="input"><input placeholder="请输入密码" class="input-editor" type="password" v-model="form.password">
        </view>
      </view>
      <view class="line">
        <view class="title">验证码</view>
        <view class="input">
          <input placeholder="请输入验证码" class="input-editor" type="text" v-model="form.captcha">
          <img class="captcha" :src="'data:image/gif;base64,' + attrs.captcha" alt="" @click="get_captcha()">
        </view>
      </view>
      <view class="line">
        <view style="font-size: 30rpx;">
          <u-checkbox v-model="attrs.checked" shape="circle" active-color="blue" size="40"></u-checkbox> 我已阅读并同意<text
            @click="agreement()" style="color: blue;">《用户协议》</text>
        </view>
      </view>
      <view class="login-btn">
        <button type="primary" @click="submit"
          style="border-radius: 60rpx;height: 100rpx;font-size: 30rpx;display: flex;align-items: center;justify-content: center;background-color: blue;margin-bottom: 20rpx;">一键登录</button>
        <view style="display: flex;align-items: center;justify-content: space-between;">
          <button type="primary" @click="navigate('/pages/login/signin')"
            style="width: 40%;padding: 0; border-radius: 60rpx;height: 70rpx;font-size: 30rpx;display: flex;align-items: center;justify-content: center;background-color: rgb(142, 142, 145);">注册</button>
          <button type="primary"
            style="width: 40%; padding: 0;border-radius: 60rpx;height: 70rpx;font-size: 30rpx;display: flex;align-items: center;justify-content: center;background-color: rgb(134, 134, 138);">忘记密码</button>
        </view>
      </view>
    </view>

  </view>
</template>
<script setup>

//const props = defineProps(['modelValue']); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['update:modelValue']); // emits 触发父组件函数
import { reactive } from 'vue';
import { navigate } from '../../utils/data'
import store from '../../store';
import r from "../../utils/request";
import { onLoad, onReady, onShow, onHide, onUnload, onPullDownRefresh, onReachBottom, onPageScroll, onShareAppMessage } from '@dcloudio/uni-app';
const attrs = reactive({
  checked: false,
});
const form = reactive({
  username: 'admin',
  password: 'admin',
  captcha: null,
})
onShow(() => {
  if (store().is_login) {
    uni.switchTab({
      url: '/pages/index/index',
      success: () => {
      }
    })
  }
})
// uni.login({
//   "provider": "weixin",
//   "onlyAuthorize": true, // 微信登录仅请求授权认证
//   success: function (event) {
//     const { code } = event
//     //客户端成功获取授权临时票据（code）,向业务服务器发起登录请求。
//     uni.request({
//       url: 'https://www.example.com/loginByWeixin', //仅为示例，并非真实接口地址。
//       data: {
//         code: event.code
//       },
//       success: (res) => {
//         //获得token完成登录
//         uni.setStorageSync('token', res.token)
//       }
//     });
//   },
//   fail: function (err) {
//     // 登录授权失败  
//     // err.code是错误码
//   }
// })
const submit = () => {
  if (form.captcha == null) {
    // https://uniapp.dcloud.net.cn/api/ui/prompt.html
    uni.showToast({ //TODO:uni-屏幕提示
      title: "请输入验证码",
      icon: 'none'
    });
    return
  }

  r.form('/token/', form).then((res) => {
    console.log(res);
    if (res.statusCode === 200) {
      uni.setStorage({
        key: 'access',
        data: res.data.access,
        success: function () {
          console.log('access set success');
          store().is_login = true
          store().get_userinfo().then(() => {
            uni.switchTab({
              url: '/pages/index/index',
              success: () => {
              }
            })
          })
        }
      });
    }


  })
}

const get_captcha = () => {
  r.get('/data/captcha/').then((res) => {
    console.log(res);
    attrs.captcha = res.data.data
  })
}

get_captcha()
</script>

<style scoped lang='scss'>
.login {
  width: 100vw;
  height: 100vh;
  position: relative;
  z-index: 2;
  border-radius: 50%;
}


.bg {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}

.header {
  position: absolute;
  width: 100vw;
  height: 300rpx;
  left: 50%;
  top: 20%;
  transform: translate(-50%, -50%);
  font-size: 25px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;

  .text {
    color: rgb(0, 0, 0);
    font-size: 50rpx;
  }
}

.form {
  position: absolute;
  width: 80%;
  left: 50%;
  top: 60%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: Arial, Helvetica, sans-serif;

  .line {
    // height: 140rpx;
    width: 100%;
    display: flex;
    flex-direction: column;
    // align-items: center;
    justify-content: space-around;
    margin-bottom: 30rpx;

    .title {
      font-size: 50rpx;
      height: 55rpx;
      display: flex;
      flex-direction: row;
      align-items: center;
      display: none;
      // justify-content: center;
    }

    .input {
      height: 80rpx;
      display: flex;
      flex-direction: row;
      align-items: center;
      border-bottom: 1px solid #0000005d;

      .input-editor {
        flex: 1;
        font-size: 38rpx;
        height: 100%;
        // border: 1px solid #000;
      }

      .captcha {
        flex: 1;
        height: 100%;
      }
    }
  }

  .login-btn {
    width: 100%;


  }
}
</style>
