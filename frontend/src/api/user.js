// 用户API
import request from './request'

export const userApi = {
  list: (params) => request.get('/api/users', { params }),
  create: (data) => request.post('/api/users', data),
  update: (id, data) => request.put(`/api/users/${id}`, data),
  delete: (id) => request.delete(`/api/users/${id}`),
}
