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
            </div>
            <div class="right-image" v-else-if="i[type] == 1">
                <t-imagewall :data="i[image]"></t-imagewall>
            </div>
            <div class="right-action">
                <div class="action"><el-icon>
                        <View />
                    </el-icon>
                    <div class="action-icon">{{ i[view] }}</div>
                </div>
                <div class="action">
                    <ph:thumbs-up-bold></ph:thumbs-up-bold>
                    <div class="action-icon">{{ i[like] }}</div>
                </div>
                <div class="action">
                    <el-icon>
                        <ChatLineSquare />
                    </el-icon>
                    <div class="action-icon">{{ i[comment] }}</div>
                </div>
                <div class="action">
                    <el-icon>
                        <Star />
                    </el-icon>
                    <div class="action-icon">{{ i[collect] }}</div>
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
        }

        .right-image {
            width: 100%;
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

            .action {
                flex: 1;
                display: flex;
                flex-direction: row;
                align-items: center;
                justify-content: center;
                gap: 5px;
            }
        }
    }
}
</style>