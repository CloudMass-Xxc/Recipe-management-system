import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosError, AxiosResponse } from 'axios';
import { getFromSessionStorage } from '../utils/localStorage';

// 直接硬编码baseURL，包含/api前缀，配合Vite代理
const API_BASE_URL = '/api'; // 使用相对路径，配合Vite代理

console.log('API_BASE_URL设置为:', API_BASE_URL);

// 创建axios实例
const axiosInstance: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// 请求拦截器
axiosInstance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 记录请求URL，用于调试
    console.log('API请求URL:', `${config.baseURL ?? ''}${config.url ?? ''}`);
    console.log('完整请求配置:', config);
    
    // 从sessionStorage获取access_token
    const token = getFromSessionStorage('access_token');
    
    // 如果有token，则添加到请求头
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// 基础响应拦截器（不包含认证相关逻辑）
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
