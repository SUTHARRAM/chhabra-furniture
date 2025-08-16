import { useFieldArray, useForm } from 'react-hook-form'
import { useEffect } from 'react'

export type Item = { description: string; rate: number; quantity: number; unit?: string }
export type BillFormValues = {
  bill_date: string
  from: { name: string; address: string; phone?: string; gstin?: string }
  to: { name: string; address: string; phone?: string; gstin?: string }
  items: Item[]
  discount: number
  tax: { label: string; amount: number }
  language: 'en' | 'hi'
  notes?: string
}

// helper: create a value suitable for <input type="datetime-local">
function toDatetimeLocalValue(d: Date) {
  const off = d.getTimezoneOffset()
  const local = new Date(d.getTime() - off * 60000)
  return local.toISOString().slice(0, 16) // "YYYY-MM-DDTHH:mm"
}

export default function BillForm({ onSubmit, defaults }:{
  onSubmit: (data: BillFormValues)=>void,
  defaults?: Partial<BillFormValues>
}) {
  const { register, control, handleSubmit, watch, setValue } = useForm<BillFormValues>({
    defaultValues: (defaults as any) ?? {
      // ✅ make the input happy (local, no seconds)
      bill_date: toDatetimeLocalValue(new Date()),
      from: { name: 'Chhabra Furniture', address: 'Address here' },
      to: { name: '', address: '' },
      items: [{ description: '', rate: 0, quantity: 1 }],
      discount: 0,
      tax: { label: 'GST 18%', amount: 0 },
      language: 'en',
      notes: ''
    }
  })
  const { fields, append, remove } = useFieldArray({ control, name: 'items' })
  const items = watch('items')
  const subtotal = items.reduce((s, it)=> s + (Number(it.rate||0) * Number(it.quantity||0)), 0)

  useEffect(()=> {
    if (watch('tax.label')?.includes('18')) setValue('tax.amount', +(subtotal*0.18).toFixed(2))
  }, [subtotal, watch('tax.label')])

  const total = subtotal - Number(watch('discount')||0) + Number(watch('tax.amount')||0)

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="billform">
      <div className="row">
        <label>Bill Date</label>
        {/* ✅ convert the submitted value to RFC3339 so Go's time.Time can parse it */}
        <input
          type="datetime-local"
          {...register('bill_date', {
            setValueAs: (v: string) => v ? new Date(v).toISOString() : ''
          })}
        />
        <label>Language</label>
        <select {...register('language')}>
          <option value="en">English</option>
          <option value="hi">हिंदी</option>
        </select>
      </div>

      <div className="grid">
        <div>
          <h3>From</h3>
          <input placeholder="Name" {...register('from.name')} />
          <textarea placeholder="Address" {...register('from.address')} />
        </div>
        <div>
          <h3>To</h3>
          <input placeholder="Name" {...register('to.name')} />
          <textarea placeholder="Address" {...register('to.address')} />
        </div>
      </div>

      <h3>Items</h3>
      {fields.map((f, i)=>(
        <div className="itemrow" key={f.id}>
          <input placeholder="Description" {...register(`items.${i}.description` as const)} />
          <input type="number" step="0.01" placeholder="Rate" {...register(`items.${i}.rate` as const, { valueAsNumber: true })}/>
          <input type="number" step="0.01" placeholder="Qty" {...register(`items.${i}.quantity` as const, { valueAsNumber: true })}/>
          <div className="price">{(Number(watch(`items.${i}.rate`)||0) * Number(watch(`items.${i}.quantity`)||0)).toFixed(2)}</div>
          <button type="button" onClick={()=>remove(i)}>✕</button>
        </div>
      ))}
      <button type="button" onClick={()=>append({ description:'', rate:0, quantity:1 })}>+ Add Item</button>

      <div className="row">
        <label>Discount</label>
        <input type="number" step="0.01" {...register('discount', { valueAsNumber: true })}/>
        <label>Tax Label</label>
        <input {...register('tax.label')}/>
        <label>Tax Amount</label>
        <input type="number" step="0.01" {...register('tax.amount', { valueAsNumber: true })}/>
      </div>

      <div className="totals">
        <div>Subtotal: ₹{subtotal.toFixed(2)}</div>
        <div>Total: ₹{total.toFixed(2)}</div>
      </div>

      <textarea placeholder="Notes" {...register('notes')} />
      <button type="submit">Save Bill</button>
    </form>
  )
}
