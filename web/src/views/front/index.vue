<template>
    <div class="article">
        <div class="banner"></div>
        <div class="side">

        </div>
        <div class="list">
            <div v-if="attrs.data" class="article" v-for="i in attrs.data"
                @click="router.push({ name: 'article_detail', params: { id: i.id } })">
                <div class="article-title">
                    {{ i.name }}
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
//const props = defineProps(['modelValue']); // defineProps的参数, 可以直接使用

import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

import rest from '../../utils/rest';
const router = useRouter()
const attrs = reactive({
    page: 1,
    limit: 10
})
onMounted(() => {

    rest.list('article', { page: attrs.page, limit: attrs.limit, values: ['name', 'create_time', 'id'] }, attrs, 'data', null)
})
</script>
<style scoped lang='scss'>
.article {
    background-color: aliceblue;
    width: 100%;
    height: 100%;
    overflow: auto;

    .banner {
        width: 100%;
        height: 100%;
        background: url(../../assets/img/banner.jpg) no-repeat;
        background-position: center;
        background-size: cover;
    }

    .list {
        margin: auto;
        text-align: center;
    }
}
</style>
