export default function ShareButtons({ billNo, total, shareSlug }:{
  billNo: string, total: number, shareSlug: string
}) {
  const shareUrl = `${window.location.origin}/share/${shareSlug}`
  const text = encodeURIComponent(`Invoice ${billNo} - Total: ₹${total.toFixed(2)} ${shareUrl}`)
  const wa = `https://wa.me/?text=${text}`
  const fb = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`
  const webshare = async () => {
    if (navigator.share) await navigator.share({ title: `Invoice ${billNo}`, text: `Total ₹${total.toFixed(2)}`, url: shareUrl })
  }
  return (
    <div className="share">
      <a href={wa} target="_blank">WhatsApp</a>
      <a href={fb} target="_blank">Facebook</a>
      <button onClick={webshare}>Share</button>
    </div>
  )
}
