import { useState } from 'react'
import ManThuThap from './ManThuThap'
import Hop from '../components/Hop'
import { chayTrends } from '../api'

/** Màn Google Trends — chỉ khai phần tùy chọn riêng, khung dùng chung. */
export default function ManTrends({ khoiDong }) {
  const macDinh = khoiDong?.trends?.tu_khoa_mac_dinh ?? []
  const [tuKhoa, datTuKhoa] = useState(macDinh.join('\n'))
  const [timeframe, datTimeframe] = useState('today 1-m')
  const [geo, datGeo] = useState('VN')
  const [themRising, datThemRising] = useState(false)

  const soNhom = Math.ceil(
    tuKhoa.split('\n').filter((d) => d.trim()).length / 5)

  return (
    <ManThuThap
      bieu="xu-huong"
      tieuDe="Google Trends — từ khóa đột biến"
      moTa="Trả lời câu hỏi: cái gì đang nóng lên tuần này? Dùng để canh nhập hàng
            và bắt sóng, chạy khoảng một lần mỗi tuần."
      nhanKeyword="Từ khóa hạt giống"
      goiYKeyword="Giữ từ ngắn và KHÔNG DẤU — người Việt gõ không dấu nhiều hơn."
      tuKhoa={tuKhoa} datTuKhoa={datTuKhoa} tuKhoaMacDinh={macDinh}
      cotLoc="Query Type"
      goiAPIChay={(ds) => chayTrends({
        tu_khoa: ds, timeframe, geo, include_rising: themRising,
      })}
      tuyChon={
        <>
          {/* Hai ô chọn ngắn nên xếp cạnh nhau cho đỡ tốn chiều cao màn hình. */}
          <div className="cap-truong">
            <div className="truong">
              <label htmlFor="o-khung">Khung thời gian</label>
              <select id="o-khung" className="o-chon" value={timeframe}
                      onChange={(e) => datTimeframe(e.target.value)}>
                {(khoiDong?.trends?.khung_thoi_gian ?? []).map((k) => (
                  <option key={k.ma} value={k.ma}>{k.ten}</option>
                ))}
              </select>
            </div>

            <div className="truong">
              <label htmlFor="o-khu-vuc">Khu vực</label>
              <select id="o-khu-vuc" className="o-chon" value={geo}
                      onChange={(e) => datGeo(e.target.value)}>
                {(khoiDong?.trends?.khu_vuc ?? []).map((k) => (
                  <option key={k.ma} value={k.ma}>{k.ten}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="truong">
            <label className="bat-tat">
              <input type="checkbox" checked={themRising}
                     onChange={(e) => datThemRising(e.target.checked)} />
              <span>
                <span className="bat-tat-ten">Lấy thêm từ khóa Rising</span>
                <div className="goi-y">
                  Mặc định chỉ lấy Breakout (tăng trên 5.000%). Bật thêm Rising
                  (từ 500%) khi lần chạy trước ra quá ít kết quả.
                </div>
              </span>
            </label>
          </div>
        </>
      }
      truocKhiChay={
        soNhom > 0 && (
          <Hop kieu="chinh" bieu="dong-ho">
            Chia thành <b>{soNhom} nhóm</b> (Google chỉ cho so sánh tối đa 5 từ
            mỗi lần), nghỉ 5–12 giây giữa các nhóm.
            Dự kiến khoảng <b>{Math.max(1, Math.round(soNhom * 10 / 60))} phút</b>.
          </Hop>
        )
      }
      canhBao={
        <Hop kieu="canh-bao" tieuDe="Đừng chạy liên tiếp nhiều lần">
          Google Trends chặn IP khá gắt. Nên giãn cách <b>ít nhất 1–2 giờ</b>
          {' '}giữa hai lần chạy. Đã gặp thật: một nhóm bị bỏ qua vì chạy dày quá.
        </Hop>
      }
    />
  )
}
