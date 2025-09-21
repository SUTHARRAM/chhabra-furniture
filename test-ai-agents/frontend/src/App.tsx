import { BrowserRouter, Route, Routes, Navigate, Link } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { api } from './lib/api'
import { useEffect, useState } from 'react'

function RequireAuth({ children }: { children: JSX.Element }) {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />
  return children
}

function LoginPage() {
  const { login, register } = useAuth()
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('password123')
  return (
    <div className="max-w-sm mx-auto mt-20 space-y-2">
      <h1 className="text-xl font-semibold mb-2">Login</h1>
      <input className="border px-3 py-2 w-full" placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="border px-3 py-2 w-full" placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <div className="flex gap-2">
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={async()=>{ const ok=await login(email,password); if(!ok) alert('Login failed') }}>Login</button>
        <button className="bg-gray-200 px-4 py-2 rounded" onClick={async()=>{ const ok=await register(email,password); alert(ok?'Registered':'Failed')}}>Register</button>
      </div>
    </div>
  )
}

function InvoicesPage() {
  const { token, logout } = useAuth()
  const [invoices, setInvoices] = useState<any[]>([])
  const [from, setFrom] = useState('')
  const [to, setTo] = useState('')
  const load = async () => {
    const res = await api.listInvoices(token!, { from, to })
    if (!res.ok) { alert('Failed to load'); return }
    setInvoices(await res.json())
  }
  const createDummy = async () => {
    const res = await api.createInvoice(token!, { clientName: 'John Doe', clientEmail: 'john@example.com', clientPhone: '9999999999', items: [{ description: 'Chair', quantity: 2, unitPrice: 50, taxRate: 18 }] })
    if (res.ok) load()
  }
  useEffect(() => { load() }, [])
  return (
    <div className="p-6 max-w-5xl mx-auto space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Invoices</h1>
        <button className="text-sm text-red-600" onClick={logout}>Logout</button>
      </div>
      <div className="flex gap-2 items-end">
        <div>
          <label className="block text-xs text-gray-600">From</label>
          <input type="date" className="border px-3 py-2" value={from} onChange={e=>setFrom(e.target.value)} />
        </div>
        <div>
          <label className="block text-xs text-gray-600">To</label>
          <input type="date" className="border px-3 py-2" value={to} onChange={e=>setTo(e.target.value)} />
        </div>
        <button className="bg-gray-200 px-4 py-2 rounded" onClick={load}>Search</button>
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={createDummy}>Create Dummy</button>
      </div>
      <ul className="divide-y bg-white rounded shadow">
        {invoices.map(inv => (
          <li key={inv.id || inv.invoiceId} className="p-3 flex justify-between">
            <div>
              <div className="font-medium"><Link className="text-blue-600" to={`/invoices/${inv.invoiceId}`}>{inv.invoiceId}</Link></div>
              <div className="text-sm text-gray-600">{inv.clientName} • {new Date(inv.createdAt).toLocaleDateString()}</div>
            </div>
            <div className="text-right">
              <div className="font-semibold">₹ {Number(inv.total).toFixed(2)}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}

function InvoiceViewPage() {
  const { token } = useAuth()
  const id = location.pathname.split('/').pop()!
  const [inv, setInv] = useState<any | null>(null)
  const load = async () => {
    const res = await api.getInvoice(token!, id)
    if (res.ok) setInv(await res.json())
  }
  useEffect(() => { load() }, [id])
  const downloadPdf = async () => {
    const res = await api.exportPdf(token!, id)
    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `invoice-${id}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  }
  const share = async () => {
    const phone = prompt('Enter phone with country code (e.g., +911234567890)')
    if (!phone) return
    const res = await api.shareWhatsApp(token!, id, phone)
    if (res.ok) alert('Queued')
  }
  if (!inv) return <div className="p-6">Loading...</div>
  return (
    <div className="p-6 max-w-3xl mx-auto space-y-3">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">{inv.invoiceId}</h1>
        <div className="flex gap-2">
          <button className="bg-gray-200 px-3 py-2 rounded" onClick={downloadPdf}>Download PDF</button>
          <button className="bg-green-600 text-white px-3 py-2 rounded" onClick={share}>Share WhatsApp</button>
        </div>
      </div>
      <div className="bg-white rounded shadow p-4">
        <div className="font-medium">{inv.clientName}</div>
        <div className="text-sm text-gray-600">{inv.clientEmail} • {inv.clientPhone}</div>
      </div>
      <div className="bg-white rounded shadow p-4">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left border-b">
              <th>Description</th>
              <th>Qty</th>
              <th>Unit</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            {inv.items.map((it:any, idx:number)=> (
              <tr key={idx} className="border-b last:border-0">
                <td>{it.description}</td>
                <td>{it.quantity}</td>
                <td>{it.unitPrice}</td>
                <td>{(it.quantity*it.unitPrice).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="text-right">
        <div>Subtotal: ₹ {Number(inv.subtotal).toFixed(2)}</div>
        <div>Tax: ₹ {Number(inv.taxTotal).toFixed(2)}</div>
        <div className="font-semibold">Total: ₹ {Number(inv.total).toFixed(2)}</div>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage/>} />
          <Route path="/" element={<RequireAuth><InvoicesPage/></RequireAuth>} />
          <Route path="/invoices/:id" element={<RequireAuth><InvoiceViewPage/></RequireAuth>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}


