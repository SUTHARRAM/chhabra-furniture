import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import App from './App'
import Login from './pages/Login'
import BillsList from './pages/BillsList'
import BillEditor from './pages/BillEditor'
import PublicShare from './pages/PublicShare'
import './i18n'
import './styles.css'

const Private: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const token = localStorage.getItem('token')
  return token ? <>{children}</> : <Navigate to="/login" replace />
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Private><App /></Private>} >
          <Route index element={<BillsList/>} />
          <Route path="bills/new" element={<BillEditor/>} />
          <Route path="bills/:id" element={<BillEditor/>} />
        </Route>
        <Route path="/login" element={<Login/>} />
        <Route path="/share/:slug" element={<PublicShare/>} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
