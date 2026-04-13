// 资产API
import request from './request'

export const assetApi = {
  // 获取列表
  list: (params) => request.get('/api/assets', { params }),

  // 获取详情
  get: (id) => request.get(`/api/assets/${id}`),

  // 新增
  create: (data) => request.post('/api/assets', data),

  // 修改
  update: (id, data) => request.put(`/api/assets/${id}`, data),

  // 删除
  delete: (id) => request.delete(`/api/assets/${id}`),

  // 获取统计
  stats: () => request.get('/api/assets/stats'),

  // 批量导入
  import: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/api/assets/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
