import { useState, useCallback, useContext, createContext, ReactNode, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthService from '../services/auth.service';
import { setToLocalStorage, removeFromLocalStorage, getFromLocalStorage } from '../utils/localStorage';

// 直接在文件中定义所有需要的接口，避免导入问题
interface LoginData {
  username: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  phone: string;
  password: string;
}

interface TokenResponse {
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

interface AuthResponse {
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

interface User {
  user_id: string;
  username: string;
  email: string;
  phone: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
  login: (loginData: LoginData) => Promise<void>;
  register: (registerData: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
  isAuthenticated: boolean;
}

// 创建认证上下文
const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

// 认证提供者组件
export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  // 初始化时检查认证状态
  useEffect(() => {
    const initAuth = async () => {
      setLoading(true);
      try {
        // 从存储中获取令牌和用户信息
        const storedToken = sessionStorage.getItem('access_token');
        const storedUser = localStorage.getItem('user');
        
        console.log('从存储中获取的令牌:', storedToken);
        console.log('从存储中获取的用户信息:', storedUser);
        
        if (storedToken && storedUser) {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
          
          // 验证令牌是否有效
          try {
            // 尝试获取用户资料，验证令牌是否有效
            const userData = await AuthService.getCurrentUser();
            if (userData) {
              setUser(userData);
            }
          } catch (error) {
            console.error('验证令牌失败，清除认证状态:', error);
            // 清除认证状态
            setToken(null);
            setUser(null);
            localStorage.removeItem('user');
            localStorage.removeItem('refresh_token');
            sessionStorage.removeItem('access_token');
          }
        } else {
          // 没有令牌或用户信息，清除认证状态
          setToken(null);
          setUser(null);
          localStorage.removeItem('user');
          localStorage.removeItem('refresh_token');
          sessionStorage.removeItem('access_token');
        }
      } catch (error) {
        console.error('检查认证状态时发生错误:', error);
        setToken(null);
        setUser(null);
        localStorage.removeItem('user');
        localStorage.removeItem('refresh_token');
        sessionStorage.removeItem('access_token');
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  // 清除错误
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // 登录
  const login = useCallback(async (loginData: LoginData) => {
    setLoading(true);
    setError(null);

    try {
      const authResponse = await AuthService.login(loginData);
      
      // 检查响应数据
      if (!authResponse || !authResponse.success) {
        throw new Error('登录失败: ' + (authResponse?.message || '无效的登录响应'));
      }
      
      // 从存储中获取最新的用户信息和令牌
      const storedToken = sessionStorage.getItem('access_token');
      const storedUser = localStorage.getItem('user');
      
      if (storedToken && storedUser) {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      } else {
        throw new Error('登录成功但未获取到认证信息');
      }
      
      navigate('/');
    } catch (err: any) {
      // 处理AuthService抛出的错误信息
      setError(err.message || '登录失败，请检查用户名和密码');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [navigate]);

  // 注册
  const register = useCallback(async (registerData: RegisterData) => {
    setLoading(true);
    setError(null);

    try {
      const authResponse = await AuthService.register(registerData);
      
      // 检查响应数据
      if (!authResponse || !authResponse.success) {
        throw new Error('注册失败: ' + (authResponse?.message || '无效的注册响应'));
      }
      
      // 从存储中获取最新的用户信息和令牌
      const storedToken = sessionStorage.getItem('access_token');
      const storedUser = localStorage.getItem('user');
      
      if (storedToken && storedUser) {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      } else {
        throw new Error('注册成功但未获取到认证信息');
      }
      
      navigate('/');
    } catch (err: any) {
      // 处理AuthService抛出的错误信息
      setError(err.message || '注册失败，请稍后重试');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [navigate]);

  // 登出
  const logout = useCallback(async () => {
    setLoading(true);

    try {
      await AuthService.logout();
    } catch (err) {
      console.error('登出失败:', err);
    } finally {
      setUser(null);
      setToken(null);
      // 清除存储中的认证数据
      localStorage.removeItem('user');
      localStorage.removeItem('refresh_token');
      sessionStorage.removeItem('access_token');
      setLoading(false);
      navigate('/login');
    }
  }, [navigate]);

  const value = {
    user,
    token,
    loading,
    error,
    login,
    register,
    logout,
    clearError,
    isAuthenticated: !!user && !!token,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// useAuth hook
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
};

export default useAuth;