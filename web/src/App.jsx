import { useEffect, useState } from 'react'
import { layTrangThai } from './api'
import ManTrends from './man/ManTrends'
import ManSuggest from './man/ManSuggest'
import Hop from './components/Hop'

const CAC_MAN = [
  { ma: 'trends',  bieu: '📈', ten: 'Google Trends',  phu: 'Từ khóa đột biến' },
  { ma: 'suggest', bieu: '💡', ten: 'Google Suggest', phu: 'Từ khóa làm bài' },
]

/** Đọc lựa chọn giao diện đã lưu. Bọc try/catch vì chế độ ẩn danh chặn lưu trữ. */
function giaoDienDaLuu() {
  try { return localStorage.getItem('giao-dien') || 'toi' } catch { return 'toi' }
}

export default function App() {
  const [man, datMan]           = useState('trends')
  const [khoiDong, datKhoiDong] = useState(null)
  const [loi, datLoi]           = useState(null)
  const [giaoDien, datGiaoDien] = useState(giaoDienDaLuu)

  useEffect(() => {
    document.documentElement.dataset.giaoDien = giaoDien
    try { localStorage.setItem('giao-dien', giaoDien) } catch { /* không lưu được thì thôi */ }
  }, [giaoDien])

  useEffect(() => {
    layTrangThai().then(datKhoiDong).catch((e) => datLoi(e.message))
  }, [])

  return (
    <div className="khung">
      <aside className="thanh-ben">
        <div className="hieu">
          <div className="hieu-o">🔎</div>
          <div>
            <div className="hieu-ten">SEO Keyword Tools</div>
            <div className="hieu-phu">giaphongpc.vn</div>
          </div>
        </div>

        <div className="nhan-nhom">Công cụ</div>
        {CAC_MAN.map((m) => (
          <button key={m.ma}
                  className={`muc${man === m.ma ? ' chon' : ''}`}
                  onClick={() => datMan(m.ma)}>
            <span className="muc-bieu">{m.bieu}</span>
            <span>
              {m.ten}
              <div className="muc-phu">{m.phu}</div>
            </span>
          </button>
        ))}

        <div className="day-ben">
          <button className="muc" onClick={() =>
                    datGiaoDien(giaoDien === 'toi' ? 'sang' : 'toi')}>
            <span className="muc-bieu">{giaoDien === 'toi' ? '☀️' : '🌙'}</span>
            <span>{giaoDien === 'toi' ? 'Nền sáng' : 'Nền tối'}</span>
          </button>

          <div className="den-trang-thai">
            <span className={`cham ${loi ? 'loi' : khoiDong ? 'tot' : 'chay'}`} />
            {loi ? 'Mất kết nối máy chủ' : khoiDong ? 'Máy chủ đang chạy' : 'Đang kết nối…'}
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
              <div style={{ marginBottom: 18 }}>
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
