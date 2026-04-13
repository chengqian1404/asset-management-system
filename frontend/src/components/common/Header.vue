<template>
  <div class="header">
    <div class="header-left">
      <el-icon class="toggle-btn" @click="toggleSidebar">
        <Fold v-if="!sidebarCollapsed" />
        <Expand v-else />
      </el-icon>
      <span class="breadcrumb">{{ currentTitle }}</span>
    </div>
    <div class="header-right">
      <el-dropdown @command="handleCommand">
        <span class="user-info">
          <el-avatar :size="32" icon="UserFilled" />
          <span class="username">{{ userInfo?.full_name || userInfo?.username }}</span>
          <el-icon><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人信息</el-dropdown-item>
            <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { useSystemStore } from '../../stores/system'
import { ElMessageBox, ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const systemStore = useSystemStore()

const currentTitle = computed(() => route.meta.title || '首页')
const userInfo = computed(() => userStore.userInfo)
const sidebarCollapsed = computed(() => systemStore.sidebarCollapsed)

function toggleSidebar() {
  systemStore.toggleSidebar()
}

async function handleCommand(command) {
  if (command === 'logout') {
    await ElMessageBox.confirm('确认退出登录？', '提示', { type: 'warning' })
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  }
}
</script>

<style scoped lang="scss">
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 20px;
  background: #fff;
  border-bottom: 1px solid #ebeef5;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.toggle-btn {
  font-size: 20px;
  cursor: pointer;
  color: #606266;
  &:hover { color: #409eff; }
}
.breadcrumb {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}
.header-right {
  display: flex;
  align-items: center;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 4px;
  &:hover { background: #f5f7fa; }
}
.username {
  font-size: 14px;
  color: #303133;
}
</style>
