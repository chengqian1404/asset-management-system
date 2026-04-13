<template>
  <div class="page-container">
    <el-card header="新增资产">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" style="max-width: 600px">
        <el-form-item label="资产编号" prop="asset_number">
          <el-input v-model="form.asset_number" placeholder="如: IT-2024-001" />
        </el-form-item>
        <el-form-item label="资产名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入资产名称" />
        </el-form-item>
        <el-form-item label="资产分类">
          <el-select v-model="form.category_id" placeholder="请选择分类" clearable style="width: 100%">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="资产状态">
          <el-select v-model="form.status" style="width: 100%">
            <el-option v-for="(v, k) in ASSET_STATUS_MAP" :key="k" :label="v.label" :value="k" />
          </el-select>
        </el-form-item>
        <el-form-item label="存放位置">
          <el-input v-model="form.location" placeholder="请输入存放位置" />
        </el-form-item>
        <el-form-item label="购置日期">
          <el-date-picker v-model="form.purchase_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="购置金额">
          <el-input-number v-model="form.purchase_price" :precision="2" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="供应商">
          <el-input v-model="form.supplier" placeholder="请输入供应商名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="资产描述" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">提交</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { assetApi } from '../../api/asset'
import { categoryApi } from '../../api/category'
import { ASSET_STATUS_MAP } from '../../utils/format'

const router = useRouter()
const formRef = ref()
const loading = ref(false)
const categories = ref([])

const form = reactive({
  asset_number: '',
  name: '',
  category_id: null,
  status: 'idle',
  location: '',
  purchase_date: null,
  purchase_price: null,
  supplier: '',
  description: '',
})

const rules = {
  asset_number: [{ required: true, message: '请输入资产编号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入资产名称', trigger: 'blur' }],
}

async function handleSubmit() {
  await formRef.value.validate()
  loading.value = true
  try {
    await assetApi.create(form)
    ElMessage.success('资产创建成功')
    router.push('/assets')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  categories.value = await categoryApi.list()
})
</script>
