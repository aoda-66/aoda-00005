import axios from 'axios'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const bookAPI = {
  getAll: () => request.get('/books'),
  getById: (id) => request.get(`/books/${id}`),
  create: (data) => request.post('/books', data),
  update: (id, data) => request.put(`/books/${id}`, data),
  delete: (id) => request.delete(`/books/${id}`)
}

export const damageAPI = {
  getAll: (params = {}) => request.get('/damages', { params }),
  getById: (id) => request.get(`/damages/${id}`),
  create: (data) => request.post('/damages', data),
  update: (id, data) => request.put(`/damages/${id}`, data),
  delete: (id) => request.delete(`/damages/${id}`)
}

export const procedureAPI = {
  getAll: (params = {}) => request.get('/procedures', { params }),
  getById: (id) => request.get(`/procedures/${id}`),
  create: (data) => request.post('/procedures', data),
  update: (id, data) => request.put(`/procedures/${id}`, data),
  delete: (id) => request.delete(`/procedures/${id}`)
}

export const materialAPI = {
  getAll: () => request.get('/materials'),
  getById: (id) => request.get(`/materials/${id}`),
  create: (data) => request.post('/materials', data),
  update: (id, data) => request.put(`/materials/${id}`, data),
  delete: (id) => request.delete(`/materials/${id}`),
  getLowStock: () => request.get('/materials/low_stock')
}

export const materialUsageAPI = {
  getAll: (params = {}) => request.get('/material_usages', { params }),
  getById: (id) => request.get(`/material_usages/${id}`),
  create: (data) => request.post('/material_usages', data),
  update: (id, data) => request.put(`/material_usages/${id}`, data),
  delete: (id) => request.delete(`/material_usages/${id}`)
}

export const archiveAPI = {
  getAll: (params = {}) => request.get('/archives', { params }),
  getById: (id) => request.get(`/archives/${id}`),
  create: (data) => request.post('/archives', data),
  update: (id, data) => request.put(`/archives/${id}`, data),
  delete: (id) => request.delete(`/archives/${id}`)
}