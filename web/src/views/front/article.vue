<template>
    <div class="article">
        <v-md-preview v-if="attrs.item" :text="attrs.item.content">

        </v-md-preview>
    </div>
</template>
<script setup>
import { useRoute, useRouter } from 'vue-router';
import rest from '../../utils/rest';
const router = useRouter()
const route = useRoute()
//const emits = defineEmits(['update:modelValue']); // emits 触发父组件函数
const attrs = reactive({})
rest.item('article', route.params.id, attrs)
</script>
<style scoped lang='scss'>
.article {
    background-color: aliceblue;
    width: 100%;
    height: 100%;
    overflow: auto;
}
</style>
