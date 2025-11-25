import axios from 'axios';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') || 'http://localhost:8001';

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL, // 后端API基础URL
  timeout: 15000, // 增加超时时间
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  },
  withCredentials: true, // 确保跨域请求时携带cookies
});

const existingToken = localStorage.getItem('token');
if (existingToken) {
  api.defaults.headers.common['Authorization'] = `Bearer ${existingToken}`;
}

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // 添加时间戳防止缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now(),
      };
    }
    
    return config;
  },
  (error) => {
    console.error('请求配置错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    // 直接返回完整的响应对象，让调用者自行处理data
    return response;
  },
  (error) => {
    // 统一错误处理
    console.error('API响应错误:', error.response?.data);
    
    if (error.response) {
      // 服务器响应了但状态码不是2xx
      const { status, data } = error.response;
      
      // 提取并格式化错误信息
      let errorMessage = '';
      
      if (typeof data === 'string') {
        errorMessage = data;
      } else if (data.message) {
        errorMessage = data.message;
      } else if (data.detail) {
        errorMessage = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
      } else if (data.errors) {
        const errorMessages = [];
        for (const [field, msgs] of Object.entries(data.errors)) {
          if (Array.isArray(msgs)) {
            errorMessages.push(`${field}: ${msgs.join(', ')}`);
          } else {
            errorMessages.push(`${field}: ${msgs}`);
          }
        }
        errorMessage = errorMessages.join('; ');
      } else if (data.username) {
        errorMessage = data.username.join('; ');
      } else if (data.email) {
        errorMessage = data.email.join('; ');
      } else if (data.password) {
        errorMessage = data.password.join('; ');
      } else {
        try {
          errorMessage = JSON.stringify(data);
        } catch (e) {
          errorMessage = `未知错误 (状态码: ${status})`;
        }
      }
      
      // 根据状态码进行特定处理
      switch (status) {
        case 401:
          // 未授权，清除token并重定向到登录页
          localStorage.removeItem('token');
          // 避免循环重定向
          if (window.location.pathname !== '/login') {
            window.location.href = '/login';
          }
          errorMessage = errorMessage || '登录已过期，请重新登录';
          break;
        case 403:
          console.error('权限错误:', errorMessage);
          errorMessage = errorMessage || '没有权限访问此资源';
          break;
        case 404:
          console.error('资源不存在:', errorMessage);
          errorMessage = errorMessage || '请求的资源不存在';
          break;
        case 429:
          console.error('请求频率过高，请稍后再试');
          errorMessage = '请求频率过高，请稍后再试';
          break;
        case 500:
        case 502:
        case 503:
        case 504:
          console.error('服务器错误:', errorMessage);
          errorMessage = errorMessage || '服务器暂时无法处理请求';
          break;
        default:
          console.error(`请求失败 (状态码: ${status}):`, errorMessage);
      }
      
      // 设置错误消息
      error.message = errorMessage;
    } else if (error.request) {
      // 请求已发出但没有收到响应
      console.error('网络错误:', '无法连接到服务器，请检查您的网络连接');
      error.message = '无法连接到服务器，请检查您的网络连接';
    } else {
      // 设置请求时发生了错误
      console.error('请求错误:', error.message);
      error.message = error.message || '请求配置错误';
    }
    
    // 保留原始错误结构，同时确保有正确的message属性
    return Promise.reject(error);
  }
);

export default api;