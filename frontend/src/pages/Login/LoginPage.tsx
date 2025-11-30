import React, { useState } from 'react';
import { Box, Container, Paper, Typography, TextField, Button, Alert, Link } from '@mui/material';
import { LockOutlined, AccountCircleOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, loading, error, clearError } = useAuth();
  const [formData, setFormData] = useState({
    identifier: '',
    password: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    clearError();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(formData);
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
            <LockOutlined sx={{ fontSize: 40, color: '#4caf50' }} />
          </Box>
          <Typography component="h1" variant="h5" sx={{ textAlign: 'center', mb: 3, fontWeight: 'bold' }}>
            登录
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {typeof error === 'string' ? error : JSON.stringify(error)}
            </Alert>
          )}
          
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="identifier"
              label="手机号/邮箱/用户名"
              name="identifier"
              autoComplete="username"
              autoFocus
              value={formData.identifier}
              onChange={handleChange}
              slotProps={{
                input: {
                  startAdornment: <AccountCircleOutlined sx={{ mr: 1, color: 'action.active' }} />,
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
              autoComplete="current-password"
              value={formData.password}
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
              {loading ? '登录中...' : '登录'}
            </Button>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
              <Box>
                <Link href="#" variant="body2" sx={{ color: '#4caf50' }}>
                  忘记密码?
                </Link>
              </Box>
              <Box>
                <Link href="/register" variant="body2" sx={{ color: '#4caf50', fontWeight: 'bold' }}>
                  没有账号? 注册
                </Link>
              </Box>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default LoginPage;
