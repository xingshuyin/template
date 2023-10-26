<template>
    <div class="article" v-if="attrs.item" @scroll="handleScroll">
        <div class="title">
            {{ attrs.item.name }}
        </div>

        <v-md-preview :text="attrs.item.content">
        </v-md-preview>
        <div class="right-video" v-if="attrs.item.type == 2">
            <t-video v-for="v in attrs.item.video" :data="v"></t-video>
        </div>
        <div class="right-image" v-else-if="attrs.item.type == 1">
            <t-imagewall :data="attrs.item.image"></t-imagewall>
        </div>
        <div class="actions" v-if="attrs.item">
            <!-- <ph:eye-fill></ph:eye-fill> -->
            <el-row :gutter="20">
                <el-col :span="6">
                    <ph:eye-duotone></ph:eye-duotone>
                    <span class="action-num">{{ attrs.item.view }}</span>
                </el-col>
                <el-col :span="6" @click="like">
                    <ph:thumbs-up-fill v-if="attrs.liked"></ph:thumbs-up-fill>
                    <ph:thumbs-up-duotone v-else></ph:thumbs-up-duotone>
                    <span class="action-num">{{ attrs.item.like }}</span>
                </el-col>
                <el-col :span="6" @click="collect">
                    <ph:star-fill v-if="attrs.collected"></ph:star-fill>
                    <ph:star-duotone v-else></ph:star-duotone>
                    <span class="action-num">{{ attrs.item.collect }}</span>
                </el-col>
                <el-col :span="6">
                    <ph:share-network-duotone></ph:share-network-duotone>
                    <span class="action-num">{{ attrs.item.view }}</span>
                </el-col>
            </el-row>
        </div>
        <t-comments :data="attrs.comments" :callback="get_comment_" :media_id="route.params.id"
            :media_type="attrs.base_url">
        </t-comments>

        <chat v-if="attrs.info && attrs.item" :group="attrs.item.id" :user_info="attrs.info"></chat>

    </div>
</template>
<script setup>
import { useRoute, useRouter } from 'vue-router';
import rest from '../../utils/rest';
import r from '../../utils/request';
import { onBeforeMount } from 'vue';
import chat from '../../components/chat/chat.vue'
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
    messages: []
})

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
            attrs.info = info
            rest.item(attrs.base_url, route.params.id, attrs, null, (res) => {

            })
            r().get("/data/view/", { params: { type: 'article', id: route.params.id } })
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

const like = (id) => {
    id = route.params.id
    r().get('/data/like/', { params: { type: 'article', id: id, liked: attrs.liked } }).then((res) => {
        let temp = false;
        console.log(res);
        if (res.data.data == 'true') {
            store().userinfo.article_like.push(id)
            temp = true
        } else {
            store().userinfo.article_like.splice(store().userinfo.article_like.indexOf(id), 1)
            temp = false
        }
        if (temp) { attrs.item.like += 1 } else { attrs.item.like -= 1 }
        attrs.liked = temp
    })
}

const collect = (id) => {
    id = route.params.id
    r().get('/data/collect/', { params: { type: 'article', id: id, collected: attrs.collected } }).then((res) => {
        let temp = false;

        if (res.data.data == 'true') {
            store().userinfo.article_like.push(id)
            temp = true
        } else {
            store().userinfo.article_collect.splice(store().userinfo.article_collect.indexOf(id), 1)
            temp = false
        }
        if (temp) { attrs.item.collect += 1 } else { attrs.item.collect -= 1 }
        attrs.collected = temp
    })
}




</script>
<style scoped lang='scss'>
.article {
    background-color: aliceblue;
    width: 1000px;
    height: 100%;
    overflow: auto;
    margin: auto;
    padding: 20px;
    box-sizing: border-box;

    .title {
        font-size: 30px;
        text-align: center;
        margin-bottom: 20px;
    }

    .actions {
        margin: 20px auto;
        width: 400px;
        font-size: 19px;
        color: rgba(41, 44, 236, 0.801);

        :deep(.el-col) {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
            gap: 3px;
        }
    }
}
</style>
