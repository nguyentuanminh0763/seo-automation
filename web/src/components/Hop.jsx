import Bieu from './Bieu'

/** Hộp thông báo: hướng dẫn, cảnh báo, lỗi. */
export default function Hop({ kieu = 'chinh', bieu, tieuDe, children }) {
  const macDinh = { chinh: 'thong-tin', 'canh-bao': 'canh-bao',
                    loi: 'loi', tot: 'tot' }[kieu]
  return (
    <div className={`hop ${kieu}`}>
      <Bieu ten={bieu ?? macDinh} co={15} className="bieu hop-bieu" />
      <div>
        {tieuDe && <b>{tieuDe}</b>}
        {tieuDe && children && <br />}
        {children}
      </div>
    </div>
  )
}
