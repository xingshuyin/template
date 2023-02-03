<!--
 * @Filename     : CommentTree.vue
 * @Description  : wjt-前端-评论树
                    data => [{id: 1,user_avatar: 'a',createAt: '2121',...},...]
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-10-07 14:41:30
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-17 14:30:06
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
//import { ref } from 'vue';
//import {useRoute, useRouter} from 'vue-router';
//const route = useRoute() //当前路由
//const router = useRouter() //全局路由对象
const props = defineProps(['data']); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['onclick']); // emits 触发父组件函数
//const map = ref(null); //获取ref值为map的元素
//defineExpose({ map,}); //暴露组件的内容, 父组件通过组件对象(如ref)的value获取暴露的对象
</script>
<template>
    <div class="comment" v-for="i in data" :key="i.id">
        <div class="left">
            <el-avatar shape="circle" :src="i.user_avatar"></el-avatar>
        </div>
        <div class="right">
            <div class="title">
                <div class="user_name">{{ i.user_nick_name }}</div>
                <div class="create_time">{{ i.createAt }}</div>
            </div>
            <div class="content">
                {{ i.content }}
            </div>

            <div class="replys" v-if="i?.replys?.length">
                <div class="reply" v-for="reply in i.replys">
                    <div class="reply-left">
                        <el-avatar shape="circle" :src="r.user_avatar"></el-avatar>
                    </div>
                    <div class="reply-right">
                        <div class="title">
                            <div class="user_name">
                                {{
                                    reply.user_nick_name + (reply.reply_user_nick_name ? (' 回复@ ' +
                                        reply.reply_user_nick_name) : '')
                                }}
                            </div>
                            <div class="create_time">{{ reply.createAt }}</div>
                        </div>
                        <div class="content">
                            {{ reply.content }}
                        </div>
                    </div>
                </div>
            </div>
        </div>



    </div>
</template>
<style scoped lang='scss'>
.comment {
    border-top-color: rgb(55, 58, 60);
    display: flex;
    width: 100%;
    margin: 32px 0;

    .left {
        width: 50px;
        margin-right: 15px;

        img {
            width: 50px;
            height: 50px;
            border-radius: 50%;
        }
    }

    .right {
        width: 100%;

        .title {
            display: flex;
            align-items: center;
            justify-content: space-between;

            .user_name {
                height: 50px;
                font-weight: 700;
                font-size: 15px;
                color: #252933;
                display: flex;
                align-items: center;
                justify-content: space-between;
                width: calc(100% - 150px);
                white-space: no-warp;
            }

            .create_time {
                white-space: no-warp;
                width: 150px;
                text-align: right;
                font-size: 14px;
                color: #8a919f;
                font-family: -apple-system, BlinkMacSystemFont, Helvetica Neue, Helvetica, Arial, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif;
            }

            ;

        }

    }

    .content {
        margin-top: .2rem;
        margin-bottom: 0.4rem;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 2rem;
        color: #515767;
    }

    .replys {

        background-color: #cbcccf1e;
        padding: 20px;

        .reply {
            width: 100%;
            display: flex;

            .reply-left {
                width: 30px;
                margin-right: 20px;

                img {
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                }
            }

            .reply-right {
                width: 100%;

                .title {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;

                    .user_name {
                        height: 40px;
                        font-weight: 500;
                        font-size: 15px;
                        color: #252933;
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        width: calc(100% - 150px);
                        white-space: no-warp;
                    }

                    .create_time {
                        white-space: no-warp;
                        width: 150px;
                        text-align: right;
                        font-size: 14px;
                        color: #8a919f;

                    }

                }
            }
        }

    }
}
</style>
