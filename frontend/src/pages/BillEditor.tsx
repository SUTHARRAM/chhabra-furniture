import { useNavigate, useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../api/client'
import BillForm, { BillFormValues } from '../components/BillForm'
import ShareButtons from '../components/ShareButtons'

export default function BillEditor() {
  const { id } = useParams()
  const nav = useNavigate()
  const [bill, setBill] = useState<any>(null)
  const [links, setLinks] = useState<any>(null)

  useEffect(()=>{ if (id) (async ()=>{
    const res = await api.get(`/bills/${id}`); setBill(res.data)
    const lk = await api.get(`/bills/${id}/share-links`); setLinks(lk.data)
  })() },[id])

  const save = async (data: BillFormValues) => {
    const res = await api.post('/bills', data)
    setBill(res.data)
    const lk = await api.get(`/bills/${res.data.id}/share-links`); setLinks(lk.data)
    alert('Saved!')
    nav(`/bills/${res.data.id}`)
  }

  const genPDF = async () => {
    const res = await api.post(`/bills/${bill.id}/pdf`)
    window.open(res.data.pdf_url, '_blank')
  }

  return (
    <div>
      <h2>{id ? `Edit ${bill?.bill_no ?? ''}` : 'New Bill'}</h2>
      <div className="logo-corner">
        {/* Vishwakarma corner image on UI */}
        <img src="/vishwakarma.png" alt="Vishwakarma" />
      </div>
      <BillForm onSubmit={save} defaults={bill ?? undefined}/>
      {bill && (
        <>
          <button onClick={genPDF}>Generate PDF</button>
          {links && <ShareButtons billNo={bill.bill_no} total={bill.total} shareSlug={bill.share_slug} />}
        </>
      )}
    </div>
  )
}
