<script setup>

//const props = defineProps(['modelValue']); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['update:modelValue']); // emits 触发父组件函数
import { onLoad } from '@dcloudio/uni-app'; //页面生命周期
import { reactive, ref, onMounted } from 'vue';
import store from '../../store';
import r from "../../utils/request";
const uForm = ref()
const form = reactive({
  user_name: 'superadmin',
  password: 'wjt_admin_123',
  password_: 'wjt_admin_123',
})
const submit = () => {
  if (form.password == form.password_) {
    r.post('/data/signin/', {
      user_name: form.user_name,
      password: form.password,
    }).then((res) => {
      if (res.statusCode == 200) {
        uni.showToast({
          title: '注册成功',
        });
        setTimeout(() => {
          to('/pages/login/index')
        }, 1500)
      }
      else {
        uni.showToast({
          title: res.data.detail,
          icon: 'error'
        });
      }
    })
  } else {
    uni.showToast({
      title: "两次密码不同",
      icon: 'error'
    });
  }


}

</script>
<template>
  <view class="login">
    <u-navbar back-text="返回" :title="'注册'"></u-navbar>
    <view class="header">
      <!-- <image class="icon" style="width:200rpx; height: 200rpx;" mode="scaleToFill"
                                                                                                                            src="../../static/img/ic_launcher_round.png"></image> -->
      <!-- <text class="text">注册账号</text> -->
    </view>
    <view class="form">
      <u-form :model="form" ref="uForm" class="input">
        <u-form-item label="账号" label-width="160" prop="user_name"><u-input class="input-item" height="100"
            :custom-style="{ 'border-radius': '50%' }" placeholder-style="color: #222;" border v-model="form.user_name"
            placeholder="请输入账号" /></u-form-item>
        <u-form-item label="密码" label-width="160" prop="password"><u-input class="input-item" height="100"
            :custom-style="{ 'border-radius': '50%' }" placeholder-style="color: #222;" border v-model="form.password"
            type="password" placeholder="请输入密码" /></u-form-item>
        <u-form-item label="确认密码" label-width="160" prop="password_"><u-input class="input-item" height="100"
            :custom-style="{ 'border-radius': '50%' }" placeholder-style="color: #222;" border v-model="form.password_"
            type="password" placeholder="请再次输入密码" /></u-form-item>
      </u-form>
    </view>
    <u-button class="login-btn" type="primary" shape="circle" @click="submit">注册</u-button>
  </view>
  <!-- <image class="bg" style="width: 100vw; height: 100vh;" mode="aspectFill" src="~@/static/img/Login_bg.png"></image> -->
</template>
<style scoped lang='scss'>
.login {
  // background-image: url('~@/static/img/Login_bg.png');
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
  top: 40%;
  transform: translate(-50%, -50%);

  .input {
    margin-bottom: 50rpx;
  }

  :deep(.u-form-item) {
    border: 0;

    .u-form-item__body {
      border: 0;
      background-color: rgb(252, 252, 252);

      // border-radius: 100rpx;

      .u-input {
        border: 0;
        color: rgb(238, 235, 235);
      }
    }
  }
}

.login-btn {
  position: absolute;
  width: 70%;
  left: 50%;
  bottom: 20%;
  transform: translate(-50%, -50%);
}
</style>
