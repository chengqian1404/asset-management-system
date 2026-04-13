<template>
  <div class="page-container">
    <el-card header="待审批借用申请">
      <el-table :data="pendingBorrows" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="reason" label="借用原因" />
        <el-table-column prop="expected_return_date" label="预计归还" width="120" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" type="success" @click="handleApprove(row, true)">批准</el-button>
            <el-button size="small" type="danger" @click="handleApprove(row, false)">拒绝</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { borrowApi } from '../../api/borrow'

const pendingBorrows = ref([])
const loading = ref(false)

async function fetchData() {
  loading.value = true
  try {
    const data = await borrowApi.list({ status: 'pending' })
    pendingBorrows.value = data.data || []
  } finally {
    loading.value = false
  }
}

async function handleApprove(row, approve) {
  await borrowApi.approve(row.id, { approve })
  ElMessage.success(approve ? '已批准' : '已拒绝')
  fetchData()
}

onMounted(fetchData)
</script>
