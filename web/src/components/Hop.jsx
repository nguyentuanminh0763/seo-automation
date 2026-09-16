/** Hộp thông báo: hướng dẫn, cảnh báo, lỗi. */
export default function Hop({ kieu = 'chinh', bieu, tieuDe, children }) {
  const bieuMacDinh = { chinh: 'ℹ️', 'canh-bao': '⚠️', loi: '⛔', tot: '✅' }[kieu]
  return (
    <div className={`hop ${kieu}`}>
      <span className="hop-bieu">{bieu ?? bieuMacDinh}</span>
      <div>
        {tieuDe && <b>{tieuDe}</b>}
        {tieuDe && children && <br />}
        {children}
      </div>
    </div>
  )
}
