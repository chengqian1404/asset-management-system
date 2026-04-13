// 认证API
import request from './request'

export const authApi = {
  // 登录
  login: (data) => request.post('/api/auth/login', data),

  // 刷新Token
  refresh: (refreshToken) => request.post('/api/auth/refresh', { refresh_token: refreshToken }),

  // 注册
  register: (data) => request.post('/api/auth/register', data),

  // 获取当前用户
  getMe: () => request.get('/api/auth/me'),
}
