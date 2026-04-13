// 权限检查工具
import { useUserStore } from '../stores/user'

// 检查是否是管理员
export function isAdmin() {
  const userStore = useUserStore()
  return userStore.userInfo?.role === 'admin'
}

// 检查是否是管理员或主管
export function isManagerOrAdmin() {
  const userStore = useUserStore()
  return ['admin', 'manager'].includes(userStore.userInfo?.role)
}

// 检查是否登录
export function isLoggedIn() {
  const userStore = useUserStore()
  return !!userStore.token
}
