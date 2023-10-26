<template>
    <div class="article" v-for="i in data" :key="i[id]">
        <div class="article-left">
            <u-avatar class="icon" :src="i[icon]" />
        </div>
        <div class="article-right">
            <div class="right-head">
                <div class="head-name">{{ i[username] }} </div>
                <div class="head-message"> {{ format(i[create_time], 'zh_CN') }} {{ }}</div>
            </div>
            <div class="right-content" @click="navigate(`/pages/detail/article?id=${i[id]}`)">
                {{ i[name] }}
            </div>
            <div class="right-video" v-if="i[type] == 2">
                <t-video v-for="v, index in i[video]" :data="v" :key="index"></t-video>
            </div>
            <div class="right-image" v-else-if="i[type] == 1">
                <t-imagewall :data="i[image]"></t-imagewall>
            </div>
            <div class="right-action">
                <div class="action">
                    <u-icon name="eye"></u-icon>
                    <div class="action-icon">{{ i[view] }}</div>
                </div>
                <div class="action">
                    <u-icon name="thumb-up"></u-icon>
                    <div class="action-icon">{{ i[like] }}</div>
                </div>
                <div class="action">
                    <u-icon name="chat"></u-icon>
                    <div class="action-icon">{{ i[comment] }}</div>
                </div>
                <div class="action">
                    <u-icon name="star"></u-icon>
                    <div class="action-icon">{{ i[collect] }}</div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { format } from 'timeago.js/lib';
import { navigate } from '../../utils/data';
import store from '../../store';
import tImagewall from '../../components/tools/t-imagewall'
import tVideo from '../../components/tools/t-video'
import { reactive } from 'vue';
const props = defineProps({
    data: {},
    id: { default: 'id' },
    icon: { default: 'icon' },
    username: { default: 'username' },
    name: { default: 'name' },
    source: { default: 'source' },
    content: { default: 'content' },
    video: { default: 'video' },
    image: { default: 'image' },
    like: { default: 'like' },
    type: { default: 'type' },
    comment: { default: 'comment' },
    view: { default: 'view' },
    collect: { default: 'collect' },
    create_time: { default: 'create_time' }
}); //子向父传数据

const attrs = reactive({
    info: {}
});
const check = (start) => {
    if (store().is_login) {
        store().get_userinfo(false).then((info) => {
            attrs.info = info
            for (let i = start; i < props.data?.length; i++) {
                is_like(i)
                is_collect(i)
            }
        })
    } else {
        console.log('未登录');
    }


}


const is_like = (index) => {
    let id = props.data[index].id
    let temp = false;
    for (let i = 0; i < attrs.info.article_like.length; i++) {
        const element = attrs.info.article_like[i];
        if (element == id) {
            temp = true
            break
        } else {
            temp = false
        }
    }
    props.data[index].liked = temp
}


const is_collect = (index) => {
    let id = props.data[index].id
    let temp = false;
    for (let i = 0; i < attrs.info.article_collect.length; i++) {
        const element = attrs.info.article_collect[i];
        if (element == id) {
            temp = true
            break
        } else {
            temp = false
        }
    }
    props.data[index].collected = temp
}


const like = (id, index) => {
    r.get('/data/like/', { type: 'article', id: id, liked: props.data[index].liked }).then((res) => {
        let temp = false;

        if (res.data.data == 'true') {
            store().userinfo.article_like.push(id)
            temp = true
        } else {
            store().userinfo.article_like.splice(store().userinfo.article_like.indexOf(id), 1)
            temp = false
        }
        if (temp) { props.data[index].like += 1 } else { props.data[index].like -= 1 }
        props.data[index].liked = temp
    })

}

const collect = (id, index) => {
    r.get('/data/collect/', { type: 'article', id: id, collected: props.data[index].collected }).then((res) => {
        let temp = false;
        if (res.data.data == 'true') {
            store().userinfo.article_collect.push(id)
            temp = true
        } else {
            store().userinfo.article_collect.splice(store().userinfo.article_collect.indexOf(id), 1)
            temp = false
        }
        if (temp) { props.data[index].collect += 1 } else { props.data[index].collect -= 1 }
        props.data[index].collected = temp
    })
}

defineExpose({ check })

</script>
<style scoped lang='scss'>
.article {
    width: 100%;
    display: flex;
    flex-direction: row;
    padding: 16px;
    // box-sizing: border-box;
    // margin: 16px;
    background-color: white;
    margin-top: 500px;

    .article-left {
        width: 104rpx;
        padding-right: 20rpx;

        .icon {
            width: 104rpx;
            height: 104rpx;
        }
    }

    .article-right {
        flex: 1;

        .right-head {
            height: 104rpx;
            display: flex;
            flex-direction: column;
            // align-items: center;
            justify-content: space-around;

            .head-name {
                cursor: pointer;
                font-weight: bolder;
                line-height: 42rpx;
                font-size: 30rpx;
            }

            .head-message {
                cursor: pointer;
                color: #939393;
                font-size: 26rpx;
            }
        }

        .right-content {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
            line-height: 48rpx;
            font-size: 30rpx;
            color: #333;
            width: 100%;
            // overflow-x: auto;
        }

        .right-video {
            width: 100%;
        }

        .right-image {
            width: 100%;
        }

        .right-action {
            width: 100%;
            height: 80rpx;
            font-size: 32rpx;
            line-height: 1;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            font-weight: 400;
            color: grey;

            .action {
                flex: 1;
                display: flex;
                flex-direction: row;
                align-items: center;
                justify-content: center;
                gap: 10rpx;
            }
        }
    }
}
</style>