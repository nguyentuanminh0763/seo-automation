import { useState } from 'react'
import { useViec } from '../hooks/useViec'
import { xuatFile } from '../api'
import OKeyword from '../components/OKeyword'
import OLog from '../components/OLog'
import BangKetQua from '../components/BangKetQua'
import TheThongKe from '../components/TheThongKe'
import Hop from '../components/Hop'

/**
 * Khung chung cho hai màn thu thập.
 *
 * Trends và Suggest giống nhau tới 90%: nhập từ khóa → chỉnh tùy chọn → chạy →
 * xem log → xem bảng → xuất file. Chỗ khác nhau chỉ là mấy ô tùy chọn riêng,
 * nên tách khung ra đây, mỗi màn chỉ khai phần của mình.
 *
 * Giống hệt cách gui/tab_base.py làm cho bản tkinter.
 */
export default function ManThuThap({
  bieu, tieuDe, moTa, nhanKeyword, goiYKeyword,
  tuKhoa, datTuKhoa, tuKhoaMacDinh,
  tuyChon, truocKhiChay, canhBao,
  goiAPIChay, cotLoc,
}) {
  const v = useViec()
  const [dangXuat, datDangXuat] = useState(false)
  const [daXuat, datDaXuat]     = useState(null)
  const [loiXuat, datLoiXuat]   = useState(null)

  const danhSach = tuKhoa.split('\n').map((d) => d.trim()).filter(Boolean)

  const bamChay = () => {
    datDaXuat(null); datLoiXuat(null)
    v.batDau(() => goiAPIChay(danhSach))
  }

  const bamXuat = async (dinhDang) => {
    datDangXuat(true); datLoiXuat(null)
    try {
      const kq = await xuatFile(v.ma, dinhDang)
      datDaXuat(kq)
      // Tải thẳng về máy luôn, người dùng không phải đi tìm thư mục output/.
      window.location.href = kq.lien_ket_tai
    } catch (e) {
      datLoiXuat(e.message)
    } finally {
      datDangXuat(false)
    }
  }

  const phut = Math.floor(v.giay / 60)
  const dongHo = phut > 0 ? `${phut} phút ${v.giay % 60} giây` : `${v.giay} giây`

  return (
    <>
      <div className="dau-trang">
        <div>
          <h1>{bieu} {tieuDe}</h1>
          <p>{moTa}</p>
        </div>
      </div>

      <div className="luoi">
        {/* ------------ CỘT TRÁI: thiết lập ------------ */}
        <div className="cot dinh">
          <div className="the">
            <div className="the-dau"><h2>Thiết lập</h2></div>
            <div className="the-than">
              <OKeyword
                nhan={nhanKeyword} goiY={goiYKeyword}
                giaTri={tuKhoa} doiGiaTri={datTuKhoa}
                khoa={v.dangChay} matDinh={tuKhoaMacDinh}
              />
              {tuyChon}
            </div>
          </div>

          {truocKhiChay}

          <div className="hang-nut">
            {!v.dangChay ? (
              <button className="nut chinh to" onClick={bamChay}
                      disabled={danhSach.length === 0}>
                ▶ Bắt đầu chạy
              </button>
            ) : (
              <button className="nut nguy to" onClick={v.bamDung}>
                ■ Dừng lại
              </button>
            )}
          </div>

          {v.dangChay && (
            <Hop kieu="chinh" bieu={<span className="quay" style={{ borderTopColor: 'var(--chinh)' }} />}
                 tieuDe={`Đang chạy — ${dongHo}`}>
              Cứ để yên, đừng đóng cửa sổ đen. Bấm <b>Dừng lại</b> bất cứ lúc nào
              cũng được, <b>phần kết quả đã thu vẫn giữ nguyên</b>.
            </Hop>
          )}

          {canhBao}
        </div>

        {/* ------------ CỘT PHẢI: kết quả ------------ */}
        <div className="cot">
          {v.loi && (
            <Hop kieu="loi" tieuDe="Lần chạy này gặp lỗi">
              <pre>{v.loi}</pre>
            </Hop>
          )}

          {v.trangThai === 'da_dung' && (
            <Hop kieu="canh-bao" tieuDe="Đã dừng giữa chừng">
              Toàn bộ kết quả thu được trước lúc dừng vẫn còn nguyên bên dưới và
              xuất file được bình thường.
            </Hop>
          )}

          {v.ketQua && <TheThongKe cacMuc={v.ketQua.thong_ke} />}

          <div className="the">
            <div className="the-dau">
              <h2>Nhật ký chạy</h2>
              <span className="the-nho">
                {v.trangThai === 'dang_chay' ? `⏱ ${dongHo}`
                  : v.trangThai === 'xong'    ? `✓ xong sau ${dongHo}`
                  : v.trangThai === 'da_dung' ? `■ đã dừng sau ${dongHo}`
                  : v.trangThai === 'loi'     ? '⛔ lỗi'
                  : 'chưa chạy'}
              </span>
            </div>
            <div className="the-than" style={{ paddingTop: 0 }}>
              <OLog cacDong={v.cacDongLog} dangChay={v.dangChay} />
            </div>
          </div>

          {daXuat && (
            <Hop kieu="tot" tieuDe={`Đã xuất: ${daXuat.ten_file}`}>
              File vừa được tải về, đồng thời lưu sẵn trong thư mục
              {' '}<code>output/</code> cạnh công cụ.
              <br />
              <a href={daXuat.lien_ket_tai} style={{ color: 'var(--chinh)' }}>
                Tải lại file này
              </a>
            </Hop>
          )}
          {loiXuat && <Hop kieu="loi" tieuDe="Không xuất được file">{loiXuat}</Hop>}

          {v.ketQua?.bang?.tong_dong > 0 ? (
            <BangKetQua bang={v.ketQua.bang} cotLoc={cotLoc}
                        onXuat={bamXuat} dangXuat={dangXuat} />
          ) : v.ketQua ? (
            <div className="the"><div className="trong">
              <div className="trong-bieu">📭</div>
              <b>Lần chạy này không ra kết quả nào</b>
              <span>Xem nhật ký bên trên để biết lý do.</span>
            </div></div>
          ) : !v.dangChay && (
            <div className="the"><div className="trong">
              <div className="trong-bieu">{bieu}</div>
              <b>Chưa có kết quả</b>
              <span>Kiểm tra lại từ khóa bên trái rồi bấm <b>Bắt đầu chạy</b>.</span>
            </div></div>
          )}
        </div>
      </div>
    </>
  )
}
