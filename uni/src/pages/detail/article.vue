<template>
    <view>
        <!-- #ifndef MP-WEIXIN -->
        <view class="status_bar">
            <!-- 这里是状态栏 -->
        </view>
        <u-navbar back-text="返回" :title="attrs?.item?.name"></u-navbar>
        <!-- #endif -->
        <!-- #ifdef MP-WEIXIN -->
        <u-navbar back-text="返回" :title="attrs?.item?.name"></u-navbar>
        <!-- #endif -->

        <view class="article" v-if="attrs.item != null">
            <view>
                <text class="article-title">
                    {{ attrs?.item[props.name] }}
                </text>
            </view>
            <view class="article-detail">
                <view class="article-user_name">
                    {{ attrs?.item[props.source] }} {{ attrs?.item[props.create_time].slice(0, 10) }}
                </view>
            </view>
            <div class="right-video" v-if="attrs?.item?.type == 2">
                <t-video v-for="v, index in attrs?.item?.video" :data="v" :key="index"></t-video>
            </div>
            <div class="right-image" v-else-if="attrs?.item?.type == 1">
                <t-imagewall :data="attrs?.item?.image"></t-imagewall>
            </div>
            <!-- <rich-text v-if="!!attrs.item" :nodes="attrs.item.content"></rich-text> -->
            <view class="article-body" v-html="attrs?.item[props.content]"></view>
            <u-gap height="20"></u-gap>
            <view class="read-source" @click="navigate(`/pages/detail/webview?url=${attrs?.item[props.url]}`)">阅读原文</view>
            <view class="article-comment">
                <text style="font-size: large;font-weight: 800;">评论</text>
                <CommentTree :data="attrs.comments"></CommentTree>
            </view>
        </view>
        <view class="buttons" v-if="attrs.item != null">
            <u-icon class="buttons-comment" name="eye" color="black" size="38">
            </u-icon>
            {{ attrs?.item[props.view] }}
            <u-icon class="buttons-comment" name="chat" color="black" size="47"
                @click="attrs.comment_root = true; attrs.comment_show = true;">
            </u-icon>
            {{ attrs?.item[props.comment] }}
            <u-icon class="buttons-comment" v-if="store().is_login && attrs.liked" name="thumb-up-fill" color="black"
                size="47" @click="like()">
            </u-icon>
            <u-icon class="buttons-comment" v-else-if="store().is_login && !attrs.liked" name="thumb-up" color="black"
                size="47" @click="like()">
            </u-icon>
            <u-icon class="buttons-comment" v-else name="thumb-up" color="black" size="47" @click="like()">
            </u-icon>
            {{ attrs?.item[props.like] }}
            <u-icon class="buttons-comment" v-if="store().is_login && attrs.collected" name="star-fill" color="black"
                size="47" @click="collect()">
            </u-icon>
            <u-icon class="buttons-comment" v-else-if="store().is_login && !attrs.collected" name="star" color="black"
                size="47" @click="collect()">
            </u-icon>
            <u-icon class="buttons-comment" v-else name="star" color="black" size="47" @click="collect()">
            </u-icon>
            {{ attrs?.item[props.collect] }}
            <u-icon class="buttons-comment" name="share" color="black" size="47" @click="share.open()">
            </u-icon>
        </view>
        <canvas ref="poster" canvas-id="poster" class="poster" />
        <canvas ref="qrcode" canvas-id="qrcode" class="qrcode" />
        <u-popup v-model="attrs.comment_show" mode="bottom" border-radius="24">
            <view class="comment">
                <view class="comment-body">
                    <u-input class="comment-input" v-model="attrs.comment.content"
                        :placeholder="attrs.comment_root ? '善言善语, 以理服人' : '回复 ' + attrs.comment_reply + ' : '"
                        type="textarea" height="400" />
                    <u-button class="comment-btn" type="primary" shape="circle" @click="comment()">发送</u-button>
                </view>
            </view>
        </u-popup>
        <u-mask :show="attrs.img_view" @click="attrs.img_view = false">
            <u-image width="100%" height="100%" :src="attrs.img_view_url" mode="aspectFit"></u-image>
        </u-mask>
        <FatFatMeng-PopupShare ref="share" :SharelistConfing="SharelistConfing" @changeShare="changeShareTap">
        </FatFatMeng-PopupShare>
    </view>
</template>
<script setup>
import tVideo from '../../components/tools/t-video.vue';
import tImagewall from '../../components/tools/t-imagewall.vue';
//const props = defineProps(['modelValue']); // defineProps的参数, 可以直接使用
//const emits = defineEmits(['update:modelValue']); // emits 触发父组件函数
import {
    reactive,
    onMounted,
    onUnmounted,
    ref
} from 'vue';
// import { get_share_url } from '../utils/data'
// import UQRCode from '../uni_modules/Sansnn-uQRCode/js_sdk/uqrcode/uqrcode';
import rest from "../../utils/rest";
import r from "../../utils/request";
import store from '../../store';
import CommentTree from "../../components/CommentTree.vue";
import {
    onLoad, onReachBottom
} from '@dcloudio/uni-app';
import { navigate } from '../../utils/data';


