<template>
    <template v-for="(item, index) in data" :key="index">
        <el-sub-menu v-if="item?.children?.length" :index="item.path" popper-class="menu-poper">
            <template #title>
                <!-- 有子集的菜单icon要放到title里 -->
                <img class="menu-icon" v-if="item.icon.indexOf('.') != -1" :src="item.icon">
                <el-icon v-else :size="20" style="color: yellow;">
                    <component :is='item.icon'></component>
                </el-icon>
                <span class="menu-text">{{ item.label }}</span>
            </template>
            <MenuTree :data="item.children" :parent_path="parent_path + '/' + item.path"></MenuTree>
        </el-sub-menu>
        <el-menu-item v-else :route="parent_path + '/' + item.path" :index="parent_path + '/' + item.path"
            @click="add_menu_tab_(item)">
            <!-- 没有子集的菜单icon要放到title外 -->

            <img class="menu-icon" v-if="item.icon.indexOf('.') != -1" :src="item.icon">
            <el-icon v-else :size="20" style="color: yellow;">
                <component :is='item.icon'></component>
            </el-icon>
            <template #title>
                <!-- <router-link class="menu-text" :to="{ name: item.name }">{{ item.label }}</router-link> -->
                <span class="menu-text">{{ item.label }}</span>

            </template>
        </el-menu-item>
    </template>
</template>
<script setup >
// TODO:elementui  菜单树, 需要放到 <el-menu> 中使用
import store from '../store';
import { add_menu_tab_ } from '../hooks/table_common'

const props = defineProps(['data', 'parent_path'])
// const add_menu_tab_ = (item) => {
//     if (item.name != 'enterprise') {
//         store().menu_tab.push({ label: item.label, name: item.name })
//         store().menu_tab = DuplicateObject(store().menu_tab, 'name')
//     }
//     store().current_menu = item.name
// }
</script>
<style lang="scss">
.menu-poper {
    background-color: #2da4dc;
}

.menu-icon {
    width: 18px;
    height: 18px;
    margin-right: 5px;
}

.menu-text {
    user-select: none;
    font-size: 16px;
    text-decoration: none !important;
    // color: black;
}

// .router-link-active {
//     color: white !important;
// }
</style>
