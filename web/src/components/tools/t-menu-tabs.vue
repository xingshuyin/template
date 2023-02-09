<script setup>
//const props = defineProps(['modelValue']); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['update:modelValue']); // emits 触发父组件函数
import store from '../../store'
import { onBeforeMount } from 'vue';
const router = useRouter()
const route = useRoute()
const default_page = 'enterprise'   //默认菜单路由name
// store().menu_tab => [{name: 'enterprise', label: '企业管理'}]
// store().current_menu => 'enterprise'
const menu_tab_change = (tab) => {
    router.push({ name: tab.props.name })
}
const menu_tab_remove = (tab) => {
    if (tab != store().current_menu) {
        store().menu_tab = store().menu_tab.filter((i) => {
            return i.name != tab
        })
    } else {
        store().menu_tab = store().menu_tab.filter((i, index) => {
            if (i.name != tab) return true;
            else {
                if (index != 0) {
                    store().current_menu = store().menu_tab[index - 1].name
                    router.push({ name: store().menu_tab[index - 1].name })
                    return false
                } else {
                    store().current_menu = default_page
                    router.push({ name: default_page })
                }

            }
        })
    }
}
const menu_tab_close_all = () => {
    store().menu_tab = []
    store().current_menu = default_page
    router.push({ name: default_page })
}
const menu_tab_close_other = () => {
    store().menu_tab = store().menu_tab.filter((i) => {
        return i.name == store().current_menu
    })
}
const menu_tab_close_left = () => {
    let finded = false;
    store().menu_tab = store().menu_tab.filter((i) => {
        if (i.name == store().current_menu) {
            finded = true
        }
        if (!finded) return false;
        else return true
    })
}
const menu_tab_close_right = () => {
    let finded = false;
    store().menu_tab = store().menu_tab.filter((i) => {
        if (i.name == store().current_menu) {
            finded = true
            return true
        } else {
            if (!finded) return true;
            else return false
        }
    })
}
watch(() => { return store().menu_tab }, () => {
    localStorage.setItem('menu_tab', JSON.stringify(store().menu_tab))
})
onBeforeMount(() => {
    if (localStorage.getItem('menu_tab')) {
        store().menu_tab = JSON.parse(localStorage.getItem('menu_tab'))
    }
    store().current_menu = route.name
})
</script>
<template>
    <div class="menu-tab">
        <!-- TODO:菜单标签 -->
        <el-tabs v-model="store().current_menu" type="card" @tab-remove="menu_tab_remove" @tab-click="menu_tab_change">
            <el-tab-pane key="enterprise" label="企业管理" name="enterprise" :closable="false">
                <!-- {{ item.content }} -->
            </el-tab-pane>
            <el-tab-pane v-for="item in store().menu_tab" :key="item.name" :label="item.label" :name="item.name"
                closable>
                <!-- {{ item.content }} -->
            </el-tab-pane>
            <!-- <el-button type="danger">Danger</el-button> -->
        </el-tabs>
        <div class="menu-tab-tool">
            <el-dropdown split-button type="primary" @click="menu_tab_close_all">
                <mdi:close-circle></mdi:close-circle>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item @click="menu_tab_close_all">关闭全部</el-dropdown-item>
                        <el-dropdown-item @click="menu_tab_close_other">关闭其他</el-dropdown-item>
                        <el-dropdown-item @click="menu_tab_close_left">关闭左侧</el-dropdown-item>
                        <el-dropdown-item @click="menu_tab_close_right">关闭右侧</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</template>
<style scoped lang='scss'>
.menu-tab {
    position: relative;
    width: 100%;

    :deep(.el-tabs) {
        .el-tabs__header {
            margin-bottom: 0;
        }

        .el-tabs__item {
            //tab样式
            // border-radius: 2px;
            // margin: 1px;
            // background-color: rgba(247, 242, 236, 0.459);
            // border: 1px solid rgb(216, 207, 207);
            box-sizing: border-box;
        }

        .is-active {
            // 激活tab颜色
            background-color: rgba(255, 255, 255, 0.459);
        }
    }


    .menu-tab-tool {
        position: absolute;
        right: 0;
        top: 50%;

        transform: translateY(-50%);
    }
}
</style>
