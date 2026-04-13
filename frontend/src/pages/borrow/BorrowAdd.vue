<template>
  <div class="page-container">
    <el-card header="申请借用">
      <BorrowForm
        :assets="availableAssets"
        @success="$router.push('/borrows')"
        @cancel="$router.back()"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { assetApi } from '../../api/asset'
import BorrowForm from '../../components/business/BorrowForm.vue'

const availableAssets = ref([])

onMounted(async () => {
  const data = await assetApi.list({ status: 'idle', page_size: 100 })
  availableAssets.value = data.data || []
})
</script>
