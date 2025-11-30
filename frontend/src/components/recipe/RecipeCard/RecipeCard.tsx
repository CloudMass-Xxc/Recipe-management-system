import React, { useState } from 'react';
import { Card, CardContent, CardMedia, Typography, Rating, Button, Box, Chip, CardActions, Dialog, DialogTitle, DialogContent, DialogActions as MuiDialogActions, DialogContentText } from '@mui/material';
import { Favorite, FavoriteBorder, Book, Delete } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import type { RecipeListItem, Recipe } from '../../../types/recipe';

  interface RecipeCardProps {
    recipe: RecipeListItem | Recipe;
    onFavorite?: (recipeId: string) => void;
    onDelete?: (recipeId: string) => void;
    isFavorite?: boolean;
  }

const RecipeCard: React.FC<RecipeCardProps> = ({ recipe, onFavorite, onDelete, isFavorite = false }) => {
  // 检查图片URL是否有效
  // 验证图片URL的有效性（暂时注释，因为当前未使用）
  // const isImageUrlValid = recipe.image_url && typeof recipe.image_url === 'string' && recipe.image_url.trim() !== '';

  const navigate = useNavigate();
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);

  const handleFavoriteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    onFavorite?.(recipe.recipe_id);
  };

  const handleCardClick = () => {
    if (recipe.recipe_id) {
      navigate(`/recipe-detail/${recipe.recipe_id}`);
    }
  };

  const handleDeleteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setOpenDeleteDialog(true);
  };

  const handleConfirmDelete = () => {
    onDelete?.(recipe.recipe_id);
    setOpenDeleteDialog(false);
  };

  const handleCancelDelete = () => {
    setOpenDeleteDialog(false);
  };

  return (
    <Card
      sx={{
        maxWidth: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        borderRadius: 2,
        overflow: 'hidden',
        transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-8px)',
          boxShadow: '0 16px 32px rgba(0,0,0,0.15)',
          cursor: 'pointer'
        },
      }}
      onClick={handleCardClick}
    >
      <CardMedia
        sx={{
          height: { xs: 180, md: 220 },
          backgroundImage: `url(${recipe.image_url || 'https://picsum.photos/400/220?random=recipe'})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          transition: 'transform 0.5s ease',
          '&:hover': {
            transform: 'scale(1.05)',
          },
        }}
      />
      <CardContent sx={{ flexGrow: 1, p: { xs: 2, md: 3 } }}>
        <Typography gutterBottom variant="h6" component="div" sx={{ 
          fontWeight: 700, 
          fontSize: { xs: '1.125rem', md: '1.25rem' },
          mb: 1,
          lineHeight: 1.3,
        }}>
          {recipe.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ 
          mb: 2, 
          display: '-webkit-box', 
          WebkitLineClamp: 2, 
          WebkitBoxOrient: 'vertical', 
          overflow: 'hidden',
          fontSize: { xs: '0.875rem', md: '0.9375rem' },
          lineHeight: 1.5,
        }}>
          {recipe.description}
        </Typography>
        <Box sx={{ display: 'flex', gap: 1.5, mb: 2 }}>
          <Chip
            label={`${recipe.cooking_time}分钟`}
            size="small"
            sx={{ 
              backgroundColor: '#e3f2fd', 
              color: '#1976d2',
              fontWeight: 500,
              borderRadius: 1,
              fontSize: '0.75rem',
            }}
          />
          <Chip
            label={recipe.difficulty}
            size="small"
            sx={{ 
              backgroundColor: '#e8f5e8', 
              color: '#388e3c',
              fontWeight: 500,
              borderRadius: 1,
              fontSize: '0.75rem',
            }}
          />
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Rating 
            value={0} 
            precision={0.5} 
            readOnly 
            size="small" 
            sx={{
              '& .MuiRating-iconFilled': {
                color: '#ff9800',
              },
              '& .MuiRating-iconEmpty': {
                color: '#e0e0e0',
              },
            }}
          />
          <Typography variant="caption" color="text.secondary" sx={{ 
            ml: 1, 
            fontWeight: 500,
            fontSize: '0.75rem',
          }}>
            (0)
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.75 }}>
            {recipe.tags && recipe.tags.length > 0 ? (
              recipe.tags.map((tag, index) => (
                <Chip 
                  key={index} 
                  label={tag} 
                  size="small" 
                  variant="outlined" 
                  sx={{ 
                    fontSize: '0.75rem',
                    borderRadius: 1,
                  }}
                />
              ))
            ) : (
              <Typography variant="body2" color="text.secondary">
                暂无标签
              </Typography>
            )}
          </Box>
      </CardContent>
      <CardActions sx={{
        justifyContent: 'space-between', 
        p: { xs: 2, md: 3 },
        pt: 0,
      }}>
        <Button
          size="small"
          startIcon={<Book />}
          onClick={(e) => {
            e.stopPropagation();
            if (recipe.recipe_id) {
              navigate(`/recipe-detail/${recipe.recipe_id}`);
            }
          }}
          sx={{
            textTransform: 'none',
            fontWeight: 600,
            color: '#4caf50',
            padding: '6px 12px',
            borderRadius: 1.5,
            '&:hover': {
              backgroundColor: 'rgba(76, 175, 80, 0.1)',
            },
          }}
        >
          查看详情
        </Button>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            size="small"
            startIcon={isFavorite ? <Favorite /> : <FavoriteBorder />}
            onClick={handleFavoriteClick}
            sx={{
              textTransform: 'none',
              fontWeight: 600,
              color: isFavorite ? '#f44336' : 'inherit',
              padding: '6px 12px',
              borderRadius: 1.5,
              '&:hover': {
                backgroundColor: isFavorite ? 'rgba(244, 67, 54, 0.1)' : 'rgba(0, 0, 0, 0.04)',
              },
            }}
          >
            {isFavorite ? '已收藏' : '收藏'}
          </Button>
          <Button
            size="small"
            startIcon={<Delete />}
            onClick={handleDeleteClick}
            sx={{
              textTransform: 'none',
              fontWeight: 600,
              color: '#f44336',
              padding: '6px 12px',
              borderRadius: 1.5,
              '&:hover': {
                backgroundColor: 'rgba(244, 67, 54, 0.1)',
              },
            }}
          >
            删除
          </Button>
        </Box>
      </CardActions>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={openDeleteDialog}
        onClose={handleCancelDelete}
        aria-labelledby="delete-dialog-title"
      >
        <DialogTitle id="delete-dialog-title">确认删除</DialogTitle>
        <DialogContent>
          <DialogContentText>
            确定要删除食谱「{recipe.title}」吗？
            此操作不可逆，删除后数据将无法恢复。
          </DialogContentText>
        </DialogContent>
        <MuiDialogActions>
          <Button onClick={handleCancelDelete} sx={{ textTransform: 'none' }}>
            取消
          </Button>
          <Button
            onClick={handleConfirmDelete}
            sx={{
              textTransform: 'none',
              color: '#f44336',
              fontWeight: 600,
            }}
          >
            确认删除
          </Button>
        </MuiDialogActions>
      </Dialog>
    </Card>
  );
};

export default RecipeCard;
