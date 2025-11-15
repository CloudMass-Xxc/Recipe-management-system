import React from 'react';
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Box,
  Chip,
  CardActions,
  Button,
  Avatar
} from '@mui/material';
import { Star, Clock, Users, ChefHat, Heart, Share } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { RecipeResponse } from '../../types/recipe';

interface RecipeCardProps {
  recipe: RecipeResponse;
  onFavorite?: (id: string) => void;
  isFavorite?: boolean;
}

const RecipeCard: React.FC<RecipeCardProps> = ({ 
  recipe, 
  onFavorite, 
  isFavorite = false 
}) => {
  const navigate = useNavigate();

  const handleViewDetails = () => {
    navigate(`/recipes/${recipe.id}`);
  };

  const handleFavoriteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onFavorite) {
      onFavorite(recipe.id);
    }
  };

  const handleShareClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    // 分享功能实现
    alert('分享功能将在后续版本中实现');
  };

  const getDifficultyLabel = (difficulty: string): string => {
    switch (difficulty) {
      case 'easy': return '简单';
      case 'medium': return '中等';
      case 'hard': return '困难';
      default: return difficulty;
    }
  };

  const getDifficultyColor = (difficulty: string): string => {
    switch (difficulty) {
      case 'easy': return 'success';
      case 'medium': return 'warning';
      case 'hard': return 'error';
      default: return 'default';
    }
  };

  const getMealTypeLabel = (mealType?: string): string => {
    if (!mealType) return '';
    switch (mealType) {
      case 'breakfast': return '早餐';
      case 'lunch': return '午餐';
      case 'dinner': return '晚餐';
      case 'snack': return '小吃';
      case 'dessert': return '甜点';
      default: return mealType;
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

  return (
    <Card 
      elevation={2} 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 10px 20px rgba(0,0,0,0.12), 0 4px 8px rgba(0,0,0,0.06)'
        }
      }}
    >
      <Box sx={{ position: 'relative', cursor: 'pointer' }} onClick={handleViewDetails}>
        {recipe.image_url ? (
          <CardMedia
            component="img"
            height="200"
            image={recipe.image_url}
            alt={recipe.title}
            sx={{ objectFit: 'cover' }}
          />
        ) : (
          <Box sx={{ height: 200, bgcolor: 'grey.100', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <ChefHat fontSize="large" color="disabled" />
          </Box>
        )}
        
        {/* 食谱标签 */}
        <Box sx={{ position: 'absolute', top: 8, left: 8, display: 'flex', flexDirection: 'column', gap: 4 }}>
          {recipe.meal_type && (
            <Chip 
              label={getMealTypeLabel(recipe.meal_type)} 
              size="small" 
              sx={{ bgcolor: 'rgba(255,255,255,0.9)', fontWeight: 'medium' }}
            />
          )}
          <Chip 
            label={getDifficultyLabel(recipe.difficulty)} 
            size="small" 
            color={getDifficultyColor(recipe.difficulty)} 
            sx={{ bgcolor: `${getDifficultyColor(recipe.difficulty)}.main`, color: 'white', fontWeight: 'medium' }}
          />
        </Box>
        
        {/* 收藏按钮 */}
        <Button 
          variant="text" 
          sx={{ 
            position: 'absolute', 
            top: 8, 
            right: 8,
            minWidth: 'auto',
            bgcolor: 'rgba(255,255,255,0.9)',
            '&:hover': {
              bgcolor: 'rgba(255,255,255,1)'
            }
          }}
          onClick={handleFavoriteClick}
        >
          <Heart 
            fontSize="small" 
            color={isFavorite ? "error" : "default"} 
            fill={isFavorite ? "currentColor" : "none"}
          />
        </Button>
      </Box>

      <CardContent sx={{ flexGrow: 1 }} onClick={handleViewDetails} style={{ cursor: 'pointer' }}>
        <Typography gutterBottom variant="h6" component="div" noWrap>
          {recipe.title}
        </Typography>
        
        <Typography variant="body2" color="text.secondary" paragraph lineClamp={2}>
          {recipe.description}
        </Typography>

        {/* 食谱基本信息 */}
        <Box sx={{ display: 'flex', gap: 3, mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Clock fontSize="small" color="disabled" />
            <Typography variant="caption">
              {formatTime(recipe.prep_time + recipe.cook_time)}
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Users fontSize="small" color="disabled" />
            <Typography variant="caption">
              {recipe.servings}人份
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Star fontSize="small" color="warning" />
            <Typography variant="caption" fontWeight="medium">
              {recipe.average_rating || 0}
            </Typography>
          </Box>
        </Box>

        {/* 食谱标签 */}
        {recipe.tags && recipe.tags.length > 0 && (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
            {recipe.tags.slice(0, 3).map((tag, index) => (
              <Chip key={index} label={tag} size="small" variant="outlined" />
            ))}
            {recipe.tags.length > 3 && (
              <Chip label={`+${recipe.tags.length - 3}`} size="small" variant="outlined" disabled />
            )}
          </Box>
        )}
      </CardContent>

      <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
        <Button 
          size="small" 
          variant="contained" 
          onClick={handleViewDetails}
          sx={{ fontWeight: 'medium' }}
        >
          查看详情
        </Button>
        <Button 
          size="small" 
          variant="text" 
          onClick={handleShareClick}
        >
          <Share fontSize="small" />
        </Button>
      </CardActions>
    </Card>
  );
};

export default RecipeCard;