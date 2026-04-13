// 分类API
import request from './request'

export const categoryApi = {
  list: () => request.get('/api/categories'),
  create: (data) => request.post('/api/categories', data),
  update: (id, data) => request.put(`/api/categories/${id}`, data),
  delete: (id) => request.delete(`/api/categories/${id}`),
}
