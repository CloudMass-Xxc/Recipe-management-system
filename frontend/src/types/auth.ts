// 用户注册请求接口
export interface UserRegister {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

// 用户登录请求接口
export interface UserLogin {
  email: string;
  password: string;
}

// 用户响应接口
export interface UserResponse {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

// Token响应接口
export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user?: UserResponse;
}

// 修改密码请求接口
export interface ChangePasswordRequest {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

// 错误响应接口
export interface ErrorResponse {
  detail?: string;
  errors?: Record<string, string[]>;
  message?: string;
}

// 用户配置文件接口
export interface UserProfile {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  profile_image?: string;
  preferences?: UserPreferences;
}

// 用户偏好设置接口
export interface UserPreferences {
  dietary_restrictions?: string[];
  favorite_cuisines?: string[];
  preferred_difficulty?: 'easy' | 'medium' | 'hard';
  meal_types?: ('breakfast' | 'lunch' | 'dinner' | 'snack' | 'dessert')[];
  exclude_ingredients?: string[];
}

// 认证状态接口
export interface AuthState {
  user: UserResponse | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}