import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, useMediaQuery, Button, Box, Avatar, Menu, MenuItem, CircularProgress } from '@mui/material';
import { Menu as MenuIcon, AccountCircle } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../hooks/useAuth';

interface HeaderProps {
  onSidebarToggle?: () => void;
}

const Header: React.FC<HeaderProps> = ({ onSidebarToggle }) => {
  const navigate = useNavigate();
  const isMobile = useMediaQuery('(max-width:600px)');
  const { user, isAuthenticated, loading, logout } = useAuth();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = async () => {
    await logout();
    handleMenuClose();
  };

  return (
    <AppBar position="static" sx={{ backgroundColor: '#4caf50' }}>
      <Toolbar>
        {/* 只在移动设备上显示侧边栏切换按钮 */}
        {isMobile && (
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={onSidebarToggle}
          >
            <MenuIcon />
          </IconButton>
        )}
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          个性化食谱管理系统
        </Typography>
        
        {/* 登录和注册按钮或用户信息 */}
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', justifyContent: 'flex-end' }}>
          {loading ? (
            <CircularProgress size={24} color="inherit" sx={{ mr: 1 }} />
          ) : !isAuthenticated ? (
            <>
              <Button 
                variant="text" 
                color="inherit" 
                onClick={() => navigate('/login')}
                sx={{
                  textTransform: 'none',
                  fontWeight: 600,
                  fontSize: { xs: '0.875rem', md: '1rem' },
                  '&:hover': {
                    backgroundColor: 'rgba(255,255,255,0.1)',
                    borderRadius: 2,
                  },
                }}
              >
                登录
              </Button>
              <Button 
                variant="contained" 
                onClick={() => navigate('/register')}
                sx={{
                  backgroundColor: 'white',
                  color: '#4caf50',
                  textTransform: 'none',
                  fontWeight: 600,
                  fontSize: { xs: '0.875rem', md: '1rem' },
                  borderRadius: 2,
                  '&:hover': {
                    backgroundColor: '#f5f5f5',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                    transform: 'translateY(-1px)',
                  },
                  transition: 'all 0.2s ease',
                }}
              >
                注册
              </Button>
            </>
          ) : (
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              {!isMobile && user?.username && (
                <Typography 
                  variant="body1" 
                  color="inherit" 
                  sx={{
                    fontWeight: 600,
                    mr: 1,
                    display: { xs: 'none', md: 'block' },
                  }}
                >
                  {user.username}
                </Typography>
              )}
              <IconButton
                size="large"
                edge="end"
                color="inherit"
                aria-label="user menu"
                onClick={handleMenuClick}
                sx={{
                  '&:hover': {
                    backgroundColor: 'rgba(255,255,255,0.1)',
                    borderRadius: '50%',
                  },
                }}
              >
                {user?.username ? (
                  <Avatar sx={{ bgcolor: '#fff', color: '#4caf50' }}>
                    {user.username.charAt(0).toUpperCase()}
                  </Avatar>
                ) : (
                  <AccountCircle />
                )}
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
                keepMounted
                transformOrigin={{ vertical: 'top', horizontal: 'right' }}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
              >
                <MenuItem onClick={() => { navigate('/profile'); handleMenuClose(); }}>个人中心</MenuItem>
                <MenuItem onClick={() => { navigate('/favorites'); handleMenuClose(); }}>我的收藏</MenuItem>
                <MenuItem onClick={() => { navigate('/dietplan'); handleMenuClose(); }}>饮食计划</MenuItem>
                <MenuItem onClick={handleLogout}>退出登录</MenuItem>
              </Menu>
            </Box>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
