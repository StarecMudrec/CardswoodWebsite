import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    host: true,
    allowedHosts: ['cardswood.ru'],
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false
      },
      '/auth': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false
      },
      '/card_imgs': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
