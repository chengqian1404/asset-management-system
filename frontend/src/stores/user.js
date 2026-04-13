// 用户状态管理
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { storage } from '../utils/storage'
import { authApi } from '../api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(storage.getToken())
  const userInfo = ref(storage.getUserInfo())

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const isManagerOrAdmin = computed(() =>
    ['admin', 'manager'].includes(userInfo.value?.role)
  )

  // 登录
  async function login(username, password) {
    const data = await authApi.login({ username, password })
    token.value = data.access_token
    storage.setToken(data.access_token)
    storage.setRefreshToken(data.refresh_token)

    // 获取用户信息
    const info = await authApi.getMe()
    userInfo.value = info
    storage.setUserInfo(info)

    return data
  }

  // 登出
  function logout() {
    token.value = null
    userInfo.value = null
    storage.clear()
  }

  // 刷新用户信息
  async function refreshUserInfo() {
    const info = await authApi.getMe()
    userInfo.value = info
    storage.setUserInfo(info)
  }

  return { token, userInfo, isLoggedIn, isAdmin, isManagerOrAdmin, login, logout, refreshUserInfo }
})
