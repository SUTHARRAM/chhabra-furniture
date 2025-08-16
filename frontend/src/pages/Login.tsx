import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../auth/auth'

export default function Login() {
  const [email, setEmail] = useState('admin@chhabrafurniture.com')
  const [password, setPassword] = useState('Admin@123')
  const [err, setErr] = useState('')
  const nav = useNavigate()

  const submit = async (e: any) => {
    e.preventDefault()
    try {
      await login(email, password)
      nav('/')
    } catch (e:any) {
      setErr(e?.response?.data?.error || 'Login failed')
    }
  }

  return (
    <div className="auth">
      <form onSubmit={submit}>
        <h2>Login</h2>
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" />
        <input value={password} type="password" onChange={e=>setPassword(e.target.value)} placeholder="Password" />
        {err && <div className="error">{err}</div>}
        <button>Login</button>
      </form>
    </div>
  )
}
