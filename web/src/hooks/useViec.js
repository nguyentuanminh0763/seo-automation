import { useCallback, useEffect, useRef, useState } from 'react'
import { ngheViec, dungViec } from '../api'

/**
 * Quản lý trọn vòng đời một lượt chạy: bắt đầu → nghe tiến trình → xong/lỗi.
 *
 * Hai màn Trends và Suggest dùng chung hook này; chúng chỉ khác nhau ở hàm
 * gọi API lúc bắt đầu, nên phần điều phối không phải viết hai lần.
 */
export function useViec() {
  const [ma, datMa]           = useState(null)
  const [trangThai, datTT]    = useState('nhan_roi')   // nhan_roi|dang_chay|xong|da_dung|loi
  const [cacDongLog, datLog]  = useState([])
  const [ketQua, datKetQua]   = useState(null)
  const [loi, datLoi]         = useState(null)
  const [giay, datGiay]       = useState(0)

  const dongKenh = useRef(null)
  const batDauLuc = useRef(null)

  // Đồng hồ đếm giây. Chạy Suggest mất hơn 10 phút nên phải cho người dùng
  // thấy thời gian trôi, không thì họ tưởng máy treo.
  useEffect(() => {
    if (trangThai !== 'dang_chay') return
    const dem = setInterval(() => {
      datGiay(Math.round((Date.now() - batDauLuc.current) / 1000))
    }, 1000)
    return () => clearInterval(dem)
  }, [trangThai])

  // Đóng kênh khi rời màn hình, tránh để kết nối treo lại.
  useEffect(() => () => dongKenh.current?.(), [])

  const xuLySuKien = useCallback((sk) => {
    if (sk.loai === 'log') {
      // Gộp theo lô nhỏ: Suggest bắn ra hàng nghìn dòng, mỗi dòng vẽ lại cả
      // trang thì trình duyệt ì ngay. Chỉ giữ 1500 dòng gần nhất.
      datLog((cu) => {
        const moi = [...cu, { muc: sk.muc, chu: sk.chu, stt: sk.stt }]
        return moi.length > 1500 ? moi.slice(-1500) : moi
      })
    } else if (sk.loai === 'trang_thai') {
      datTT('dang_chay')
    } else if (sk.loai === 'xong') {
      datKetQua(sk.ket_qua)
      datTT(sk.trang_thai === 'da_dung' ? 'da_dung' : 'xong')
      datGiay(sk.giay)
    } else if (sk.loai === 'loi') {
      datLoi(sk.chu)
      datTT('loi')
    }
  }, [])

  const batDau = useCallback(async (goiAPI) => {
    datLog([]); datKetQua(null); datLoi(null); datGiay(0)
    datTT('dang_chay')
    batDauLuc.current = Date.now()
    try {
      const { id } = await goiAPI()
      datMa(id)
      dongKenh.current?.()
      dongKenh.current = ngheViec(id, xuLySuKien)
    } catch (e) {
      datLoi(e.message)
      datTT('loi')
      // Máy chủ báo bận: kèm luôn thông tin việc đang chạy để giao diện
      // nói rõ người dùng phải chờ cái gì.
      return e.duLieu?.viec_dang_chay ?? null
    }
    return null
  }, [xuLySuKien])

  const bamDung = useCallback(async () => {
    if (!ma) return
    try { await dungViec(ma) } catch (e) { datLoi(e.message) }
  }, [ma])

  return {
    ma, trangThai, cacDongLog, ketQua, loi, giay,
    dangChay: trangThai === 'dang_chay',
    batDau, bamDung,
  }
}
