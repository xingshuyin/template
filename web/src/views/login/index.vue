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
  captcha: null,
  // openid: '1234567890',
})
const form_dom = ref()
const rules = reactive({
  username: [{ required: true, message: '请填写账号', trigger: 'blur' }],
  password: [{ required: true, message: '请填写密码', trigger: 'blur' }],
  captcha: [{ required: true, message: '请填写验证码', trigger: 'blur' }],
})
const router = useRouter();

const login = () => { //TODO:登录
  form_dom.value.validate((valid, fields) => {
    if (valid) {
      r().post('/token/', { ...toRaw(form) }).then((response) => {
        if (response?.status == 200) {
          console.log('set token')
          localStorage.setItem('token', response.data.access)
          localStorage.setItem('refresh', response.data.refresh)
          console.log('set token sucess')
          store().get_userinfo(true).then(res => {
            if (res.name) localStorage.setItem('username', res.name);
            else localStorage.setItem('username', res.username)
            console.log("login---userinfo", res)
            if (res.is_super || res.type == 2) {
              router.push('/admin/article') //TODO:管理员进入后台管理界面
            } else {
              router.push('/') //TODO:普通用户进入前台
            }
          })
        }
      })
    } else {
      ElMessage({
        showClose: true,
        message: '请填写账号或密码',
        center: true,
      });
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
    if (response?.status == 200) {
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

const signin = () => {
  r().post('/data/signin/', { ...toRaw(form) }).then((res) => {
    if (res.status == 200) {
      ElMessage({
        showClose: true,
        message: '注册成功',
        center: true,
      });
    }

  })
}
const get_captcha = () => {
  r().get('/data/captcha/').then((res) => {
    console.log(res);
    attrs.captha = res.data.data
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
          <el-form ref="form_dom" :model="form" status-icon :rules="rules" label-width="65px" label-position="left">
            <el-form-item label="账号" prop="username">
              <el-input @keyup.enter="login" v-model="form.username" size="large" autocomplete="off" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input @keyup.enter="login" v-model="form.password" type="password" size="large" autocomplete="off" />
            </el-form-item>
            <el-form-item label="验证码" prop="captcha">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-input @keyup.enter="login" v-model="form.captcha" size="large" autocomplete="off" />
                </el-col>
                <el-col :span="8" @click="get_captcha">
                  <el-image style=" height: 40px" :src="'data:image/gif;base64,' + attrs.captha" fit="contain" />
                  <!-- <img @click="get_captcha" :src="'data:image/gif;base64,' + attrs.captha" alt="" /> -->
                </el-col>
              </el-row>

            </el-form-item>
          </el-form>
        </div>
        <div class="btn">
          <el-button class="login-btn" type="primary" @click="login">登录</el-button>
          <el-button class="login-btn" type="primary" @click="signin">注册</el-button>
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
