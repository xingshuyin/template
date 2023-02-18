<!-- 
modelValue = ref([
    { type: 'text', label: '名称', prop: 'name', size: 'small', align: "left", show: true },
    { type: 'select', width: 180, label: '角色', prop: 'role', size: 'small', align: "center", show: true },
    { type: 'jimage', width: 150, label: '图片', prop: 'user_image', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
    { type: 'jfile', width: 160, label: '文件', prop: 'file', size: 'small', align: "center", show: true },
])
 -->
<script setup>
//TODO:列编辑
import { watch } from 'vue';
import draggable from 'vuedraggable'
const props = defineProps(['modelValue', 'base_url']); // defineProps的参数, 可以直接使用
const emits = defineEmits(['update:modelValue']); // emits 触发父组件函数
const attrs = reactive({
    drag: false,
    columns: [],
    show: false,
})
const columns = []
onBeforeMount(() => {
    let temp = []
    for (const key in props.modelValue) {
        temp.push({ prop: key, ...props.modelValue[key] })
        columns.push({ prop: key, ...props.modelValue[key] })

    }
    if (localStorage.getItem(`columns_${props.base_url}`)) {
        attrs.columns = JSON.parse(localStorage.getItem(`columns_${props.base_url}`))
    } else {
        attrs.columns = temp
    }
})

watch(() => { return attrs.columns }, () => {
    localStorage.setItem(`columns_${props.base_url}`, JSON.stringify(attrs.columns))
    let r = {}
    for (let index = 0; index < attrs.columns.length; index++) {
        r[attrs.columns[index].prop] = attrs.columns[index]
    }
    console.log('watch', r, attrs.columns)
    emits('update:modelValue', r)
}, { deep: true })
const reset_column = () => {
    console.log('reset_column -> columns', columns)
    let temp = []
    for (let index = 0; index < columns.length; index++) {
        temp.push(columns[index])
    }
    attrs.columns = temp
}
</script>
<template>
    <el-button icon="Sort" circle @click="attrs.show = true;" />
    <!-- 编辑列 -->
    <el-drawer v-model="attrs.show" size="680px" center append-to-body :modal="true" :show-close="false">
        <template v-slot:header>
            <span style="font-size: 16px;">
                编辑列(拖动以修改顺序)
            </span>
            <el-tooltip content="重置" placement="bottom" effect="light">
                <el-button icon="Refresh" size="small" style="width: 20px;position: absolute;right: 17px;" circle
                    @click="reset_column" />
            </el-tooltip>

        </template>
        <draggable v-model="attrs.columns" @start="attrs.drag = true" @end="attrs.drag = false;" item-key="label">
            <template #item="{ element, index }">
                <div class="column-manager-line">
                    <table>
                        <tr>
                            <td>{{ index + 1 }}</td>
                            <td style="width: 30px;"><el-switch v-model="element.show" inline-prompt /></td>
                            <td style="width: 150px;">
                                <el-input v-model="element.label" placeholder="列名" />
                            </td>
                            <td style="width: 20px;"><el-input-number v-model="element.width" :min="1" :max="500"
                                    controls-position="right" />
                            </td>
                            <td style="width: 120px;">
                                <el-radio-group v-model="element.align" size="small">
                                    <el-radio-button key="left" label="left">左</el-radio-button>
                                    <el-radio-button key="center" label="center">中</el-radio-button>
                                    <el-radio-button key="right" label="right">右</el-radio-button>
                                </el-radio-group>
                            </td>
                        </tr>
                    </table>
                </div>
            </template>
        </draggable>
    </el-drawer>
</template>
<style scoped lang='scss'>
.column-manager-line {
    background-color: #f7f2f2;
    border-radius: 10px;
    margin-bottom: 3px;

    table {
        tr {
            td {
                width: 70px;
                padding: 3px;
                text-align: center;
            }
        }
    }
}
</style>
