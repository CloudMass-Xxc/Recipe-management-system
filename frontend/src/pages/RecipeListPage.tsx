import React, { useState, useEffect } from 'react';
import { Box, Typography, Card, CardContent, CardMedia, Button, TextField, Chip, ToggleButton, ToggleButtonGroup, Container, useMediaQuery, useTheme } from '@mui/material';
import { Link } from 'react-router-dom';

interface Recipe {
  id: string;
  title: string;
  description: string;
  cookTime: string;
  difficulty: string;
  image: string;
  isVegetarian: boolean;
  isBeginnerFriendly: boolean;
}

const RecipeListPage: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [filteredRecipes, setFilteredRecipes] = useState<Recipe[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [filters, setFilters] = useState({
    vegetarian: false,
    beginnerFriendly: false,
  });
  const [sortBy, setSortBy] = useState('default');

  useEffect(() => {
    // 模拟获取食谱列表数据
    const mockRecipes: Recipe[] = [
      {
        id: '1',
        title: '健康蔬菜炒饭',
        description: '营养丰富的蔬菜炒饭，适合素食者。',
        cookTime: '20分钟',
        difficulty: '简单',
        image: 'https://via.placeholder.com/400x300?text=健康蔬菜炒饭',
        isVegetarian: true,
        isBeginnerFriendly: true,
      },
      {
        id: '2',
        title: '香煎三文鱼',
        description: '美味的香煎三文鱼配时蔬。',
        cookTime: '30分钟',
        difficulty: '中等',
        image: 'https://via.placeholder.com/400x300?text=香煎三文鱼',
        isVegetarian: false,
        isBeginnerFriendly: false,
      },
      {
        id: '3',
        title: '番茄鸡蛋面',
        description: '经典的家常菜，简单又美味。',
        cookTime: '15分钟',
        difficulty: '简单',
        image: 'https://via.placeholder.com/400x300?text=番茄鸡蛋面',
        isVegetarian: false,
        isBeginnerFriendly: true,
      },
      {
        id: '4',
        title: '素食沙拉',
        description: '新鲜的蔬菜沙拉，健康又清爽。',
        cookTime: '10分钟',
        difficulty: '简单',
        image: 'https://via.placeholder.com/400x300?text=素食沙拉',
        isVegetarian: true,
        isBeginnerFriendly: true,
      },
    ];
    setRecipes(mockRecipes);
    setFilteredRecipes(mockRecipes);
  }, []);

  useEffect(() => {
    // 应用搜索和筛选
    let result = recipes.filter(recipe => 
      recipe.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      recipe.description.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (filters.vegetarian) {
      result = result.filter(recipe => recipe.isVegetarian);
    }

    if (filters.beginnerFriendly) {
      result = result.filter(recipe => recipe.isBeginnerFriendly);
    }

    // 应用排序
    if (sortBy === 'cookTime') {
      result.sort((a, b) => {
        const timeA = parseInt(a.cookTime);
        const timeB = parseInt(b.cookTime);
        return timeA - timeB;
      });
    } else if (sortBy === 'difficulty') {
      const difficultyOrder: Record<string, number> = { '简单': 0, '中等': 1, '困难': 2 };
      result.sort((a, b) => (difficultyOrder[a.difficulty] || 0) - (difficultyOrder[b.difficulty] || 0));
    }

    setFilteredRecipes(result);
  }, [recipes, searchTerm, filters, sortBy]);

  const handleViewModeChange = (_event: React.MouseEvent<HTMLElement>, newMode: 'grid' | 'list' | null) => {
    if (newMode !== null) {
      setViewMode(newMode);
    }
  };

  const handleFilterChange = (filter: 'vegetarian' | 'beginnerFriendly') => {
    setFilters(prev => ({ ...prev, [filter]: !prev[filter] }));
  };

  const renderFilters = () => (
    <Box sx={{ mb: { xs: 3, sm: 4 } }}>
      <Typography variant="h6" gutterBottom>筛选条件</Typography>
      
      {/* 在小屏幕上堆叠搜索框和筛选标签 */}
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2, mb: 3, width: '100%' }}>
        <TextField
          label="搜索食谱"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          variant="outlined"
          size={isMobile ? "small" : "medium"}
          fullWidth
          sx={{ 
            '& .MuiOutlinedInput-root': {
              fontSize: isMobile ? '0.875rem' : '1rem',
              padding: 0
            }
          }}
        />
        <Box sx={{ 
          display: 'flex', 
          gap: 1,
          flexWrap: 'wrap',
          justifyContent: { xs: 'flex-start', sm: 'flex-end' },
          alignItems: 'center'
        }}>
          <Chip
            label="素食"
            onClick={() => handleFilterChange('vegetarian')}
            color={filters.vegetarian ? "primary" : "default"}
            variant={filters.vegetarian ? "filled" : "outlined"}
            size={isMobile ? "small" : "medium"}
          />
          <Chip
            label="适合新手"
            onClick={() => handleFilterChange('beginnerFriendly')}
            color={filters.beginnerFriendly ? "primary" : "default"}
            variant={filters.beginnerFriendly ? "filled" : "outlined"}
            size={isMobile ? "small" : "medium"}
          />
        </Box>
      </Box>
      
      {/* 排序选项 - 在小屏幕上调整布局 */}
      <Box sx={{ 
        display: 'flex', 
        flexDirection: { xs: 'column', sm: 'row' },
        alignItems: { xs: 'stretch', sm: 'center' }, 
        gap: { xs: 2, sm: 1 }
      }}>
        <Typography variant="subtitle2">排序方式：</Typography>
        <ToggleButtonGroup
          value={sortBy}
          exclusive
          onChange={(_event: React.MouseEvent<HTMLElement>, newValue: string | null) => {
            if (newValue !== null) {
              setSortBy(newValue);
            }
          }}
          size={isMobile ? "small" : "medium"}
          fullWidth={isMobile}
          sx={{
            '& .MuiToggleButton-root': {
              py: { xs: 0.75, sm: 1 },
              minWidth: isMobile ? 'auto' : 'auto'
            }
          }}
        >
          <ToggleButton value="default">默认</ToggleButton>
          <ToggleButton value="cookTime">烹饪时间</ToggleButton>
          <ToggleButton value="difficulty">难度</ToggleButton>
        </ToggleButtonGroup>
      </Box>
    </Box>
  );

  const renderRecipeGrid = () => (
      <Box className="recipe-grid" sx={{ 
        display: 'flex', 
        flexWrap: 'wrap', 
        gap: { xs: 2, sm: 3 },
        justifyContent: 'center'
      }}>
        {filteredRecipes.map(recipe => (
          <Box
            key={recipe.id}
            sx={{
              width: {
                xs: '100%',     // 小屏幕单栏
                sm: 'calc(50% - 16px)', // 平板双栏
                lg: 'calc(33.333% - 16px)', // 桌面三栏
                xl: 'calc(25% - 16px)' // 大屏幕四栏
              },
              maxWidth: { xs: '100%', md: 'none' },
              transition: 'transform 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                transition: 'transform 0.2s'
              }
            }}
          >
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardMedia
                component="img"
                height="200"
                image={recipe.image}
                alt={recipe.title}
                sx={{ 
                  objectFit: 'cover',
                  height: { xs: 160, sm: 180, md: 200 }
                }}
              />
              <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                <Typography 
                  variant={isMobile ? "subtitle1" : "h6"} 
                  gutterBottom
                  sx={{ fontWeight: 600, height: { xs: 56, sm: 'auto' } }}
                  noWrap={isMobile}
                >
                  {recipe.title}
                </Typography>
                <Typography 
                  variant="body2" 
                  color="text.secondary" 
                  gutterBottom
                  sx={{ height: 40, overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }}
                >
                  {recipe.description}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                  {recipe.isVegetarian && (
                    <Chip label="素食" size="small" color="success" />
                  )}
                  {recipe.isBeginnerFriendly && (
                    <Chip label="适合新手" size="small" color="info" />
                  )}
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 'auto' }}>
                  <Typography variant="body2" color="text.secondary">
                    {recipe.cookTime} | {recipe.difficulty}
                  </Typography>
                  <Button 
                    component={Link} 
                    to={`/recipe/${recipe.id}`} 
                    variant="contained" 
                    size={isMobile ? "small" : "medium"}
                    sx={{ py: isMobile ? 0.5 : 0.75 }}
                  >
                    查看详情
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Box>
        ))}
      </Box>
    );

  const renderRecipeList = () => (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: { xs: 2, sm: 3 } }}>
      {filteredRecipes.map(recipe => (
        <Card 
          key={recipe.id} 
          sx={{ 
            display: 'flex', 
            flexDirection: { xs: 'column', md: 'row' },
            borderRadius: 2,
            overflow: 'hidden',
            transition: 'transform 0.2s',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: theme.shadows[3],
              transition: 'transform 0.2s, box-shadow 0.2s'
            }
          }}
        >
          <CardMedia
            component="img"
            width="200"
            height="180"
            image={recipe.image}
            alt={recipe.title}
            sx={{ 
              objectFit: 'cover',
              width: { xs: '100%', md: 200 },
              height: { xs: 180, md: 'auto' }
            }}
          />
          <CardContent sx={{ 
            flex: 1, 
            display: 'flex', 
            flexDirection: 'column',
            p: { xs: 2, sm: 3 }
          }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 1, flexWrap: 'wrap', gap: 1 }}>
              <Typography 
                variant={isMobile ? "subtitle1" : "h6"} 
                sx={{ fontWeight: 600 }}
              >
                {recipe.title}
              </Typography>
              <Button 
                component={Link} 
                to={`/recipe/${recipe.id}`} 
                variant="contained" 
                size={isMobile ? "small" : "medium"}
              >
                查看详情
              </Button>
            </Box>
            <Typography 
              variant="body2" 
              color="text.secondary" 
              gutterBottom
              sx={{ 
                display: '-webkit-box',
                WebkitLineClamp: isMobile ? 2 : 3,
                WebkitBoxOrient: 'vertical',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                lineHeight: 1.5
              }}
            >
              {recipe.description}
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, mb: 1, flexWrap: 'wrap' }}>
              {recipe.isVegetarian && (
                <Chip label="素食" size="small" color="success" />
              )}
              {recipe.isBeginnerFriendly && (
                <Chip label="适合新手" size="small" color="info" />
              )}
            </Box>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 'auto' }}>
              {recipe.cookTime} | {recipe.difficulty}
            </Typography>
          </CardContent>
        </Card>
      ))}
    </Box>
  );

  return (
    <Container maxWidth={isMobile ? "md" : "lg"} sx={{ p: { xs: 0, sm: 2 } }}>
      <Box sx={{ mb: { xs: 3, sm: 4 } }}>
        <Typography 
          variant={isMobile ? "h5" : "h4"} 
          component="h1" 
          gutterBottom
          sx={{ fontWeight: 700, color: theme.palette.primary.main }}
        >
          食谱列表
        </Typography>
        <Typography 
          variant="body1" 
          gutterBottom
          sx={{ color: theme.palette.text.secondary, maxWidth: { xs: '100%', md: '80%' } }}
        >
          发现美味的食谱，满足您的味蕾需求
        </Typography>
      </Box>

      <Box sx={{ mb: { xs: 3, sm: 4 }, bgcolor: 'background.paper', borderRadius: 2, p: { xs: 2, sm: 3 }, boxShadow: theme.shadows[1] }}>
        {/* 视图切换按钮 */}
        <Box sx={{ 
          display: 'flex', 
          justifyContent: { xs: 'center', md: 'flex-start' }, 
          alignItems: 'center', 
          mb: { xs: 3, sm: 4 } 
        }}>
          <ToggleButtonGroup
            value={viewMode}
            exclusive
            onChange={handleViewModeChange}
            size={isMobile ? "small" : "medium"}
            sx={{
              '& .MuiToggleButton-root': {
                fontSize: { xs: '0.875rem', sm: '1rem' },
                py: { xs: 0.75, sm: 1 }
              }
            }}
          >
            <ToggleButton value="grid">网格视图</ToggleButton>
            <ToggleButton value="list">列表视图</ToggleButton>
          </ToggleButtonGroup>
        </Box>
        
        {/* 筛选区域 */}
        {renderFilters()}
      </Box>

      <Box sx={{ pb: 6 }}>
        <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 500 }}>
          共找到 {filteredRecipes.length} 个食谱
        </Typography>
        
        {filteredRecipes.length === 0 ? (
          <Box 
            sx={{ 
              bgcolor: 'background.paper', 
              borderRadius: 2, 
              p: { xs: 4, sm: 6 }, 
              textAlign: 'center',
              boxShadow: theme.shadows[1]
            }}
          >
            <Typography 
              variant="body1" 
              color="text.secondary" 
              gutterBottom
              sx={{ mb: 2 }}
            >
              没有找到匹配的食谱，请尝试调整筛选条件
            </Typography>
            <Button 
              variant="outlined" 
              onClick={() => {
                setSearchTerm('');
                setFilters({ vegetarian: false, beginnerFriendly: false });
                setSortBy('default');
              }}
            >
              重置筛选条件
            </Button>
          </Box>
        ) : viewMode === 'grid' ? (
          renderRecipeGrid()
        ) : (
          renderRecipeList()
        )}
      </Box>
    </Container>
  );
};

export default RecipeListPage;