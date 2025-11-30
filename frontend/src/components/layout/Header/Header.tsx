import React from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Menu, MenuItem, Avatar, Box, useMediaQuery } from '@mui/material';
import { Person, Logout, Menu as MenuIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../hooks/useAuth';

interface HeaderProps {
  onSidebarToggle?: () => void;
}

const Header: React.FC<HeaderProps> = ({ onSidebarToggle }) => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const isMobile = useMediaQuery('(max-width:600px)');

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/');
    handleMenuClose();
  };

  // 移除顶部菜单栏，只使用侧边栏导航

  if (!isAuthenticated) {
    return (
      <AppBar position="static" sx={{ backgroundColor: '#4caf50' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            个性化食谱管理系统
          </Typography>
          <Button color="inherit" onClick={() => navigate('/login')}>登录</Button>
          <Button color="inherit" onClick={() => navigate('/register')}>注册</Button>
        </Toolbar>
      </AppBar>
    );
  }

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
        
        {/* 移除桌面菜单栏 */}

        {/* 用户菜单 */}
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography variant="body2" sx={{ mr: 2, display: { xs: 'none', md: 'block' } }}>
            {user?.username}
          </Typography>
          <IconButton
            size="large"
            aria-label="account of current user"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleMenuOpen}
            color="inherit"
          >
            <Avatar sx={{ width: 32, height: 32 }}>
              {user?.username?.charAt(0) || 'U'}
            </Avatar>
          </IconButton>
        </Box>

        {/* 桌面用户菜单 */}
        <Menu
          id="menu-appbar"
          anchorEl={anchorEl}
          anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
          keepMounted
          transformOrigin={{ vertical: 'top', horizontal: 'right' }}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
        >
          <MenuItem onClick={() => { navigate('/profile'); handleMenuClose(); }}>
            <Person sx={{ mr: 1 }} />
            个人资料
          </MenuItem>
          <MenuItem onClick={handleLogout}>
            <Logout sx={{ mr: 1 }} />
            退出登录
          </MenuItem>
        </Menu>

        {/* 移除移动端菜单 */}
      </Toolbar>
    </AppBar>
  );
};

export default Header;
