<script setup>
//import { ref } from 'vue';
//import {useRoute, useRouter} from 'vue-router';
//const route = useRoute() //当前路由
//const router = useRouter() //全局路由对象
import store from '../store';
import { base_url } from '../utils/request';
const props = defineProps(['data']); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['onclick']); // emits 触发父组件函数
//const map = ref(null); //获取ref值为map的元素
//defineExpose({ map,}); //暴露组件的内容, 父组件通过组件对象(如ref)的value获取暴露的对象
</script>
<template>
    <view class="comment" v-for="i in data" :key="i.id">
        <view class="left">
            <u-image class="left-img" width='40px' height="40px"
                :src="i.user_icon.includes('http') ? i.user_icon : base_url + '/' + i.user_icon" shape="circle"
                mode="aspectFit"></u-image>
        </view>
        <view class="right">
            <view class="title">
                <view class="user_name">{{ i.user_name }}</view>
                <view class="create_time">{{ i.create_time }}</view>
            </view>
            <view class="content"
                @click="store().comment_root = false; store().comment_reply = i.user_name ? i.user_name : i.user_name; store().comment_show = true; store().comment.root_id = i.id; store().comment.reply_id = undefined;">
                {{ i.content }}
            </view>

            <view class="replys" v-if="i?.replys?.length">
                <view class="reply" v-for="r in i.replys" :key="r.id">
                    <view class="reply-left">
                        <u-image class="reply-left-avatar" width='30px' height="30px"
                            :src="i.user_icon.includes('http') ? i.user_icon : base_url + '/' + i.user_icon"
                            shape="circle"></u-image>
                    </view>
                    <view class="reply-right">
                        <view class="title">
                            <view class="user_name">
                                <text
                                    style="overflow: hidden;text-overflow: ellipsis;display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical;">
                                    {{
                                        r.user_name
                                    }}
                                </text>

                            </view>
                            <view class="create_time">{{ r.create_time }}</view>
                        </view>
                        <view class="content"
                            @click="store().comment_root = false; store().comment_reply = i.user_name ? i.user_name : i.user_name; store().comment_show = true; store().comment.root_id = i.id; store().comment.reply_id = r.id;">
                            {{ (r.reply_user_name ? (' 回复@ ' + r.reply_user_name) :
                                '') }} {{ r.content }}
                        </view>
                    </view>
                </view>
            </view>
        </view>



    </view>
</template>
<style scoped lang='scss'>
.comment {
    border-top-color: rgb(55, 58, 60);
    display: flex;
    width: 100%;
    margin: 32px 0;

    .left {
        width: 40px;
        margin-right: 5px;

        .left-img {
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
                height: 40px;
                font-weight: 700;
                font-size: 15px;
                color: #252933;
                display: flex;
                align-items: center;
                justify-content: space-between;
                width: calc(100% - 120px);
                white-space: no-warp;
            }

            .create_time {
                white-space: no-warp;
                width: 120px;
                text-align: right;
                font-size: 12px;
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
        padding: 10px;

        .reply {
            width: 100%;
            display: flex;

            .reply-left {
                width: 30px;
                margin-right: 5px;

                .reply-left-avatar {
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
                        height: 30px;
                        font-weight: 500;
                        font-size: 12px;
                        color: #252933;
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        width: calc(100% - 120px);
                        white-space: no-warp;
                    }

                    .create_time {
                        white-space: no-warp;
                        width: 120px;
                        text-align: right;
                        font-size: 12px;
                        color: #8a919f;

                    }

                }
            }
        }

    }
}
</style>
