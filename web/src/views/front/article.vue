<template>
    <div class="article" @click.self="hdie_comment" @scroll="handleScroll">
        <v-md-preview v-if="attrs.item" :text="attrs.item.content">

        </v-md-preview>

        <el-button v-if="attrs.liked" @click="like">取消点赞</el-button>
        <el-button v-else @click="like">点赞</el-button>

        <el-button v-if="attrs.collected" @click="collect">取消收藏</el-button>
        <el-button v-else @click="collect">收藏</el-button>
        <!-- <t-comment :callback="comment"></t-comment> -->
        <t-comments :data="attrs.comments" :callback="get_comment_" :media_id="route.params.id"
            :media_type="attrs.base_url"></t-comments>

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
    base_url: 'article',
    comments: [],
    liked: false,
    collected: false,
    comment_end: false,
})

rest.item(attrs.base_url, route.params.id, attrs)
const handleScroll = (e) => {
    if (attrs.comment_end == false) {
        // console.log('sssssssss', e);
        // 变量scrollTop是滚动条滚动时，距离顶部的距离
        let scrollTop = e.target.scrollTop
        //变量windowHeight是可视区的高度
        let windowHeight = e.target.clientHeight
        //变量scrollHeight是滚动条的总高度
        let scrollHeight = e.target.scrollHeight
        //滚动条到底部的条件
        // console.log('scrollTop', scrollTop, 'windowHeight', windowHeight, 'scrollTop + windowHeight', scrollTop + windowHeight, 'scrollHeight', scrollHeight);
        if (scrollTop + windowHeight >= scrollHeight) {
            console.log('bottom');
            get_comment_()
        }
    }

}
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
    get_comment_()
    window.addEventListener('scroll', handleScroll)//监听函数
})


const get_comment_ = async (replace) => {
    //获取评论
    if (replace) attrs.comment_page = 1;
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
        } else {
            attrs.comment_end = true
        }
    });
};




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
    width: 50%;
    height: 100%;
    overflow: auto;
    margin: auto;
    padding: 20px;
    box-sizing: border-box;
}
</style>
