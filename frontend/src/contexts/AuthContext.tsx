import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { UserResponse } from '../types/auth';
import authService from '../services/authService';

interface AuthContextType {
  user: UserResponse | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => void;
  updateProfile: (userData: Partial<UserResponse>) => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 初始化时检查用户认证状态
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        // 检查本地存储是否有token
        if (authService.isAuthenticated()) {
          // 获取当前用户信息
          const userInfo = await authService.getCurrentUser();
          setUser(userInfo);
          setIsAuthenticated(true);
        } else {
          // 尝试从本地存储获取用户信息
          const storedUser = authService.getStoredUser();
          if (storedUser) {
            setUser(storedUser);
            setIsAuthenticated(true);
          }
        }
      } catch (err) {
        // 如果获取用户信息失败，清除本地存储
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // 登录方法
  const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.login({ email, password });
      setUser(response.user || authService.getStoredUser() || null);
      setIsAuthenticated(true);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        err.response?.data?.message || 
        '登录失败，请检查您的邮箱和密码'
      );
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // 注册方法
  const register = async (userData: any) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.register(userData);
      // 注册成功后不自动登录，返回登录页面让用户自己登录
      return response;
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        err.response?.data?.message || 
        '注册失败，请稍后重试'
      );
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // 登出方法
  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  // 更新用户信息
  const updateProfile = async (userData: Partial<UserResponse>) => {
    setIsLoading(true);
    setError(null);
    try {
      const updatedUser = await authService.updateProfile(userData);
      setUser(updatedUser);
      // 更新本地存储的用户信息
      localStorage.setItem('user', JSON.stringify(updatedUser));
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        err.response?.data?.message || 
        '更新用户信息失败'
      );
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // 刷新用户信息
  const refreshUser = async () => {
    if (!isAuthenticated) return;
    
    setIsLoading(true);
    setError(null);
    try {
      const userInfo = await authService.getCurrentUser();
      setUser(userInfo);
      // 更新本地存储的用户信息
      localStorage.setItem('user', JSON.stringify(userInfo));
    } catch (err) {
      // 如果刷新失败，可能是token过期，清除认证状态
      logout();
    } finally {
      setIsLoading(false);
    }
  };

  const value = {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    updateProfile,
    refreshUser
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};