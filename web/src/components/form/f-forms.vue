<!-- 
attrs.columns = [
    { type: 'text', label: '名称', prop: 'name', size: 'small', align: "left", show: true },
    { type: 'select', width: 180, label: '角色', prop: 'role', size: 'small', align: "center", show: true },
    { type: 'jimage', width: 150, label: '图片', prop: 'user_image', size: 'small', align: "center", show: true, option: { false: '否', true: '是' } },
    { type: 'jfile', width: 160, label: '文件', prop: 'file', size: 'small', align: "center", show: true },
])
 -->
<script setup>
//TODO:动态列
const props = defineProps(['modelValue']); // defineProps的参数, 可以直接使用
const emits = defineEmits(['update:modelValue']); // emits 触发父组件函数


</script>
<template>
    <el-form :model="attrs.add_form" label-width="120px">
        <template v-for="i in modelValue">
            <!-- 普通文本 -->
            <el-form-item label="名称">
                <el-input v-if="i.type == 'text' && i.show" v-model="attrs.add_form.name" />

            </el-form-item>
            <el-table-column v-if="i.type == 'text' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
                :width="i.width">
            </el-table-column>
            <!-- 单选用标签 -->
            <el-table-column v-else-if="i.type == 'select' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
                :width="i.width">
                <template #default="scope">
                    <el-tag effect="dark">
                        {{ i.option[scope.row[i.prop]] }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column v-else-if="i.type == 'list' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
                :width="i.width">
                <template #default="scope">
                    <el-tag effect="dark" v-for="v in scope.row[i.prop]">
                        {{ i.option[v].name }}
                    </el-tag>
                </template>
            </el-table-column>
            <!-- 文件 -->
            <el-table-column v-else-if="i.type == 'jfile' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
                :width="i.width">
                <template #default="scope">
                    <div class="form-files">
                        <div v-for="i in scope.row[i.prop]">
                            <a :href="i.url" target="_blank">
                                {{ i.name }}
                            </a>
                        </div>
                    </div>
                </template>
            </el-table-column>
            <!-- 图片 -->
            <el-table-column v-else-if="i.type == 'jimage' && i.show" :align="i.align" :label="i.label" :prop="i.prop"
                :width="i.width">
                <template #default="scope">
                    <el-image v-if="scope.row[i.prop][0]" style="width: 70px; height: 70px" fit="cover" :z-index="30"
                        :src="scope.row[i.prop][0]?.url"
                        :preview-src-list="scope.row[i.prop].reduce((pre, cur) => { pre.push(cur.url); return pre; }, [])"
                        preview-teleported hide-on-click-modal />
                    <div v-else></div>
                </template>
            </el-table-column>
        </template>
        <!-- <el-form-item label="名称">
            <el-input v-model="attrs.add_form.name" />
        </el-form-item>
        <el-form-item label="地址" prop="area">
            <el-cascader v-model="attrs.add_form.area" :options="attrs.areas_tree"
                :props="{ emitPath: false, value: 'code', label: 'name' }" />
        </el-form-item>
        <el-form-item label="文件" prop="file">
            <f-jfile v-model="attrs.add_form.file" :limit="10" :size="3" />
        </el-form-item>
        <el-form-item label="图片" prop="image">
            <f-jimage v-model="attrs.add_form.image" :limit="10" :size="3" />
        </el-form-item> -->
    </el-form>
</template>
<style scoped lang='scss'></style>
