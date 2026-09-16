/**
 * Bộ biểu tượng vẽ bằng SVG — MỘT MÀU, ăn theo màu chữ xung quanh.
 *
 * VÌ SAO KHÔNG DÙNG EMOJI (bản đầu dùng 📈 💡 ⚠️ ✅ …):
 *   Emoji do hệ điều hành vẽ, không phải do mình. Windows vẽ một kiểu, điện
 *   thoại vẽ kiểu khác, và màu thì cố định — nền tối hay sáng cũng vậy, không
 *   chỉnh được. Nhìn vào thấy như dán sticker lên phần mềm.
 *   Icon SVG kẻ nét lấy màu từ `currentColor` nên tự đổi theo nền, tự mờ đi khi
 *   chữ mờ, và in ra cũng sắc nét.
 *
 * VÌ SAO KHÔNG CÀI THƯ VIỆN ICON:
 *   Cả ứng dụng dùng đúng chừng này hình. Kéo về một thư viện vài nghìn icon để
 *   xài 19 cái là thêm phụ thuộc phải bảo trì mà không được gì.
 *
 * Thêm hình mới: chép phần bên trong <svg> (viewBox 24×24, nét, không tô màu)
 * vào bảng dưới rồi gọi <Bieu ten="ten-moi" />.
 */
const HINH = {
  // --- Hai công cụ ---
  'xu-huong': <><polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
                <polyline points="17 6 23 6 23 12" /></>,
  'y-tuong':  <><path d="M9 18h6" /><path d="M10 22h4" />
                <path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14" /></>,

  // --- Nền sáng / tối ---
  'sang': <><circle cx="12" cy="12" r="4" />
            <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" /></>,
  'toi':  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />,

  // --- Hộp thông báo ---
  'thong-tin': <><circle cx="12" cy="12" r="10" /><path d="M12 16v-4M12 8h.01" /></>,
  'canh-bao':  <><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                 <path d="M12 9v4M12 17h.01" /></>,
  'loi':       <><circle cx="12" cy="12" r="10" /><path d="m15 9-6 6M9 9l6 6" /></>,
  'tot':       <><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                 <polyline points="22 4 12 14.01 9 11.01" /></>,

  // --- Trạng thái lần chạy ---
  'dong-ho':  <><circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" /></>,
  'dau-tich': <polyline points="20 6 9 17 4 12" />,

  // --- Nút bấm ---
  'chay':      <polygon points="7 4 20 12 7 20" fill="currentColor" stroke="none" />,
  'dung':      <rect x="6" y="6" width="12" height="12" rx="2" fill="currentColor" stroke="none" />,
  'tai-xuong': <><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                 <polyline points="7 10 12 15 17 10" /><line x1="12" y1="15" x2="12" y2="3" /></>,
  'lam-moi':   <><polyline points="1 4 1 10 7 10" />
                 <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" /></>,

  // --- Ô trống ---
  'kinh-lup':  <><circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" /></>,
  'hop-trong': <><polyline points="22 12 16 12 14 15 10 15 8 12 2 12" />
                 <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" /></>,

  // --- Thanh bên thu ra vào ---
  'thu-gon':  <><rect x="3" y="3" width="18" height="18" rx="2" /><path d="M9 3v18" />
                <path d="m16 15-3-3 3-3" /></>,
  'mo-rong':  <><rect x="3" y="3" width="18" height="18" rx="2" /><path d="M9 3v18" />
                <path d="m14 9 3 3-3 3" /></>,
}

export default function Bieu({ ten, co = 16, day = 1.7, ...con }) {
  const hinh = HINH[ten]
  if (!hinh) return null
  return (
    <svg className="bieu" width={co} height={co} viewBox="0 0 24 24"
         fill="none" stroke="currentColor" strokeWidth={day}
         strokeLinecap="round" strokeLinejoin="round"
         aria-hidden="true" focusable="false" {...con}>
      {hinh}
    </svg>
  )
}
