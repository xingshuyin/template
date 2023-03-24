<script setup>
import store from "../store/index";
import { add_menu_tab_ } from '../hooks/table_common'
import { pinyin } from 'pinyin-pro';
import { deep_search } from "../utils/tools";
const router = useRouter()
const logout = () => {
  // localStorage.clear()
  localStorage.removeItem('uid')
  localStorage.removeItem('token')
  localStorage.removeItem('refresh')
  router.push('/login')
}
const username = ref(localStorage.getItem('username'))
const centerDialogVisible = ref(false)
const search = ref(undefined)
const search_change = (value) => {
  if (value != undefined) {

    let item = deep_search(store().menu, 'name', value)
    add_menu_tab_({ label: item.label, name: value })
    router.push({ name: value })
    search.value = undefined
  }
}
const filter_method = (node, key) => {
  console.log(node, key)
  let p = pinyin(node.label, { toneType: 'none', type: 'array' }).join('');
  return p.includes(key) || node.label.includes(key)
}
const env = import.meta.env
</script>
<template>
  <div class="head">

    <!-- 退出登陆弹窗 -->
    <el-dialog v-model="centerDialogVisible" title="注销账户" width="300px" align-center center>
      <div style="width: 100%;text-align: center">确定要注销当前用户吗</div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="centerDialogVisible = false; logout()">确定</el-button>
          <el-button type="primary" @click="centerDialogVisible = false">取消</el-button>
        </span>
      </template>
    </el-dialog>
    <!-- 标题 -->
    <div class="title" :style="{ width: store().menu_width }">
      <div class="title-img">
        <img src="../assets/img/logo.png" style="height: 80%;" />
      </div>
      <div class="title-text" v-if="!store().toggle_side">
        {{ env.VITE_TITLE }}
      </div>
    </div>
    <Expand style="width: 2em; height: 2em; margin-right: 8px;color: white;" v-if="store().toggle_side"
      @click="store().toggle_side = !store().toggle_side; store().toggle_side ? store().menu_width = '50px' : store().menu_width = '200px'" />
    <Fold style="width: 2em; height: 2em; margin-right: 8px;color: white;" v-else
      @click="store().toggle_side = !store().toggle_side; store().toggle_side ? store().menu_width = '50px' : store().menu_width = '200px'" />

    <!-- 按钮 -->
    <div class="buttons ">
      <el-button icon="Monitor" circle @click="router.push({ name: 'front' })"></el-button>
      <t-time style="margin-left: 15px;"></t-time>
      <div class="buttons-item">
        <el-cascader v-model="search" :options="store().menu" @change="search_change" :filter-method="filter_method"
          placeholder="搜索" :props="{ emitPath: false, value: 'name', label: 'label', }" filterable clearable
          size="small" />
      </div>
      <el-tooltip content="全屏" placement="bottom" effect="light">
        <t-fullscreen class="buttons-item"></t-fullscreen>
      </el-tooltip>
      <div class="user buttons-item">
        <span style="font-size: 16px; padding-right: 5px;">
          <span style="color: yellow ;">{{ username }}</span>
        </span>
        <el-avatar class="avatar" size="small" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
          @click="centerDialogVisible = true" />
      </div>

    </div>
  </div>
</template>
<style scoped lang='scss'>
.head {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
  background-image: linear-gradient(-225deg, #6c6c6c 0%, #216855 50%, #565604 100%); //绿色渐变
  // background-image: linear-gradient(-225deg, #82a7e3 0%, #c9e1f4 50%, #00a0f9 100%);
  // background: #6fd6e5;
  // background: rgb(31 104 84);
  display: flex;
  align-items: center;

  .logo {
    height: 100%;
    min-width: 50px;
    white-space: nowarp;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffedad;
    font-size: 18px;
    text-align: center;
    background: linear-gradient(to right, #b3ffcb 0%, rgb(31, 104, 84) 100%);
  }

  .title {
    height: 100%;
    font-size: 1.3rem;
    display: flex;
    justify-content: center;
    align-items: center;
    color: rgb(255, 255, 255);
    font-family: Kumbh Sans, sans-serif;
    transition-duration: 600ms;

    .title-img {
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .title-text {
      margin-left: 10px;
      transition-duration: 200ms;
      white-space: nowrap;
      overflow: hidden;
    }
  }

  .buttons {
    height: 100%;
    position: absolute;
    right: 0;
    top: 0;
    color: white;
    // gap: 4px;
    display: flex;
    justify-content: center;
    align-items: center;


    .buttons-item {
      margin: 0 3px !important;
    }



    .user {

      height: 100%;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;

      .avatar {}
    }

    .username {
      padding-left: 9px;
      padding-right: 3px;
      font-size: 25px;
      color: white;
      height: 25px;
      background-color: #0a274a;
      border-radius: 10px;
    }
  }
}
</style>
