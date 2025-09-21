import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { api } from '../lib/api'

type AuthContextType = {
  token: string | null
  login: (email: string, password: string) => Promise<boolean>
  register: (email: string, password: string) => Promise<boolean>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))
  useEffect(() => {
    if (token) localStorage.setItem('token', token)
    else localStorage.removeItem('token')
  }, [token])

  const value = useMemo<AuthContextType>(() => ({
    token,
    login: async (email, password) => {
      const res = await api.login(email, password)
      if (!res.ok) return false
      const data = await res.json()
      setToken(data.token)
      return true
    },
    register: async (email, password) => {
      const res = await api.register(email, password)
      return res.ok
    },
    logout: () => setToken(null),
  }), [token])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}


