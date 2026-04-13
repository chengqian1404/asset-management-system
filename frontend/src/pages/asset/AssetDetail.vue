<template>
  <div class="page-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>资产详情</span>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>
      <el-descriptions :column="2" border v-if="asset">
        <el-descriptions-item label="资产编号">{{ asset.asset_number }}</el-descriptions-item>
        <el-descriptions-item label="资产名称">{{ asset.name }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="ASSET_STATUS_MAP[asset.status]?.type">
            {{ ASSET_STATUS_MAP[asset.status]?.label }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="存放位置">{{ asset.location || '-' }}</el-descriptions-item>
        <el-descriptions-item label="购置日期">{{ asset.purchase_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="购置金额">{{ formatMoney(asset.purchase_price) }}</el-descriptions-item>
        <el-descriptions-item label="供应商">{{ asset.supplier || '-' }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ asset.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDateTime(asset.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ formatDateTime(asset.updated_at) }}</el-descriptions-item>
      </el-descriptions>

      <div v-if="asset?.qr_code" style="margin-top: 20px">
        <h4 style="margin-bottom: 10px">资产二维码</h4>
        <img :src="asset.qr_code" alt="二维码" style="width: 150px; height: 150px" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { assetApi } from '../../api/asset'
import { ASSET_STATUS_MAP, formatMoney, formatDateTime } from '../../utils/format'

const route = useRoute()
const asset = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    asset.value = await assetApi.get(route.params.id)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
