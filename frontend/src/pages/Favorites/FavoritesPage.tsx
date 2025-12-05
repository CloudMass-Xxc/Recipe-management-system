import React, { useState, useEffect, useCallback } from 'react';
import {
  Typography,
  Grid,
  Box,
  CircularProgress,
  Pagination,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Snackbar,
  Alert,
  Paper,
  Button,
  Stack
} from '@mui/material';
import {
  FilterList as FilterListIcon,
  Sort as SortIcon,
  Refresh as RefreshIcon,
  Favorite as FavoriteIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import RecipeCard from '../../components/recipe/RecipeCard/RecipeCard';
import { recipeService } from '../../services/recipe.service';
import type { RecipeListItem } from '../../types/recipe';
import { useAuth } from '../../hooks/useAuth';
import Layout from '../../components/layout/Layout';

const FavoritesPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();
  
  // 状态管理
  const [recipes, setRecipes] = useState<RecipeListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(12);
  const [total, setTotal] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'created_at' | 'cooking_time' | 'difficulty'>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [filterDifficulty, setFilterDifficulty] = useState<string>('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [availableTags, setAvailableTags] = useState<string[]>([]);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error' | 'info' | 'warning'>('success');

  // 获取收藏列表
  const fetchFavorites = useCallback(async (pageNum: number = 1) => {
    try {
      setLoading(true);
      setError(null);
      
      // 构建请求参数 - 只传递额外的过滤和排序参数
      const params = {
        search: searchQuery,
        sort_by: sortBy,
        sort_order: sortOrder,
        difficulty: filterDifficulty,
        tags: selectedTags
      };
      
      const response = await recipeService.getUserFavorites(pageNum, limit, params);
      
      if (response && response.recipes) {
        setRecipes(response.recipes);
        setTotal(response.total);
        setPage(pageNum);
        
        // 提取所有可用标签
        const allTags = new Set<string>();
        response.recipes.forEach(recipe => {
          recipe.tags?.forEach(tag => allTags.add(tag));
        });
        setAvailableTags(Array.from(allTags));
      } else {
        setRecipes([]);
        setTotal(0);
        setAvailableTags([]);
      }
    } catch (err: any) {
      console.error('获取收藏列表失败:', err);
      setError(err.response?.data?.message || '获取收藏列表失败，请稍后重试');
      setRecipes([]);
      setTotal(0);
      setAvailableTags([]);
    } finally {
      setLoading(false);
    }
  }, [limit, searchQuery, sortBy, sortOrder, filterDifficulty, selectedTags]);

  // 初始加载和依赖变化时获取收藏列表
  useEffect(() => {
    if (!isAuthenticated || !user) {
      setError('请先登录查看收藏');
      setLoading(false);
      return;
    }
    fetchFavorites(page);
  }, [fetchFavorites, page, isAuthenticated, user]);

  // 处理页面变化
  const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  // 处理搜索
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
    setPage(1);
  };

  // 处理排序变化
  const handleSortChange = (e: React.ChangeEvent<{ value: unknown }>) => {
    const [newSortBy, newSortOrder] = (e.target.value as string).split(':');
    setSortBy(newSortBy as 'created_at' | 'cooking_time' | 'difficulty');
    setSortOrder(newSortOrder as 'asc' | 'desc');
    setPage(1);
  };

  // 处理难度筛选变化
  const handleDifficultyChange = (e: React.ChangeEvent<{ value: unknown }>) => {
    setFilterDifficulty(e.target.value as string);
    setPage(1);
  };

  // 处理标签选择
  const handleTagToggle = (tag: string) => {
    setSelectedTags(prev => {
      if (prev.includes(tag)) {
        return prev.filter(t => t !== tag);
      } else {
        return [...prev, tag];
      }
    });
    setPage(1);
  };

  // 处理食谱点击
  const handleViewRecipe = (recipeId: string) => {
    navigate(`/recipe-detail/${recipeId}`);
  };

  // 处理收藏状态变化
  const handleFavoriteChange = (recipeId: string, isFavorite: boolean) => {
    if (!isFavorite) {
      setRecipes(prevRecipes => prevRecipes.filter(recipe => recipe.recipe_id !== recipeId));
      setTotal(prevTotal => Math.max(0, prevTotal - 1));
      setSnackbarMessage('已取消收藏');
      setSnackbarSeverity('success');
      setSnackbarOpen(true);
    }
  };

  // 关闭消息提示
  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  // 刷新数据
  const handleRefresh = () => {
    fetchFavorites(page);
  };

  // 清空筛选条件
  const handleClearFilters = () => {
    setSearchQuery('');
    setSortBy('created_at');
    setSortOrder('desc');
    setFilterDifficulty('');
    setSelectedTags([]);
    setPage(1);
  };

  // 检查是否有筛选条件
  const hasActiveFilters = searchQuery || filterDifficulty || selectedTags.length > 0;

  return (
    <Layout>
      <Box sx={{ mb: 4 }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
            <FavoriteIcon sx={{ color: '#ff4081' }} />
            我的收藏
          </Typography>
          <Button 
            variant="outlined" 
            startIcon={<RefreshIcon />}
            onClick={handleRefresh}
            disabled={loading}
            sx={{ textTransform: 'none' }}
          >
            刷新
          </Button>
        </Stack>
        
        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          这里展示您收藏的所有食谱
        </Typography>

        <Paper elevation={1} sx={{ p: 3, mb: 4, borderRadius: 2 }}>
          <Stack direction="column" gap={3}>
            <TextField
              fullWidth
              placeholder="搜索收藏的食谱..."
              value={searchQuery}
              onChange={handleSearch}
              sx={{ mb: 2 }}
              InputProps={{
                startAdornment: <FilterListIcon sx={{ mr: 1, color: 'action.active' }} />,
              }}
              variant="outlined"
              size="medium"
            />

            <Grid container spacing={3}>
              <Grid item xs={12} sm={6} md={4}>
                <FormControl fullWidth size="medium">
                  <InputLabel id="sort-by-label">排序方式</InputLabel>
                  <Select
                    labelId="sort-by-label"
                    id="sort-by"
                    value={`${sortBy}:${sortOrder}`}
                    label="排序方式"
                    onChange={handleSortChange}
                  >
                    <MenuItem value="created_at:desc">最近收藏</MenuItem>
                    <MenuItem value="created_at:asc">最早收藏</MenuItem>
                    <MenuItem value="cooking_time:asc">烹饪时间（从短到长）</MenuItem>
                    <MenuItem value="cooking_time:desc">烹饪时间（从长到短）</MenuItem>
                    <MenuItem value="difficulty:asc">难度（从易到难）</MenuItem>
                    <MenuItem value="difficulty:desc">难度（从难到易）</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} sm={6} md={4}>
                <FormControl fullWidth size="medium">
                  <InputLabel id="difficulty-filter-label">难度筛选</InputLabel>
                  <Select
                    labelId="difficulty-filter-label"
                    id="difficulty-filter"
                    value={filterDifficulty}
                    label="难度筛选"
                    onChange={handleDifficultyChange}
                  >
                    <MenuItem value="">全部难度</MenuItem>
                    <MenuItem value="简单">简单</MenuItem>
                    <MenuItem value="中等">中等</MenuItem>
                    <MenuItem value="困难">困难</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>

            {availableTags.length > 0 && (
              <Box>
                <Typography variant="body2" fontWeight="medium" sx={{ mb: 1 }}>
                  标签筛选
                </Typography>
                <Stack direction="row" flexWrap="wrap" gap={1}>
                  {availableTags.map(tag => (
                    <Chip
                      key={tag}
                      label={tag}
                      onClick={() => handleTagToggle(tag)}
                      color={selectedTags.includes(tag) ? 'primary' : 'default'}
                      variant={selectedTags.includes(tag) ? 'filled' : 'outlined'}
                      sx={{ cursor: 'pointer', textTransform: 'capitalize' }}
                    />
                  ))}
                </Stack>
              </Box>
            )}

            {hasActiveFilters && (
              <Button 
                variant="text" 
                onClick={handleClearFilters}
                sx={{ textTransform: 'none', color: 'primary', alignSelf: 'flex-start' }}
              >
                清空所有筛选条件
              </Button>
            )}
          </Stack>
        </Paper>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
          <CircularProgress size={60} sx={{ color: 'primary.main' }} />
        </Box>
      ) : error ? (
        <Paper elevation={2} sx={{ p: 6, borderRadius: 2, textAlign: 'center', minHeight: '400px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
          <Typography variant="h6" color="error" sx={{ mb: 2 }}>
            {error}
          </Typography>
          {error.includes('请先登录') && (
            <Button 
              variant="contained" 
              onClick={() => navigate('/login')}
              sx={{ mt: 2, textTransform: 'none' }}
            >
              去登录
            </Button>
          )}
          {!error.includes('请先登录') && (
            <Button 
              variant="contained" 
              onClick={() => fetchFavorites(page)}
              sx={{ mt: 2, textTransform: 'none' }}
            >
              重试
            </Button>
          )}
        </Paper>
      ) : recipes.length === 0 ? (
        <Paper elevation={2} sx={{ p: 6, borderRadius: 2, textAlign: 'center', minHeight: '400px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
            您还没有收藏任何食谱
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
            浏览食谱并点击收藏按钮来保存您喜欢的食谱
          </Typography>
          <Button 
            variant="contained" 
            onClick={() => navigate('/recipe-list')}
            sx={{ textTransform: 'none' }}
          >
            浏览食谱
          </Button>
        </Paper>
      ) : (
        <>
          <Grid container spacing={{ xs: 2, sm: 3, md: 4 }} sx={{ mb: 4 }}>
            {recipes.map((recipe) => (
              <Grid 
                item 
                xs={12} 
                sm={6} 
                md={4} 
                lg={3} 
                xl={3} 
                key={recipe.recipe_id}
                sx={{ display: 'flex', justifyContent: 'center' }}
              >
                <Box sx={{ width: '100%', maxWidth: 320, display: 'flex', flexDirection: 'column' }}>
                  <RecipeCard
                    recipe={recipe}
                    onView={handleViewRecipe}
                    onFavoriteChange={handleFavoriteChange}
                  />
                </Box>
              </Grid>
            ))}
          </Grid>

          {total > limit && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={Math.ceil(total / limit)}
                page={page}
                onChange={handlePageChange}
                color="primary"
                size="large"
                shape="rounded"
                showFirstButton
                showLastButton
                sx={{ '& .MuiPaginationItem-root': { borderRadius: 1 } }}
              />
            </Box>
          )}
        </>
      )}

      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert 
          onClose={handleCloseSnackbar} 
          severity={snackbarSeverity} 
          sx={{ width: '100%', borderRadius: 2 }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Layout>
  );
};

export default FavoritesPage;
