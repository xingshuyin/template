<template>
    <div class="image-wall">
        <img class="image" v-for="img in data" :src="img.url" alt=""
            @click="attrs.view_show = true; attrs.view_url = img.url">
        <el-dialog v-model="attrs.view_show" fullscreen>
            <div :style="`background-image: url(${attrs.view_url});    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;width: 100vw; height: 100vh;`" @click="attrs.view_show = false">

            </div>
            <!-- <img style="width: 100vw; height: 100vh;" :src="attrs.view_url" alt="Preview Image"
                @click="attrs.view_show = false" /> -->
        </el-dialog>
    </div>
</template>
<script setup>
const props = defineProps(['data']); //子向父传数据
const attrs = reactive({
    view_url: null,
    view_show: false,
});
</script>
<style scoped lang='scss'>
.image-wall {
    display: flex;
    flex-direction: row;
    // align-items: center;
    // justify-content: space-around;
    gap: 10px;
    flex-wrap: wrap;

    .image {
        width: 150px;
        height: 150px;
    }

    background-image: url();
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;

    :deep(.el-dialog) {
        .el-dialog__body {
            padding: 0;
        }

        .el-dialog__header {
            display: none;
        }
    }
}
</style>