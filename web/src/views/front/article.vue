<template>
    <div class="article">
        <v-md-preview v-if="attrs.item" :text="attrs.item.content">

        </v-md-preview>

        <el-button v-if="attrs.liked" @click="like">取消点赞</el-button>
        <el-button v-else @click="like">点赞</el-button>

        <el-button v-if="attrs.collected" @click="collect">取消收藏</el-button>
        <el-button v-else @click="collect">收藏</el-button>
        <el-input v-model="store().comment.content" :rows="2" type="textarea" @click="store().comment_root = true;"
            placeholder="善言善语, 以理服人" />
        <el-button @click="comment">评论</el-button>
        <t-comment :data="attrs.comments"></t-comment>

    </div>
</template>
<script setup>
import { useRoute, useRouter } from 'vue-router';
import rest from '../../utils/rest';
import r from '../../utils/request';
import { onBeforeMount } from 'vue';
const router = useRouter()
const route = useRoute()
import store from '../../store';
//const emits = defineEmits(['update:modelValue']); // emits 触发父组件函数
const attrs = reactive({
    comments: [],
    liked: false,
    collected: false,
})
rest.item('article', route.params.id, attrs)
onBeforeMount(() => {
    if (store().is_login) {
        store().get_userinfo(true).then((info) => {
            let temp = false;
            for (let i = 0; i < info.article_like.length; i++) {
                const element = info.article_like[i];
                if (element == route.params.id) {
                    temp = true
                    break
                } else {
                    temp = false
                }
            }
            attrs.liked = temp

            temp = false;
            for (let i = 0; i < info.article_collect.length; i++) {
                const element = info.article_collect[i];
                if (element == route.params.id) {
                    temp = true
                    break
                } else {
                    temp = false
                }
            }
            attrs.collected = temp
        })
    }
    store().comment.media_id = route.params.id
    store().comment.media_type = "article"
    get_comment_()
})

const get_comment_ = async (replace) => {
    //获取评论
    attrs.comment_page ? 1 : (attrs.comment_page = 1);
    attrs.comment_limit ? 1 : (attrs.comment_limit = 10);
    attrs.comment_total ? 1 : (attrs.comment_total = 0);
    await r().get('/data/article_comment/', { params: { page: attrs.comment_page, limit: attrs.comment_limit, id: route.params.id } }).then(res => {
        if (res.data.data.length > 0) {
            if (replace) {
                attrs.comments = res.data.data;
            } else {
                attrs.comments = attrs.comments.concat(res.data.data);
            }
            attrs.comment_total = res.data.total;
            attrs.comment_page++
        }

    });
};

const comment = () => {
    if (store().is_login) {
        store().get_userinfo().then(() => {
            if (store().comment_root) {
                store().comment.reply_id = undefined;
                store().comment.root_id = undefined;
            }
            r().get("/data/comment/", { params: store().comment }).then(res => {
                attrs.comment_page = 1;
                store().comment.content = null
                get_comment_(true);
                store().comment_show = false;
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
const like = () => {
    r().get('/data/like/', { params: { type: 'article', id: route.params.id, liked: attrs.liked } }).then(() => {
        store().get_userinfo(true).then((info) => {
            console.log(info);
            let temp = false;
            for (let i = 0; i < info.article_like.length; i++) {
                const element = info.article_like[i];
                if (element == route.params.id) {
                    temp = true
                    break
                } else {
                    temp = false
                }
            }
            attrs.liked = temp
        })
    })
}

const collect = () => {
    r().get('/data/collect/', { params: { type: 'article', id: route.params.id, collected: attrs.collected } }).then(() => {
        store().get_userinfo(true).then((info) => {
            let temp = false;
            for (let i = 0; i < info.article_collect.length; i++) {
                const element = info.article_collect[i];
                if (element == route.params.id) {
                    temp = true
                    break
                } else {
                    temp = false
                }
            }
            attrs.collected = temp
        })
    })
}
</script>
<style scoped lang='scss'>
.article {
    background-color: aliceblue;
    width: 70%;
    height: 100%;
    overflow: auto;
    margin: auto;
    padding: 20px;
    box-sizing: border-box;
}
</style>
