/** Dãy ô số liệu ở đầu phần kết quả. */
export default function TheThongKe({ cacMuc }) {
  if (!cacMuc?.length) return null
  return (
    <div className="day-so">
      {cacMuc.map((m, i) => (
        <div key={m.ten} className={`the-so${i === 0 ? ' nhan-manh' : ''}`}>
          <div className="the-so-nhan">{m.ten}</div>
          <div className="the-so-gia-tri">{m.so_luong.toLocaleString('vi-VN')}</div>
        </div>
      ))}
    </div>
  )
}
