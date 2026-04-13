<template>
  <el-table :data="assets" v-loading="loading" stripe>
    <el-table-column prop="asset_number" label="资产编号" width="140" />
    <el-table-column prop="name" label="资产名称" min-width="160" />
    <el-table-column label="状态" width="100">
      <template #default="{ row }">
        <el-tag :type="ASSET_STATUS_MAP[row.status]?.type || 'info'" size="small">
          {{ ASSET_STATUS_MAP[row.status]?.label || row.status }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="location" label="位置" width="150" />
    <el-table-column label="购置金额" width="120">
      <template #default="{ row }">
        {{ formatMoney(row.purchase_price) }}
      </template>
    </el-table-column>
    <el-table-column label="操作" width="180" fixed="right">
      <template #default="{ row }">
        <el-button size="small" @click="$emit('view', row)">查看</el-button>
        <el-button size="small" type="primary" @click="$emit('edit', row)">编辑</el-button>
        <el-button size="small" type="danger" @click="$emit('delete', row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import { ASSET_STATUS_MAP, formatMoney } from '../../utils/format'

defineProps({
  assets: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

defineEmits(['view', 'edit', 'delete'])
</script>
