import { Link, Outlet, useNavigate } from 'react-router-dom'

export default function App() {
  const nav = useNavigate()
  const logout = () => { localStorage.removeItem('token'); nav('/login') }
  return (
    <div className="container">
      <header className="topbar">
        <div className="brand">Chhabra Billing</div>
        <nav>
          <Link to="/">Bills</Link>
          <Link to="/bills/new">New Bill</Link>
          <button onClick={logout}>Logout</button>
        </nav>
      </header>
      <Outlet/>
    </div>
  )
}
