import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// The build output lands in ../dist and is copied to the PHP webroot by the
// Dockerfile, next to server.php. base './' keeps every asset URL relative so
// the app works no matter where the webroot is mounted.
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
  },
  server: {
    // `npm run dev` against a running docker stack: proxy the PHP gateway
    proxy: {
      '/server.php': 'http://localhost:8080',
    },
  },
})