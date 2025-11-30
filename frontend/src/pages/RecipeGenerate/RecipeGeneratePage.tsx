import React from 'react';
import { Typography, Box } from '@mui/material';
import Layout from '../../components/layout/Layout';
import RecipeGenerator from '../../components/recipe/RecipeGenerator/RecipeGenerator';

const RecipeGeneratePage: React.FC = () => {
  return (
    <Layout>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" sx={{ fontWeight: 'bold', color: '#333', mb: 1 }}>
          个性化食谱生成
        </Typography>
        <Typography variant="body1" color="text.secondary">
          根据您的食材、饮食禁忌和个人偏好，生成专属于您的美味食谱
        </Typography>
      </Box>
      <RecipeGenerator />
    </Layout>
  );
};

export default RecipeGeneratePage;
