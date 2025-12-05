import React, { useState, useRef, useEffect } from 'react';
import { Box, CssBaseline, useMediaQuery } from '@mui/material';
import Header from './Header/Header';
import Sidebar from './Sidebar/Sidebar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const isMobile = useMediaQuery('(max-width:600px)');

  // 处理侧边栏关闭
  const handleSidebarClose = () => {
    setSidebarOpen(false);
  };

  // 处理侧边栏切换（用于移动设备的按钮）
  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // 添加全局鼠标事件监听
  useEffect(() => {
    // 节流函数，限制事件处理频率
    let lastCall = 0;
    const THROTTLE_DELAY = 100; // 100ms节流延迟

    // 处理鼠标移动事件 - 检测鼠标是否靠近左侧边框
    const handleMouseMove = (e: MouseEvent) => {
      const now = Date.now();
      // 节流：只在指定时间间隔后处理事件
      if (now - lastCall < THROTTLE_DELAY) {
        return;
      }
      lastCall = now;

      // 只有在桌面端且侧边栏未打开时，才检测鼠标是否靠近左侧边框
      if (!isMobile && !sidebarOpen && e.clientX <= 10) {
        setSidebarOpen(true);
      }
    };

    // 为文档添加鼠标移动事件监听
    document.addEventListener('mousemove', handleMouseMove);

    // 清理事件监听
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
    };
  }, [isMobile, sidebarOpen]);

  return (
    <Box
      ref={containerRef}
      sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', backgroundColor: '#f5f5f5' }}
    >
      <CssBaseline />
      <Header onSidebarToggle={handleSidebarToggle} />
      <Box sx={{ flex: 1 }}>
        {/* 抽屉式侧边栏 */}
        <Sidebar
          open={sidebarOpen}
          onClose={handleSidebarClose}
        />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: { xs: 2, md: 4 },
          }}
        >
          <Box sx={{ 
            width: '100%',
            maxWidth: 1400,
            mx: 'auto',
            mt: 2,
            mb: 6,
          }}>
            {children}
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;
