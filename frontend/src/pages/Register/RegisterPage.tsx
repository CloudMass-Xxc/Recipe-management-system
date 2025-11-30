import React, { useState } from 'react';
import { Box, Container, Paper, Typography, TextField, Button, Alert, Link } from '@mui/material';
import { PersonAddOutlined, EmailOutlined, LockOutlined, PhoneOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register, loading, error, clearError } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: ''
  });
  const [formError, setFormError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    clearError();
    setFormError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      setFormError('两次输入的密码不一致');
      return;
    }
    
    try {
      await register({
        username: formData.username,
        email: formData.email,
        phone: formData.phone,
        password: formData.password
      });
      navigate('/');
    } catch {
      // Error is handled by the auth hook
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper sx={{ p: 4, borderRadius: 3, width: '100%', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
            <Button
              variant="text"
              onClick={() => navigate('/')}
              sx={{ color: '#4caf50', fontWeight: 'bold', textTransform: 'none' }}
            >
              ← 返回主页
            </Button>
          </Box>
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
            <PersonAddOutlined sx={{ fontSize: 40, color: '#4caf50' }} />
          </Box>
          <Typography component="h1" variant="h5" sx={{ textAlign: 'center', mb: 3, fontWeight: 'bold' }}>
            注册
          </Typography>
          
          {(error || formError) && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {typeof error === 'string' ? error : JSON.stringify(error) || formError}
            </Alert>
          )}
          
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="用户名"
              name="username"
              autoComplete="username"
              autoFocus
              value={formData.username}
              onChange={handleChange}
              slotProps={{
                input: {
                  startAdornment: <PersonAddOutlined sx={{ mr: 1, color: 'action.active' }} />,
                },
              }}
              sx={{
                mb: 2,
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                },
              }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="邮箱"
              name="email"
              autoComplete="email"
              value={formData.email}
              onChange={handleChange}
              slotProps={{
                input: {
                  startAdornment: <EmailOutlined sx={{ mr: 1, color: 'action.active' }} />,
                },
              }}
              sx={{
                mb: 2,
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                },
              }}
            />
            <TextField
              margin="normal"
              fullWidth
              id="phone"
              label="手机号（选填）"
              name="phone"
              autoComplete="tel"
              value={formData.phone}
              onChange={handleChange}
              slotProps={{
                input: {
                  startAdornment: <PhoneOutlined sx={{ mr: 1, color: 'action.active' }} />,
                },
              }}
              sx={{
                mb: 2,
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                },
              }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="密码"
              type="password"
              id="password"
              autoComplete="new-password"
              value={formData.password}
              onChange={handleChange}
              slotProps={{
                input: {
                  startAdornment: <LockOutlined sx={{ mr: 1, color: 'action.active' }} />,
                },
              }}
              sx={{
                mb: 2,
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                },
              }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="confirmPassword"
              label="确认密码"
              type="password"
              id="confirmPassword"
              autoComplete="new-password"
              value={formData.confirmPassword}
              onChange={handleChange}
              slotProps={{
                input: {
                  startAdornment: <LockOutlined sx={{ mr: 1, color: 'action.active' }} />,
                },
              }}
              sx={{
                mb: 3,
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                },
              }}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={loading}
              sx={{
                mt: 3,
                mb: 2,
                padding: '10px',
                fontSize: '1rem',
                backgroundColor: '#4caf50',
                '&:hover': {
                  backgroundColor: '#388e3c',
                },
                borderRadius: 2,
                textTransform: 'none',
                fontWeight: 'bold',
              }}
            >
              {loading ? '注册中...' : '注册'}
            </Button>
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
              <Link href="/login" variant="body2" sx={{ color: '#4caf50', fontWeight: 'bold' }}>
                已有账号? 登录
              </Link>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default RegisterPage;
