import React from 'react';
import { Box, Typography, Container } from '@mui/material';
import LoginForm from '../../components/auth/LoginForm';

const LoginPage: React.FC = () => {
  return (
    <Container component="main" maxWidth="lg">
      <Box sx={{ 
        minHeight: '100vh', 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        justifyContent: 'center',
        py: 8
      }}>
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom>
            欢迎回来
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            登录以使用个性化食谱推荐和AI生成功能
          </Typography>
        </Box>
        <LoginForm />
      </Box>
    </Container>
  );
};

export default LoginPage;