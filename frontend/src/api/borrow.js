// 借用API
import request from './request'

export const borrowApi = {
  list: (params) => request.get('/api/borrows', { params }),
  myBorrows: (params) => request.get('/api/borrows/my', { params }),
  create: (data) => request.post('/api/borrows', data),
  approve: (id, data) => request.put(`/api/borrows/${id}/approve`, data),
  return: (id) => request.put(`/api/borrows/${id}/return`),
}
