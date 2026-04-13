<template>
  <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
    <el-form-item label="借用资产" prop="asset_id">
      <el-select v-model="form.asset_id" placeholder="请选择资产" style="width: 100%">
        <el-option
          v-for="asset in assets"
          :key="asset.id"
          :label="`${asset.asset_number} - ${asset.name}`"
          :value="asset.id"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="借用原因" prop="reason">
      <el-input v-model="form.reason" type="textarea" :rows="3" placeholder="请说明借用原因" />
    </el-form-item>
    <el-form-item label="预计归还" prop="expected_return_date">
      <el-date-picker
        v-model="form.expected_return_date"
        type="date"
        placeholder="选择日期"
        value-format="YYYY-MM-DD"
        style="width: 100%"
      />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="handleSubmit" :loading="loading">提交申请</el-button>
      <el-button @click="$emit('cancel')">取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { borrowApi } from '../../api/borrow'

defineProps({
  assets: { type: Array, default: () => [] },
})

const emit = defineEmits(['success', 'cancel'])

const formRef = ref()
const loading = ref(false)
const form = reactive({
  asset_id: null,
  reason: '',
  expected_return_date: null,
})

const rules = {
  asset_id: [{ required: true, message: '请选择借用资产', trigger: 'change' }],
  reason: [{ required: true, message: '请填写借用原因', trigger: 'blur' }],
}

async function handleSubmit() {
  await formRef.value.validate()
  loading.value = true
  try {
    await borrowApi.create(form)
    ElMessage.success('借用申请已提交')
    emit('success')
  } finally {
    loading.value = false
  }
}
</script>
