import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, Button, Box, useMediaQuery, useTheme, Drawer, IconButton } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import FastfoodIcon from '@mui/icons-material/Fastfood';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';

const Header: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  
  const handleNavigate = (path: string) => {
    console.log('导航到路径:', path); // 调试日志
    setMobileMenuOpen(false); // 关闭移动菜单
    navigate(path); // 使用navigate进行导航
  };

  // 导航链接配置
  const navLinks = [
    { label: '首页', path: '/' },
    { label: '生成食谱', path: '/generate' },
    { label: '我的食谱', path: '/my-recipes' },
  ];

  // 用户操作链接
  const userLinks = [
    { label: '登录', path: '/login', variant: 'outlined' },
    { label: '注册', path: '/register', variant: 'contained' }
  ];

  // 移动菜单内容
  const mobileMenu = (
    <Box sx={{ width: 250, height: '100%', bgcolor: '#fff', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', p: 2, borderBottom: 1, borderColor: 'divider', bgcolor: '#1976d2' }}>
        <Typography variant="h6" sx={{ color: '#fff', fontWeight: 600 }}>菜单</Typography>
        <IconButton color="inherit" onClick={() => setMobileMenuOpen(false)}>
          <CloseIcon />
        </IconButton>
      </Box>
      <Box sx={{ p: 2, display: 'flex', flexDirection: 'column', gap: 2, flex: 1 }}>
        {navLinks.map((link, index) => (
          <Button 
            key={index} 
            component={Link} 
            to={link.path}
            onClick={() => setMobileMenuOpen(false)}
            sx={{ 
              justifyContent: 'flex-start',
              textTransform: 'none',
              fontWeight: 500,
              color: '#333',
              '&:hover': { bgcolor: 'rgba(0,0,0,0.05)' }
            }}
          >
            {link.label}
          </Button>
        ))}
      </Box>
      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider', display: 'flex', flexDirection: 'column', gap: 2 }}>
        {userLinks.map((link, index) => (
          <Button 
            key={index} 
            component={Link} 
            to={link.path}
            onClick={() => setMobileMenuOpen(false)}
            variant={link.variant}
            fullWidth
            sx={{
              textTransform: 'none',
              fontWeight: 500,
              ...(link.variant === 'outlined' && { 
                borderColor: '#1976d2',
                color: '#1976d2',
                '&:hover': { 
                  borderColor: '#1565c0',
                  color: '#1565c0'
                }
              }),
              ...(link.variant === 'contained' && { 
                bgcolor: '#1976d2',
                '&:hover': { bgcolor: '#1565c0' }
              })
            }}
          >
            {link.label}
          </Button>
        ))}
      </Box>
    </Box>
  );

  return (
    <>
      <AppBar 
        position="fixed" 
        sx={{
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          bgcolor: '#1976d2',
          zIndex: theme.zIndex.drawer + 1
        }}
      >
        <Toolbar sx={{ px: { xs: 2, sm: 4 }, justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <FastfoodIcon sx={{ color: '#fff' }} />
            <Typography 
              variant="h5" 
              component="div" 
              sx={{
                fontWeight: 600,
                letterSpacing: '0.02em',
                color: '#fff',
                // 响应式字体大小，屏幕越小字体越小
                fontSize: {
                  xs: '1rem',     // 超小屏幕（<600px）
                  sm: '1.1rem',   // 小屏幕（600px-960px）
                  md: '1.2rem',   // 中等屏幕（960px-1280px）
                  lg: '1.3rem',   // 大屏幕（1280px-1920px）
                  xl: '1.4rem'    // 超大屏幕（>1920px）
                },
                // 确保标题始终可见
                whiteSpace: 'nowrap',
                display: 'block'
              }}
            >
              个性化食谱管理系统
            </Typography>
          </Box>
          
          {/* 移动端菜单按钮 */}
          {isMobile && (
            <IconButton 
              color="inherit" 
              edge="end" 
              onClick={() => setMobileMenuOpen(true)}
              sx={{ mr: 1 }}
            >
              <MenuIcon />
            </IconButton>
          )}
          
          {/* 平板和桌面端导航 */}
          {!isMobile && (
            <Box sx={{ display: 'flex', gap: isTablet ? 1 : 2, alignItems: 'center' }}>
              {navLinks.map((link, index) => (
                <Button 
                  key={index}
                  color="inherit" 
                  component={Link} 
                  to={link.path}
                  sx={{ 
                    textTransform: 'none',
                    fontWeight: 500,
                    display: { xs: 'none', sm: 'inline-flex' },
                    '&:hover': { bgcolor: 'rgba(255,255,255,0.15)' }
                  }}
                >
                  {link.label}
                </Button>
              ))}
              {userLinks.map((link, index) => (
                <Button 
                  key={index}
                  color="inherit" 
                  component={Link} 
                  to={link.path}
                  variant={link.variant}
                  size={isTablet ? "small" : "medium"}
                  sx={{ 
                    textTransform: 'none',
                    borderColor: link.variant === 'outlined' ? 'white' : 'transparent',
                    color: 'white',
                    minWidth: { xs: 60, sm: 'auto' },
                    '&:hover': { 
                      ...(link.variant === 'outlined' && { 
                        borderColor: 'rgba(255,255,255,0.8)',
                        bgcolor: 'rgba(255,255,255,0.1)' 
                      }),
                      ...(link.variant === 'contained' && { 
                        bgcolor: 'rgba(255,255,255,0.3)' 
                      })
                    }
                  }}
                >
                  {link.label}
                </Button>
              ))}
            </Box>
          )}
        </Toolbar>
      </AppBar>
      
      {/* 移动端抽屉菜单 */}
      <Drawer
        anchor="right"
        open={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
      >
        {mobileMenu}
      </Drawer>
    </>
  );
};

export default Header;