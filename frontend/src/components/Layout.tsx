import React, { useState } from 'react';
import { Box, Button, useMediaQuery, useTheme } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Sidebar from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isTablet = useMediaQuery(theme.breakpoints.down('lg'));
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleSidebarOpen = () => {
    setSidebarOpen(true);
  };

  const handleSidebarClose = () => {
    setSidebarOpen(false);
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: '#f5f5f5', display: 'flex', flexDirection: 'column' }}>
      <Header />
      <Box sx={{ display: 'flex', flex: 1, pt: 8, position: 'relative' }}>
        {/* 移动端菜单按钮 */}
        {isMobile && (
          <Box sx={{ position: 'fixed', top: 16, left: 16, zIndex: 100 }}>
            <Button 
              color="primary" 
              onClick={handleSidebarOpen}
              sx={{ minWidth: 'auto', p: 1 }}
              variant="contained"
            >
              <MenuIcon />
            </Button>
          </Box>
        )}
        
        {/* 侧边栏 */}
        <Sidebar open={sidebarOpen} onClose={handleSidebarClose} />
        
        {/* 主内容区 - 增强响应式设计 */}
        <Box 
          component="main" 
          sx={{
            flex: 1,
            p: { xs: 1, sm: 2, md: 3, lg: 4 },
            maxWidth: '100%',
            mx: { xs: 0, md: isTablet ? 1 : 2 },
            transition: theme.transitions.create('margin', { duration: theme.transitions.duration.shortest }),
            marginLeft: isMobile ? 0 : 250,
            // 在小屏幕上增加额外的顶部内边距，避免被固定菜单遮挡
            pt: isMobile ? 14 : 8,
            overflowX: 'hidden',
            // 确保内容区域不会超出屏幕
            '& .container': {
              maxWidth: { sm: '100%', md: '90%', lg: '80%', xl: '70%' },
              margin: '0 auto',
              width: '100%'
            }
          }}
          className="fade-in"
        >
          <Box className="container">
            <Outlet />
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;