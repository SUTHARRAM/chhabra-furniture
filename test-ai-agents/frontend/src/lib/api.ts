const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8080'

export function authHeaders(token?: string) {
  return token ? { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' }
}

export const api = {
  login: (email: string, password: string) => fetch(`${apiBase}/api/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) }),
  register: (email: string, password: string) => fetch(`${apiBase}/api/auth/register`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) }),
  listInvoices: (token: string, params?: { from?: string; to?: string }) => {
    const q = new URLSearchParams(params as any).toString()
    const u = q ? `${apiBase}/api/invoices?${q}` : `${apiBase}/api/invoices`
    return fetch(u, { headers: authHeaders(token) })
  },
  createInvoice: (token: string, payload: any) => fetch(`${apiBase}/api/invoices`, { method: 'POST', headers: authHeaders(token), body: JSON.stringify(payload) }),
  getInvoice: (token: string, id: string) => fetch(`${apiBase}/api/invoices/${id}`, { headers: authHeaders(token) }),
  updateInvoice: (token: string, id: string, payload: any) => fetch(`${apiBase}/api/invoices/${id}`, { method: 'PUT', headers: authHeaders(token), body: JSON.stringify(payload) }),
  deleteInvoice: (token: string, id: string) => fetch(`${apiBase}/api/invoices/${id}`, { method: 'DELETE', headers: authHeaders(token) }),
  exportPdf: (token: string, id: string) => fetch(`${apiBase}/api/invoices/${id}/pdf`, { headers: { 'Authorization': `Bearer ${token}` } }),
  shareWhatsApp: (token: string, id: string, phone: string) => fetch(`${apiBase}/api/invoices/${id}/share/whatsapp`, { method: 'POST', headers: authHeaders(token), body: JSON.stringify({ phone }) }),
}


