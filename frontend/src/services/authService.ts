import { apiRequest } from './api';
import { UserLogin, UserRegister, UserResponse, TokenResponse, ChangePasswordRequest } from '../types/auth';

class AuthService {
  // 用户注册
  async register(userData: UserRegister): Promise<UserResponse> {
    return apiRequest.post<UserResponse>('/auth/register', userData);
  }

  // 用户登录
  async login(credentials: UserLogin): Promise<TokenResponse> {
    const response = await apiRequest.post<TokenResponse>('/auth/login', credentials);
    
    // 保存token和用户信息到localStorage
    if (response.access_token) {
      localStorage.setItem('auth_token', response.access_token);
      if (response.user) {
        localStorage.setItem('user', JSON.stringify(response.user));
      }
    }
    
    return response;
  }

  // 登出
  logout(): void {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
  }

  // 获取当前用户信息
  async getCurrentUser(): Promise<UserResponse> {
    return apiRequest.get<UserResponse>('/auth/me');
  }

  // 更新用户信息
  async updateProfile(userData: Partial<UserRegister>): Promise<UserResponse> {
    return apiRequest.put<UserResponse>('/auth/profile', userData);
  }

  // 修改密码
  async changePassword(passwordData: ChangePasswordRequest): Promise<{ message: string }> {
    return apiRequest.put<{ message: string }>('/auth/change-password', passwordData);
  }

  // 检查用户是否已登录
  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  }

  // 获取存储的用户信息
  getStoredUser(): UserResponse | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch (error) {
        console.error('解析用户信息失败:', error);
        return null;
      }
    }
    return null;
  }

  // 刷新token
  async refreshToken(): Promise<TokenResponse> {
    return apiRequest.post<TokenResponse>('/auth/refresh-token');
  }
}

export default new AuthService();