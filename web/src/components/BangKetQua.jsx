import { useMemo, useState } from 'react'
import Hop from './Hop'

/**
 * Bảng kết quả: tìm nhanh, sắp xếp theo cột, lọc theo nhóm, xuất file.
 *
 * Nhận dữ liệu dạng {cot: [...], dong: [[...]]} thay vì mảng đối tượng, vì hai
 * công cụ có số cột khác hẳn nhau và còn đổi trong tương lai. Bảng không cần
 * biết cột tên gì — cứ có gì hiện nấy.
 */
export default function BangKetQua({ bang, cotLoc, onXuat, dangXuat }) {
  const [tim, datTim]       = useState('')
  const [nhom, datNhom]     = useState('tat-ca')
  const [sapXep, datSapXep] = useState({ cot: null, giam: false })

  const viTriLoc = cotLoc ? bang.cot.indexOf(cotLoc) : -1

  // Đếm số dòng theo từng nhóm, để hiện ngay trên nút lọc.
  const cacNhom = useMemo(() => {
    if (viTriLoc < 0) return []
    const dem = new Map()
    for (const d of bang.dong) {
      const k = String(d[viTriLoc])
      dem.set(k, (dem.get(k) || 0) + 1)
    }
    return [...dem.entries()].sort((a, b) => b[1] - a[1])
  }, [bang, viTriLoc])

  const dongHien = useMemo(() => {
    const tuKhoa = tim.trim().toLowerCase()
    let ds = bang.dong

    if (nhom !== 'tat-ca' && viTriLoc >= 0) {
      ds = ds.filter((d) => String(d[viTriLoc]) === nhom)
    }
    if (tuKhoa) {
      ds = ds.filter((d) => d.some((o) => String(o).toLowerCase().includes(tuKhoa)))
    }
    if (sapXep.cot !== null) {
      const i = sapXep.cot
      // Cột số phải so sánh theo giá trị, không theo chữ cái — nếu không thì
      // 9.000 sẽ đứng trên 87.100.
      ds = [...ds].sort((a, b) => {
        const x = a[i], y = b[i]
        const soX = typeof x === 'number', soY = typeof y === 'number'
        const kq = (soX && soY) ? x - y
                                : String(x).localeCompare(String(y), 'vi')
        return sapXep.giam ? -kq : kq
      })
    }
    return ds
  }, [bang, tim, nhom, viTriLoc, sapXep])

  const doiSapXep = (i) => datSapXep((cu) =>
    cu.cot === i ? { cot: i, giam: !cu.giam } : { cot: i, giam: false })

  return (
    <div className="the">
      <div className="the-dau">
        <h2>Kết quả</h2>
        <div className="hang-nut">
          <input
            className="o-nhap" style={{ width: 200 }}
            placeholder="Tìm nhanh trong bảng…"
            value={tim} onChange={(e) => datTim(e.target.value)}
          />
          <button className="nut nho" disabled={dangXuat} onClick={() => onXuat('xlsx')}>
            {dangXuat ? <span className="quay" /> : '⬇'} Excel
          </button>
          <button className="nut nho" disabled={dangXuat} onClick={() => onXuat('csv')}>
            CSV
          </button>
        </div>
      </div>

      {cacNhom.length > 1 && (
        <div className="loc-day">
          <button className={`loc-nut${nhom === 'tat-ca' ? ' chon' : ''}`}
                  onClick={() => datNhom('tat-ca')}>
            Tất cả<span className="loc-dem">{bang.dong.length.toLocaleString('vi-VN')}</span>
          </button>
          {cacNhom.map(([ten, so]) => (
            <button key={ten} className={`loc-nut${nhom === ten ? ' chon' : ''}`}
                    onClick={() => datNhom(ten)}>
              {ten}<span className="loc-dem">{so.toLocaleString('vi-VN')}</span>
            </button>
          ))}
        </div>
      )}

      {bang.da_cat && (
        <div style={{ padding: '12px 16px 0' }}>
          <Hop kieu="canh-bao" tieuDe={
            `Bảng chỉ hiện ${bang.dong.length.toLocaleString('vi-VN')} trên ` +
            `${bang.tong_dong.toLocaleString('vi-VN')} dòng`}>
            Hiện hết một lúc thì trang bị ì. <b>File Excel xuất ra vẫn có đủ
            toàn bộ {bang.tong_dong.toLocaleString('vi-VN')} dòng</b> — không mất gì cả.
          </Hop>
        </div>
      )}

      <div className="bang-khung">
        <table>
          <thead>
            <tr>
              {bang.cot.map((c, i) => (
                <th key={c} onClick={() => doiSapXep(i)}
                    title="Bấm để sắp xếp theo cột này">
                  {c}
                  {sapXep.cot === i && <span className="mui">{sapXep.giam ? '▼' : '▲'}</span>}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {dongHien.map((d, i) => (
              <tr key={i}>
                {d.map((o, j) => (
                  <td key={j} className={typeof o === 'number' ? 'so' : undefined}>
                    {typeof o === 'number' ? o.toLocaleString('vi-VN') : o}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>

        {dongHien.length === 0 && (
          <div className="trong">
            <div className="trong-bieu">🔍</div>
            <b>Không có dòng nào khớp</b>
            <span>Thử xóa bớt chữ trong ô tìm nhanh hoặc chọn lại nhóm.</span>
          </div>
        )}
      </div>

      <div style={{ padding: '10px 16px', borderTop: '1px solid var(--vien)',
                    fontSize: 12, color: 'var(--chu-rat-mo)' }}>
        Hiện {dongHien.length.toLocaleString('vi-VN')} dòng
        {dongHien.length !== bang.tong_dong &&
          ` · tổng ${bang.tong_dong.toLocaleString('vi-VN')} dòng`}
      </div>
    </div>
  )
}
