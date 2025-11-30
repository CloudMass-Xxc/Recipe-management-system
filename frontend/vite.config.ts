import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  // 项目根目录
  root: process.cwd(),
  
  // 插件配置
  plugins: [
    react()
  ],
  
  // 解析配置
  resolve: {
    // 别名配置，提高模块解析速度
    alias: {
      '@': resolve(__dirname, './src'),
      '@components': resolve(__dirname, './src/components'),
      '@pages': resolve(__dirname, './src/pages'),
      '@store': resolve(__dirname, './src/store'),
      '@services': resolve(__dirname, './src/services'),
      '@utils': resolve(__dirname, './src/utils'),
      '@assets': resolve(__dirname, './src/assets'),
    },
    // 优化扩展名解析顺序
    extensions: ['.tsx', '.ts', '.jsx', '.js', '.json']
  },
  
  // 服务器配置
  server: {
    // 自动打开浏览器
    open: true,
    // 服务器端口
    port: 5174,
    // 启用热模块替换
    hmr: true
  },
  
  // 构建配置
  build: {
    // 输出目录
    outDir: 'dist',
    // 生成源映射文件
    sourcemap: false,
    // 优化构建速度
    minify: 'esbuild',
    // 资源优化配置
    assetsDir: 'assets',
    // 静态资源文件名哈希长度
    assetsInlineLimit: 4096, // 4KB以内的资源内联
    // 构建目标
    target: 'es2020',
    // 代码分割配置
    rollupOptions: {
      // 输入配置
      input: {
        main: resolve(__dirname, 'index.html')
      },
      // 输出配置
      output: {
        // 代码分割策略
        manualChunks: {
          // React核心库
          'react-vendor': [
            'react',
            'react-dom',
            'react-router-dom'
          ],
          // Material UI组件库
          'mui-vendor': [
            '@mui/material',
            '@mui/icons-material',
            '@mui/system',
            '@emotion/react',
            '@emotion/styled'
          ],
          // Redux状态管理
          'redux-vendor': [
            '@reduxjs/toolkit',
            'react-redux'
          ],
          // HTTP客户端
          'axios-vendor': [
            'axios'
          ],
          // 表单处理
          'form-vendor': [
            'react-hook-form',
            'zod'
          ]
        },
        // 分块大小警告阈值
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    }
  },
  
  // 预览服务器配置
  preview: {
    // 预览服务器端口
    port: 5173
  },
  
  // 环境变量配置
  envDir: process.cwd(),
  envPrefix: 'VITE_'
})
