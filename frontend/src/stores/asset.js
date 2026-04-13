// 资产状态管理
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { assetApi } from '../api/asset'

export const useAssetStore = defineStore('asset', () => {
  const assets = ref([])
  const total = ref(0)
  const loading = ref(false)
  const stats = ref(null)

  async function fetchAssets(params = {}) {
    loading.value = true
    try {
      const data = await assetApi.list(params)
      assets.value = data.data || []
      total.value = data.total || 0
    } finally {
      loading.value = false
    }
  }

  async function fetchStats() {
    stats.value = await assetApi.stats()
  }

  return { assets, total, loading, stats, fetchAssets, fetchStats }
})
