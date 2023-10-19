<!--
 * @Filename     : CommentTree.vue
 * @Description  : wjt-前端-评论树
                    data => [{id: 1,user_icon: 'a',create_time: '2121',...},...]
 * @Author       : xingshuyin xingshuyin@outlook.com
 * @Date         : 2022-10-07 14:41:30
 * @LastEditors  : xingshuyin xingshuyin@outlook.com
 * @LastEditTime : 2022-11-17 14:30:06
 * Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
-->
<script setup>
import { onBeforeMount } from 'vue';
import store from '../../store';
import r from '../../utils/request';
import { format } from 'timeago.js';
//import { ref } from 'vue';
//import {useRoute, useRouter} from 'vue-router';
//const route = useRoute() //当前路由
//const router = useRouter() //全局路由对象
const props = defineProps({
    data: {},
    media_id: null,
    media_type: null,
    user_icon: { default: 'user_icon' },
    user_name: { default: 'user_name' },
    create_time: { default: 'create_time' },
    content: { default: 'content' },
    replys: { default: 'replys' },
    reply_user_icon: { default: 'reply_user_icon' },
    reply_user_name: { default: 'reply_user_name' },
    callback: {},

}); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['onclick']); // emits 触发父组件函数
//const map = ref(null); //获取ref值为map的元素
//defineExpose({ map,}); //暴露组件的内容, 父组件通过组件对象(如ref)的value获取暴露的对象
const attrs = reactive({
    clicked_reply: [],
    comment: {
        media_type: null,
        media_id: null,
        content: undefined,
        reply_id: undefined,
        root_id: undefined,
    },
    comment_show: false,
    comment_root: true,
    comment_reply: null,
});
onBeforeMount(() => {
    attrs.comment.media_type = props.media_type;
    attrs.comment.media_id = props.media_id;
})
const click_reply = (e, reply, root) => {
    for (const i of attrs.clicked_reply) {
        i.comment_show = false;
    }
    attrs.clicked_reply = [];
    let reply_id = parseInt(reply.id);
    let root_id = parseInt(root.id);
    reply.comment_show = true
    attrs.comment_show = true
    attrs.comment.reply_id = reply_id;
    attrs.comment_root = false;
    attrs.comment.root_id = root_id;
    attrs.clicked_reply.push(reply);
}

const vClickOutside = {
    mounted(el, binding) {
        console.log('vClickOutside mounted');
        // 定义事件处理函数
        function eventHandler(e) {
            // 判断点击目标是否包含在绑定元素内
            if (el.contains(e.target)) {
                // 如果是，则不执行任何操作
                return false;
            }
            // 如果不是，则执行绑定的回调函数
            if (binding.value && typeof binding.value === 'function') {
                console.log('vClickOutside');
                binding.value(e);
            }
        }
        // 为绑定元素添加一个属性，用于存储事件处理函数的引用
        el.tag = eventHandler;
        // 为 document 添加 click 事件监听器
        document.addEventListener('click', eventHandler);
    },
    beforeUnmount(el) {
        // 为 document 移除 click 事件监听器
        document.removeEventListener('click', el.tag);
        // 删除绑定元素的属性
        delete el.tag;
    }
}


const comment = () => {
    if (store().is_login) {
        store().get_userinfo().then(() => {
            if (attrs.comment_root) {
                console.log('comment_root');
                attrs.comment.reply_id = undefined;
                attrs.comment.root_id = undefined;
            }
            r().get("/data/comment/", { params: attrs.comment }).then(res => {
                attrs.comment_page = 1;
                attrs.comment.content = null
                props.callback(true);
                attrs.comment_show = false;
            })
        })
    } else {
        ElMessage({
            showClose: true,
            message: '请登录',
            center: true,
        });
    }
}

</script>
<template>
    <el-input v-model="attrs.comment.content" @click="attrs.comment_root = true" :rows="2" type="textarea"
        placeholder="善言善语, 以理服人" />
    <el-button @click="comment">评论</el-button>
    <div class="comment" v-for="i in data" :key="i.id">
        <div class="left">
            <el-avatar shape="circle" :src="i[props.user_icon]"></el-avatar>
        </div>
        <div class="right">
            <div class="title">
                <div class="user_name">{{ i[props.user_name] }}</div>
                <div class="create_time">{{ format(i[props.create_time], 'zh_CN') }}</div>
            </div>
            <div class="content" @click.self.stop="click_reply($event, i, i);">
                {{ i[props.content] }}
            </div>
            <div class="reply-comment" v-if="i.comment_show == true" v-click-outside="() => i.comment_show = false">
                <el-input v-model="attrs.comment.content" :rows="2" type="textarea" placeholder="善言善语, 以理服人" />
                <el-button @click="comment">评论</el-button>
            </div>
            <div class="replys" v-if="i?.[props.replys]?.length">
                <div class="reply" v-for="reply in i[props.replys]" :key="reply.id">
                    <div class="reply-left">
                        <el-avatar shape="circle" :src="reply[props.reply_user_icon]"></el-avatar>
                    </div>
                    <div class="reply-right">
                        <div class="title">
                            <div class="user_name">
                                {{
                                    reply[props.user_name] + ' ' + (reply[props.reply_user_name] ?
                                        (' 回复@ ' + reply[props.reply_user_name]) : '')
                                }}
                            </div>
                            <div class="create_time">{{ format(reply[props.create_time], 'zh_CN') }}</div>
                        </div>
                        <div class="content" @click.self.stop="click_reply($event, reply, i);">
                            {{ reply[props.content] }}
                        </div>
                        <div class="reply-comment" v-if="reply.comment_show == true"
                            v-click-outside="() => reply.comment_show = false">
                            <el-input v-model="attrs.comment.content" :rows="2" type="textarea" placeholder="善言善语, 以理服人" />
                            <el-button @click="comment">评论</el-button>
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
