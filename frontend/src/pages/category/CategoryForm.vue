<template>
  <div class="page-container">
    <el-card :header="isEdit ? '编辑分类' : '新增分类'">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" style="max-width: 500px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" placeholder="分类描述" />
        </el-form-item>
        <el-form-item label="图标">
          <el-input v-model="form.icon" placeholder="图标名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">保存</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { categoryApi } from '../../api/category'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const formRef = ref()
const loading = ref(false)

const form = reactive({ name: '', description: '', icon: '' })
const rules = { name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }] }

async function handleSubmit() {
  await formRef.value.validate()
  loading.value = true
  try {
    if (isEdit.value) {
      await categoryApi.update(route.params.id, form)
      ElMessage.success('更新成功')
    } else {
      await categoryApi.create(form)
      ElMessage.success('创建成功')
    }
    router.push('/categories')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (isEdit.value) {
    // 编辑模式：从分类列表中找到对应项并填充表单
    const list = await categoryApi.list()
    const item = list.find((c) => String(c.id) === String(route.params.id))
    if (item) Object.assign(form, item)
  }
})
</script>
