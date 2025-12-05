import React, { useEffect, useState } from 'react';
import { Box, Typography, TextField, Button, Chip, Pagination, Alert, CircularProgress, Snackbar } from '@mui/material';
import { Search } from '@mui/icons-material';
import Layout from '../../components/layout/Layout';
import RecipeCard from '../../components/recipe/RecipeCard/RecipeCard';
import { useRecipe } from '../../hooks/useRecipe';

const RecipeListPage: React.FC = () => {
  const { fetchRecipes, recipeList, pagination, loading, error, clearError } = useRecipe();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error'
  });
  const filterTags = ['家常菜', '健康', '快速', '素食', '低卡路里'];

  // 当页面加载、页码或标签变化时获取数据
  useEffect(() => {
    // 只在组件挂载或相关依赖变化时获取数据
    fetchRecipes(currentPage, 8, selectedTags.length > 0 ? selectedTags : undefined).catch(() => {
      clearError();
    });
  }, [currentPage, selectedTags, fetchRecipes, clearError]); // 添加fetchRecipes和clearError到依赖数组，确保函数引用正确

  // 处理标签切换
  const handleTagToggle = (tag: string) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter(t => t !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
    setCurrentPage(1);
  };

  // 处理搜索
  const handleSearch = () => {
    // 搜索功能将在后续实现
  };

  // 处理页码变化
  const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
    setCurrentPage(value);
  };



  // 关闭通知
  const handleCloseSnackbar = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };

  // 错误提示
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        clearError();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, clearError]);

  return (
    <Layout>
      <Box sx={{ mb: 6 }}>
        <Typography variant="h3" sx={{ fontWeight: 700, color: '#333', mb: 1, fontSize: { xs: '2rem', md: '2.5rem' } }}>
          食谱列表
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ fontSize: { xs: '1rem', md: '1.125rem' } }}>
          浏览我们丰富的食谱库，发现更多美味佳肴
        </Typography>
      </Box>

      {/* 搜索和过滤区域 */}
      <Box sx={{ 
        mb: 6, 
        display: 'flex', 
        flexDirection: { xs: 'column', sm: 'row' }, 
        gap: 3, 
        alignItems: 'flex-start', 
        justifyContent: 'space-between',
        p: 3,
        backgroundColor: '#f8f9fa',
        borderRadius: 2
      }}>
        <Box sx={{ display: 'flex', gap: 2, flexGrow: 1, alignItems: 'center' }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="搜索食谱..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            sx={{ 
              flexGrow: 1,
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                '& fieldset': {
                  borderColor: '#e0e0e0',
                },
                '&:hover fieldset': {
                  borderColor: '#4caf50',
                },
                '&.Mui-focused fieldset': {
                  borderColor: '#4caf50',
                },
              },
            }}
          />
          <Button
            variant="contained"
            startIcon={<Search />}
            onClick={handleSearch}
            sx={{
              backgroundColor: '#4caf50',
              borderRadius: 2,
              textTransform: 'none',
              fontWeight: 600,
              padding: '10px 24px',
              '&:hover': {
                backgroundColor: '#45a049',
                transform: 'translateY(-1px)',
                boxShadow: '0 4px 12px rgba(76, 175, 80, 0.3)',
              },
              transition: 'all 0.2s ease',
            }}
          >
            搜索
          </Button>
        </Box>
      </Box>

      {/* 标签过滤 */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2, color: '#666', fontSize: { xs: '0.875rem', md: '1rem' } }}>
          按标签筛选：
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
          {filterTags.map((tag) => (
            <Chip
              key={tag}
              label={tag}
              onClick={() => handleTagToggle(tag)}
              color={selectedTags.includes(tag) ? 'primary' : 'default'}
              variant={selectedTags.includes(tag) ? 'filled' : 'outlined'}
              sx={{
                cursor: 'pointer',
                borderRadius: 1.5,
                fontWeight: 500,
                padding: '20px 8px',
                fontSize: { xs: '0.75rem', md: '0.875rem' },
                '&:hover': {
                  transform: 'translateY(-1px)',
                },
                transition: 'transform 0.2s ease',
              }}
            />
          ))}
        </Box>
        {selectedTags.length > 0 && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="subtitle2" sx={{ color: '#666', mb: 1, fontWeight: 500 }}>
              已选择的标签：
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
              {selectedTags.map((tag) => (
                <Chip
                  key={tag}
                  label={tag}
                  onDelete={() => handleTagToggle(tag)}
                  color="primary"
                  sx={{
                    borderRadius: 1.5,
                    fontWeight: 500,
                    fontSize: { xs: '0.75rem', md: '0.875rem' },
                  }}
                />
              ))}
            </Box>
          </Box>
        )}
      </Box>

      {/* 错误消息 */}
      {error && (
        <Box sx={{ mb: 4 }}>
          <Alert severity="error" onClose={clearError}>
            {error}
          </Alert>
        </Box>
      )}
      
      {/* 通知提示 */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbar.severity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
      
      {/* 加载状态 */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '200px' }}>
          <CircularProgress size={60} color="primary" />
        </Box>
      ) : (
        /* 食谱列表 */
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: {
            xs: '1fr',
            sm: 'repeat(2, 1fr)',
            md: 'repeat(3, 1fr)',
            lg: 'repeat(3, 1fr)', // 修改为最多3列
          },
          gap: 4,
        }}>
          {Array.isArray(recipeList) && recipeList.length > 0 ? (
            recipeList.map((recipe) => (
              <Box key={recipe.recipe_id} sx={{ 
                borderRadius: 2,
                overflow: 'hidden',
                '&:hover': {
                  transform: 'translateY(-2px)',
                },
                transition: 'transform 0.2s ease',
              }}>
                <RecipeCard recipe={recipe} />
              </Box>
            ))
          ) : (
            <Box sx={{ gridColumn: '1 / -1', textAlign: 'center', py: 8, color: '#666' }}>
              <Typography variant="h6">暂无食谱数据</Typography>
              <Typography variant="body2">尝试调整筛选条件或添加新的食谱</Typography>
            </Box>
          )}
        </Box>
      )}

      {/* 分页 */}
      {pagination.total > 0 && (
        <Box sx={{ mt: 8, display: 'flex', justifyContent: 'center', p: 2 }}>
          <Pagination
            count={Math.ceil(pagination.total / pagination.limit)}
            page={currentPage}
            onChange={handlePageChange}
            color="primary"
            size="large"
            sx={{
              '& .MuiPaginationItem-root': {
                borderRadius: 2,
                margin: '0 4px',
                minWidth: 40,
                height: 40,
                fontSize: { xs: '0.875rem', md: '1rem' },
              },
              '& .Mui-selected': {
                backgroundColor: '#4caf50',
                color: 'white',
                fontWeight: 600,
                '&:hover': {
                  backgroundColor: '#45a049',
                },
              },
              '& .MuiPaginationItem-ellipsis': {
                fontSize: '1.25rem',
              },
            }}
          />
        </Box>
      )}
    </Layout>
  );
};

export default RecipeListPage;