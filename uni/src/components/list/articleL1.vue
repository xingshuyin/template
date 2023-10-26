<template>
    <div class="article" v-for=" i, index in props.data" :key="i[props.id]">
        <div class="article-left" @click="navigate(`/pages/detail/article?id=${i[props.id]}`)">
            <div class="article-title">
                <div class="title-left"><u-avatar :src="i[props.icon]" size="50"></u-avatar> </div>
                <div class="title-right">
                    <div class="right-top">{{ i[props.source_root] }}</div>
                    <div class="right-bottom"> {{ i[props.source_sub] }} {{ i[props.create_time] }}</div>
                </div>

            </div>
            <div class="article-content">
                <div style="height: min-content;">
                    {{ i[props.name] }}
                </div>
            </div>
            <!-- <div class="article-time">
                <div>{{ i[props.source] }}</div>
                <div>{{ i[props.time] }}</div>
            </div> -->
        </div>
        <div class="article-right">
            <view class="source">{{ i[props.source] }}</view>
            <view class="buttons">
                <u-icon class="buttons-comment" name="eye" color="#cfcfcf" size="38">
                </u-icon>
                {{ i.view }}
                <u-icon class="buttons-comment" name="chat" color="#cfcfcf" size="38"
                    @click="attrs.comment_index = index; attrs.comment_show = true;">
                </u-icon>
                {{ i.comment }}
                <u-icon class="buttons-comment" v-if="store().is_login && i?.liked == true" name="thumb-up-fill"
                    color="#cfcfcf" size="38" @click.stop="like(i[props.id], index)">
                </u-icon>
                <u-icon class="buttons-comment" v-else-if="store().is_login && i?.liked == false" name="thumb-up"
                    color="#cfcfcf" size="38" @click.stop="like(i[props.id], index)">
                </u-icon>
                <u-icon class="buttons-comment" v-else name="thumb-up" color="#cfcfcf" size="38" @click="like()">
                </u-icon>
                {{ i.like }}
                <u-icon class="buttons-comment" v-if="store().is_login && i?.collected == true" name="star-fill"
                    color="#cfcfcf" size="38" @click.stop="collect(i[props.id], index)">
                </u-icon>
                <u-icon class="buttons-comment" v-else-if="store().is_login && i?.collected == false" name="star"
                    color="#cfcfcf" size="38" @click.stop="collect(i[props.id], index)">
                </u-icon>
                <u-icon class="buttons-comment" v-else name="star" color="#cfcfcf" size="38"
                    @click="collect(i[props.id], index)">
                </u-icon>
                {{ i.collect }}
                <!-- <u-icon class="buttons-comment" name="share" color="#cfcfcf" size="38" @click="share.open()">
                </u-icon> -->
            </view>
        </div>
    </div>
</template>
<script setup>
import { navigate } from '../../utils/data';
import r from '../../utils/request';
import store from '../../store';
import { onMounted, reactive } from 'vue';
import { onLoad, onReady, onShow, onHide, onUnload, onPullDownRefresh, onReachBottom, onPageScroll, onShareAppMessage } from '@dcloudio/uni-app';
import { watch } from 'vue';
const props = defineProps({
    data: {},
    id: { default: "id" },
    icon: { default: "icon" },
    name: { default: "name" },
    content_text: { default: "content_text" },
    source: { default: "source" },
    source_root: { default: "source_root" },
    source_sub: { default: "source_sub" },
    create_time: { default: "create_time" },
}); //子向父传数据
const attrs = reactive({
    comment_index: null,
    comment_content: null,
});



const check = (start) => {
    if (store().is_login) {
        console.log('check');
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
    console.log('attrs.info', index, attrs.info, props.data);
    for (let i = 0; i < attrs.info.article_like.length; i++) {
        const element = attrs.info.article_like[i];
        if (element == id) {
            temp = true
            break
        } else {
            temp = false
        }
    }
    console.log(temp);
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
    background-color: rgb(255, 255, 255);
    padding: 30rpx 30rpx;
    margin: 0rpx 0rpx;
    // border-radius: 20rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    border: 1px solid rgba(221, 221, 221, 0.384);

    .article-left {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;

        .article-title {
            font-size: 28rpx;
            font-weight: 800;
            width: 100%;
            margin-bottom: 16rpx;
            display: flex;
            flex-direction: row;
            align-items: center;

            // justify-content: center;
            .title-left {}

            .title-right {
                margin-left: 20rpx;

                .right-top {
                    font-size: 26rpx;
                }

                .right-bottom {
                    font-size: 22rpx;
                    color: rgba(128, 125, 125, 0.815);
                }
            }
        }

        .article-content {
            font-size: 26rpx;
            min-height: 100rpx;
            font-weight: 600;
            font-family: fantasy;
            color: rgb(46 46 46);
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;

        }

        // .article-time {
        //     margin-top: 10rpx;
        //     width: 100%;
        //     font-size: 26rpx;
        //     color: rgba(65, 64, 64, 0.877);
        //     display: flex;
        //     flex-direction: row;
        //     align-items: center;
        //     gap: 20rpx;
        //     // justify-content: space-between;
        // }
    }

    .article-right {
        width: 100%;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;

        .source {
            white-space: nowrap;
            font-size: 22rpx;
            color: rgba(112, 110, 110, 0.842);
            font-weight: 700;
            width: 14rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .buttons {
            // position: fixed;
            bottom: 0;
            width: 100%;
            display: flex;
            justify-content: flex-end;
            align-items: center;
            background-color: white;

            .buttons-comment {
                margin: 5px 15px;
            }
        }

    }
}
</style>