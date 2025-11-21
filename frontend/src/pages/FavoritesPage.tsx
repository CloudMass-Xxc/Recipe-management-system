import React, { useEffect, useState } from 'react';
import { 
  Container, 
  Typography, 
  Card, 
  CardContent, 
  CardMedia, 
  Button, 
  Box, 
  Chip,
  useMediaQuery,
  useTheme
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAppSelector, useAppDispatch } from '../redux/hooks';
import { fetchRecipes, toggleFavorite } from '../redux/slices/recipeSlice';
// import { Favorite, FavoriteBorder, ArrowBack } from '@mui/icons-material';

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

const FavoritesPage: React.FC = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { recipes, favorites } = useAppSelector((state) => state.recipes);
  const [favoriteRecipes, setFavoriteRecipes] = useState<Recipe[]>([]);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  useEffect(() => {
    // 获取所有食谱
    dispatch(fetchRecipes());
  }, [dispatch]);

  useEffect(() => {
    // 过滤出收藏的食谱
    const filtered = recipes.filter(recipe => favorites.includes(recipe.id));
    setFavoriteRecipes(filtered);
  }, [recipes, favorites]);

  const handleRecipeClick = (recipeId: string) => {
    navigate(`/recipe/${recipeId}`);
  };

  const handleToggleFavorite = (event: React.MouseEvent, recipeId: string) => {
    event.stopPropagation();
    dispatch(toggleFavorite(recipeId));
  };

  const handleBack = () => {
    navigate('/profile');
  };

  // 模拟收藏数据（当Redux中没有数据时显示）
  const mockFavoriteRecipes: Recipe[] = [
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
      id: '3',
      title: '番茄鸡蛋面',
      description: '经典的家常菜，简单又美味。',
      cookTime: '15分钟',
      difficulty: '简单',
      image: 'https://via.placeholder.com/400x300?text=番茄鸡蛋面',
      isVegetarian: false,
      isBeginnerFriendly: true,
    },
  ];

  // 如果没有收藏的食谱，使用模拟数据
  const displayRecipes = favoriteRecipes.length > 0 ? favoriteRecipes : mockFavoriteRecipes;

  return (
    <Container maxWidth="lg" sx={{ mt: { xs: 3, sm: 4 }, mb: 4, pt: { xs: 2 } }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: { xs: 3, sm: 4 } }}>
        <Button onClick={handleBack} sx={{ mr: { xs: 1, sm: 2 } }} size={isMobile ? "small" : "medium"}>
          返回
        </Button>
        <Typography 
          variant={isMobile ? "h5" : "h4"} 
          component="h1"
          sx={{ wordBreak: 'break-word' }}
        >
          我的收藏
        </Typography>
      </Box>

      {displayRecipes.length === 0 ? (
        <Box sx={{ textAlign: 'center', py: { xs: 6, sm: 8 } }}>
          <Typography variant={isMobile ? "subtitle1" : "h6"} color="text.secondary" gutterBottom>
            您还没有收藏任何食谱
          </Typography>
          <Button 
            variant="contained" 
            onClick={() => navigate('/recipes')}
            size={isMobile ? "small" : "medium"}
          >
            浏览食谱
          </Button>
        </Box>
      ) : (
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: { xs: 2, sm: 3 } }}>
          {displayRecipes.map((recipe) => (
            <Box 
              sx={{ 
                width: { 
                  xs: '100%', 
                  sm: 'calc(50% - 12px)', 
                  md: 'calc(33.333% - 12px)',
                  xl: 'calc(25% - 12px)'
                } 
              }} 
              key={recipe.id}>
              <Card 
                elevation={2} 
                sx={{ 
                  height: '100%', 
                  display: 'flex', 
                  flexDirection: 'column',
                  '&:hover': { boxShadow: 3 }
                }}
                onClick={() => handleRecipeClick(recipe.id)}
              >
                <Box sx={{ position: 'relative' }}>
                  <CardMedia
                    component="img"
                    height="180"
                    image={recipe.image}
                    alt={recipe.title}
                    sx={{ objectFit: 'cover' }}
                  />
                  <Button 
                    sx={{ 
                      position: 'absolute', 
                      top: { xs: 4, sm: 8 }, 
                      right: { xs: 4, sm: 8 },
                      minWidth: 'auto',
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f0f0f0' },
                      p: { xs: 1, sm: 1.5 }
                    }}
                    onClick={(e) => handleToggleFavorite(e, recipe.id)}
                    size={isMobile ? "small" : "medium"}
                  >
                    {favorites.includes(recipe.id) ? "取消收藏" : "收藏"}
                  </Button>
                  <Box sx={{ position: 'absolute', bottom: { xs: 4, sm: 8 }, left: { xs: 4, sm: 8 }, display: 'flex', gap: 1 }}>
                    {recipe.isVegetarian && (
                      <Chip 
                        label="素食" 
                        size="small" 
                        sx={{ bgcolor: '#4caf50', color: 'white' }}
                      />
                    )}
                    {recipe.isBeginnerFriendly && (
                      <Chip 
                        label="适合新手" 
                        size="small" 
                        sx={{ bgcolor: '#2196f3', color: 'white' }}
                      />
                    )}
                  </Box>
                </Box>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" component="h3" gutterBottom>
                    {recipe.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {recipe.description}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                    <Chip 
                      label={recipe.cookTime} 
                      size="small" 
                      variant="outlined"
                    />
                    <Chip 
                      label={recipe.difficulty} 
                      size="small" 
                      variant="outlined"
                    />
                  </Box>
                </CardContent>
                <Box sx={{ p: 2, borderTop: '1px solid rgba(0, 0, 0, 0.1)' }}>
                  <Button 
                    variant="outlined" 
                    fullWidth
                    onClick={() => handleRecipeClick(recipe.id)}
                  >
                    查看详情
                  </Button>
                </Box>
              </Card>
            </Box>
          ))}
        </Box>
      )}
    </Container>
  );
};

export default FavoritesPage;