<template>
    <div class="index">
        <div class="article-list">
            <articleL :data="attrs.data" username="user__name" icon="user__icon"></articleL>
        </div>
        <el-button icon="Plus" circle @click="attrs.adding = true; attrs.submit_type = 'add'"
            style="position: fixed; right: 20px;bottom: 20px;" />
        <el-dialog v-model="attrs.adding" class="add_form" :title="attrs.submit_type == 'add' ? '新增' : '编辑'" width="80%"
            :modal="false" fullscreen append-to-body>
            <el-form :model="attrs.add_form" label-width="80px" :rules="rules" ref="form_dom" label-position="left"
                require-asterisk-position="right">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="attrs.add_form.name" />
                </el-form-item>
                <el-form-item label="类型" prop="type">
                    <el-select v-model="attrs.add_form.type" filterable default-first-option :reserve-keyword="false"
                        placeholder="类型">
                        <el-option v-for="value, key in article_type" :key="key" :label="value" :value="key" />
                    </el-select>
                </el-form-item>
                <el-form-item label="标签" prop="tag">
                    <el-select v-model="attrs.add_form.tag" multiple filterable allow-create default-first-option
                        :reserve-keyword="false" placeholder="添加标签">
                    </el-select>
                </el-form-item>
                <el-row :gutter="30">
                    <el-col :span="2">
                        <el-form-item label="是否删除" prop="is_delete">
                            <el-switch v-model="attrs.add_form.is_delete" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="2">
                        <el-form-item label="是否置顶" prop="is_top">
                            <el-switch v-model="attrs.add_form.is_top" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="2">
                        <el-form-item label="是否热门" prop="is_hot">
                            <el-switch v-model="attrs.add_form.is_hot" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="2">
                        <el-form-item label="是否原创" prop="is_original">
                            <el-switch v-model="attrs.add_form.is_original" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="2">
                        <el-form-item label="是否推荐" prop="is_recommend">
                            <el-switch v-model="attrs.add_form.is_recommend" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="36">
                    <el-col :span="4">
                        <el-form-item label="文件" prop="file">
                            <f-jfile v-model="attrs.add_form.file" :limit="10" :size="3" accept="" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="4">
                        <el-form-item label="图片" prop="image">
                            <f-jimage v-model="attrs.add_form.image" :limit="10" :size="3" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="4">
                        <el-form-item label="视频" prop="video">
                            <f-jvideo v-model="attrs.add_form.video" :limit="10" :size="30" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="4"></el-col>
                    <el-col :span="4"></el-col>
                    <el-col :span="4"></el-col>
                </el-row>
                <el-form-item label="链接" prop="link">
                    <el-input v-model="attrs.add_form.link" />
                </el-form-item>
                <el-form-item label="" prop="content">
                    <v-md-editor v-model="attrs.add_form.content" height="550px" :disabled-menus="[]"
                        @upload-image="upload_image"></v-md-editor>
                </el-form-item>

            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="attrs.adding = false">取消</el-button>
                    <el-button type="primary" @click="validate">
                        提交
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>
<script setup>
//const props = defineProps(['modelValue']); // defineProps的参数, 可以直接使用

import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import articleL from '../../components/list/articleL.vue';
import rest from '../../utils/rest';
import { article_type } from '../../utils/data';
import { submit_ } from '../../hooks/table_common';
import store from '../../store';
const router = useRouter()
const attrs = reactive({
    filter: {
        page: 1,
        limit: 100,
        sort: '-create_time',
        'extra[]': ['user__name', 'user__icon'],
    },
    adding: false,
    add_form: {},
})
onMounted(() => {
    get_data()
})

const get_data = () => {
    rest.list('article', { ...attrs.filter }, attrs, 'data', null)
}

const form_dom = ref()
const rules = reactive({  //https://element-plus.gitee.io/zh-CN/component/form.html#%E8%87%AA%E5%AE%9A%E4%B9%89%E6%A0%A1%E9%AA%8C%E8%A7%84%E5%88%99
    name: [
        { required: true, message: '请填写名称', trigger: 'blur' },
    ],
    content: [
        { required: true, message: '请填写内容', trigger: 'blur' },
    ],
})
const validate = () => {
    console.log('啊水水水水水水');
    form_dom.value.validate((valid, fields) => {
        if (valid) {
            store().get_userinfo().then((info) => {
                console.log('info----------------', info);
                submit_('article', { user: info.id, ...attrs.add_form }, attrs.submit_type, submit_success);
            })
        } else {
            console.log(fields);
        }
    })
}
const submit_success = (res) => {
    console.log(res);

    if (res.status < 400) {
        attrs.adding = false
        if (attrs.submit_type == 'add') {
            attrs.data.shift(res.data)
            attrs.add_form = {};
        }
        get_data()
    }
}

const upload_image = (event, insertImage, files) => {
    console.log(files)
    r().post('/data/upload/', { file: files[0] }, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then((res) => {
        insertImage({
            url:
                window.location.protocol + "//" + window.location.host + '/' + res.data.url,
            desc: res.data.name,
            id: res.data.id,
            // width: 'auto',
            // height: 'auto',
        });
    })
}
</script>
<style scoped lang='scss'>
.index {

    width: 100%;
    margin: auto;
    height: 100%;
    overflow: auto;

    .article-list {
        width: 640px;
        margin: auto;
    }
}
</style>
