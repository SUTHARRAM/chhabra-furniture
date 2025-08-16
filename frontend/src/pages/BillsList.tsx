import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/client'

export default function BillsList() {
  const [rows, setRows] = useState<any[]>([])
  useEffect(()=>{ (async ()=>{
    const res = await api.get('/bills?limit=50&page=1')
    setRows(res.data.data)
  })() },[])
  return (
    <div>
      <div className="actions">
        <Link to="/bills/new">+ New Bill</Link>
      </div>
      <table>
        <thead><tr><th>Date</th><th>Bill No</th><th>Customer</th><th>Total</th><th></th></tr></thead>
        <tbody>
          {rows.map(r=>(
            <tr key={r.id}>
              <td>{new Date(r.bill_date).toLocaleString()}</td>
              <td>{r.bill_no}</td>
              <td>{r.to?.name}</td>
              <td>₹{r.total?.toFixed(2)}</td>
              <td><Link to={`/bills/${r.id}`}>Open</Link></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
