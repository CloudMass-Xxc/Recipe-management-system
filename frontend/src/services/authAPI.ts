import api from './api';

// 定义接口
interface LoginCredentials {
  identifier: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  phone: string;
  password: string;
  display_name?: string;
  diet_preferences?: string[];
}

interface AuthenticatedUser {
  user_id: string;
  username: string;
  email: string;
  phone?: string;
  display_name: string;
  avatar_url?: string | null;
  bio?: string | null;
  diet_preferences?: string[];
  created_at: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: AuthenticatedUser;
}

// 定义类
class AuthAPI {
  private static persistToken(token: string) {
    localStorage.setItem('token', token);
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  private static clearToken() {
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
  }

  static async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await api.post('/auth/login', credentials);
      const authData = response.data as AuthResponse;
      if (authData.access_token) {
        AuthAPI.persistToken(authData.access_token);
      }
      return authData;
    } catch (error: any) {
      // 改进错误处理，支持多种错误信息格式
      if (error.response?.data) {
        if (error.response.data.message) {
          error.message = error.response.data.message;
        } else if (error.response.data.detail) {
          error.message = error.response.data.detail;
        } else if (typeof error.response.data === 'string') {
          error.message = error.response.data;
        }
      }
      throw error;
    }
  }

  static async register(userData: RegisterData): Promise<AuthResponse> {
    try {
      const payload = {
        ...userData,
        display_name: userData.display_name || userData.username,
        diet_preferences: userData.diet_preferences || [],
      };
      const response = await api.post('/auth/register', payload);
      const authData = response.data as AuthResponse;
      if (authData.access_token) {
        AuthAPI.persistToken(authData.access_token);
      }
      return authData;
    } catch (error: any) {
      // 增强错误处理，支持多种错误信息格式
      console.error('注册API错误响应:', error.response?.data);
      
      if (error.response?.data) {
        const data = error.response.data;
        
        // 处理字符串错误
        if (typeof data === 'string') {
          error.message = data;
        }
        // 处理包含message字段的对象
        else if (data.message) {
          error.message = data.message;
        }
        // 处理包含detail字段的对象
        else if (data.detail) {
          error.message = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
        }
        // 处理包含错误信息的对象（如密码验证错误）
        else if (data.errors) {
          const errorMessages = [];
          for (const [field, msgs] of Object.entries(data.errors)) {
            if (Array.isArray(msgs)) {
              errorMessages.push(`${field}: ${msgs.join(', ')}`);
            } else {
              errorMessages.push(`${field}: ${msgs}`);
            }
          }
          error.message = errorMessages.join('; ');
        }
        // 处理用户名已存在等特定错误
        else if (data.username) {
          error.message = data.username.join('; ');
        }
        else if (data.email) {
          error.message = data.email.join('; ');
        }
        else if (data.password) {
          error.message = data.password.join('; ');
        }
        // 尝试将整个错误对象转换为可读字符串
        else {
          try {
            error.message = JSON.stringify(data);
          } catch (e) {
            error.message = '注册失败: 未知错误格式';
          }
        }
      } else if (error.request) {
        // 请求发出但没有收到响应
        error.message = '无法连接到服务器，请检查网络连接';
      } else {
        // 请求配置出错
        error.message = error.message || '注册请求失败';
      }
      
      console.error('处理后的注册错误:', error.message);
      throw error;
    }
  }

  static async logout(): Promise<void> {
    try {
      await api.post('/auth/logout');
    } finally {
      AuthAPI.clearToken();
    }
  }

  static async getCurrentUser(): Promise<AuthenticatedUser | null> {
    try {
      const response = await api.get('/users/me');
      return response.data as AuthenticatedUser;
    } catch (error: any) {
      if (error.response?.status === 401) {
        AuthAPI.clearToken();
      }
      return null;
    }
  }

  static isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }
}

// 统一导出
export type { LoginCredentials, RegisterData, AuthenticatedUser };
export default AuthAPI;
