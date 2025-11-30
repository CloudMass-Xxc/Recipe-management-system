import axios from 'axios';
import { getFromSessionStorage } from '../utils/localStorage';
import AuthService from './auth.service';

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

// 无论开发还是生产环境，都实际发送请求到后端
// 这样可以测试前端与后端的实际连接
// if (import.meta.env.DEV) {
//   // 请求拦截器 - 在开发环境下不实际发送请求
//   api.interceptors.request.use(
//     (config) => {
//       // 从localStorage获取token（如果有）
//       const token = getLocalStorageItem('access_token');
//       if (token) {
//         config.headers['Authorization'] = `Bearer ${token}`;
//       }
//       
//       // 在开发环境下，我们的服务文件已经提供了模拟数据，所以这里不需要实际发送请求
//       // 直接返回一个解析的Promise，让服务层的模拟数据生效
//       return Promise.resolve({
//         ...config,
//         adapter: (config) => {
//           // 这里返回一个被拒绝的Promise，这样服务层的模拟数据实现才会被使用
//           return Promise.reject({
//             message: 'Mock mode - Request intercepted',
//             config
//           });
//         }
//       });
//     },
//     (error) => {
//       return Promise.reject(error);
//     }
//   );
// } else {
  // 所有环境下的请求拦截器
  api.interceptors.request.use(
    (config) => {
      // 从sessionStorage获取access_token
      const token = getFromSessionStorage<string>('access_token');
      if (token) {
        console.log('API Request: Adding Authorization header with token');
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      console.error('API Request Error:', error);
      return Promise.reject(error);
    }
  );
//}

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // 在开发环境下，忽略模拟请求的错误（如果还在使用模拟模式）
    // if (import.meta.env.DEV && error.message === 'Mock mode - Request intercepted') {
    //   return Promise.reject(error);
    // }
    
    // 处理实际的401错误
    if (error.response && error.response.status === 401) {
      console.log('API Response: 401 Unauthorized, clearing auth data and redirecting to login');
      // 清除认证数据
      AuthService.clearAuth();
      // 重定向到登录页面
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

export default api;
