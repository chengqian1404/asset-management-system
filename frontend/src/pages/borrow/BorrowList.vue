<template>
  <div class="page-container">
    <el-card>
      <div class="search-bar">
        <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 140px" @change="fetchData">
          <el-option v-for="(v, k) in BORROW_STATUS_MAP" :key="k" :label="v.label" :value="k" />
        </el-select>
        <el-button type="primary" @click="$router.push('/borrows/add')">
          <el-icon><Plus /></el-icon> 申请借用
        </el-button>
      </div>

      <el-table :data="borrows" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="BORROW_STATUS_MAP[row.status]?.type" size="small">
              {{ BORROW_STATUS_MAP[row.status]?.label || row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="借用原因" min-width="150" />
        <el-table-column prop="expected_return_date" label="预计归还" width="120" />
        <el-table-column prop="actual_return_date" label="实际归还" width="120" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending' && isManagerOrAdmin"
              size="small"
              type="success"
              @click="handleApprove(row, true)"
            >批准</el-button>
            <el-button
              v-if="row.status === 'pending' && isManagerOrAdmin"
              size="small"
              type="danger"
              @click="handleApprove(row, false)"
            >拒绝</el-button>
            <el-button
              v-if="row.status === 'approved'"
              size="small"
              type="warning"
              @click="handleReturn(row)"
            >归还</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="page"
          :total="total"
          :page-size="20"
          layout="total, prev, pager, next"
          @current-change="fetchData"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { borrowApi } from '../../api/borrow'
import { useUserStore } from '../../stores/user'
import { BORROW_STATUS_MAP } from '../../utils/format'

const userStore = useUserStore()
const isManagerOrAdmin = computed(() => userStore.isManagerOrAdmin)

const borrows = ref([])
const total = ref(0)
const loading = ref(false)
const page = ref(1)
const filterStatus = ref('')

async function fetchData() {
  loading.value = true
  try {
    const data = await borrowApi.list({
      page: page.value,
      page_size: 20,
      status: filterStatus.value || undefined,
    })
    borrows.value = data.data || []
    total.value = data.total || 0
  } finally {
    loading.value = false
  }
}

async function handleApprove(row, approve) {
  await ElMessageBox.confirm(`确认${approve ? '批准' : '拒绝'}此借用申请？`, '提示', { type: 'warning' })
  await borrowApi.approve(row.id, { approve })
  ElMessage.success(approve ? '已批准' : '已拒绝')
  fetchData()
}

async function handleReturn(row) {
  await ElMessageBox.confirm('确认归还此资产？', '提示', { type: 'warning' })
  await borrowApi.return(row.id)
  ElMessage.success('归还成功')
  fetchData()
}

onMounted(fetchData)
</script>

<style scoped>
.search-bar { display: flex; gap: 10px; margin-bottom: 16px; }
.pagination { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
