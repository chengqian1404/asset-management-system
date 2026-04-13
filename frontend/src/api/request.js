// Axios封装
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { storage } from '../utils/storage'
import router from '../router'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
})

// 请求拦截器 - 添加Token
request.interceptors.request.use(
  (config) => {
    const token = storage.getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器 - 处理错误
request.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    const { response } = error
    if (response?.status === 401) {
      storage.clear()
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
    } else if (response?.status === 403) {
      ElMessage.error('权限不足')
    } else if (response?.status === 404) {
      ElMessage.error('请求的资源不存在')
    } else if (response?.status >= 500) {
      ElMessage.error('服务器错误，请稍后重试')
    } else {
      ElMessage.error(response?.data?.detail || '请求失败')
    }
    return Promise.reject(error)
  }
)

export default request
