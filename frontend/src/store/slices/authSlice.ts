import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

import AuthService from '../../services/auth.service';
import { getFromLocalStorage, getFromSessionStorage } from '../../utils/localStorage';

// 定义认证状态接口
interface AuthState {
  user: any | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

// 从存储初始化认证状态
const initialUser = getFromLocalStorage<any>('user');

const initialState: AuthState = {
  user: initialUser,
  isAuthenticated: !!getFromSessionStorage('access_token'),
  loading: false,
  error: null,
};

// 登录异步thunk
export const login = createAsyncThunk(
  'auth/login',
  async (credentials: { identifier: string; password: string }, { rejectWithValue }) => {
    try {
      console.log('AuthSlice: Attempting login with credentials');
      const response = await AuthService.login(credentials);
      console.log('AuthSlice: Login successful');
      return response;
    } catch (error: any) {
      console.error('AuthSlice: Login failed', error);
      return rejectWithValue(error.response?.data?.message || '登录失败');
    }
  }
);

// 注册异步thunk
export const register = createAsyncThunk(
  'auth/register',
  async (data: { username: string; email: string; phone_number?: string; password: string }, { rejectWithValue }) => {
    try {
      console.log('AuthSlice: Attempting to register new user');
      const response = await AuthService.register(data);
      console.log('AuthSlice: Registration successful');
      return response;
    } catch (error: any) {
      console.error('AuthSlice: Registration failed', error);
      return rejectWithValue(error.response?.data?.message || '注册失败');
    }
  }
);

// 获取当前用户异步thunk
export const getCurrentUser = createAsyncThunk(
  'auth/getCurrentUser',
  async (_, { rejectWithValue }) => {
    try {
      console.log('AuthSlice: Fetching current user data');
      return await AuthService.getCurrentUser();
    } catch (error: any) {
      console.error('AuthSlice: Failed to fetch current user', error);
      return rejectWithValue(error.response?.data?.message || '获取用户信息失败');
    }
  }
);

// 登出异步thunk
export const logout = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      console.log('AuthSlice: User logging out');
      AuthService.logout();
      console.log('AuthSlice: Logout completed successfully');
      return;
    } catch (error: any) {
      console.error('AuthSlice: Logout failed', error);
      // 即使API调用失败，也清除本地认证状态
      AuthService.clearAuth();
      return rejectWithValue(error.response?.data?.message || '登出失败');
    }
  }
);

// 创建认证切片
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    // 清除认证状态（用于应用重启时）
    clearAuth: (state) => {
      state.isAuthenticated = false;
      state.user = null;
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // 登录处理
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        console.log('AuthSlice: Authentication state updated with user data from server');
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // 注册处理
      .addCase(register.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state, action) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // 获取当前用户处理
      .addCase(getCurrentUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getCurrentUser.fulfilled, (state, action) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload;
        console.log('AuthSlice: Current user data updated from server');
      })
      .addCase(getCurrentUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
        // 如果获取用户信息失败，可能是token过期，清除认证状态
        state.isAuthenticated = false;
        state.user = null;
        AuthService.clearAuth();
      })
      // 登出处理
      .addCase(logout.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(logout.fulfilled, (state) => {
        state.loading = false;
        state.isAuthenticated = false;
        state.user = null;
      })
      .addCase(logout.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
        // 确保状态被清除
        state.isAuthenticated = false;
        state.user = null;
      });
  },
});

export const { clearError, clearAuth } = authSlice.actions;

export default authSlice.reducer;
