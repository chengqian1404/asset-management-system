// 应用配置
export const CONFIG = {
  // API基础URL
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  // 应用标题
  APP_TITLE: import.meta.env.VITE_APP_TITLE || '资产管理系统',
  // 分页默认配置
  DEFAULT_PAGE_SIZE: 20,
  // Token存储Key
  TOKEN_KEY: 'access_token',
  REFRESH_TOKEN_KEY: 'refresh_token',
  USER_INFO_KEY: 'user_info',
}
