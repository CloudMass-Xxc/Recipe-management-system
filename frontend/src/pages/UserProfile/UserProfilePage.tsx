import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Avatar, TextField, Button, CircularProgress, Alert, Snackbar } from '@mui/material';
import { Edit, Close } from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { fetchProfile, updateProfile, clearError } from '../../store/slices/userSlice';
import type { RootState, AppDispatch } from '../../store';
import Layout from '../../components/layout/Layout';
import useAuth from '../../hooks/useAuth';

const UserProfilePage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { profile, loading, error } = useSelector((state: RootState) => state.user);
  const { isAuthenticated, user: authUser } = useAuth();
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error' | 'warning' | 'info'>('info');

  // 显示通知
  const showSnackbar = (message: string, severity: 'success' | 'error' | 'warning' | 'info' = 'info') => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setSnackbarOpen(true);
  };

  // 关闭通知
  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  // 在组件挂载时获取用户资料
  useEffect(() => {
    console.log('UserProfilePage 组件挂载，认证状态:', isAuthenticated);
    console.log('认证用户信息:', authUser);
    console.log('Redux 用户资料:', profile);
    
    if (isAuthenticated) {
      console.log('用户已认证，正在获取用户资料...');
      dispatch(fetchProfile());
    } else {
      console.log('用户未认证，无法获取用户资料');
      showSnackbar('请先登录以查看个人资料', 'warning');
    }
  }, [dispatch, isAuthenticated]);

  // 监听错误状态变化
  useEffect(() => {
    if (error) {
      console.error('获取用户资料错误:', error);
      showSnackbar(error, 'error');
    }
  }, [error]);

  // 表单状态管理 - 初始值优先使用authUser，然后是profile
  const [formData, setFormData] = React.useState({
    username: profile?.username || authUser?.username || '',
    email: profile?.email || authUser?.email || '',
    phone: profile?.phone || authUser?.phone || '',
    bio: profile?.bio || ''
  });

  // 当profile或authUser变化时更新表单数据
  React.useEffect(() => {
    // 优先使用profile数据，如果没有则使用authUser
    const userData = profile || authUser;
    if (userData) {
      console.log('用户资料更新，更新表单数据:', userData);
      setFormData({
        username: userData.username || '',
        email: userData.email || '',
        phone: userData.phone || '',
        bio: profile?.bio || ''
      });
      showSnackbar('用户资料加载成功', 'success');
    }
  }, [profile, authUser]);

  // 处理表单输入变化
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // 处理表单提交
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(updateProfile(formData));
  };

  return (
    <Layout>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" sx={{ fontWeight: 'bold', color: '#333', mb: 1 }}>
          个人资料
        </Typography>
        <Typography variant="body1" color="text.secondary">
          查看和编辑您的个人信息
        </Typography>
        
        {/* 认证状态指示器 */}
        <Alert 
          severity={isAuthenticated ? "success" : "warning"} 
          sx={{ mt: 2, mb: 3 }}
        >
          当前认证状态: {isAuthenticated ? '已认证' : '未认证'}
          {authUser && ` (用户ID: ${authUser.user_id})`}
        </Alert>
      </Box>

      {/* 错误提示 */}
      {error && (
        <Alert severity="error" sx={{ mb: 3, display: 'flex', alignItems: 'center' }}>
          {error}
          <Button
            startIcon={<Close />}
            onClick={() => dispatch(clearError())}
            sx={{ ml: 2, p: 0, minWidth: 0 }}
          />
        </Alert>
      )}

      {/* 加载状态 */}
      {loading && !profile ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '300px' }}>
          <CircularProgress />
          <Typography variant="h6" sx={{ ml: 2 }}>加载用户资料中...</Typography>
        </Box>
      ) : (
        !isAuthenticated ? (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h5" color="text.secondary" sx={{ mb: 2 }}>
              请先登录以查看个人资料
            </Typography>
            <Button 
              variant="contained" 
              onClick={() => window.location.href = '/login'}
              sx={{ backgroundColor: '#4caf50' }}
            >
              前往登录
            </Button>
          </Box>
        ) : (
        <Box>
          <Paper sx={{ p: 4, borderRadius: 2 }}>
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 4 }}>
              {/* 左侧：头像和基本信息 */}
              <Box sx={{ flex: '1 1 100%', md: '0 0 30%' }}>
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 4 }}>
                  <Avatar sx={{ width: 120, height: 120, bgcolor: '#4caf50', fontSize: '3rem' }}>
                    {profile?.username?.charAt(0) || 'U'}
                  </Avatar>
                  <Typography variant="h5" sx={{ mt: 2, fontWeight: 'bold' }}>
                    {profile?.username || '用户名'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {profile?.email || 'user@example.com'}
                  </Typography>
                  <Button
                    variant="outlined"
                    startIcon={<Edit />}
                    sx={{ mt: 3, borderRadius: 2 }}
                  >
                    更换头像
                  </Button>
                </Box>
              </Box>

              {/* 右侧：详细信息和编辑表单 */}
              <Box sx={{ flex: '1 1 100%', md: '0 0 70%' }}>
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 3 }}>
                  个人信息
                </Typography>
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
                  <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)' }, gap: 3 }}>
                    <Box>
                      <TextField
                        fullWidth
                        label="用户名"
                        name="username"
                        value={formData.username}
                        onChange={handleInputChange}
                        sx={{ '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
                      />
                    </Box>
                    <Box>
                      <TextField
                        fullWidth
                        label="邮箱"
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        sx={{ '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
                      />
                    </Box>
                    <Box>
                      <TextField
                        fullWidth
                        label="电话"
                        name="phone"
                        type="tel"
                        value={formData.phone}
                        onChange={handleInputChange}
                        sx={{ '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
                      />
                    </Box>
                    <Box sx={{ gridColumn: '1 / -1' }}>
                      <TextField
                        fullWidth
                        label="简介"
                        name="bio"
                        multiline
                        rows={4}
                        value={formData.bio}
                        onChange={handleInputChange}
                        sx={{ '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
                      />
                    </Box>
                    <Box sx={{ gridColumn: '1 / -1' }}>
                      <Button
                        variant="contained"
                        type="submit"
                        sx={{ backgroundColor: '#4caf50', borderRadius: 2, textTransform: 'none', px: 4 }}
                      >
                        保存修改
                      </Button>
                    </Box>
                  </Box>
                </Box>
              </Box>
            </Box>
          </Paper>

          {/* 最近访问的食谱 */}
          <Paper sx={{ p: 4, borderRadius: 2, mt: 4 }}>
            <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 3 }}>
              最近访问的食谱
            </Typography>
            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)', md: 'repeat(3, 1fr)' }, gap: 3 }}>
              {/* 模拟数据 - 实际项目中应从API获取 */}
              {[1, 2, 3].map((item) => (
                <Box key={item} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, cursor: 'pointer', transition: 'all 0.3s ease', '&:hover': { boxShadow: '0 2px 8px rgba(0,0,0,0.1)' } }}>
                  <Box sx={{ width: '100%', height: 120, bgcolor: '#f5f5f5', borderRadius: 1, mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Typography variant="h4" color="text.secondary">🍳</Typography>
                  </Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                    食谱名称 {item}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    最近访问于 {new Date().toLocaleDateString()}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" color="text.secondary">⏱️</Typography>
                      <Typography variant="body2">30分钟</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" color="text.secondary">⭐</Typography>
                      <Typography variant="body2">4.5</Typography>
                    </Box>
                  </Box>
                </Box>
              ))}
            </Box>
          </Paper>

          {/* 最近生成的食谱 */}
          <Paper sx={{ p: 4, borderRadius: 2, mt: 4 }}>
            <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 3 }}>
              最近生成的食谱
            </Typography>
            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)', md: 'repeat(3, 1fr)' }, gap: 3 }}>
              {/* 模拟数据 - 实际项目中应从API获取 */}
              {[1, 2, 3].map((item) => (
                <Box key={item} sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 2, cursor: 'pointer', transition: 'all 0.3s ease', '&:hover': { boxShadow: '0 2px 8px rgba(0,0,0,0.1)' } }}>
                  <Box sx={{ width: '100%', height: 120, bgcolor: '#f5f5f5', borderRadius: 1, mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Typography variant="h4" color="text.secondary">🍝</Typography>
                  </Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                    生成食谱 {item}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    生成于 {new Date().toLocaleDateString()}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" color="text.secondary">👥</Typography>
                      <Typography variant="body2">2人份</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" color="text.secondary">🔥</Typography>
                      <Typography variant="body2">中热量</Typography>
                    </Box>
                  </Box>
                </Box>
              ))}
            </Box>
          </Paper>
        </Box>
        )
      )}

      {/* 通知 */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleSnackbarClose} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Layout>
  );
};

export default UserProfilePage;
