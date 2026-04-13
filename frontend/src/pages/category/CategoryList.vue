<template>
  <div class="page-container">
    <el-card>
      <div class="toolbar">
        <el-button type="primary" @click="showDialog()" v-if="isAdmin">
          <el-icon><Plus /></el-icon> 新增分类
        </el-button>
      </div>

      <el-table :data="categories" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="分类名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="icon" label="图标" width="100" />
        <el-table-column label="操作" width="160" v-if="isAdmin">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="showDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="editItem ? '编辑分类' : '新增分类'" width="400px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" placeholder="分类描述" />
        </el-form-item>
        <el-form-item label="图标">
          <el-input v-model="form.icon" placeholder="如: el-icon-monitor" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { categoryApi } from '../../api/category'
import { useUserStore } from '../../stores/user'

const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const categories = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitLoading = ref(false)
const editItem = ref(null)
const formRef = ref()

const form = reactive({ name: '', description: '', icon: '' })
const rules = { name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }] }

async function fetchData() {
  loading.value = true
  try {
    categories.value = await categoryApi.list()
  } finally {
    loading.value = false
  }
}

function showDialog(item = null) {
  editItem.value = item
  if (item) {
    Object.assign(form, item)
  } else {
    form.name = ''
    form.description = ''
    form.icon = ''
  }
  dialogVisible.value = true
}

async function handleSubmit() {
  await formRef.value.validate()
  submitLoading.value = true
  try {
    if (editItem.value) {
      await categoryApi.update(editItem.value.id, form)
      ElMessage.success('更新成功')
    } else {
      await categoryApi.create(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } finally {
    submitLoading.value = false
  }
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确认删除分类"${row.name}"？`, '警告', { type: 'warning' })
  await categoryApi.delete(row.id)
  ElMessage.success('删除成功')
  fetchData()
}

onMounted(fetchData)
</script>

<style scoped>
.toolbar { margin-bottom: 16px; }
</style>