const props = defineProps({
    data: {},
    id: { default: "id" },
    name: { default: "name" },
    source: { default: "source" },
    content: { default: "content" },
    school_name: { default: "school_name" },
    create_time: { default: "create_time" },
    comment: { default: 'comment' },
    like: { default: 'like' },
    collect: { default: 'collect' },
    view: { default: 'view' },

}); //子向父传数据

const poster = ref(null)
const uTips = ref(null)
const attrs = reactive({
    item: null,
    id: null,
    liked: false,
    collected: false,
    comments: [],
    comment: {
        content: null,
        root_id: null,
        reply_id: null,
        media_id: null,
        media_type: null,
    },
    img_count: 0,
    qr_finish: false,
    text_finish: false,
    comment_root: true,
    comment_show: false,
    comment_page: 1,
    comment_limit: 10,
    comment_total: 1,
})




onLoad((option) => {
    attrs.article_id = parseInt(option.id)
    if (store().is_login) {
        store().get_userinfo(true).then((info) => {
            let temp = false;
            for (let i = 0; i < info.article_like.length; i++) {
                const element = info.article_like[i];
                if (element == attrs.article_id) {
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
                if (element == attrs.article_id) {
                    temp = true
                    break
                } else {
                    temp = false
                }
            }
            attrs.collected = temp
        })
    }

    attrs.comment.media_id = attrs.article_id
    attrs.comment.media_type = "article"
    rest.get('article', option.id, attrs, null, (res) => {
        attrs.item.content = attrs.item.content.replace(/<img(.*?)(sytle="(.*?)")?(.*?)>/g, '<img$1 width="320" $4 style="width:100%">');
        attrs.item.content = attrs.item.content.replace(/<img(.*?)(sytle="(.*?)")?(.*?)>/g, '<img$1 width="320" $4 style="width:100%">');
        attrs.item.content = attrs.item.content.replace(/<table(.*?)(sytle="(.*?)")?(.*?)>/g, '<table$1 width="320" $4 style="width:100%;$3">');
    })
    get_comment_()
    view()
    // draw_qrcode()

})
onUnmounted(() => {
    if (store().is_login) {
        r.get("/data/view/", { type: 'article', id: attrs.article_id })
    }
})
onReachBottom(() => {
    get_comment_(false)
})
const get_comment_ = async (replace = false) => {
    //获取评论
    attrs.comment_page ? 1 : (attrs.comment_page = 1);
    attrs.comment_limit ? 1 : (attrs.comment_limit = 10);
    attrs.comment_total ? 1 : (attrs.comment_total = 0);
    await r.get('/data/article_comment/', { page: attrs.comment_page, limit: attrs.comment_limit, id: attrs.article_id }).then(res => {
        if (res.data.data.length > 0) {
            if (replace) {
                attrs.comments = res.data.data;
                uni.stopPullDownRefresh()
            } else {
                attrs.comments = attrs.comments.concat(res.data.data);
            }
            attrs.comment_total = res.data.total;
            attrs.comment_page++
        }

    });
};

const comment = () => {
    store().get_userinfo().then(() => {
        if (attrs.comment_root) {
            attrs.comment.reply_id = undefined;
            attrs.comment.root_id = undefined;
        }
        r.get("/data/comment/", attrs.comment).then(res => {
            attrs.comment_show = false;
            attrs.comment_page = 1
            attrs.item[props.comment] += 1
            get_comment_(true)
        })
    })

}

const view = () => {
    r.get('/data/view/', { type: 'article', id: attrs.article_id })
}

const like = (id) => {
    id = attrs.article_id
    r.get('/data/like/', { type: 'article', id: id, liked: attrs.liked }).then((res) => {
        let temp = false;

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
    id = attrs.article_id
    r.get('/data/collect/', { type: 'article', id: id, collected: attrs.collected }).then((res) => {
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


// --------------分享-----------------

const share = ref()
const SharelistConfing = [
    {
        imgurl: '/uni_modules/FatFatMeng-PopupShare/static/FatFatMeng-apps/images/share/ic_share_postcard.png',
        name: '生成海报',
        isShow: true,
    },
    {
        imgurl: '/uni_modules/FatFatMeng-PopupShare/static/FatFatMeng-apps/images/share/ic_share_wechat.png',
        name: '微信好友',
        isShow: true,
    },
    {
        imgurl: '/uni_modules/FatFatMeng-PopupShare/static/FatFatMeng-apps/images/share/ic_share_wechatmoments.png',
        name: '朋友圈',
        isShow: true,
    },
    {
        imgurl: '/uni_modules/FatFatMeng-PopupShare/static/FatFatMeng-apps/images/share/ic_share_qq.png',
        name: 'QQ',
        isShow: true,
    },
    {
        imgurl: '/uni_modules/FatFatMeng-PopupShare/static/FatFatMeng-apps/images/share/ic_share_qzone.png',
        name: 'QQ空间',
        isShow: true,
    },
    {
        imgurl: '/uni_modules/FatFatMeng-PopupShare/static/FatFatMeng-apps/images/share/ic_share_weibo.png',
        name: '微博',
        isShow: true,
    },
    {
        imgurl: '/uni_modules/FatFatMeng-PopupShare/static/FatFatMeng-apps/images/share/ic_share_links.png',
        name: '复制链接', // 7
        isShow: true,
    },
]
const changeShareTap = (event) => {
    share.value.close()
    // 返回值 event={index:索引项,name:名称}
    if (event.index == 1) {
        uni.showLoading({
            mask: true,
            title: '正在生成',
            success: () => {
                uni.hideLoading()
            }
        })
        draw_poster(0, 0, attrs.item.name, attrs.item.content, attrs?.item?.source, attrs?.item?.hold_time, 'poster')
    } else if (event.index == 2) {
        to_qq(attrs.video_id, 'video', attrs?.item?.name)
    } else if (event.index == 3) {
        to_qq(attrs.video_id, 'video', attrs?.item?.name)
    } else if (event.index == 4) {
        to_qq(attrs.video_id, 'video', attrs?.item?.name)
    } else if (event.index == 5) {
        to_qq(attrs.video_id, 'video', attrs?.item?.name)
    } else if (event.index == 6) {
        to_weibo(attrs.video_id, 'video', attrs?.item?.name)
    } else if (event.index == 7) {
        let url = get_share_url(attrs.article_id, 'article')
        uni.setClipboardData({
            data: url,
            success: function () {
                uni.showToast({
                    title: '链接已复制到剪贴板'
                })
            }
        });
    }
}


const draw_qrcode = () => {

    const qr_canvas = uni.createCanvasContext('qrcode')
    var qr = new UQRCode();
    // 设置二维码内容
    qr.data = get_share_url(attrs.article_id, 'article');
    // 设置二维码大小，必须与canvas设置的宽高一致
    qr.size = 200;
    // 调用制作二维码方法
    qr.make();
    // 获取canvas上下文
    // 设置uQRCode实例的canvas上下文
    qr.canvasContext = qr_canvas;
    // 调用绘制方法将二维码图案绘制到canvas上
    qr.drawCanvas().then(() => {

    });

}

const draw_poster = (x, y, title, text, author, time, canvas_id) => {
    const ctx = uni.createCanvasContext(canvas_id)
    ctx.setFillStyle('white')
    ctx.fillRect(0, 0, 99999, 999999)
    let first_indent = 20
    let padding = 20
    let line_height = 20
    let font_size = 15
    let title_line_height = 26
    let title_size = 21
    let author_size = 14

    x = x + padding
    y = y + title_line_height
    const draw_logo_head = (width) => {
        let height_bg = parseInt(width / 540 * 385 / 2)
        ctx.drawImage('../../static/img/user_top_header.png', 0, 0, width, height_bg);
        ctx.drawImage('../../static/img/lans_icon.png', 130, parseInt(height_bg / 2 - 30), 166, 60);
        ctx.drawImage('../../static/img/ic_launcher_round.png', 10, parseInt(height_bg / 2 - 50), 100, 100);
        y = y + height_bg
    }
    const draw_title = (width) => {
        ctx.font = `${title_size}px Arial`;
        ctx.fillStyle = "black";
        ctx.textBaseline = "middle";
        let temp = ''
        let lines = [];
        let temp_text_list = title.split('')
        temp_text_list.forEach(i => {
            if (ctx.measureText(temp).width >= width - title_size - padding * 2) {
                lines.push(temp)
                temp = ''
            }
            temp += i
        });
        lines.push(temp)
        temp = ''
        for (let i = 0; i < lines.length; i++) {
            ctx.fillText(lines[i], x, y);
            y = y + title_line_height
        }
        y = y + 20
    }
    const draw_author = () => {
        ctx.font = `${author_size}px Arial`;
        ctx.fillStyle = "black";
        ctx.textBaseline = "middle";
        ctx.fillText(author, x, y);
        ctx.fillText(time, x + ctx.measureText(author).width + 5, y)
        y = y + 40
    }
    const draw_text = (width) => {
        ctx.font = `${font_size}px Arial`;
        ctx.fillStyle = "black";
        ctx.textBaseline = "middle";
        text = attrs.item.content
        text = text.replace(/<img.*?src="(.*?)".*?>/g, "|img,$1|");
        text = text.replace(/<\/p>/g, "|newline,|");
        text = text.replace(/<script>.*?<\/script>|<style.*?<\/style>|<.*?>/g, "")
        text = text.replace(/\s+/g, "")
        let temp = ''
        let is_first = true
        let lines = [];

        text.split("|").forEach(p => {
            if (p.startsWith('img,')) {
                lines.push(p)
                attrs.img_count += 1
            } else if (p.startsWith('newline,')) {
                lines.push(p)
                is_first = true
            }
            else {
                let temp_text_list = p.split('')
                temp_text_list.forEach(i => {
                    if (ctx.measureText(temp).width >= width - font_size - first_indent - padding * 2 && is_first) {
                        lines.push(temp)
                        temp = ''
                        is_first = false
                    }
                    else if (ctx.measureText(temp).width >= width - font_size - padding * 2) {
                        lines.push(temp)
                        temp = ''
                    }
                    temp += i
                });
                lines.push(temp)
                temp = ''
                is_first = true
            }
        });
        for (let i = 0; i < lines.length; i++) {
            if (lines[i].startsWith('img,')) {
                let x_img = x
                let y_img = y
                y = y + 200
                uni.getImageInfo({
                    src: lines[i].split(',')[1],
                    success: (res) => {
                        y = y + line_height
                        ctx.drawImage(res.path, x_img, y_img, width - padding * 2, 200);
                        // ctx.drawImage('../../static/img/Login_bg.png', 0, 0, 200, 200);
                        ctx.draw(true, () => {
                            attrs.img_count -= 1
                        });
                    }
                })

            } else if (lines[i].startsWith('newline,')) {
                y = y + 5
                is_first = true
            }
            else {
                if (is_first) {
                    ctx.fillText(lines[i], x + first_indent, y);
                    is_first = false
                } else {
                    ctx.fillText(lines[i], x, y);
                }
                y = y + line_height
            }
        }
        attrs.text_finish = true
    }
    const canvas_to_temp = (width, height) => {
        console.log('绘图时高度', height)
        uni.canvasToTempFilePath({
            height: height,
            canvasId: 'poster',
            success: function (res) {
                // 在H5平台下，tempFilePath 为 base64
                uni.saveImageToPhotosAlbum({
                    filePath: res.tempFilePath,
                    success: () => {
                        uni.showToast({
                            title: '图片已保存'
                        })
                    }
                })
            }
        })
    }


    uni.getSystemInfo({
        success: res => {
            draw_logo_head(res.windowWidth)
            draw_title(res.windowWidth)
            draw_author(res.windowWidth)
            draw_text(res.windowWidth)
            uni.canvasToTempFilePath({
                canvasId: 'qrcode',
                success: function (r) {
                    ctx.drawImage(r.tempFilePath, parseInt(x + res.windowWidth / 2 - 100), y, 200, 200);
                    ctx.save();
                    ctx.draw(true);
                    y = y + 200
                    attrs.qr_finish = true
                }
            })
            ctx.save();
            ctx.draw(false);
            setTimeout(() => {
                canvas_to_temp(res.windowWidth, y)
            }, 1500)
        }
    })


}
</script>

<style scoped lang='scss'>
.article {
    padding: 20rpx;

    &-title {
        font-size: 30rpx;
        font-weight: 700;
        width: 100%;
        line-height: 2rem;
        text-align: center;
    }

    &-detail {
        .article-user_name {
            margin-bottom: 20px;
            margin-top: 10px;
            font-size: 30rpx;
            font-weight: 200;
        }
    }

    &-body {
        line-height: 2rem;
    }

    .article-comment {
        margin-top: 30px;
        margin-bottom: 30px;
    }
}




.read-source {}

.comment {
    padding: 20rpx;
}

.poster {
    position: fixed;
    top: -9999999;
    left: -9999999;
    z-index: -100;
    width: 100%;
    height: 25600rpx;
}

.qrcode {
    width: 100%;
    height: 400rpx;
    width: 400rpx;
    position: fixed;
    top: -9999999;
    left: -9999999;
    z-index: -100;
}

.comment {
    .comment-body {
        padding: 20rpx;
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    z-index: 10073;

    .comment-input {
        flex: 11;
    }

    .comment-btn {
        flex: 2;
    }

    .comment_reply {
        font-size: 33rpx;
        padding: 20rpx;
    }
}

.buttons {
    position: fixed;
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

.follow-btn {
    width: 60rpx;

    .u-btn {
        width: 60rpx !important;
    }
}
</style>
