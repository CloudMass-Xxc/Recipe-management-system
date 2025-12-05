import axiosInstance from './axios-instance';
import { setToLocalStorage, setToSessionStorage, removeFromLocalStorage, removeFromSessionStorage } from '../utils/localStorage';

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  phone: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: {
    user_id: string;
    username: string;
    email: string;
    phone: string;
    is_active: boolean;
  };
}

export interface AuthResponse {
  message: string;
  success: boolean;
  data?: TokenResponse | {
    user_id: string;
    username: string;
    email: string;
    phone: string;
    is_active: boolean;
  };
}

export class AuthService {
  /**
   * 用户登录
   * @param loginData 登录数据
   * @returns 认证响应
   */
  async login(loginData: LoginData): Promise<AuthResponse> {
    try {
      // 确保使用正确的参数名发送到后端
      const payload = {
        username: loginData.username,
        password: loginData.password
      };
      const response = await axiosInstance.post<AuthResponse>('/auth/login', payload);
      
      // 处理登录响应，提取令牌和用户信息
      if (response.data.success && response.data.data && 'access_token' in response.data.data) {
        const tokenResponse = response.data.data as TokenResponse;
        
        // 存储认证数据 - 注意：后端只返回access_token，没有refresh_token
        this.setAuthData(tokenResponse.access_token, '', tokenResponse.user);
      }
      
      return response.data;
    } catch (error: any) {
      console.error('登录失败:', error);
      // 处理错误，提取具体的验证错误信息
      if (error.response) {
        console.log('登录错误响应详情:', {
          status: error.response.status,
          data: error.response.data,
          headers: error.response.headers
        });
        
        // 处理后端实际返回的错误格式: {"error":{"type":"http_error","message":"错误信息"}}
        if (error.response.data.error && error.response.data.error.message) {
          throw new Error(`登录失败：${error.response.data.error.message}`);
        } else if (error.response.data.detail) {
          let errorMessage = '登录失败：';
          if (Array.isArray(error.response.data.detail)) {
            // 提取所有验证错误信息
            const errorDetails = error.response.data.detail.map((err: any) => {
              if (err.loc && err.msg) {
                const field = err.loc[err.loc.length - 1];
                return `${this.formatFieldName(field)}: ${err.msg}`;
              }
              return err.msg || '验证失败';
            });
            errorMessage += errorDetails.join('; ');
          } else {
            errorMessage += error.response.data.detail;
          }
          throw new Error(errorMessage);
        } else if (error.response.data.message) {
          throw new Error(`登录失败：${error.response.data.message}`);
        }
      }
      throw error;
    }
  }

  /**
   * 用户注册
   * @param registerData 注册数据
   * @returns 认证响应
   */
  async register(registerData: RegisterData): Promise<AuthResponse> {
    try {
      console.log('开始注册流程，注册数据:', registerData);
      // 获取axios实例的baseURL
      const baseURL = axiosInstance.defaults.baseURL || 'http://localhost:8002';
      console.log('API基础URL:', baseURL);
      console.log('完整注册接口URL:', `${baseURL}/api/auth/register`);
      
      const response = await axiosInstance.post<AuthResponse>('/auth/register', registerData);
      
      console.log('注册响应:', response);
      
      // 注册成功后自动登录，因为后端注册接口只返回用户信息，不返回令牌
      if (response.data.success && response.data.data) {
        console.log('注册成功，开始自动登录...');
        // 使用注册的用户名和密码进行自动登录
        const loginData: LoginData = {
          username: registerData.username,
          password: registerData.password
        };
        
        // 调用登录方法获取令牌
        await this.login(loginData);
      }
      
      return response.data;
    } catch (error: any) {
      console.error('注册失败:', error);
      console.error('错误详情:', {
        message: error.message,
        name: error.name,
        stack: error.stack,
        response: error.response ? {
          status: error.response.status,
          data: error.response.data,
          headers: error.response.headers
        } : 'No response',
        request: error.request ? 'Request sent' : 'No request'
      });
      
      // 处理各种HTTP错误状态码
      if (error.response) {
        console.log('错误响应详情:', {
          status: error.response.status,
          data: error.response.data,
          headers: error.response.headers
        });
        
        switch (error.response.status) {
          case 400:
            // 提取后端返回的具体错误信息
            if (error.response.data) {
              // 处理后端实际返回的错误格式: {"error":{"type":"http_error","message":"错误信息"}}
              if (error.response.data.error && error.response.data.error.message) {
                throw new Error(`注册失败：${error.response.data.error.message}`);
              } else if (error.response.data.message) {
                throw new Error(`注册失败：${error.response.data.message}`);
              } else if (error.response.data.detail) {
                let errorMessage = '注册失败：';
                if (Array.isArray(error.response.data.detail)) {
                  // 提取所有验证错误信息
                  const errorDetails = error.response.data.detail.map((err: any) => {
                    if (err.loc && err.msg) {
                      const field = err.loc[err.loc.length - 1];
                      return `${this.formatFieldName(field)}: ${err.msg}`;
                    }
                    return err.msg || '验证失败';
                  });
                  errorMessage += errorDetails.join('; ');
                } else {
                  errorMessage += error.response.data.detail;
                }
                throw new Error(errorMessage);
              } else if (typeof error.response.data === 'string') {
                throw new Error(`注册失败：${error.response.data}`);
              }
            }
            // 如果无法提取具体错误信息，提供更详细的默认错误
            throw new Error(`注册失败：请求参数错误 (400) - ${JSON.stringify(error.response.data || {})}`);
          case 401:
            throw new Error('注册失败：未授权');
          case 403:
            throw new Error('注册失败：禁止访问');
          case 404:
            throw new Error(`注册失败：API接口未找到 (404) - ${error.response.config?.url}`);
          case 422:
            if (error.response.data.detail) {
              let errorMessage = '注册失败：';
              if (Array.isArray(error.response.data.detail)) {
                // 提取所有验证错误信息
                const errorDetails = error.response.data.detail.map((err: any) => {
                  if (err.loc && err.msg) {
                    const field = err.loc[err.loc.length - 1];
                    return `${this.formatFieldName(field)}: ${err.msg}`;
                  }
                  return err.msg || '验证失败';
                });
                errorMessage += errorDetails.join('; ');
              } else {
                errorMessage += error.response.data.detail;
              }
              throw new Error(errorMessage);
            }
            break;
          case 500:
            // 提取后端返回的具体错误信息
            if (error.response.data.message) {
              throw new Error(`注册失败：${error.response.data.message}`);
            }
            throw new Error('注册失败：服务器内部错误');
          default:
            throw new Error(`注册失败：未知错误 (${error.response.status})`);
        }
      } else if (error.request) {
        // 请求已发出，但没有收到响应
        throw new Error('注册失败：服务器无响应，请检查网络连接');
      }
      
      throw new Error('注册失败：' + error.message);
    }
  }
  
