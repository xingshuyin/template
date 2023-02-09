<!--
 * @Filename     : index.vue
 * @Description  : wjt-前端-登录页
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-09-30 18:19:48
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-12-11 18:06:58
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
import { reactive, toRaw } from 'vue';
import axios from "axios";
// import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router';
import store from "../../store/index";
import r from '../../utils/request'
// import { removeinter, addinter } from '../../utils/request'
// import { userinfo } from '../../utils/data';
//const route = useRoute() //当前路由
//const props = defineProps({ data: Object, title: String}); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['onclick']); // emits 触发父组件函数
//const map = ref(null); //获取ref值为map的元素
//defineExpose({ map,}); //暴露组件的内容, 父组件通过组件对象(如ref)的value获取暴露的对象
const form = reactive({
  username: null,
  password: null,
  // openid: '1234567890',
})
const rules = reactive({
  username: [{ required: true, message: '请填写账号', trigger: 'blur' }],
  password: [{ required: true, message: '请填写密码', trigger: 'blur' }]
})
const router = useRouter();

const login = () => { //TODO:登录
  r().post('/token/', { ...toRaw(form) }).then((response) => {
    console.log('loginresponse', response)
    if (response.status == 200) {
      console.log('set token')
      localStorage.setItem('token', response.data.access)
      localStorage.setItem('refresh', response.data.refresh)
      console.log('set token sucess')
      store().get_userinfo(true).then(res => {
        if (res.name) localStorage.setItem('username', res.name);
        else localStorage.setItem('username', res.username)
        console.log("login---userinfo", res)
        if (res.is_super || res.type == 2) {
          router.push('/admin/enterprise')
        } else {
          router.push('/')
          // ElMessage({
          //   showClose: true,
          //   message: '未绑定企业信息',
          //   center: true,
          // })
        }
      })


    } else {
      ElMessage({
        showClose: true,
        message: '用户名或密码错误',
        center: true,
      })
    }
  }).catch((err) => {
    if (err?.response?.status == 401) {
      localStorage.setItem('token', '')
      localStorage.setItem('refresh', '')
      ElMessage({
        showClose: true,
        message: '用户名或密码错误',
        center: true,
      })
    } else {
      console.log(err)
    }
  })
}
/**
 * @description: 刷新token令牌
 * @return {*}
 */
const refresh = () => {
  r().post('/refresh/', { refresh: localStorage.getItem('refresh') }).then((response) => {
    console.log('loginresponse', response)
    if (response.status == 200) {
      localStorage.setItem('token', response.data.access)
    }
    else {
      localStorage.removeItem('uid')
      localStorage.removeItem('token')
      localStorage.removeItem('refresh')
    }
  }).catch((err) => {
  })
}
const env = import.meta.env
</script>
<template>
  <div class="login">
    <div class="login_form ">
      <!-- <div class="left">
        <img src="../../assets/img/logo.webp" alt="" style="width: 300px;height: 300px;">
        <div class="footer">
          <div class="chinese">
            {{ env.VITE_FOOTER_CHINESE }}
          </div>
          <div class="english">
            <div>
              {{ env.VITE_FOOTER_ENGLISH1 }}
            </div>
            <div>
              {{ env.VITE_FOOTER_ENGLISH2 }}
            </div>

          </div>
        </div>
      </div> -->
      <div class="right">
        <div class="title">{{ env.VITE_TITLE }}</div>
        <div class="form">
          <el-form :model="form" status-icon :rules="rules" label-width="40px">
            <el-form-item label="账号" prop="checkPass">
              <el-input v-model="form.username" size="large" autocomplete="off" />
            </el-form-item>
            <el-form-item label="密码" prop="pass">
              <el-input v-model="form.password" type="password" size="large" autocomplete="off" />
            </el-form-item>
          </el-form>
        </div>
        <div class="btn">
          <el-button class="login-btn" type="primary" @click="login">登录</el-button>
        </div>
      </div>


    </div>

  </div>

</template>
<style scoped lang='scss'>
.login {
  background: url('../../assets/img/login_bg.jpg') center no-repeat;
  background-size: cover;
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;


  .login_form {
    border-radius: 10px;
    display: flex;
    width: 840px;
    height: 500px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    .left {
      border-bottom-left-radius: 5px;
      border-top-left-radius: 5px;
      flex: 1;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-around;
      align-items: center;
      background-color: rgba(255, 255, 255, 0.68);

      .footer {
        color: rgb(0, 0, 0);
        font-size: 10px;
        text-align: center;
        width: 100%;
      }
    }

    .right {
      border-bottom-right-radius: 5px;
      border-top-right-radius: 5px;
      flex: 1;
      position: relative;
      background-color: #ffffff56;
      display: flex;
      flex-direction: column;
      justify-content: space-around;
      align-items: center;

      .title {
        flex: 1;
        font-size: 30px;

        width: 100%;
        text-align: center;
        color: rgb(42 100 80);
        display: flex;
        justify-content: center;
        align-items: flex-end
      }

      .form {
        flex: 1.5;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;

        :deep(.el-form-item) {
          margin: 15px;

          .el-form-item__label {
            font-size: 14px;
          }

          .el-form-item__content {
            border-radius: 10px;
            overflow: hidden;
          }
        }



        :deep(.el-input) {

          --el-input-bg-color: #ffffff;

          .el-input__inner {
            color: #000000;
            box-shadow: 0 0 0px 1000px #ffffff00 inset;
            -webkit-box-shadow: 0 0 0px 1000px #ffffff inset; //TODO:自动填充背景色
            -webkit-text-fill-color: #070000; //TODO:自动填充文字颜色   
          }
        }


      }

      .btn {
        flex: 1;
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: left;
        width: 100%;


        .login-btn {

          width: 200px;
          background: rgb(77, 175, 141);
          border: 0;
          color: #ffffff;
        }

        .login-btn:hover {
          background: #2fe7b0d3;
        }
      }


    }


  }


}
</style>
