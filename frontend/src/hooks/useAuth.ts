import { useDispatch, useSelector } from 'react-redux';
import { useEffect } from 'react';
import type { RootState, AppDispatch } from '../store';
import { login, register, getCurrentUser, logout, clearError, clearAuth } from '../store/slices/authSlice';
import type { LoginCredentials, RegisterData } from '../types/auth';
import AuthService from '../services/auth.service';

export const useAuth = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { user, isAuthenticated, loading, error } = useSelector((state: RootState) => state.auth);

  // 初始化认证检查，在组件挂载时调用
  useEffect(() => {
    console.log('useAuth: Initializing authentication check');
    // 调用AuthService的初始化方法，检查应用是否重启
    AuthService.initialize();
    
    // 如果存在用户信息但没有访问令牌，清除认证状态
    if (user && !AuthService.isAuthenticated()) {
      console.log('useAuth: User data exists but no valid token, clearing auth state');
      dispatch(clearAuth());
    }
    
    // 如果用户已认证但没有用户信息，获取用户信息
    if (AuthService.isAuthenticated() && !user) {
      console.log('useAuth: Authenticated but no user data, fetching current user');
      dispatch(getCurrentUser());
    }
  }, [dispatch, user]);

  const handleLogin = (credentials: LoginCredentials) => {
    return dispatch(login(credentials)).unwrap();
  };

  const handleRegister = (data: RegisterData) => {
    // Convert RegisterData to match register thunk expected format
    const registerData = {
      username: data.username,
      email: data.email,
      password: data.password,
      phone: data.phone // Use the correct field name that backend expects
    };
    return dispatch(register(registerData)).unwrap();
  };

  const handleLogout = () => {
    dispatch(logout());
  };

  const fetchCurrentUser = () => {
    return dispatch(getCurrentUser()).unwrap();
  };

  const handleClearError = () => {
    dispatch(clearError());
  };

  return {
    user,
    isAuthenticated,
    loading,
    error,
    login: handleLogin,
    register: handleRegister,
    logout: handleLogout,
    fetchCurrentUser,
    clearError: handleClearError
  };
};