  /**
   * 格式化字段名，使其更易读
   * @param field 字段名
   * @returns 格式化后的字段名
   */
  private formatFieldName(field: string): string {
    const fieldNames: Record<string, string> = {
      username: '用户名',
      email: '邮箱',
      phone: '手机号',
      password: '密码',
      display_name: '显示名称'
    };
    return fieldNames[field] || field;
  }

  /**
   * 用户登出
   */
  async logout(): Promise<void> {
    try {
      await axiosInstance.post('/auth/logout');
    } catch (error) {
      console.error('登出失败:', error);
    } finally {
      // 清除认证数据
      this.clearAuth();
    }
  }

  /**
   * 刷新访问令牌
   * @param refreshToken 刷新令牌
   * @returns 新的访问令牌和刷新令牌对
   */
  async refreshToken(refreshToken: string): Promise<any> {
    try {
      // 注意：目前后端可能不支持刷新令牌功能
      // 这里保留方法但添加警告，防止调用时出错
      console.warn('刷新令牌功能可能不被后端支持');
      throw new Error('刷新令牌功能暂不可用');
    } catch (error) {
      console.error('刷新令牌失败:', error);
      // 刷新失败，清除认证数据
      this.clearAuth();
      throw error;
    }
  }

  /**
   * 获取当前用户信息
   * @returns 用户信息
   */
  async getCurrentUser(): Promise<any> {
    try {
      const response = await axiosInstance.get('/auth/me');
      
      // 更新用户信息
      setToLocalStorage('user', response.data);
      
      return response.data;
    } catch (error) {
      console.error('获取用户信息失败:', error);
      throw error;
    }
  }

  /**
   * 存储认证数据
   * @param accessToken 访问令牌
   * @param refreshToken 刷新令牌（可选）
   * @param user 用户信息
   */
  private setAuthData(accessToken: string, refreshToken: string, user: any): void {
    // 访问令牌存储在sessionStorage，浏览器关闭后自动清除
    setToSessionStorage('access_token', accessToken);
    
    // 如果有刷新令牌，存储在localStorage（后端目前不提供）
    if (refreshToken) {
      setToLocalStorage('refresh_token', refreshToken);
    }
    
    // 用户信息存储在localStorage，用于持久化登录状态
    setToLocalStorage('user', user);
  }

  /**
   * 清除认证数据
   */
  clearAuth(): void {
    removeFromSessionStorage('access_token');
    removeFromLocalStorage('refresh_token');
    removeFromLocalStorage('user');
    removeFromLocalStorage('userProfile');
    removeFromLocalStorage('userPreferences');
    
  }

  /**
   * 检查用户是否已认证
   * @returns 是否已认证
   */
  isAuthenticated(): boolean {
    const accessToken = this.getAccessToken();
    return !!accessToken;
  }

  /**
   * 获取访问令牌
   * @returns 访问令牌
   */
  getAccessToken(): string | null {
    return this.getFromStorage('access_token', 'session');
  }

  /**
   * 获取刷新令牌
   * @returns 刷新令牌
   */
  getRefreshToken(): string | null {
    return this.getFromStorage('refresh_token', 'local');
  }

  /**
   * 获取用户信息
   * @returns 用户信息
   */
  getUser(): any {
    return this.getFromStorage('user', 'local');
  }

  /**
   * 从存储中获取数据
   * @param key 存储键
   * @param type 存储类型
   * @returns 存储的数据
   */
  private getFromStorage(key: string, type: 'local' | 'session'): any {
    try {
      const storage = type === 'local' ? localStorage : sessionStorage;
      const item = storage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.error(`获取${key}失败:`, error);
      return null;
    }
  }
}

// 创建并导出AuthService实例
export default new AuthService();

