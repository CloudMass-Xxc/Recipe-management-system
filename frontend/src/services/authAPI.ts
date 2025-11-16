import api from './api';

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

interface AuthResponse {
  user: {
    id: string;
    username: string;
    email: string;
  };
  token: string;
}

class AuthAPI {
  // 用户登录
  static async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      // 模拟API调用响应
      const mockResponse: AuthResponse = {
        user: {
          id: '1',
          username: credentials.username,
          email: `${credentials.username}@example.com`,
        },
        token: 'mock-token-123456',
      };
      
      // 保存token到localStorage
      localStorage.setItem('token', mockResponse.token);
      
      return mockResponse;
    } catch (error) {
      console.error('登录失败:', error);
      throw error;
    }
  }

  // 用户注册
  static async register(userData: RegisterData): Promise<AuthResponse> {
    try {
      // 模拟API调用响应
      const mockResponse: AuthResponse = {
        user: {
          id: '1',
          username: userData.username,
          email: userData.email,
        },
        token: 'mock-token-123456',
      };
      
      // 保存token到localStorage
      localStorage.setItem('token', mockResponse.token);
      
      return mockResponse;
    } catch (error) {
      console.error('注册失败:', error);
      throw error;
    }
  }

  // 用户登出
  static logout(): void {
    localStorage.removeItem('token');
    // 可以在这里添加其他登出逻辑，比如清除用户信息等
  }

  // 获取当前用户信息
  static async getCurrentUser() {
    try {
      const response = await api.get('/auth/me');
      return response;
    } catch (error) {
      console.error('获取用户信息失败:', error);
      throw error;
    }
  }

  // 检查用户是否已登录
  static isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }
}

export default AuthAPI;