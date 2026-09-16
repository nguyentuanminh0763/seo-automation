import { useMemo } from 'react'

/**
 * Ô nhập từ khóa: mỗi dòng một từ.
 *
 * Cố ý dùng ô văn bản nhiều dòng thay vì "thẻ từ khóa" bấm thêm từng cái:
 * người dùng đã quen chép cả cột từ Excel dán thẳng vào, kiểu thẻ sẽ chặn
 * mất thao tác đó.
 */
export default function OKeyword({ giaTri, doiGiaTri, khoa, matDinh, nhan, goiY }) {
  const danhSach = useMemo(
    () => giaTri.split('\n').map((d) => d.trim()).filter(Boolean),
    [giaTri]
  )
  const soTrung = danhSach.length -
    new Set(danhSach.map((d) => d.toLowerCase())).size

  return (
    <div className="truong">
      <label htmlFor="o-tu-khoa">
        {nhan}
        <span className="the-nho" style={{ marginLeft: 8 }}>
          {danhSach.length} từ
        </span>
        {soTrung > 0 && (
          <span className="the-nho canh-bao" style={{ marginLeft: 5 }}>
            {soTrung} trùng
          </span>
        )}
      </label>

      <textarea
        id="o-tu-khoa"
        className="o-van-ban"
        value={giaTri}
        onChange={(e) => doiGiaTri(e.target.value)}
        disabled={khoa}
        spellCheck={false}
        placeholder={'Mỗi dòng một từ khóa\npc gaming\nlaptop cũ'}
      />

      <div className="goi-y">
        {goiY}
        {soTrung > 0 && ' · Từ trùng sẽ được tự bỏ, không tốn thêm lượt hỏi Google.'}
      </div>

      {matDinh && (
        <button type="button" className="nut nho" disabled={khoa}
                onClick={() => doiGiaTri(matDinh.join('\n'))}
                style={{ alignSelf: 'flex-start' }}>
          ↺ Khôi phục danh sách mặc định
        </button>
      )}
    </div>
  )
}
