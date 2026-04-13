<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <StatCard label="资产总数" :value="stats?.total || 0" icon="Box" color="#409EFF" />
      </el-col>
      <el-col :span="6">
        <StatCard label="在用资产" :value="stats?.in_use || 0" icon="Monitor" color="#67C23A" />
      </el-col>
      <el-col :span="6">
        <StatCard label="待审批借用" :value="pendingBorrows" icon="Document" color="#E6A23C" />
      </el-col>
      <el-col :span="6">
        <StatCard label="维修中" :value="stats?.maintenance || 0" icon="Tools" color="#F56C6C" />
      </el-col>
    </el-row>

    <el-row :gutter="20" class="content-row">
      <el-col :span="12">
        <el-card header="资产状态分布">
          <div v-if="stats" class="chart-area">
            <el-progress
              v-for="(item, key) in statusItems"
              :key="key"
              :percentage="getPercentage(item.value)"
              :color="item.color"
              :format="() => `${item.label}: ${item.value}`"
              style="margin-bottom: 12px"
            />
          </div>
          <el-empty v-else description="暂无数据" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="最近操作">
          <el-timeline>
            <el-timeline-item
              v-for="log in recentLogs"
              :key="log.id"
              :timestamp="log.created_at"
              placement="top"
            >
              <p>{{ log.action }} - {{ log.table_name }}</p>
            </el-timeline-item>
            <el-timeline-item v-if="!recentLogs.length">
              <p style="color: #909399">暂无操作记录</p>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="24">
        <el-card header="快速操作">
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/assets/add')">
              <el-icon><Plus /></el-icon> 新增资产
            </el-button>
            <el-button type="success" @click="$router.push('/borrows/add')">
              <el-icon><Document /></el-icon> 申请借用
            </el-button>
            <el-button @click="$router.push('/assets')">
              <el-icon><Box /></el-icon> 查看资产
            </el-button>
            <el-button @click="$router.push('/borrows')">
              <el-icon><List /></el-icon> 借用记录
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { assetApi } from '../../api/asset'
import { borrowApi } from '../../api/borrow'
import StatCard from '../../components/business/StatCard.vue'

const stats = ref(null)
const pendingBorrows = ref(0)
const recentLogs = ref([])

const statusItems = computed(() => {
  if (!stats.value) return {}
  return {
    in_use: { label: '在用', value: stats.value.in_use || 0, color: '#67C23A' },
    idle: { label: '闲置', value: stats.value.idle || 0, color: '#909399' },
    maintenance: { label: '维修中', value: stats.value.maintenance || 0, color: '#E6A23C' },
    borrowed: { label: '借出中', value: stats.value.borrowed || 0, color: '#409EFF' },
    scrapped: { label: '已报废', value: stats.value.scrapped || 0, color: '#F56C6C' },
  }
})

function getPercentage(value) {
  if (!stats.value?.total) return 0
  return Math.round((value / stats.value.total) * 100)
}

onMounted(async () => {
  try {
    stats.value = await assetApi.stats()
    const borrowData = await borrowApi.list({ status: 'pending', page_size: 100 })
    pendingBorrows.value = borrowData.total || 0
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.stats-row { margin-bottom: 20px; }
.content-row { margin-bottom: 20px; }
.chart-area { padding: 8px 0; }
.quick-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
</style>
