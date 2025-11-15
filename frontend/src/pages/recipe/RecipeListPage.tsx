import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  CircularProgress,
  Alert,
  Button,
  IconButton,
  Tooltip,
  Drawer,
  Divider,
  ToggleButton,
  ToggleButtonGroup
} from '@mui/material';
import {
  Search,
  FilterList,
  ArrowUpDown,
  Star,
  Clock,
  Users,
  ChefHat,
  X,
  Heart,
  Refresh,
  Plus
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import RecipeCard from '../../components/recipe/RecipeCard';
import recipeService from '../../services/recipeService';
import { RecipeResponse } from '../../types/recipe';

interface FilterOptions {
  searchTerm: string;
  category: string;
  difficulty: string;
  timeRange: string;
  servings: string;
  sortBy: string;
  dietaryPreferences: string[];
  favoriteOnly: boolean;
}

const RecipeListPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  
  const [recipes, setRecipes] = useState<RecipeResponse[]>([]);
  const [filteredRecipes, setFilteredRecipes] = useState<RecipeResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  
  const [filters, setFilters] = useState<FilterOptions>({
    searchTerm: '',
    category: '',
    difficulty: '',
    timeRange: '',
    servings: '',
    sortBy: 'recent',
    dietaryPreferences: [],
    favoriteOnly: false
  });

  const categories = ['全部', '早餐', '午餐', '晚餐', '小吃', '甜点', '饮品', '素食', '海鲜', '肉类'];
  const difficulties = ['全部', '简单', '中等', '困难'];
  const timeRanges = ['全部', '15分钟内', '30分钟内', '1小时内', '1小时以上'];
  const servingsOptions = ['全部', '1人份', '2人份', '3-4人份', '5人以上'];
  const dietaryPreferences = [
    '素食', '纯素', '无麸质', '低碳水', '无乳糖', '高蛋白', '生酮饮食', '地中海饮食'
  ];
  const sortOptions = [
    { value: 'recent', label: '最新发布' },
    { value: 'popular', label: '最受欢迎' },
    { value: 'rating', label: '评分最高' },
    { value: 'time', label: '烹饪时间' }
  ];

  useEffect(() => {
    loadRecipes();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [recipes, filters]);

  const loadRecipes = async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setRefreshing(true);
        setPage(1);
      } else {
        setLoading(true);
      }
      setError(null);
      
      const params = {
        page: isRefresh ? 1 : page,
        limit: 12,
        sort_by: filters.sortBy
      };
      
      const data = await recipeService.getRecipes(params);
      
      if (isRefresh || page === 1) {
        setRecipes(data.recipes);
      } else {
        setRecipes(prev => [...prev, ...data.recipes]);
      }
      
      setHasMore(data.recipes.length > 0 && data.recipes.length === params.limit);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        err.response?.data?.message || 
        '获取食谱列表失败'
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleLoadMore = () => {
    if (hasMore && !loading) {
      setPage(prev => prev + 1);
      loadRecipes();
    }
  };

  const handleRefresh = () => {
    loadRecipes(true);
  };

  const applyFilters = () => {
    let result = [...recipes];
    
    // 搜索词过滤
    if (filters.searchTerm) {
      const searchTerm = filters.searchTerm.toLowerCase();
      result = result.filter(recipe => 
        recipe.title.toLowerCase().includes(searchTerm) ||
        recipe.description.toLowerCase().includes(searchTerm) ||
        recipe.tags?.some(tag => tag.toLowerCase().includes(searchTerm))
      );
    }
    
    // 分类过滤
    if (filters.category && filters.category !== '全部') {
      const categoryMap: Record<string, string> = {
        '早餐': 'breakfast',
        '午餐': 'lunch',
        '晚餐': 'dinner',
        '小吃': 'snack',
        '甜点': 'dessert'
      };
      result = result.filter(recipe => 
        recipe.meal_type === categoryMap[filters.category] ||
        recipe.tags?.includes(filters.category)
      );
    }
    
    // 难度过滤
    if (filters.difficulty && filters.difficulty !== '全部') {
      const difficultyMap: Record<string, string> = {
        '简单': 'easy',
        '中等': 'medium',
        '困难': 'hard'
      };
      result = result.filter(recipe => 
        recipe.difficulty === difficultyMap[filters.difficulty]
      );
    }
    
    // 时间范围过滤
    if (filters.timeRange && filters.timeRange !== '全部') {
      const totalTimeMap: Record<string, number> = {
        '15分钟内': 15,
        '30分钟内': 30,
        '1小时内': 60
      };
      
      if (filters.timeRange === '1小时以上') {
        result = result.filter(recipe => 
          (recipe.prep_time + recipe.cook_time) > 60
        );
      } else if (totalTimeMap[filters.timeRange]) {
        result = result.filter(recipe => 
          (recipe.prep_time + recipe.cook_time) <= totalTimeMap[filters.timeRange]
        );
      }
    }
    
    // 份量过滤
    if (filters.servings && filters.servings !== '全部') {
      const servingsMap: Record<string, number | null> = {
        '1人份': 1,
        '2人份': 2,
        '3-4人份': null,
        '5人以上': null
      };
      
      if (filters.servings === '3-4人份') {
        result = result.filter(recipe => 
          recipe.servings >= 3 && recipe.servings <= 4
        );
      } else if (filters.servings === '5人以上') {
        result = result.filter(recipe => 
          recipe.servings >= 5
        );
      } else if (servingsMap[filters.servings] !== null) {
        result = result.filter(recipe => 
          recipe.servings === servingsMap[filters.servings]
        );
      }
    }
    
    // 饮食偏好过滤
    if (filters.dietaryPreferences.length > 0) {
      result = result.filter(recipe => 
        filters.dietaryPreferences.some(pref => 
          recipe.tags?.includes(pref) ||
          recipe.dietary_restrictions?.includes(pref)
        )
      );
    }
    
    // 仅显示收藏
    if (filters.favoriteOnly && isAuthenticated) {
      result = result.filter(recipe => recipe.is_favorited);
    }
    
    setFilteredRecipes(result);
  };

  const handleFilterChange = (key: keyof FilterOptions, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleDietaryPreferenceToggle = (preference: string) => {
    setFilters(prev => ({
      ...prev,
      dietaryPreferences: prev.dietaryPreferences.includes(preference)
        ? prev.dietaryPreferences.filter(p => p !== preference)
        : [...prev.dietaryPreferences, preference]
    }));
  };

  const resetFilters = () => {
    setFilters({
      searchTerm: '',
      category: '',
      difficulty: '',
      timeRange: '',
      servings: '',
      sortBy: 'recent',
      dietaryPreferences: [],
      favoriteOnly: false
    });
  };

  const handleViewModeChange = (
    _event: React.MouseEvent<HTMLElement>,
    newMode: 'grid' | 'list' | null
  ) => {
    if (newMode !== null) {
      setViewMode(newMode);
    }
  };

  const renderFilters = () => (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">筛选条件</Typography>
        <IconButton onClick={resetFilters} size="small">
          <Refresh fontSize="small" />
        </IconButton>
      </Box>
      
      {/* 搜索框 */}
      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          placeholder="搜索食谱名称、描述或标签"
          value={filters.searchTerm}
          onChange={(e) => handleFilterChange('searchTerm', e.target.value)}
          InputProps={{
            startAdornment: <Search fontSize="small" />
          }}
        />
      </Box>

      <Divider sx={{ my: 3 }} />

      {/* 分类筛选 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" gutterBottom>分类</Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          <Chip
            label="全部"
            color={filters.category === '' ? 'primary' : 'default'}
            onClick={() => handleFilterChange('category', '')}
            sx={{ cursor: 'pointer' }}
          />
          {categories.slice(1).map((category) => (
            <Chip
              key={category}
              label={category}
              color={filters.category === category ? 'primary' : 'default'}
              onClick={() => handleFilterChange('category', category)}
              sx={{ cursor: 'pointer' }}
            />
          ))}
        </Box>
      </Box>

      {/* 难度筛选 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" gutterBottom>难度</Typography>
        <FormControl fullWidth>
          <Select
            value={filters.difficulty}
            onChange={(e) => handleFilterChange('difficulty', e.target.value)}
            displayEmpty
          >
            <MenuItem value="">全部</MenuItem>
            {difficulties.slice(1).map((diff) => (
              <MenuItem key={diff} value={diff}>{diff}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {/* 时间筛选 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" gutterBottom>烹饪时间</Typography>
        <FormControl fullWidth>
          <Select
            value={filters.timeRange}
            onChange={(e) => handleFilterChange('timeRange', e.target.value)}
            displayEmpty
          >
            <MenuItem value="">全部</MenuItem>
            {timeRanges.slice(1).map((time) => (
              <MenuItem key={time} value={time}>{time}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {/* 份量筛选 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" gutterBottom>份量</Typography>
        <FormControl fullWidth>
          <Select
            value={filters.servings}
            onChange={(e) => handleFilterChange('servings', e.target.value)}
            displayEmpty
          >
            <MenuItem value="">全部</MenuItem>
            {servingsOptions.slice(1).map((serving) => (
              <MenuItem key={serving} value={serving}>{serving}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {/* 饮食偏好 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" gutterBottom>饮食偏好</Typography>
        <Box sx={{ maxHeight: 180, overflowY: 'auto' }}>
          {dietaryPreferences.map((pref) => (
            <Box key={pref} sx={{ mb: 1 }}>
              <ToggleButton
                value={pref}
                selected={filters.dietaryPreferences.includes(pref)}
                onClick={() => handleDietaryPreferenceToggle(pref)}
                fullWidth
                size="small"
              >
                {pref}
              </ToggleButton>
            </Box>
          ))}
        </Box>
      </Box>

      {/* 仅显示收藏 */}
      {isAuthenticated && (
        <Box sx={{ mb: 3 }}>
          <ToggleButton
            value="favoriteOnly"
            selected={filters.favoriteOnly}
            onClick={() => handleFilterChange('favoriteOnly', !filters.favoriteOnly)}
            fullWidth
            startIcon={<Heart />}
          >
            仅显示收藏
          </ToggleButton>
        </Box>
      )}

      <Divider sx={{ my: 3 }} />

      {/* 排序 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" gutterBottom>排序方式</Typography>
        <FormControl fullWidth>
          <Select
            value={filters.sortBy}
            onChange={(e) => handleFilterChange('sortBy', e.target.value)}
            IconComponent={ArrowUpDown}
          >
            {sortOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
      {/* 顶部搜索和筛选栏 */}
      <Box sx={{ bgcolor: 'white', boxShadow: 1, py: 2, sticky: 'top', zIndex: 10 }}>
        <Box sx={{ maxWidth: '1200px', mx: 'auto', px: { xs: 2, md: 4 }, display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'center' }}>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'block' } }}>
            <TextField
              fullWidth
              placeholder="搜索食谱名称、描述或标签"
              value={filters.searchTerm}
              onChange={(e) => handleFilterChange('searchTerm', e.target.value)}
              InputProps={{
                startAdornment: <Search fontSize="small" />
              }}
            />
          </Box>
          
          <Box sx={{ display: 'flex', gap: 1 }}>
            <ToggleButtonGroup
              size="small"
              value={viewMode}
              exclusive
              onChange={handleViewModeChange}
            >
              <ToggleButton value="grid" aria-label="grid view">
                <Grid fontSize="small" />
              </ToggleButton>
              <ToggleButton value="list" aria-label="list view">
                <Typography variant="body2">列表</Typography>
              </ToggleButton>
            </ToggleButtonGroup>
            
            <Button 
              startIcon={<Plus />}
              color="primary"
              onClick={() => navigate('/recipes/create')}
            >
              发布食谱
            </Button>
            
            <IconButton 
              variant="outlined"
              color="primary"
              onClick={() => setMobileFilterOpen(true)}
              sx={{ display: { md: 'none' } }}
            >
              <FilterList />
            </IconButton>
          </Box>
        </Box>
      </Box>

      {/* 移动端筛选抽屉 */}
      <Drawer
        anchor="right"
        open={mobileFilterOpen}
        onClose={() => setMobileFilterOpen(false)}
      >
        <Box sx={{ width: 300, maxWidth: '80vw' }}>
          {renderFilters()}
        </Box>
      </Drawer>

      <Box sx={{ maxWidth: '1200px', mx: 'auto', px: { xs: 2, md: 4 }, py: 6 }}>
        {/* 标题和结果统计 */}
        <Box sx={{ mb: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
          <Box>
            <Typography variant="h4" gutterBottom>食谱探索</Typography>
            <Typography variant="body2" color="text.secondary">
              发现 {filteredRecipes.length} 个食谱
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            {filters.searchTerm && (
              <Chip
                label={`搜索: ${filters.searchTerm}`}
                size="small"
                color="primary"
                onDelete={() => handleFilterChange('searchTerm', '')}
                sx={{ mr: 1 }}
              />
            )}
            {filters.difficulty && (
              <Chip
                label={`难度: ${filters.difficulty}`}
                size="small"
                color="primary"
                onDelete={() => handleFilterChange('difficulty', '')}
                sx={{ mr: 1 }}
              />
            )}
            {filters.favoriteOnly && (
              <Chip
                icon={<Heart fontSize="small" />}
                label="仅收藏"
                size="small"
                color="error"
                onDelete={() => handleFilterChange('favoriteOnly', false)}
                sx={{ mr: 1 }}
              />
            )}
            {filters.dietaryPreferences.length > 0 && (
              <Chip
                label={`偏好: ${filters.dietaryPreferences.length}`}
                size="small"
                color="primary"
                onDelete={() => handleFilterChange('dietaryPreferences', [])}
                sx={{ mr: 1 }}
              />
            )}
            {(filters.searchTerm || filters.difficulty || filters.favoriteOnly || filters.dietaryPreferences.length > 0) && (
              <Button 
                size="small" 
                onClick={resetFilters}
                startIcon={<X fontSize="small" />}
              >
                清除筛选
              </Button>
            )}
          </Box>
        </Box>

        <Grid container spacing={4}>
          {/* 桌面端筛选侧边栏 */}
          <Grid item xs={12} md={3} sx={{ display: { xs: 'none', md: 'block' } }}>
            <Paper elevation={2} sx={{ position: 'sticky', top: 100 }}>
              {renderFilters()}
            </Paper>
          </Grid>

          {/* 食谱列表 */}
          <Grid item xs={12} md={9}>
            {loading && page === 1 ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
                <CircularProgress />
              </Box>
            ) : error ? (
              <Paper elevation={2} sx={{ p: 4, textAlign: 'center' }}>
                <Alert severity="error" sx={{ mb: 4 }}>
                  {error}
                </Alert>
                <Button variant="contained" onClick={handleRefresh}>
                  重试
                </Button>
              </Paper>
            ) : filteredRecipes.length === 0 ? (
              <Paper elevation={2} sx={{ p: 8, textAlign: 'center' }}>
                <Typography variant="h6" gutterBottom>未找到匹配的食谱</Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                  尝试调整筛选条件或搜索关键词
                </Typography>
                <Button variant="outlined" onClick={resetFilters}>
                  清除所有筛选
                </Button>
              </Paper>
            ) : (
              <>
                {/* 食谱网格/列表视图 */}
                <Grid 
                  container 
                  spacing={3} 
                  sx={{ 
                    gridTemplateColumns: viewMode === 'grid' 
                      ? { xs: 'repeat(1, 1fr)', sm: 'repeat(2, 1fr)' } 
                      : '1fr' 
                  }}
                >
                  {filteredRecipes.map((recipe) => (
                    <Grid 
                      item 
                      key={recipe.id} 
                      sx={{ 
                        display: 'flex',
                        '& > div': { 
                          width: '100%',
                          height: '100%'
                        }
                      }}
                    >
                      <RecipeCard 
                        recipe={recipe} 
                        viewMode={viewMode}
                        onRecipeClick={() => navigate(`/recipes/${recipe.id}`)}
                      />
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
                  {!hasMore && recipes.length > 0 && (
                    <Typography variant="body2" color="text.secondary">
                      已显示全部食谱
                    </Typography>
                  )}
                </Box>
              </>
            )}
          </Grid>
        </Grid>

        {/* 热门分类推荐 */}
        <Box sx={{ mt: 12, mb: 8 }}>
          <Typography variant="h5" gutterBottom>热门分类</Typography>
          <Grid container spacing={3}>
            {categories.slice(1).map((category) => (
              <Grid item xs={6} sm={4} md={3} key={category}>
                <Paper 
                  elevation={2} 
                  sx={{ 
                    p: 4, 
                    textAlign: 'center',
                    cursor: 'pointer',
                    '&:hover': { 
                      bgcolor: 'primary.light',
                      transition: '0.3s'
                    }
                  }}
                  onClick={() => handleFilterChange('category', category)}
                >
                  <Typography variant="h6" color="primary.main" gutterBottom>
                    {category}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    探索{category}食谱
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* 快速筛选 */}
        <Box sx={{ mb: 8 }}>
          <Typography variant="h6" gutterBottom>快速筛选</Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            <Chip
              label="30分钟内完成"
              color="primary"
              onClick={() => handleFilterChange('timeRange', '30分钟内')}
              sx={{ cursor: 'pointer' }}
            />
            <Chip
              label="简单易做"
              color="success"
              onClick={() => handleFilterChange('difficulty', '简单')}
              sx={{ cursor: 'pointer' }}
            />
            <Chip
              label="高评分食谱"
              color="warning"
              onClick={() => handleFilterChange('sortBy', 'rating')}
              icon={<Star fontSize="small" />}
              sx={{ cursor: 'pointer' }}
            />
            <Chip
              label="素食主义"
              color="info"
              onClick={() => {
                handleFilterChange('dietaryPreferences', ['素食']);
              }}
              sx={{ cursor: 'pointer' }}
            />
            <Chip
              label="适合新手"
              color="secondary"
              onClick={() => {
                handleFilterChange('difficulty', '简单');
                handleFilterChange('timeRange', '30分钟内');
              }}
              sx={{ cursor: 'pointer' }}
            />
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default RecipeListPage;