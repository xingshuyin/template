<template>
    <div ref="chartRef" class="my-chart"></div>
</template>
<script setup lang="ts">
import { defineProps, onBeforeUnmount, onMounted, ref } from "vue";
import { ResizeObserver } from '@juggle/resize-observer';   // npm i @juggle/resize-observer  //TODO:监听元素大小变化
import echarts from "../../hooks/echarts"; //TODO:echarts原始组件
const props = defineProps(["option"]);
const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
const ro = new ResizeObserver((entries, observer) => {
    chart?.resize()
});
ro.observe(document.body);
onMounted(() => {
    setTimeout(() => {
        initChart();
    }, 20);
});

const initChart = () => {
    chart = echarts.init(chartRef.value as HTMLDivElement);
    chart.setOption({
        ...props.option,
    });
};

onBeforeUnmount(() => {
    chart?.dispose();
});
</script>

<style lang="scss" scoped>

</style>

