<template>
  <div class="page-container">
    <el-card>
      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchParams.keyword"
          placeholder="搜索资产编号/名称"
          clearable
          style="width: 240px"
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        />
        <el-select v-model="searchParams.status" placeholder="状态筛选" clearable style="width: 140px">
          <el-option v-for="(v, k) in ASSET_STATUS_MAP" :key="k" :label="v.label" :value="k" />
        </el-select>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
        <div style="flex: 1" />
        <el-button type="primary" @click="$router.push('/assets/add')" v-if="isAdmin">
          <el-icon><Plus /></el-icon> 新增资产
        </el-button>
      </div>

      <!-- 表格 -->
      <AssetTable
        :assets="assets"
        :loading="loading"
        @view="handleView"
        @edit="handleEdit"
        @delete="handleDelete"
      />

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="searchParams.page"
          v-model:page-size="searchParams.page_size"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @change="fetchData"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { assetApi } from '../../api/asset'
import { useUserStore } from '../../stores/user'
import { ASSET_STATUS_MAP } from '../../utils/format'
import AssetTable from '../../components/business/AssetTable.vue'

const router = useRouter()
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const assets = ref([])
const total = ref(0)
const loading = ref(false)

const searchParams = reactive({
  page: 1,
  page_size: 20,
  keyword: '',
  status: '',
})

async function fetchData() {
  loading.value = true
  try {
    const data = await assetApi.list(searchParams)
    assets.value = data.data || []
    total.value = data.total || 0
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  searchParams.page = 1
  fetchData()
}

function handleReset() {
  searchParams.keyword = ''
  searchParams.status = ''
  handleSearch()
}

function handleView(row) {
  router.push(`/assets/${row.id}`)
}

function handleEdit(row) {
  router.push(`/assets/${row.id}/edit`)
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确认删除资产"${row.name}"？`, '警告', { type: 'warning' })
  await assetApi.delete(row.id)
  ElMessage.success('删除成功')
  fetchData()
}

onMounted(fetchData)
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.pagination {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
