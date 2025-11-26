import { createSlice, createAsyncThunk, createAction } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import AuthAPI from '../../services/authAPI';

// 接口定义
export interface LoginCredentials {
  identifier: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  phone: string;
  password: string;
  display_name?: string;
  diet_preferences?: string[];
}

export interface AuthenticatedUser {
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

interface User {
  id: string;
  username: string;
  email: string;
  phone?: string;
  displayName: string;
  recipeCount: number;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

export const adaptUser = (payload: Partial<AuthenticatedUser>): User => ({
  id: payload.user_id || '',
  username: payload.username || '',
  email: payload.email || '',
  phone: payload.phone,
  displayName: payload.display_name || payload.username || '',
  recipeCount: 0,
});

export const login = createAsyncThunk(
  'auth/login',
  async (credentials: LoginCredentials) => {
    const response = await AuthAPI.login(credentials);
    return adaptUser(response.user);
  }
);

export const register = createAsyncThunk(
  'auth/register',
  async (userData: RegisterData) => {
    const authData = await AuthAPI.register(userData);
    return adaptUser(authData.user);
  }
);

// 异步登出操作
export const logout = createAsyncThunk(
  'auth/logout',
  async () => {
    await AuthAPI.logout();
  }
);

// 获取当前用户信息
export const fetchCurrentUser = createAsyncThunk(
  'auth/fetchCurrentUser',
  async () => {
    const userData = await AuthAPI.getCurrentUser();
    if (!userData) {
      throw new Error('未找到用户信息');
    }
    return adaptUser(userData);
  }
);

// 同步操作
export const clearError = createAction('auth/clearError');
export const setAuthStatus = createAction<{isAuthenticated: boolean, user?: User | null}>('auth/setAuthStatus');

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      // 登录处理
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action: PayloadAction<User>) => {
        state.isLoading = false;
        state.user = action.payload;
        state.isAuthenticated = true;
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || '登录失败';
      })
      // 注册处理
      .addCase(register.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state, action: PayloadAction<User>) => {
        state.isLoading = false;
        state.user = action.payload;
        state.isAuthenticated = true;
      })
      .addCase(register.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || '注册失败';
      })
      // 获取当前用户信息
      .addCase(fetchCurrentUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchCurrentUser.fulfilled, (state, action: PayloadAction<User>) => {
        state.isLoading = false;
        state.user = action.payload;
        state.isAuthenticated = true;
      })
      .addCase(fetchCurrentUser.rejected, (state) => {
        state.isLoading = false;
        state.user = null;
        state.isAuthenticated = false;
      })
      // 退出登录
      .addCase(logout.fulfilled, (state) => {
        state.user = null;
        state.isAuthenticated = false;
        state.error = null;
      })
      // 清除错误
      .addCase(clearError, (state) => {
        state.error = null;
      })
      // 手动设置认证状态
      .addCase(setAuthStatus, (state, action: PayloadAction<{isAuthenticated: boolean, user?: User | null}>) => {
        state.isAuthenticated = action.payload.isAuthenticated;
        if (action.payload.user !== undefined) {
          state.user = action.payload.user;
        }
      });
  },
});

export default authSlice.reducer;