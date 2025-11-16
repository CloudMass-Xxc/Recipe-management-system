import React from 'react';
import { Drawer, List, ListItem, ListItemText, Box, Divider, ListItemIcon, Typography, useMediaQuery, useTheme } from '@mui/material';
import { Link } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import EditIcon from '@mui/icons-material/Edit';
import RecipeIcon from '@mui/icons-material/MenuBook';
import FavoriteIcon from '@mui/icons-material/Favorite';
import PersonIcon from '@mui/icons-material/Person';
import LoginIcon from '@mui/icons-material/Login';
import FastfoodIcon from '@mui/icons-material/Fastfood';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  // 导航项目配置
  const navItems = [
    { text: '首页', path: '/', icon: <HomeIcon /> },
    { text: '生成食谱', path: '/generate', icon: <EditIcon /> },
    { text: '我的食谱', path: '/my-recipes', icon: <RecipeIcon /> },
    { text: '收藏夹', path: '/favorites', icon: <FavoriteIcon /> },
  ];

  const authItems = [
    { text: '登录', path: '/login', icon: <LoginIcon /> },
    { text: '注册', path: '/register', icon: <PersonIcon /> },
  ];

  return (
    <Drawer
      anchor="left"
      open={open}
      onClose={onClose}
      PaperProps={{
        sx: {
          width: isMobile ? 280 : 260,
          backgroundColor: '#ffffff',
          boxShadow: '2px 0 8px rgba(0,0,0,0.1)',
          borderRight: 'none',
        },
      }}
      sx={{
        '& .MuiDrawer-paper': {
          width: isMobile ? 280 : 260,
          boxSizing: 'border-box',
          background: '#ffffff',
        },
      }}
    >
      <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        {/* 侧边栏头部 */}
        <Box 
          sx={{ 
            p: 3,
            borderBottom: '1px solid #f0f0f0',
            bgcolor: '#1976d2',
            color: '#fff'
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <FastfoodIcon fontSize="large" />
            <Typography variant="h6" fontWeight={600}>
              食谱管理系统
            </Typography>
          </Box>
        </Box>

        {/* 导航菜单 */}
        <List sx={{ flex: 1, padding: 0 }}>
          {navItems.map((item, index) => (
            <ListItem
              key={index}
              component={Link}
              to={item.path}
              onClick={onClose}
              sx={{
                cursor: 'pointer',
                paddingY: 1.5,
                '&:hover': {
                  backgroundColor: '#f5f5f5',
                },
                transition: theme.transitions.create('background-color', { duration: theme.transitions.duration.shortest })
              }}
            >
              <ListItemIcon sx={{ minWidth: 40, color: '#666' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.text} 
                sx={{ 
                  '& .MuiTypography-root': { 
                    fontWeight: 500,
                    color: '#333'
                  } 
                }} 
              />
            </ListItem>
          ))}
        </List>

        {/* 分割线 */}
        <Divider sx={{ marginY: 0 }} />

        {/* 认证菜单 */}
        <List sx={{ padding: 0 }}>
          {authItems.map((item, index) => (
            <ListItem
              key={index}
              component={Link}
              to={item.path}
              onClick={onClose}
              sx={{
                cursor: 'pointer',
                paddingY: 1.5,
                '&:hover': {
                  backgroundColor: '#f5f5f5',
                },
                transition: theme.transitions.create('background-color', { duration: theme.transitions.duration.shortest })
              }}
            >
              <ListItemIcon sx={{ minWidth: 40, color: '#666' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.text} 
                sx={{ 
                  '& .MuiTypography-root': { 
                    fontWeight: 500,
                    color: '#333'
                  } 
                }} 
              />
            </ListItem>
          ))}
        </List>

        {/* 侧边栏底部 */}
        <Box sx={{ p: 2, borderTop: '1px solid #f0f0f0', mt: 'auto' }}>
          <Typography variant="body2" color="text.secondary" align="center">
            个性化食谱管理系统 v1.0
          </Typography>
        </Box>
      </Box>
    </Drawer>
  );
};

export default Sidebar;