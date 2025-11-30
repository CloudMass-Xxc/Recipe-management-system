
// auth.service.ts
import api from './api';
import {
  getFromLocalStorage, 
  setToLocalStorage, 
  removeFromLocalStorage,
  getFromSessionStorage,
  setToSessionStorage,
  removeFromSessionStorage,
  checkForAppRestart,
  clearAuthData
} from '../utils/localStorage';

// Authentication token types
type TokenType = 'access_token' | 'refresh_token';

// Auth service class
export class AuthService {
  // 初始化检查 - 在应用启动时调用
  static initialize(): void {
    // 检查应用是否重启
    const isAppRestart = checkForAppRestart();
    
    if (isAppRestart) {
      console.log('Application restart detected, clearing authentication data...');
      // 清除所有认证数据
      this.clearAuth();
    }
  }

  // Get token from appropriate storage
  static getToken(type: TokenType): string | null {
    // access_token存储在sessionStorage中，浏览器关闭或标签页关闭时自动清除
    if (type === 'access_token') {
      return getFromSessionStorage<string>(type);
    }
    // refresh_token存储在localStorage中，但会在应用重启时被清除
    return getFromLocalStorage<string>(type);
  }

  // Set token to appropriate storage
  static setToken(type: TokenType, token: string): void {
    if (type === 'access_token') {
      setToSessionStorage(type, token);
    } else {
      setToLocalStorage(type, token);
    }
  }

  // Remove token from appropriate storage
  static removeToken(type: TokenType): void {
    if (type === 'access_token') {
      removeFromSessionStorage(type);
    } else {
      removeFromLocalStorage(type);
    }
  }

  // Clear all auth data
  static clearAuth(): void {
    clearAuthData();
  }

  // Register new user
  static async register(userData: {
    username: string;
    email: string;
    phone_number?: string;
    password: string;
  }): Promise<any> {
    console.log('AuthService: Registering new user with data from form');
    const sanitizedData = {
      username: userData.username,
      email: userData.email,
      password: userData.password,
      ...(userData.phone_number && { phone_number: userData.phone_number })
    };
    const response = await api.post('/auth/register', sanitizedData);
    return response.data;
  }

  // Login user
  static async login(credentials: {
    identifier: string; // Can be username, email, or phone
    password: string;
  }): Promise<any> {
    console.log('AuthService: Attempting login with provided credentials');
    const response = await api.post('/auth/login', credentials);
    
    // Store tokens and user data in appropriate storage
    if (response.data.access_token) {
      console.log('AuthService: Login successful, storing tokens securely');
      this.setToken('access_token', response.data.access_token);
      this.setToken('refresh_token', response.data.refresh_token);
      setToLocalStorage('user', response.data.user);
    }
    
    return response.data;
  }

  // Logout user
  static logout(): void {
    console.log('AuthService: User initiated logout, clearing all auth data');
    this.clearAuth();
  }

  // Get current user from API
  static async getCurrentUser(): Promise<any> {
    console.log('AuthService: Fetching current user from API');
    try {
      const response = await api.get('/auth/me');
      console.log('AuthService: Successfully fetched current user from API');
      return response.data;
    } catch (error) {
      console.error('AuthService: Failed to fetch current user from API', error);
      throw error;
    }
  }

  // Check if user is authenticated
  static isAuthenticated(): boolean {
    return !!this.getToken('access_token');
  }

  // Refresh access token using refresh token
  static async refreshToken(): Promise<string | null> {
    try {
      const refreshToken = this.getToken('refresh_token');
      if (!refreshToken) {
        console.log('AuthService: No refresh token available');
        return null;
      }

      console.log('AuthService: Attempting to refresh access token');
      const response = await api.post(
        '/auth/refresh',
        { refresh_token: refreshToken }
      );

      if (response.data.access_token) {
        console.log('AuthService: Token refresh successful');
        this.setToken('access_token', response.data.access_token);
        return response.data.access_token;
      }
      return null;
    } catch (error) {
      console.error('AuthService: Error refreshing token:', error);
      this.clearAuth();
      return null;
    }
  }
}

export default AuthService;
