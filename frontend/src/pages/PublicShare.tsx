import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api/client'

export default function PublicShare() {
  const { slug } = useParams()
  const [b, setB] = useState<any>(null)
  useEffect(()=>{ (async ()=>{
    const res = await api.get(`/share/${slug}`); setB(res.data)
  })() },[slug])
  if (!b) return <div>Loading…</div>
  return (
    <div className="public">
      <h2>Invoice {b.bill_no}</h2>
      <div>Date: {new Date(b.bill_date).toLocaleString()}</div>
      <div>From: {b.from?.name} &nbsp; To: {b.to?.name}</div>
      <table>
        <thead><tr><th>Description</th><th>Rate</th><th>Qty</th><th>Price</th></tr></thead>
        <tbody>
          {b.items?.map((it:any, i:number)=>(
            <tr key={i}>
              <td>{it.description}</td><td>₹{it.rate.toFixed(2)}</td><td>{it.quantity}</td><td>₹{it.price.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div>Total: ₹{b.total?.toFixed(2)}</div>
    </div>
  )
}
