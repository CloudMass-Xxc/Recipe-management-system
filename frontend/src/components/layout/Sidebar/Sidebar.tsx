import React from 'react';
import { Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Divider, Box } from '@mui/material';
import { Home, LocalFireDepartment as RecipeIcon, Person, Book, CalendarMonth, Favorite } from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { text: '首页', icon: <Home />, path: '/' },
    { text: '食谱生成', icon: <RecipeIcon />, path: '/recipe-generate' },
    { text: '食谱列表', icon: <Book />, path: '/recipe-list' },
    { text: '我的收藏', icon: <Favorite />, path: '/favorites' },
    { text: '饮食计划', icon: <CalendarMonth />, path: '/diet-plan' },
    { text: '个人资料', icon: <Person />, path: '/profile' },
  ];

  const handleItemClick = (path: string) => {
    navigate(path);
    // 点击菜单项后不自动关闭侧边栏，让用户自行决定何时离开
  };

  // 侧边栏内容
  const sidebarContent = (
    <Box sx={{ 
      width: 240,
      backgroundColor: '#f5f5f5',
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      boxShadow: 2,
    }}>
      <Box sx={{ p: 2, backgroundColor: '#4caf50', color: 'white' }}>
        <h2 style={{ margin: 0, fontSize: '1.2rem' }}>菜单</h2>
      </Box>
      <Divider />
      <List sx={{ flex: 1 }}>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => handleItemClick(item.path)}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: '#e8f5e8',
                  '&:hover': {
                    backgroundColor: '#dcedc8',
                  },
                },
              }}
            >
              <ListItemIcon sx={{ color: '#4caf50' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  // 使用Drawer组件实现侧边栏，确保在隐藏时完全不显示
  return (
    <Drawer
      anchor="left"
      open={open}
      onClose={onClose}
      sx={{
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
          transition: 'transform 0.3s ease-in-out',
          backgroundColor: '#f5f5f5',
        },
      }}
      // 禁用默认的点击遮罩层关闭功能，只通过鼠标离开事件关闭
      ModalProps={{
        keepMounted: false,
      }}
    >
      {sidebarContent}
    </Drawer>
  );

};

export default Sidebar;
