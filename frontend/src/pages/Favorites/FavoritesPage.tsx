import React, { useEffect } from 'react';
import { Box, Typography, Paper, CircularProgress, Alert } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { fetchFavorites } from '../../store/slices/userSlice';
import type { RootState, AppDispatch } from '../../store';
import Layout from '../../components/layout/Layout';
import RecipeCard from '../../components/recipe/RecipeCard/RecipeCard';


const FavoritesPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { favorites, loading, error } = useSelector((state: RootState) => state.user);

  // 在组件挂载时获取收藏数据
  useEffect(() => {
    dispatch(fetchFavorites({ page: 1, limit: 20 }));
  }, [dispatch]);

  return (
    <Layout>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" sx={{ fontWeight: 'bold', color: '#333', mb: 1 }}>
          我的收藏
        </Typography>
        <Typography variant="body1" color="text.secondary">
          查看您收藏的所有食谱
        </Typography>
      </Box>

      {/* 错误提示 */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* 加载状态 */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '300px' }}>
          <CircularProgress />
        </Box>
      ) : favorites.length > 0 ? (
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          {favorites.map((recipe: any) => (
            <Box key={recipe.recipe_id} sx={{ flex: '1 1 300px', maxWidth: { xs: '100%', sm: 'calc(50% - 12px)', md: 'calc(33.333% - 16px)' } }}>
              <RecipeCard recipe={recipe} isFavorite={true} />
            </Box>
          ))}
        </Box>
      ) : (
        <Paper sx={{ p: 6, borderRadius: 2, textAlign: 'center' }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            您还没有收藏任何食谱
          </Typography>
          <Typography variant="body2" color="text.secondary">
            浏览食谱并点击收藏按钮，将您喜爱的食谱添加到这里
          </Typography>
        </Paper>
      )}
    </Layout>
  );
};

export default FavoritesPage;
