import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import AuthAPI from '../services/authAPI';
import { setAuthStatus } from '../redux/slices/authSlice'; // 导入单独创建的action

const AuthInitializer = ({ children }: { children: React.ReactNode }) => {
  const dispatch = useDispatch();

  useEffect(() => {
    // 检查localStorage中是否有token
    const checkAuthStatus = async () => {
      try {
        // 使用AuthAPI的isAuthenticated方法检查是否已登录
        const isLoggedIn = AuthAPI.isAuthenticated();
        
        if (isLoggedIn) {
          // 如果已登录，尝试获取当前用户信息
          try {
            const user = await AuthAPI.getCurrentUser();
            // 更新Redux状态为已认证，并设置用户信息
            dispatch(setAuthStatus({ isAuthenticated: true, user }));
            console.log('已恢复登录状态:', user);
          } catch (error) {
            // 如果获取用户信息失败，清除token并重置状态
            AuthAPI.logout();
            console.log('登录状态验证失败，已清除无效token');
          }
        }
      } catch (error) {
        console.error('检查认证状态失败:', error);
      }
    };

    checkAuthStatus();
  }, [dispatch]);

  return <>{children}</>;
};

export default AuthInitializer;