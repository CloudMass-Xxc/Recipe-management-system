import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000', // 后端API基础URL，移除/api前缀
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // 统一错误处理
    if (error.response) {
      // 服务器响应了但状态码不是2xx
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并重定向到登录页
          localStorage.removeItem('token');
          window.location.href = '/login';
          break;
        case 403:
          console.error('没有权限访问此资源');
          break;
        case 404:
          console.error('请求的资源不存在');
          break;
        case 500:
          console.error('服务器错误');
          break;
        default:
          console.error('请求失败:', error.response.data.message || '未知错误');
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      console.error('网络错误，请检查您的网络连接');
    } else {
      // 设置请求时发生了错误
      console.error('请求配置错误:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;