import React, { useState } from 'react';
import { Box, Button, Container, Paper, Typography, TextField, useMediaQuery, useTheme, Snackbar, Alert } from '@mui/material';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch } from '../redux/hooks';
import { register } from '../redux/slices/authSlice';

interface RegisterFormValues {
  username: string;
  email: string;
  phone: string;
  password: string;
  confirmPassword: string;
}

const RegisterSchema = Yup.object().shape({
  username: Yup.string().required('用户名不能为空').min(3, '用户名至少3个字符'),
  email: Yup.string().email('邮箱格式不正确').required('邮箱不能为空'),
  phone: Yup.string()
    .matches(/^1[3-9]\d{9}$/, '请输入有效的手机号')
    .required('手机号不能为空'),
  password: Yup.string()
    .min(8, '密码至少8个字符')
    .matches(/^(?=.*[a-z])/, '密码必须包含至少一个小写字母')
    .matches(/^(?=.*[A-Z])/, '密码必须包含至少一个大写字母')
    .matches(/^(?=.*[!@#$%^&*(),.?":{}|<>])/, '密码必须包含至少一个特殊字符')
    .matches(/^(?=\S+$)/, '密码不能包含空格')
    .matches(/^(?!.*password|.*123456|.*qwerty|.*admin|.*user)/i, '密码不能包含常见密码模式')
    .required('密码不能为空'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password'), undefined], '两次密码输入不一致')
    .required('请确认密码'),
});

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const dispatch = useAppDispatch();
  const [loading, setLoading] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState<0 | 1 | 2 | 3 | 4>(0);
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: 'error' | 'success';
  }>({ open: false, message: '', severity: 'error' });

  // 计算密码强度的函数
  const calculatePasswordStrength = (password: string): 0 | 1 | 2 | 3 | 4 => {
    let strength = 0;
    
    // 长度检查
    if (password.length >= 8) strength++;
    
    // 包含小写字母
    if (/[a-z]/.test(password)) strength++;
    
    // 包含大写字母
    if (/[A-Z]/.test(password)) strength++;
    
    // 包含特殊字符
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;
    
    // 不包含常见密码模式
    if (!/password|123456|qwerty|admin|user/i.test(password)) strength++;
    
    return Math.min(strength, 4) as 0 | 1 | 2 | 3 | 4;
  };

  const getStrengthText = (strength: number): string => {
    switch (strength) {
      case 0:
        return '';
      case 1:
        return '非常弱';
      case 2:
        return '弱';
      case 3:
        return '中等';
      case 4:
        return '强';
      default:
        return '';
    }
  };

  const getStrengthColor = (strength: number): string => {
    switch (strength) {
      case 0:
        return '#d3d3d3';
      case 1:
        return '#ff4d4f';
      case 2:
        return '#faad14';
      case 3:
        return '#52c41a';
      case 4:
        return '#1890ff';
      default:
        return '#d3d3d3';
    }
  };

  const handleSubmit = async (values: RegisterFormValues) => {
    setLoading(true);
    try {
      await dispatch(register({
        username: values.username,
        email: values.email,
        phone: values.phone,
        password: values.password,
        display_name: values.username,
        diet_preferences: [],
      })).unwrap();

      setSnackbar({
        open: true,
        message: '注册成功！即将跳转到首页',
        severity: 'success'
      });
      
      // 延迟跳转，让用户看到成功消息
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (error) {
      console.error('注册失败:', error);
      setSnackbar({
        open: true,
        message: '注册失败: ' + (error instanceof Error ? error.message : '未知错误'),
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };
  
  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <Container maxWidth="sm" sx={{ my: { xs: 6, sm: 8 }, px: { xs: 2, sm: 3 } }}>
      <Paper elevation={3} sx={{ p: { xs: 3, sm: 4 } }}>
          <Typography variant={isMobile ? "h6" : "h4"} component="h1" align="center" sx={{ mb: { xs: 3, sm: 4 } }}>
            注册
          </Typography>
          <Formik
            initialValues={{
              username: '',
              email: '',
              phone: '',
              password: '',
              confirmPassword: '',
            }}
            validationSchema={RegisterSchema}
            onSubmit={handleSubmit}
          >
            {({ errors, touched }) => (
              <Form>
                <Box sx={{ mb: 3 }}>
                  <Field
                    as={TextField}
                    fullWidth
                    label="用户名"
                    name="username"
                    error={touched.username && !!errors.username}
                    helperText={touched.username && errors.username}
                    variant="outlined"
                    margin={isMobile ? "dense" : "normal"}
                    size={isMobile ? "small" : "medium"}
                  />
                </Box>
                {/* 邮箱输入框 */}
                <Box sx={{ mb: 3 }}>
                  <Field
                    as={TextField}
                    fullWidth
                    label="邮箱"
                    name="email"
                    type="email"
                    error={touched.email && !!errors.email}
                    helperText={touched.email && errors.email}
                    variant="outlined"
                    margin={isMobile ? "dense" : "normal"}
                    size={isMobile ? "small" : "medium"}
                  />
                </Box>
                
                {/* 手机号输入框 */}
                <Box sx={{ mb: 3 }}>
                  <Field
                    as={TextField}
                    fullWidth
                    label="手机号"
                    name="phone"
                    type="tel"
                    error={touched.phone && !!errors.phone}
                    helperText={touched.phone && errors.phone}
                    variant="outlined"
                    margin={isMobile ? "dense" : "normal"}
                    size={isMobile ? "small" : "medium"}
                  />
                </Box>
                
                {/* 密码输入框 */}
                <Box sx={{ mb: 3 }}>
                  <Field name="password">
                    {({ field, form }: { field: any; form: any }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="密码"
                        type="password"
                        error={touched.password && !!errors.password}
                        helperText={touched.password && errors.password}
                        variant="outlined"
                        margin={isMobile ? 'dense' : 'normal'}
                        size={isMobile ? 'small' : 'medium'}
                        onChange={(e) => {
                          form.setFieldValue('password', e.target.value);
                          setPasswordStrength(calculatePasswordStrength(e.target.value));
                        }}
                      />
                    )}
                  </Field>
                  {passwordStrength > 0 && (
                    <Box sx={{ mt: 1 }}>
                      <Box 
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: 1,
                          '& > div': {
                            height: 4,
                            borderRadius: 2,
                            transition: 'all 0.3s ease'
                          }
                        }}
                      >
                        {[0, 1, 2, 3].map((index) => (
                          <Box
                            key={index}
                            sx={{
                              width: '25%',
                              backgroundColor: index < passwordStrength - 1 
                                ? getStrengthColor(passwordStrength)
                                : '#e0e0e0'
                            }}
                          />
                        ))}
                      </Box>
                      <Typography 
                        variant="caption" 
                        sx={{ 
                          display: 'block', 
                          mt: 0.5,
                          color: getStrengthColor(passwordStrength)
                        }}
                      >
                        密码强度: {getStrengthText(passwordStrength)}
                      </Typography>
                    </Box>
                  )}
                  <Typography variant="caption" sx={{ display: 'block', mt: 0.5, color: 'text.secondary' }}>
                    密码要求: 至少8个字符，包含大小写字母、特殊字符，不含常见模式
                  </Typography>
                </Box>
                <Box sx={{ mb: 3 }}>
                  <Field
                    as={TextField}
                    fullWidth
                    label="确认密码"
                    name="confirmPassword"
                    type="password"
                    error={touched.confirmPassword && !!errors.confirmPassword}
                    helperText={touched.confirmPassword && errors.confirmPassword}
                    variant="outlined"
                    margin={isMobile ? "dense" : "normal"}
                    size={isMobile ? "small" : "medium"}
                  />
                </Box>
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ py: 1.5, mt: { xs: 2, sm: 3 }, mb: { xs: 1, sm: 2 } }}
                  size={isMobile ? "small" : "medium"}
                  disabled={loading}
                >
                  {loading ? '注册中...' : '注册'}
                </Button>
              </Form>
            )}
          </Formik>
          <Typography align="center" sx={{ mt: 3 }}>
            已有账号？ <Button component="a" href="/login">立即登录</Button>
          </Typography>
          
          {/* 错误/成功提示 */}
          <Snackbar
            open={snackbar.open}
            autoHideDuration={6000}
            onClose={handleCloseSnackbar}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          >
            <Alert
              onClose={handleCloseSnackbar}
              severity={snackbar.severity}
              sx={{ width: '100%' }}
              variant="filled"
            >
              {snackbar.message}
            </Alert>
          </Snackbar>
        </Paper>
      </Container>
  );
};

export default RegisterPage;