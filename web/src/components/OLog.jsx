import { useEffect, useRef } from 'react'

/**
 * Ô nhật ký chạy.
 *
 * Tự cuộn xuống dòng mới nhất, NHƯNG dừng tự cuộn khi người dùng đang kéo lên
 * đọc lại phần cũ — bị giật xuống giữa lúc đang đọc là một trong những thứ
 * khó chịu nhất ở màn hình kiểu này.
 */
export default function OLog({ cacDong, dangChay }) {
  const oRef = useRef(null)
  const baoDay = useRef(true)

  useEffect(() => {
    const o = oRef.current
    if (o && baoDay.current) o.scrollTop = o.scrollHeight
  }, [cacDong])

  const khiCuon = () => {
    const o = oRef.current
    if (!o) return
    baoDay.current = o.scrollHeight - o.scrollTop - o.clientHeight < 40
  }

  return (
    <div className="log" ref={oRef} onScroll={khiCuon}>
      {cacDong.length === 0 ? (
        <div className="log-trong">
          {dangChay
            ? 'Đang khởi động, chờ dòng đầu tiên…'
            : 'Nhật ký chạy sẽ hiện ở đây theo thời gian thực.'}
        </div>
      ) : (
        cacDong.map((d) => (
          <div key={d.stt} className={`log-dong ${d.muc}`}>{d.chu}</div>
        ))
      )}
    </div>
  )
}
