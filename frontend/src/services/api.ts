import axiosInstance from './axios-instance';
import type { AxiosRequestConfig, AxiosError, AxiosResponse } from 'axios';
import { toast } from 'react-toastify';
import { getFromLocalStorage } from '../utils/localStorage';
import { setToSessionStorage, removeFromLocalStorage, removeFromSessionStorage } from '../utils/localStorage';

// 创建一个新的axios实例，继承axiosInstance的配置
const api = axiosInstance;

// 响应拦截器 - 处理认证相关逻辑
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
    
    // 处理401错误
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // 获取refresh_token
        const refreshToken = getFromLocalStorage('refresh_token');
        
        if (refreshToken) {
          // 尝试刷新token - 直接使用axios实例避免循环依赖
          try {
            const response = await axiosInstance.post<{ access_token: string }>('/auth/refresh', {
              refresh_token: refreshToken
            });
            
            // 更新访问令牌
            setToSessionStorage('access_token', response.data.access_token);
            
            // 更新请求头并重试
            if (originalRequest.headers) {
              originalRequest.headers['Authorization'] = `Bearer ${response.data.access_token}`;
            }
            
            return api(originalRequest);
          } catch (refreshError) {
            // 刷新失败，清除认证数据
            removeFromSessionStorage('access_token');
            removeFromLocalStorage('refresh_token');
            removeFromLocalStorage('user');
            removeFromLocalStorage('userProfile');
            removeFromLocalStorage('userPreferences');
            
            throw refreshError;
          }
        } else {
          // 没有refresh_token，跳转到登录页
          toast.error('登录已过期，请重新登录');
          removeFromSessionStorage('access_token');
          removeFromLocalStorage('refresh_token');
          removeFromLocalStorage('user');
          removeFromLocalStorage('userProfile');
          removeFromLocalStorage('userPreferences');
          
          window.location.href = '/login';
        }
      } catch (refreshError) {
        // 刷新失败，跳转到登录页
        toast.error('登录已过期，请重新登录');
        removeFromSessionStorage('access_token');
        removeFromLocalStorage('refresh_token');
        removeFromLocalStorage('user');
        removeFromLocalStorage('userProfile');
        removeFromLocalStorage('userPreferences');
        
        window.location.href = '/login';
      }
    }
    
    // 处理其他错误
    if (error.response) {
      const message = (error.response.data as any)?.message || error.message || '请求失败';
      toast.error(message);
    } else if (error.request) {
      toast.error('网络错误，请检查您的网络连接');
    } else {
      toast.error('请求配置错误');
    }
    
    return Promise.reject(error);
  }
);

// 辅助函数，用于处理API错误
const handleApiError = (error: any): string => {
  if (error.response?.data?.message) {
    return error.response.data.message;
  } else if (error.message) {
    return error.message;
  } else {
    return '发生未知错误';
  }
};

// 导出API实例和辅助函数
export { api, handleApiError };

export default api;
