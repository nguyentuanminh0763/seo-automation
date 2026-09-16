/* ==========================================================================
   Gọi API của máy chủ Python.
   Mọi lời gọi mạng của giao diện đều đi qua file này — sửa đường dẫn API thì
   chỉ phải sửa một chỗ.
   ========================================================================== */

/**
 * Bóc thông điệp lỗi tiếng Việt mà máy chủ gửi kèm.
 *
 * FastAPI gói lỗi vào trường `detail`. Máy chủ luôn đặt câu tiếng Việt ở
 * `detail.thong_diep`, nhưng lỗi kiểm tra dữ liệu (422) do FastAPI tự sinh thì
 * `detail` là một mảng mô tả kỹ thuật — không đưa nguyên văn cho người dùng đọc.
 */
async function bocLoi(phanHoi) {
  let dl = null
  try { dl = await phanHoi.json() } catch { /* máy chủ trả về thứ không phải JSON */ }

  const ct = dl?.detail
  if (ct && typeof ct === 'object' && ct.thong_diep) {
    const loi = new Error(ct.thong_diep)
    loi.duLieu = ct
    return loi
  }
  if (typeof ct === 'string') return new Error(ct)
  if (phanHoi.status === 422) {
    return new Error('Dữ liệu gửi lên không hợp lệ. Kiểm tra lại ô nhập từ khóa.')
  }
  return new Error(`Máy chủ báo lỗi ${phanHoi.status}. Xem cửa sổ đen để biết chi tiết.`)
}

async function goi(duongDan, tuyChon = {}) {
  let phanHoi
  try {
    phanHoi = await fetch(duongDan, {
      headers: { 'Content-Type': 'application/json' },
      ...tuyChon,
    })
  } catch {
    // Không phải lỗi máy chủ mà là không gọi tới được — thường do người dùng
    // lỡ đóng cửa sổ đen. Nói đúng nguyên nhân thay vì "Failed to fetch".
    throw new Error(
      'Không liên lạc được với máy chủ.\n\n' +
      'Cửa sổ đen (Command Prompt) có thể đã bị đóng. ' +
      'Bấm đúp lại file Chay_giao_dien_web.bat rồi tải lại trang này.'
    )
  }
  if (!phanHoi.ok) throw await bocLoi(phanHoi)
  return phanHoi.json()
}

const guiJSON = (than) => ({ method: 'POST', body: JSON.stringify(than) })

export const layTrangThai   = ()      => goi('/api/trang-thai')
export const chayTrends     = (tc)    => goi('/api/trends/chay', guiJSON(tc))
export const chaySuggest    = (tc)    => goi('/api/suggest/chay', guiJSON(tc))
export const uocTinhSuggest = (n, nh) => goi('/api/suggest/uoc-tinh',
                                             guiJSON({ so_tu_khoa: n, nhanh: nh }))
export const layViec        = (ma)    => goi(`/api/viec/${ma}`)
export const dungViec       = (ma)    => goi(`/api/viec/${ma}/dung`, guiJSON({}))
export const xuatFile       = (ma, dd) => goi(`/api/viec/${ma}/xuat`,
                                              guiJSON({ dinh_dang: dd }))

/**
 * Mở kênh nghe tiến trình chạy dần của một việc.
 * Trả về hàm đóng kênh — nhớ gọi khi rời màn hình, không thì kết nối treo lại.
 */
export function ngheViec(ma, khiCoSuKien) {
  const nguon = new EventSource(`/api/viec/${ma}/dong`)

  nguon.onmessage = (sk) => {
    let suKien
    try { suKien = JSON.parse(sk.data) } catch { return /* bỏ qua gói vỡ */ }

    // Việc chạy xong -> PHẢI tự đóng kênh ở đây.
    // Máy chủ đóng kênh một cách bình thường, nhưng EventSource coi mọi lần
    // dòng chảy kết thúc là rớt mạng và tự kết nối lại sau vài giây. Kết nối
    // mới được máy chủ phát lại toàn bộ lịch sử, nên nhật ký bị chép thêm một
    // lần nữa — cứ vài giây lại một lần, không bao giờ dừng.
    if (suKien.loai === 'ket_thuc') nguon.close()

    khiCoSuKien(suKien)
  }

  // Chốt chặn cuối: trình duyệt chịu thua hẳn (máy chủ tắt giữa chừng).
  // KHÔNG dùng chỗ này để bắt lúc việc chạy xong — đã thử và SAI: máy chủ đóng
  // kênh bình thường thì readyState chuyển sang CONNECTING (đang kết nối lại),
  // không phải CLOSED, nên nhánh dưới không bao giờ chạy. Việc xong được bắt ở
  // onmessage bên trên.
  nguon.onerror = () => {
    if (nguon.readyState === EventSource.CLOSED) khiCoSuKien({ loai: 'ket_thuc' })
  }

  return () => nguon.close()
}
