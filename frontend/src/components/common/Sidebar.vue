<template>
  <div class="sidebar" :class="{ collapsed: collapsed }">
    <div class="logo">
      <span v-if="!collapsed" class="logo-text">📦 资产管理系统</span>
      <span v-else class="logo-icon">📦</span>
    </div>
    <el-menu
      :default-active="activeMenu"
      :collapse="collapsed"
      router
      background-color="#001529"
      text-color="#a6adb4"
      active-text-color="#ffffff"
    >
      <el-menu-item index="/dashboard">
        <el-icon><Odometer /></el-icon>
        <template #title>仪表板</template>
      </el-menu-item>

      <el-sub-menu index="assets">
        <template #title>
          <el-icon><Box /></el-icon>
          <span>资产管理</span>
        </template>
        <el-menu-item index="/assets">资产列表</el-menu-item>
        <el-menu-item index="/assets/add">新增资产</el-menu-item>
      </el-sub-menu>

      <el-menu-item index="/categories">
        <el-icon><Files /></el-icon>
        <template #title>分类管理</template>
      </el-menu-item>

      <el-sub-menu index="borrows">
        <template #title>
          <el-icon><Document /></el-icon>
          <span>借用管理</span>
        </template>
        <el-menu-item index="/borrows">借用列表</el-menu-item>
        <el-menu-item index="/borrows/add">申请借用</el-menu-item>
      </el-sub-menu>

      <el-menu-item v-if="isAdmin" index="/users">
        <el-icon><User /></el-icon>
        <template #title>用户管理</template>
      </el-menu-item>

      <el-menu-item v-if="isAdmin" index="/settings">
        <el-icon><Setting /></el-icon>
        <template #title>系统设置</template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { useSystemStore } from '../../stores/system'

const route = useRoute()
const userStore = useUserStore()
const systemStore = useSystemStore()

const collapsed = computed(() => systemStore.sidebarCollapsed)
const isAdmin = computed(() => userStore.isAdmin)
const activeMenu = computed(() => route.path)
</script>

<style scoped lang="scss">
.sidebar {
  width: 220px;
  min-height: 100vh;
  background: #001529;
  transition: width 0.3s;
  overflow: hidden;

  &.collapsed {
    width: 64px;
  }
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #002140;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  overflow: hidden;
}
.logo-text {
  white-space: nowrap;
  padding: 0 16px;
}
</style>
