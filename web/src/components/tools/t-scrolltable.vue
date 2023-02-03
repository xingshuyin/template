<!--
 * @Filename     : scroll_table.vue
 * @Description  : wjt-前端-平滑滚动列表
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-11-08 10:02:56
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-17 14:33:14
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
//import { ref } from 'vue';
//import {useRoute, useRouter} from 'vue-router';
//const route = useRoute() //当前路由

import { reactive } from 'vue';
import scroll from "./scroll.vue"
const router = useRouter() //全局路由对象
const props = defineProps(['data', "columus", "media_type"]); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['onclick']); // emits 触发父组件函数
//const map = ref(null); //获取ref值为map的元素
//defineExpose({ map,}); //暴露组件的内容, 父组件通过组件对象(如ref)的value获取暴露的对象
const columnss = reactive([
    {
        key: "name",
        label: "名称",
        flex: "1",

    },
    {
        key: "date",
        label: "时间",
        flex: "1",

    },
    {
        key: "address",
        label: "地址",
        flex: "2",

    },
])
const tableData = [
    {
        date: '2016-05-03',
        name: 'Tom',
        address: '---------------------------',
    },
    {
        date: '2016-05-02',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-04',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-01',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-08',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-06',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-07',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-03',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-02',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-04',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-01',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-08',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-06',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-07',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
]
console.log(props)
</script>
<template>
    <div class="scroll-table">
        <div class="scroll-table-head">
            <div class="scroll-table-cell" v-for="i in columus" :style="{ flex: i?.flex ?? '1' }">{{ i.label }}
            </div>
        </div>
        <div class="scroll-table-body">
            <scroll style="height: 100%;">
                <div>
                    <div :class="index % 2 == 0 ? 'scroll-table-body-line even' : 'scroll-table-body-line odd'"
                        v-for="i, index in data">
                        <div class="scroll-table-body-line-detail"
                            @click="router.push({ name: 'single', query: { id: i.id, media_type: media_type } })">
                            <el-button icon="Search" circle class="w10px h10px" />
                        </div>
                        <div class="scroll-table-cell" v-for="j in columus" :style="{ flex: j?.flex ?? '1' }">
                            <span v-if="j?.key == 'index'">
                                {{ index + 1 }}
                            </span>
                            <div class="roll" v-if="j?.roll">
                                {{ i[j.key] }}
                            </div>
                            <span v-else>
                                {{ i[j.key] }}
                            </span>
                        </div>
                    </div>
                </div>
            </scroll>
        </div>
    </div>
</template>
<style scoped lang='scss'>
.scroll-table {
    --height-head: 30px;
    --cell-padding: 0 10px;

    &-head {
        width: 100%;
        height: var(--height-head);
        display: flex;
        background-color: rgba(255, 255, 255, 0.158);
        color: rgb(255, 255, 255);
        border-radius: 5px;

        .scroll-table-cell {
            overflow: hidden;
            text-align: center;
            white-space: nowrap;
            padding: var(--cell-padding);
            font-size: 16px;
            height: var(--height-head);
            line-height: var(--height-head);
        }
    }

    &-body {
        width: 100%;
        height: calc(100% - var(--height-head));
        overflow: hidden;
        display: flex;
        flex-direction: column;
        background-color: rgba(106, 188, 255, 0.068);
        border-radius: 5px;

        &-line {
            display: flex;
            width: 100%;
            height: 25px;
            // margin-bottom: 5px; //有margin就会跳

            .scroll-table-cell {
                box-sizing: border-box;
                line-height: 25px;
                overflow: hidden;
                padding: var(--cell-padding);
                // border: 1px solid white;
                text-align: center;

                .roll {
                    width: max-content;
                }

                .roll:hover {
                    text-align: center;
                    animation: 6s linear wordroll infinite;
                }
            }

            &-detail {
                float: left;
                position: absolute;
                display: none;
            }
        }

        .even {
            background-color: rgba(255, 255, 255, 0.055);
        }

        .odd {
            background-color: rgba(0, 0, 0, 0);
        }

        &-line:hover>.scroll-table-body-line-detail {
            display: block;
        }
    }
}

@keyframes wordroll {
    from {
        /* transform: translateX(70%); */
        /* transform: translateX(0px); */
        /* webkittransform: translateX(0px); */
    }

    to {
        transform: translateX(-70%);
        /* webkittransform: translateX(120%); */
    }
}
</style>
