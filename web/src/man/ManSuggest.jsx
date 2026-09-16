import { useEffect, useState } from 'react'
import ManThuThap from './ManThuThap'
import Hop from '../components/Hop'
import { chaySuggest, uocTinhSuggest } from '../api'

/** Màn Google Suggest — có thêm phần ước tính thời gian trước khi chạy. */
export default function ManSuggest({ khoiDong }) {
  const macDinh = khoiDong?.suggest?.tu_khoa_mac_dinh ?? []
  const [tuKhoa, datTuKhoa] = useState(macDinh.join('\n'))
  const [nhanh, datNhanh] = useState(false)
  const [uocTinh, datUocTinh] = useState(null)

  const soTu = tuKhoa.split('\n').filter((d) => d.trim()).length

  // Hỏi máy chủ tính giúp số lượt và số phút. Cố ý KHÔNG tự nhân trong giao
  // diện: công thức nằm ở suggest/settings.py, chép sang đây là sớm muộn lệch.
  useEffect(() => {
    if (soTu === 0) { datUocTinh(null); return }
    let con = true
    const hen = setTimeout(() => {
      uocTinhSuggest(soTu, nhanh)
        .then((kq) => con && datUocTinh(kq))
        .catch(() => con && datUocTinh(null))
    }, 250)   // chờ người dùng gõ xong mới hỏi, tránh gọi liên tục
    return () => { con = false; clearTimeout(hen) }
  }, [soTu, nhanh])

  return (
    <ManThuThap
      bieu="y-tuong"
      tieuDe="Google Suggest — từ khóa làm nội dung"
      moTa="Trả lời câu hỏi: người ta hay hỏi gì? Ra hàng nghìn câu hỏi thật để
            lên kế hoạch viết bài. Chạy khoảng một lần mỗi quý."
      nhanKeyword="Từ khóa gốc"
      goiYKeyword="Ở đây nên dùng từ NGẮN VÀ RỘNG (vd: máy tính, cpu) — công cụ tự
                   ghép hàng chục biến thể để moi ra câu hỏi dài."
      tuKhoa={tuKhoa} datTuKhoa={datTuKhoa} tuKhoaMacDinh={macDinh}
      cotLoc="Nhóm ý định"
      goiAPIChay={(ds) => chaySuggest({ tu_khoa: ds, nhanh })}
      tuyChon={
        <div className="truong">
          <label className="bat-tat">
            <input type="checkbox" checked={nhanh}
                   onChange={(e) => datNhanh(e.target.checked)} />
            <span>
              <span className="bat-tat-ten">Chế độ nhanh</span>
              <div className="goi-y">
                Bỏ phần quét bảng chữ cái (a→z). Nhanh hơn khoảng 3 lần nhưng
                ra ít từ khóa hơn hẳn. Dùng khi chỉ muốn thử cho biết.
              </div>
            </span>
          </label>
        </div>
      }
      truocKhiChay={
        uocTinh && (
          <div className="the">
            <div className="the-dau"><h2>Dự kiến lần chạy này</h2></div>
            <div className="the-than">
              <div className="day-so">
                <div className="the-so nhan-manh">
                  <div className="the-so-nhan">Thời gian</div>
                  <div className="the-so-gia-tri">
                    {uocTinh.so_phut < 1 ? '< 1' : Math.round(uocTinh.so_phut)}
                    <span style={{ fontSize: 13, fontWeight: 500,
                                   color: 'var(--chu-mo)' }}> phút</span>
                  </div>
                </div>
                <div className="the-so">
                  <div className="the-so-nhan">Lượt hỏi Google</div>
                  <div className="the-so-gia-tri">
                    {uocTinh.so_luot_hoi.toLocaleString('vi-VN')}
                  </div>
                </div>
                <div className="the-so">
                  <div className="the-so-nhan">Biến thể / từ</div>
                  <div className="the-so-gia-tri">{uocTinh.so_bien_the_moi_tu}</div>
                </div>
              </div>
            </div>
          </div>
        )
      }
      canhBao={
        <Hop kieu="canh-bao" tieuDe="Google Suggest không cho biết lượng tìm kiếm">
          Thứ tự trong bảng là <b>thứ tự ưu tiên làm nội dung</b>, không phải
          thứ hạng tìm kiếm. Số lượt tìm/tháng là thứ các công cụ trả phí bán —
          nguồn miễn phí không có.
        </Hop>
      }
    />
  )
}
