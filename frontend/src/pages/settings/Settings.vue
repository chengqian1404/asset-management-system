<template>
  <div class="page-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card header="基本设置">
          <el-form label-width="120px">
            <el-form-item label="系统名称">
              <el-input v-model="settings.app_name" />
            </el-form-item>
            <el-form-item label="系统版本">
              <el-input v-model="settings.version" disabled />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSave">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card header="操作日志">
          <el-table :data="logs" v-loading="loading" size="small" max-height="400">
            <el-table-column prop="action" label="操作" />
            <el-table-column prop="table_name" label="对象" width="100" />
            <el-table-column prop="created_at" label="时间" width="160" />
          </el-table>
          <el-pagination
            v-model:current-page="logPage"
            :total="logTotal"
            :page-size="10"
            layout="total, prev, pager, next"
            @current-change="fetchLogs"
            style="margin-top: 12px"
          />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../api/request'

const settings = reactive({ app_name: '资产管理系统', version: '1.0.0' })
const logs = ref([])
const loading = ref(false)
const logPage = ref(1)
const logTotal = ref(0)

async function fetchLogs() {
  loading.value = true
  try {
    const data = await request.get('/api/system/logs', { params: { page: logPage.value } })
    logs.value = data.data || []
    logTotal.value = data.total || 0
  } finally {
    loading.value = false
  }
}

function handleSave() {
  ElMessage.success('设置已保存')
}

onMounted(() => {
  fetchLogs()
})
</script>
