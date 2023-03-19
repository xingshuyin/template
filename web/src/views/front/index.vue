<template>
    <div class="article">
        <div class="banner"></div>
        <div class="side">

        </div>
        <div class="items">
            <div v-if="attrs.data" class="item" v-for="i in attrs.data"
                @click="router.push({ name: 'article_detail', params: { id: i.id } })">
                <div class="item-title">
                    {{ i.name }}
                </div>
                <div class="item-time">
                    {{ i.create_time }}
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

    .items {
        // box-shadow: 0 0 10px 0 black;
        width: 50%;
        margin: auto;

        .item {
            background-color: rgb(241 241 241);
            box-shadow: 0 0 3px 0 black;
            padding: 15px;
            box-sizing: border-box;
            margin: 10px 0;
            border-radius: 5px;

            .item-title {
                font-size: 30px;
                // text-align: center;
            }
        }
    }

}
</style>
