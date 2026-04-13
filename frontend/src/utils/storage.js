// 本地存储工具
import { CONFIG } from '../config'

export const storage = {
  // 获取Token
  getToken() {
    return localStorage.getItem(CONFIG.TOKEN_KEY)
  },

  // 设置Token
  setToken(token) {
    localStorage.setItem(CONFIG.TOKEN_KEY, token)
  },

  // 获取刷新Token
  getRefreshToken() {
    return localStorage.getItem(CONFIG.REFRESH_TOKEN_KEY)
  },

  // 设置刷新Token
  setRefreshToken(token) {
    localStorage.setItem(CONFIG.REFRESH_TOKEN_KEY, token)
  },

  // 获取用户信息
  getUserInfo() {
    const info = localStorage.getItem(CONFIG.USER_INFO_KEY)
    return info ? JSON.parse(info) : null
  },

  // 设置用户信息
  setUserInfo(info) {
    localStorage.setItem(CONFIG.USER_INFO_KEY, JSON.stringify(info))
  },

  // 清除所有认证信息
  clear() {
    localStorage.removeItem(CONFIG.TOKEN_KEY)
    localStorage.removeItem(CONFIG.REFRESH_TOKEN_KEY)
    localStorage.removeItem(CONFIG.USER_INFO_KEY)
  },
}
