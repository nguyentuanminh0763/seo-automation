import { useEffect, useState } from 'react'
import { layTrangThai } from './api'
import ManTrends from './man/ManTrends'
import ManSuggest from './man/ManSuggest'
import Hop from './components/Hop'
import Bieu from './components/Bieu'

const CAC_MAN = [
  { ma: 'trends',  bieu: 'xu-huong', ten: 'Google Trends',  phu: 'Từ khóa đột biến' },
  { ma: 'suggest', bieu: 'y-tuong',  ten: 'Google Suggest', phu: 'Từ khóa làm bài' },
]

/** Đọc lựa chọn đã lưu. Bọc try/catch vì chế độ ẩn danh chặn lưu trữ. */
function daLuu(khoa, macDinh) {
  try { return localStorage.getItem(khoa) ?? macDinh } catch { return macDinh }
}

function luu(khoa, giaTri) {
  try { localStorage.setItem(khoa, giaTri) } catch { /* không lưu được thì thôi */ }
}

export default function App() {
  const [man, datMan]           = useState('trends')
  const [khoiDong, datKhoiDong] = useState(null)
  const [loi, datLoi]           = useState(null)
  const [giaoDien, datGiaoDien] = useState(() => daLuu('giao-dien', 'toi'))
  const [gon, datGon]           = useState(() => daLuu('thanh-ben', 'mo') === 'gon')

  useEffect(() => {
    document.documentElement.dataset.giaoDien = giaoDien
    luu('giao-dien', giaoDien)
  }, [giaoDien])

  useEffect(() => { luu('thanh-ben', gon ? 'gon' : 'mo') }, [gon])

  useEffect(() => {
    layTrangThai().then(datKhoiDong).catch((e) => datLoi(e.message))
  }, [])

  const tenGiaoDien = giaoDien === 'toi' ? 'Nền sáng' : 'Nền tối'
  const tinhTrang = loi ? 'Mất kết nối máy chủ'
                  : khoiDong ? 'Máy chủ đang chạy' : 'Đang kết nối…'

  return (
    <div className="khung" data-gon={gon ? '1' : undefined}>
      <aside className="thanh-ben">
        {/* Thu gọn thì chính ô chữ Đ thành nút mở lại — lúc đó thanh bên chỉ
            rộng 62px, không còn chỗ cho một nút riêng. */}
        <div className="hieu">
          <button className="hieu-o" onClick={() => datGon(!gon)}
                  title={gon ? 'Mở rộng thanh bên' : 'Thu gọn thanh bên'}>
            <span className="hieu-chu">Đ</span>
            <Bieu ten="mo-rong" co={17} className="bieu hieu-mo" />
          </button>
          <div className="hieu-chu-nhom">
            <div className="hieu-ten">SEO Keyword Tools</div>
            <div className="hieu-phu">Đô Lar</div>
          </div>
          <button className="nut-gon" onClick={() => datGon(true)}
                  title="Thu gọn thanh bên" aria-label="Thu gọn thanh bên">
            <Bieu ten="thu-gon" co={16} />
          </button>
        </div>

        <div className="nhan-nhom">Công cụ</div>
        {CAC_MAN.map((m) => (
          <button key={m.ma}
                  className={`muc${man === m.ma ? ' chon' : ''}`}
                  onClick={() => datMan(m.ma)}
                  title={gon ? `${m.ten} — ${m.phu}` : undefined}>
            <Bieu ten={m.bieu} co={17} />
            <span className="muc-chu">
              {m.ten}
              <span className="muc-phu">{m.phu}</span>
            </span>
          </button>
        ))}

        <div className="day-ben">
          <button className="muc" title={gon ? tenGiaoDien : undefined}
                  onClick={() => datGiaoDien(giaoDien === 'toi' ? 'sang' : 'toi')}>
            <Bieu ten={giaoDien === 'toi' ? 'sang' : 'toi'} co={17} />
            <span className="muc-chu">{tenGiaoDien}</span>
          </button>

          <div className="den-trang-thai" title={gon ? tinhTrang : undefined}>
            <span className={`cham ${loi ? 'loi' : khoiDong ? 'tot' : 'chay'}`} />
            <span className="muc-chu">{tinhTrang}</span>
          </div>
        </div>
      </aside>

      <main className="chinh">
        {loi ? (
          <Hop kieu="loi" tieuDe="Không liên lạc được với máy chủ">
            <pre>{loi}</pre>
          </Hop>
        ) : !khoiDong ? (
          <div className="trong">
            <span className="quay" style={{ borderTopColor: 'var(--chinh)',
                                            width: 22, height: 22 }} />
            <b>Đang kết nối tới máy chủ…</b>
          </div>
        ) : (
          <>
            {khoiDong.thieu_thu_vien && (
              <div style={{ marginBottom: 14 }}>
                <Hop kieu="loi" tieuDe="Chưa cài đủ thư viện nên chưa chạy được">
                  Mở PowerShell tại thư mục dự án và chạy đúng một lệnh:
                  <pre>python -m pip install -r requirements.txt</pre>
                  Cài xong thì tải lại trang này.
                </Hop>
              </div>
            )}
            {man === 'trends'  && <ManTrends  khoiDong={khoiDong} />}
            {man === 'suggest' && <ManSuggest khoiDong={khoiDong} />}
          </>
        )}
      </main>
    </div>
  )
}
