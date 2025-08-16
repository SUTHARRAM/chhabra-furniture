import api from '../api/client'

export async function login(email: string, password: string) {
  const res = await api.post('/auth/login', { email, password })
  localStorage.setItem('token', res.data.token)
  return res.data.user
}
