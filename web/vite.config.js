import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Cấu hình build giao diện.
//
// VÌ SAO ÉP TÊN FILE CỐ ĐỊNH (app.js / app.css)?
//   Vite mặc định gắn mã băm vào tên file (app-a3f9b2.js) để trình duyệt biết
//   khi nào cần tải lại. Nhưng bản build được commit vào repo, nên mỗi lần sửa
//   giao diện sẽ sinh ra một file tên mới và xóa file cũ — lịch sử git đầy rác.
//   Tên cố định thì mỗi lần sửa chỉ thấy đúng 2 file thay đổi.
//   Đổi lại phải chặn bộ nhớ đệm bằng thẻ meta trong index.html.
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: 'app.js',
        chunkFileNames: 'app-[name].js',
        assetFileNames: 'app.[ext]',
      },
    },
  },
  server: {
    port: 5173,
    // Khi chạy `npm run dev`, mọi lời gọi /api được chuyển sang máy chủ Python.
    // Nhớ khởi động máy chủ bằng: python seo_web.py --dev
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8765',
        changeOrigin: true,
      },
    },
  },
})
