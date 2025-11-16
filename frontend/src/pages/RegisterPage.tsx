import React from 'react';
import { Box, Button, Container, Paper, Typography, TextField, useMediaQuery, useTheme } from '@mui/material';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useNavigate } from 'react-router-dom';

interface RegisterFormValues {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const RegisterSchema = Yup.object().shape({
  username: Yup.string().required('用户名不能为空').min(3, '用户名至少3个字符'),
  email: Yup.string().email('邮箱格式不正确').required('邮箱不能为空'),
  password: Yup.string().min(6, '密码至少6个字符').required('密码不能为空'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password'), undefined], '两次密码输入不一致')
    .required('请确认密码'),
});

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const handleSubmit = async (values: RegisterFormValues) => {
    try {
      // 模拟注册请求
      console.log('注册请求:', values);
      // 这里将在配置API服务后替换为实际的注册API调用
      navigate('/login');
    } catch (error) {
      console.error('注册失败:', error);
    }
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
                >
                  注册
                </Button>
              </Form>
            )}
          </Formik>
          <Typography align="center" sx={{ mt: 3 }}>
            已有账号？ <Button component="a" href="/login">立即登录</Button>
          </Typography>
        </Paper>
      </Container>
  );
};

export default RegisterPage;