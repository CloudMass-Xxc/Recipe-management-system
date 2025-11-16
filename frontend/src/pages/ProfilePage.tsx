import React from 'react';
import { Container, Typography, Box, Avatar, Button, Paper, Card, CardContent, Divider } from '@mui/material';
import { useAppSelector, useAppDispatch } from '../redux/hooks';
import { logout } from '../redux/slices/authSlice';
import { useNavigate } from 'react-router-dom';

const ProfilePage: React.FC = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { user } = useAppSelector((state) => state.auth);
  const { favorites } = useAppSelector((state) => state.recipes);

  // 模拟用户数据
  const userData = user || {
    id: '1',
    username: '测试用户',
    email: 'test@example.com',
  };

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  const handleEditProfile = () => {
    // 编辑个人资料逻辑
    console.log('编辑个人资料');
  };

  const handleGoToFavorites = () => {
    navigate('/profile/favorites');
  };

  const handleGoToMyRecipes = () => {
    navigate('/profile/my-recipes');
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 4 }}>
          <Box sx={{ width: { xs: '100%', md: '25%' } }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <Avatar 
                sx={{ width: 120, height: 120, bgcolor: '#1976d2', fontSize: '2.5rem', mb: 2 }}
              >
                {userData.username.charAt(0).toUpperCase()}
              </Avatar>
              <Typography variant="h5" component="h1" gutterBottom>
                {userData.username}
              </Typography>
              <Typography variant="body1" color="text.secondary" gutterBottom>
                {userData.email}
              </Typography>
              <Box sx={{ mt: 2, display: 'flex', gap: 1, flexDirection: 'column', width: '100%' }}>
                <Button 
                  variant="contained" 
                  fullWidth 
                  onClick={handleEditProfile}
                  sx={{ mb: 1 }}
                >
                  编辑个人资料
                </Button>
                <Button 
                  variant="outlined" 
                  fullWidth 
                  onClick={handleLogout}
                  color="error"
                >
                  退出登录
                </Button>
              </Box>
            </Box>
          </Box>
          
          <Box sx={{ width: { xs: '100%', md: '75%' } }}>
            <Typography variant="h6" component="h2" gutterBottom>
              我的数据
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2, mb: 4 }}>
              <Box sx={{ width: { xs: '100%', sm: '50%' } }}>
                <Card elevation={1} sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="subtitle1" color="text.secondary">
                      收藏的食谱
                    </Typography>
                    <Typography variant="h4">{favorites.length}</Typography>
                    <Button 
                      size="small" 
                      onClick={handleGoToFavorites}
                      sx={{ mt: 1 }}
                    >
                      查看收藏
                    </Button>
                  </CardContent>
                </Card>
              </Box>
              <Box sx={{ width: { xs: '100%', sm: '50%' } }}>
                <Card elevation={1} sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="subtitle1" color="text.secondary">
                      我的食谱
                    </Typography>
                    <Typography variant="h4">3</Typography>
                    <Button 
                      size="small" 
                      onClick={handleGoToMyRecipes}
                      sx={{ mt: 1 }}
                    >
                      查看我的食谱
                    </Button>
                  </CardContent>
                </Card>
              </Box>
            </Box>

            <Divider sx={{ mb: 3 }} />
            
            <Typography variant="h6" component="h3" gutterBottom>
              最近活动
            </Typography>
            <Box sx={{ bgcolor: '#f5f5f5', p: 2, borderRadius: 1 }}>
              <Typography variant="body2" color="text.secondary">
                最近浏览了 <strong>健康蔬菜炒饭</strong>
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                3天前收藏了 <strong>香煎三文鱼</strong>
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                上周生成了 <strong>番茄鸡蛋面</strong>
              </Typography>
            </Box>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default ProfilePage;