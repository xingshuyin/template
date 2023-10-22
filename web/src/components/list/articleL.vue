<template>
    <div class="article" v-for="i in data">
        <div class="article-left">
            <el-avatar class="icon" :src="i[icon]" />
        </div>
        <div class="article-right">
            <div class="right-head">
                <div class="head-name">{{ i[username] }} </div>
                <div class="head-message"> {{ format(i[create_time], 'zh_CN') }} {{ }}</div>
            </div>
            <div class="right-content" @click="router.push(`/article/${i[id]}/`)">
                {{ i[name] }}
            </div>
            <div class="right-video" v-if="i[type] == 2">
                <t-video v-for="v in i[video]" :data="v"></t-video>
                <!-- <vue3VideoPlay @scroll="scroll_video($event)" v-for="v in i[video]"  v-bind="video_option(v.url)" /> -->
            </div>
            <div class="right-image" v-else-if="i[type] == 1">
                <t-imagewall :data="i[image]"></t-imagewall>
            </div>
            <div class="right-action">
                <div> <el-icon>
                        <View />
                    </el-icon>{{ i[view] }}
                </div>
                <div>
                    <ph:thumbs-up-bold></ph:thumbs-up-bold>
                    {{ i[like] }}
                </div>
                <div>
                    <el-icon>
                        <ChatLineSquare />
                    </el-icon>
                    {{ i[comment] }}
                </div>
                <div>
                    <el-icon>
                        <Star />
                    </el-icon>
                    {{ i[collect] }}
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { format } from 'timeago.js';
const router = useRouter();
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


// const video_option = (src) => {
//     let o = {
//         width: '100%', //播放器高度
//         height: '304px', //播放器高度
//         color: "#fff", //主题色
//         title: '', //视频名称
//         src: src, //视频源
//         muted: false, //静音
//         webFullScreen: false,
//         speedRate: ["0.75", "1.0", "1.25", "1.5", "2.0"], //播放倍速
//         autoPlay: false, //自动播放
//         loop: false, //循环播放
//         mirror: false, //镜像画面
//         ligthOff: false,  //关灯模式
//         volume: 0.3, //默认音量大小
//         control: true, //是否显示控制
//         preload: 'meta',
//         controlBtns: ['audioTrack', 'quality', 'speedRate', 'volume', 'setting', 'pip', 'pageFullScreen', 'fullScreen'] //显示所有按钮,
//     }
//     return o
// }

// const scroll_video = (e) => {
//     console.log(e);
// }
</script>
<style scoped lang='scss'>
.article {
    width: 100%;
    display: flex;
    flex-direction: row;
    padding: 16px 18px 0;
    box-sizing: border-box;
    margin: 16px;
    background-color: white;

    .article-left {
        width: 52px;
        padding-right: 10px;

        .icon {
            width: 52px;
            height: 52px;
        }
    }

    .article-right {
        flex: 1;

        .right-head {
            height: 52px;
            display: flex;
            flex-direction: column;
            // align-items: center;
            justify-content: space-around;

            .head-name {
                cursor: pointer;
                font-weight: bolder;
                line-height: 21px;
                font-size: 15px;
            }

            .head-message {
                cursor: pointer;
                color: #939393;
                font-size: 13px;
            }
        }

        .right-content {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
            line-height: 24px;
            font-size: 15px;
            color: #333;
            width: 100%;
            // overflow-x: auto;
        }

        .right-video {
            width: 100%;

            .video {
                width: 200px;
                height: 200px;
            }
        }

        .right-image {
            width: 100%;

            .image {
                width: 200px;
                height: 200px;
            }
        }

        .right-action {
            width: 100%;
            height: 40px;
            font-size: 16px;
            line-height: 1;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            font-weight: 400;
            color: grey;

            div {
                flex: 1;
                display: flex;
                flex-direction: row;
                align-items: center;
                justify-content: center;
            }
        }
    }
}
</style>