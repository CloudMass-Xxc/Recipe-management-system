import React from 'react';
import { Box, TextField, Button, Typography, Container, Paper, useMediaQuery, useTheme } from '@mui/material';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useNavigate } from 'react-router-dom';

interface LoginFormValues {
  username: string;
  password: string;
}

const LoginSchema = Yup.object().shape({
  username: Yup.string().required('用户名不能为空'),
  password: Yup.string().required('密码不能为空'),
});

const LoginPage: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();

  const handleSubmit = async (values: LoginFormValues) => {
    try {
      // 模拟登录请求
      console.log('登录请求:', values);
      // 这里将在配置API服务后替换为实际的登录API调用
      navigate('/');
    } catch (error) {
      console.error('登录失败:', error);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ my: { xs: 6, sm: 8 }, px: { xs: 2, sm: 3 } }}>
        <Paper elevation={3} sx={{ p: { xs: 3, sm: 4 } }}>
          <Typography variant={isMobile ? "h6" : "h4"} component="h1" align="center" sx={{ mb: { xs: 3, sm: 4 } }}>
            登录
          </Typography>
          <Formik
            initialValues={{ username: '', password: '' }}
            validationSchema={LoginSchema}
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
                <Box sx={{ mb: 3 }}>
                  <Field
                    as={TextField}
                    fullWidth
                    label="密码"
                    name="password"
                    type="password"
                    error={touched.password && !!errors.password}
                    helperText={touched.password && errors.password}
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
                >
                  登录
                </Button>
              </Form>
            )}
          </Formik>
          <Typography align="center" sx={{ mt: 3 }}>
            还没有账号？ <Button component="a" href="/register">立即注册</Button>
          </Typography>
        </Paper>
      </Container>
  );
};

export default LoginPage;