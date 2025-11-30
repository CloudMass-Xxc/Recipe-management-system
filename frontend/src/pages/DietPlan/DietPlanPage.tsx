import React from 'react';
import { Box, Typography, Paper, Button, Card, CardContent, Chip } from '@mui/material';
import { Add, CalendarMonth } from '@mui/icons-material';
import Layout from '../../components/layout/Layout';

const DietPlanPage: React.FC = () => {
  return (
    <Layout>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h3" sx={{ fontWeight: 'bold', color: '#333', mb: 1 }}>
            饮食计划
          </Typography>
          <Typography variant="body1" color="text.secondary">
            查看和管理您的饮食计划
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          sx={{ backgroundColor: '#4caf50', borderRadius: 2, textTransform: 'none' }}
        >
          创建新计划
        </Button>
      </Box>

      <Paper sx={{ p: 4, borderRadius: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
          <CalendarMonth sx={{ color: '#4caf50' }} />
          本周计划
        </Typography>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          {['周一', '周二', '周三', '周四', '周五', '周六', '周日'].map((day, index) => (
            <Box key={index} sx={{ flex: '1 1 300px', maxWidth: { xs: '100%', sm: 'calc(50% - 12px)', md: 'calc(33.333% - 16px)' } }}>
              <Card sx={{ height: '100%', transition: 'transform 0.3s, box-shadow 0.3s', '&:hover': { transform: 'translateY(-5px)', boxShadow: '0 8px 24px rgba(0,0,0,0.12)' } }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2, color: '#4caf50' }}>
                    {day}
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>早餐</Typography>
                    <Typography variant="body2" color="text.secondary">牛奶、鸡蛋、全麦面包</Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>午餐</Typography>
                    <Typography variant="body2" color="text.secondary">番茄鸡蛋面</Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>晚餐</Typography>
                    <Typography variant="body2" color="text.secondary">红烧肉、青菜、米饭</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    <Chip label="健康" size="small" sx={{ backgroundColor: '#e8f5e8', color: '#388e3c' }} />
                    <Chip label="均衡" size="small" sx={{ backgroundColor: '#e3f2fd', color: '#1976d2' }} />
                  </Box>
                </CardContent>
              </Card>
            </Box>
          ))}
        </Box>
      </Paper>
    </Layout>
  );
};

export default DietPlanPage;
