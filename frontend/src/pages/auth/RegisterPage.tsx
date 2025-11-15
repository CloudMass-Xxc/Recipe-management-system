import React from 'react';
import { Box, Typography, Container } from '@mui/material';
import RegisterForm from '../../components/auth/RegisterForm';

const RegisterPage: React.FC = () => {
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
            创建新账号
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            加入我们，发现美味食谱和AI烹饪助手
          </Typography>
        </Box>
        <RegisterForm />
      </Box>
    </Container>
  );
};

export default RegisterPage;