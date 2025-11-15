import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Alert,
  CircularProgress,
  Button,
  IconButton,
  Tooltip
} from '@mui/material';
import { 
  Favorite,
  ArrowBack, 
  Star, 
  AccessTime, 
  Group, 
  Kitchen,
  Search,
  X,
  Refresh
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import recipeService from '../../services/recipeService';
import type { RecipeListItem } from '../../types/recipe';

const UserFavoritesPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  
  const [favorites, setFavorites] = useState<RecipeListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [hasMore, setHasMore] = useState(false);
  const [page, setPage] = useState(1);

  const loadFavorites = useCallback(async () => {
    if (!isAuthenticated) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const limit = 20;
        const skip = (page - 1) * limit;
        const favoriteRecipes = await recipeService.getUserFavorites(skip, limit);
      
      if (page === 1) {
        setFavorites(favoriteRecipes || []);
      } else {
        setFavorites(prev => [...prev, ...(favoriteRecipes || [])]);
      }
      setHasMore(favoriteRecipes.length >= limit);
    } catch (err: unknown) {
      // 类型断言为可能包含 response 的对象
      const error = err as { response?: { data?: { detail?: string; message?: string } } };
      setError(
        error.response?.data?.detail || 
        error.response?.data?.message || 
        '获取收藏食谱失败'
      );
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, page]);

  const handleLoadMore = () => {
    if (hasMore && !loading) {
      setPage((prev: number) => prev + 1);
      loadFavorites();
    }
  };

  const handleRefresh = () => {
    loadFavorites();
  };

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    loadFavorites();
  }, [isAuthenticated, navigate, loadFavorites]);

  const handleRemoveFavorite = async (recipeId: string) => {
    try {
      await recipeService.unfavoriteRecipe(recipeId);
      // 从本地状态中移除
      setFavorites(prev => prev.filter(recipe => recipe.id !== recipeId));
    } catch {
      alert('移除收藏失败，请稍后重试');
    }
  };

  const filteredFavorites = searchTerm
    ? favorites.filter(recipe => 
        recipe.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        recipe.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        recipe.tags?.some((tag: string) => tag.toLowerCase().includes(searchTerm.toLowerCase()))
      )
    : favorites;

  const getDifficultyLabel = (difficulty: string): string => {
    switch (difficulty) {
      case 'easy': return '简单';
      case 'medium': return '中等';
      case 'hard': return '困难';
      default: return difficulty;
    }
  };

  const formatTime = (minutes: number): string => {
    if (minutes < 60) {
      return `${minutes}分钟`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}小时${mins}分钟` : `${hours}小时`;
  };

  if (!isAuthenticated) {
    return null; // 不会显示，因为已经重定向
  }

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
      {/* 顶部导航栏 */}
      <Box sx={{ bgcolor: 'white', boxShadow: 1, position: 'sticky', top: 0, zIndex: 10 }}>
        <Box sx={{ maxWidth: '1200px', mx: 'auto', px: 4, py: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
          <IconButton onClick={() => navigate(-1)}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h6">我的收藏</Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Typography variant="body2" color="text.secondary">
            {user?.username || '用户'} 的收藏
          </Typography>
        </Box>
      </Box>

      <Box sx={{ maxWidth: '1200px', mx: 'auto', px: { xs: 2, md: 4 }, py: 6 }}>
        {/* 标题和统计信息 */}
        <Box sx={{ mb: 6 }}>
          <Typography variant="h4" gutterBottom>我的收藏食谱</Typography>
          <Typography variant="body1" color="text.secondary">
            共收藏了 {filteredFavorites.length} 个食谱
          </Typography>
        </Box>

        {/* 搜索框 */}
        <Box sx={{ mb: 6 }}>
          <Paper elevation={2} sx={{ p: { xs: 2, md: 3 } }}>
            <Box sx={{ position: 'relative' }}>
              <Search 
                fontSize="small" 
                sx={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'grey.400' }}
              />
              <Box sx={{ pl: 8, pr: 4 }}>
                <input
                  type="text"
                  placeholder="搜索收藏的食谱..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '12px 0',
                    border: 'none',
                    outline: 'none',
                    fontSize: '1rem'
                  }}
                />
              </Box>
              {searchTerm && (
                <IconButton 
                  size="small" 
                  onClick={() => setSearchTerm('')}
                  sx={{ position: 'absolute', right: 8, top: '50%', transform: 'translateY(-50%)' }}
                >
                  <X fontSize="small" />
                </IconButton>
              )}
            </Box>
          </Paper>
        </Box>

        {/* 收藏食谱列表 */}
        {loading && page === 1 ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Paper elevation={2} sx={{ p: 8, textAlign: 'center' }}>
            <Alert severity="error" sx={{ mb: 4 }}>
              {error}
            </Alert>
            <Button 
              variant="contained" 
              onClick={handleRefresh}
              startIcon={<Refresh />}
            >
              重试
            </Button>
          </Paper>
        ) : filteredFavorites.length === 0 ? (
          <Paper elevation={2} sx={{ p: 8, textAlign: 'center' }}>
            <Favorite 
              fontSize="inherit" 
              color="disabled" 
              sx={{ mb: 4, opacity: 0.5, fontSize: 64 }}
            />
            <Typography variant="h6" gutterBottom>
              {searchTerm ? '没有找到匹配的收藏食谱' : '还没有收藏任何食谱'}
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 6, maxWidth: 400, mx: 'auto' }}>
              {searchTerm 
                ? '尝试使用其他关键词搜索，或清除搜索条件查看所有收藏' 
                : '浏览食谱页面，点击收藏按钮来保存您喜欢的食谱'}
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
              {searchTerm && (
                <Button 
                  variant="outlined" 
                  onClick={() => setSearchTerm('')}
                >
                  清除搜索
                </Button>
              )}
              <Button 
                variant="contained" 
                onClick={() => navigate('/recipes')}
              >
                浏览食谱
              </Button>
            </Box>
          </Paper>
        ) : (
          <>
            {/* 食谱卡片列表 */}
            <Grid container spacing={4}>
              {filteredFavorites.map((recipe) => (
                <Grid key={recipe.id} sx={{ xs: 12, sm: 6, lg: 4, width: '100%' }}>
                  <Paper 
                    elevation={2} 
                    sx={{ 
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      position: 'relative',
                      overflow: 'hidden',
                      borderRadius: 2,
                      '&:hover': {
                        boxShadow: 3
                      }
                    }}>
                    {/* 食谱图片 */}
                    <Box sx={{ position: 'relative', height: 200, overflow: 'hidden' }}>
                      {recipe.image_url ? (
                        <img 
                          src={recipe.image_url} 
                          alt={recipe.title} 
                          style={{ 
                            width: '100%', 
                            height: '100%', 
                            objectFit: 'cover',
                            transition: 'transform 0.3s'
                          }}
                          onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
                          onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'} 
                        />
                      ) : (
                        <Box sx={{ 
                          height: '100%', 
                          bgcolor: 'grey.100', 
                          display: 'flex', 
                          alignItems: 'center', 
                          justifyContent: 'center',
                          flexDirection: 'column',
                          padding: 4
                        }}>
                          <Kitchen fontSize="large" sx={{ fontSize: 48 }} color="disabled" />
                          <Typography variant="body2" color="text.secondary" sx={{ mt: 2, textAlign: 'center' }}>
                            暂无图片
                          </Typography>
                        </Box>
                      )}
                      <Tooltip title="取消收藏">
                        <IconButton 
                          sx={{
                            position: 'absolute',
                            top: 8,
                            right: 8,
                            bgcolor: 'rgba(255, 255, 255, 0.9)',
                            '&:hover': {
                              bgcolor: 'rgba(255, 255, 255, 1)'
                            }
                          }}
                          onClick={() => handleRemoveFavorite(recipe.id)}
                        >
                          <Favorite fontSize="large" color="error" fill="currentColor" />
                        </IconButton>
                      </Tooltip>
                    </Box>

                    {/* 食谱信息 */}
                    <Box sx={{ p: 3, flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                      <Typography 
                        variant="h6" 
                        gutterBottom 
                        sx={{ 
                          fontWeight: 'bold',
                          cursor: 'pointer',
                          '&:hover': {
                            color: 'primary.main'
                          }
                        }}
                        onClick={() => navigate(`/recipes/${recipe.id}`)}
                      >
                        {recipe.title}
                      </Typography>
                      
                      <Typography 
                        variant="body2" 
                        color="text.secondary" 
                        sx={{ mb: 2, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}
                      >
                        {recipe.description}
                      </Typography>

                      {/* 食谱详情指标 */}
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, bgcolor: 'grey.50', px: 2, py: 1, borderRadius: 1 }}>
                          <AccessTime fontSize="small" color="primary" />
                          <Typography variant="body2">
                            {formatTime(recipe.prep_time + recipe.cook_time)}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, bgcolor: 'grey.50', px: 2, py: 1, borderRadius: 1 }}>
                          <Group fontSize="small" color="primary" />
                          <Typography variant="body2">
                            {recipe.servings}人份
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, bgcolor: 'grey.50', px: 2, py: 1, borderRadius: 1 }}>
                          <Kitchen fontSize="small" color="primary" />
                          <Typography variant="body2">
                            {getDifficultyLabel(recipe.difficulty)}
                          </Typography>
                        </Box>
                      </Box>

                      {/* 评分和标签 */}
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 'auto' }}>
                        {recipe.average_rating && (
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Star fontSize="small" color="warning" fill="currentColor" />
                              <Typography variant="body2" fontWeight="medium">
                                {recipe.average_rating?.toFixed(1) || '0.0'}
                              </Typography>
                            </Box>
                          )}
                        
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="caption" color="text.secondary">
                            收藏于 {new Date(recipe.favorited_at || recipe?.created_at || new Date()).toLocaleDateString()}
                          </Typography>
                        </Box>
                      </Box>
                    </Box>
                  </Paper>
                </Grid>
              ))}
            </Grid>

            {/* 加载更多 */}
            <Box sx={{ mt: 6, textAlign: 'center' }}>
              {hasMore && !loading && (
                <Button 
                  variant="outlined" 
                  onClick={handleLoadMore}
                  startIcon={<Refresh />}
                >
                  加载更多
                </Button>
              )}
              {loading && page > 1 && (
                <CircularProgress />
              )}
              {!hasMore && favorites.length > 0 && (
                <Typography variant="body2" color="text.secondary">
                  已显示全部收藏
                </Typography>
              )}
            </Box>
          </>
        )}

        {/* 空收藏提示 */}
        {favorites.length === 0 && !loading && !error && !searchTerm && (
          <Paper elevation={2} sx={{ mt: 12, p: 6, textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom>发现更多美食灵感</Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 6, maxWidth: 500, mx: 'auto' }}>
              浏览我们的食谱库，发现更多美味佳肴并将它们添加到您的收藏中
            </Typography>
            <Button 
              variant="contained" 
              onClick={() => navigate('/recipes')}
              size="large"
            >
              探索食谱
            </Button>
          </Paper>
        )}
      </Box>
    </Box>
  );
};

export default UserFavoritesPage;