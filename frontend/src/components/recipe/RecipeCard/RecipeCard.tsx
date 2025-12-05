import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardMedia, Typography, Button, Box, Chip, CardActions, Dialog, DialogTitle, DialogContent, DialogActions as MuiDialogActions, DialogContentText, CircularProgress, Tooltip, Snackbar, Alert, IconButton } from '@mui/material';
import { Book, Delete, Favorite, FavoriteBorder, AccessTime, Restaurant, Star } from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import type { RecipeListItem, Recipe } from '../../../types/recipe';
import { deleteRecipe } from '../../../store/slices/recipeSlice';
import type { RootState } from '../../../store';
import { recipeService } from '../../../services/recipe.service';

interface RecipeCardProps {
  recipe: RecipeListItem | Recipe;
  onDelete?: () => void;
  onView?: (recipeId: string) => void;
  onFavoriteChange?: (recipeId: string, isFavorite: boolean) => void;
}

const RecipeCard: React.FC<RecipeCardProps> = ({ recipe, onView, onFavoriteChange }) => {
  // 检查图片URL是否有效
  const isImageUrlValid = recipe.image_url && typeof recipe.image_url === 'string' && recipe.image_url.trim() !== '';
  
  // 获取安全的图片URL，如果原始URL无效或可能被阻止，则使用备选图片
  const getSafeImageUrl = () => {
    if (isImageUrlValid) {
      // 检查是否是Unsplash图片（可能被ORB阻止）
      if (recipe.image_url && recipe.image_url.includes('unsplash.com')) {
        // 使用picsum.photos作为备选图片服务，基于recipe_id生成一致的随机图片
        const imageId = recipe.recipe_id ? recipe.recipe_id.substring(0, 8) : 'default';
        return `https://picsum.photos/seed/${imageId}/400/220`;
      }
      return recipe.image_url;
    }
    // 如果没有有效的图片URL，使用基于recipe_id的picsum图片
    const imageId = recipe.recipe_id ? recipe.recipe_id.substring(0, 8) : 'default';
    return `https://picsum.photos/seed/${imageId}/400/220`;
  };

  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();

  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [modalMessage, setModalMessage] = useState('');
  const [modalTitle, setModalTitle] = useState('');
  const [isFavorite, setIsFavorite] = useState(false);
  const [isFavoriteLoading, setIsFavoriteLoading] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error' | 'info'>('success');
  
  const globalLoading = useSelector((state: RootState) => state.recipes.loading);
  
  // 加载收藏状态
  useEffect(() => {
    const checkFavoriteStatus = async () => {
      try {
        setIsFavoriteLoading(true);
        const status = await recipeService.isFavorite(recipe.recipe_id);
        setIsFavorite(status);
      } catch (err) {
        console.error('Failed to check favorite status:', err);
      } finally {
        setIsFavoriteLoading(false);
      }
    };

    checkFavoriteStatus();
  }, [recipe.recipe_id]);

  // 处理收藏/取消收藏
  const handleToggleFavorite = async (e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      setIsFavoriteLoading(true);
      
      let newFavoriteStatus = !isFavorite;
      
      if (isFavorite) {
        // 取消收藏
        await recipeService.removeFavorite(recipe.recipe_id);
        setIsFavorite(false);
        setSnackbarMessage('已取消收藏');
      } else {
        // 添加收藏
        await recipeService.addFavorite(recipe.recipe_id);
        setIsFavorite(true);
        setSnackbarMessage('收藏成功');
      }
      
      setSnackbarSeverity('success');
      
      // 调用回调函数通知父组件收藏状态变化
      if (onFavoriteChange) {
        onFavoriteChange(recipe.recipe_id, newFavoriteStatus);
      }
      
    } catch (err: any) {
      console.error('Failed to toggle favorite:', err);
      
      // 处理已收藏的错误
      if (err.response?.data?.detail === 'Recipe already in favorites') {
        setSnackbarMessage('该食谱已在收藏列表中');
      } else if (err.response?.data?.detail === 'Favorite not found') {
        setSnackbarMessage('收藏记录不存在');
      } else {
        setSnackbarMessage('操作失败，请稍后重试');
      }
      
      setSnackbarSeverity('error');
    } finally {
      setIsFavoriteLoading(false);
      setSnackbarOpen(true);
    }
  };

  // 关闭消息提示
  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };
  
  // 处理删除点击事件
  const handleDeleteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setModalTitle('确认删除');
    setModalMessage('确定要删除此食谱吗？此操作无法撤销。');
    setDeleteModalOpen(true);
  };
  
  // 处理删除确认
  const handleConfirmDelete = async () => {
    // 关闭模态框
    setDeleteModalOpen(false);
    setDeleteLoading(true);
    
    try {
      // 执行删除操作
      await dispatch(deleteRecipe(recipe.recipe_id) as any).unwrap();
      
      // 显示删除成功提示
      setModalTitle('删除成功');
      setModalMessage('食谱已成功删除');
      setDeleteModalOpen(true);
    } catch (error) {
      console.error('删除食谱失败:', error);
      // 显示删除失败提示
      setModalTitle('操作失败');
      setModalMessage('删除食谱失败，请稍后重试');
      setDeleteModalOpen(true);
    } finally {
      setDeleteLoading(false);
    }
  };
  
  // 关闭删除模态框
  const handleCloseDeleteModal = () => {
    setDeleteModalOpen(false);
  };
  
  const handleCardClick = (e: React.MouseEvent) => {
    if (recipe.recipe_id) {
      navigate(`/recipe-detail/${recipe.recipe_id}`);
    }
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
        transition: 'transform 0.3s ease, box-shadow 0.3s ease',
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
        border: '1px solid #f0f0f0',
        backgroundColor: '#fff',
        '&:hover': {
          transform: 'translateY(-3px)',
          boxShadow: '0 4px 16px rgba(0,0,0,0.08)',
          cursor: 'pointer'
        },
      }}
      onClick={handleCardClick}
    >
      {/* 食谱图片 */}
      <Box sx={{ position: 'relative', height: 200, overflow: 'hidden' }}>
        <CardMedia
          component="img"
          src={getSafeImageUrl()}
          alt={recipe.title || '食谱图片'}
          onError={(e) => {
            // 图片加载失败时使用备选图片
            const target = e.target as HTMLImageElement;
            const imageId = recipe.recipe_id ? recipe.recipe_id.substring(0, 8) : 'fallback';
            target.src = `https://picsum.photos/seed/${imageId}/400/200`;
          }}
          sx={{
            height: '100%',
            width: '100%',
            objectFit: 'cover',
            transition: 'transform 0.5s ease',
            '&:hover': {
              transform: 'scale(1.05)',
            },
          }}
        />
        {/* 收藏按钮 */}
        <Tooltip title={isFavorite ? "取消收藏" : "收藏"}>
          <IconButton
            sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              backgroundColor: 'rgba(255, 255, 255, 0.9)',
              borderRadius: '50%',
              minWidth: '36px',
              width: '36px',
              height: '36px',
              '&:hover': {
                backgroundColor: '#fff',
                transform: 'scale(1.1)',
                boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
              },
              transition: 'all 0.2s ease',
            }}
            onClick={handleToggleFavorite}
            disabled={isFavoriteLoading || deleteLoading}
          >
            {isFavorite ? (
              <Favorite color="error" fontSize="small" />
            ) : (
              <FavoriteBorder color="error" fontSize="small" />
            )}
          </IconButton>
        </Tooltip>
      </Box>
      
      {/* 食谱内容 */}
      <CardContent sx={{ flexGrow: 1, p: 2.5 }}>
        {/* 食谱名称 */}
        <Typography 
          variant="h6" 
          component="h2" 
          sx={{ 
            fontWeight: 600, 
            fontSize: '1.1rem',
            mb: 1.2,
            color: '#333',
            lineHeight: 1.3,
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}
        >
          {recipe.title}
        </Typography>
        
        {/* 食谱简介 */}
        <Typography 
          variant="body2" 
          color="text.secondary" 
          sx={{ 
            mb: 1.5, 
            fontSize: '0.875rem',
            lineHeight: 1.5,
            display: '-webkit-box', 
            WebkitLineClamp: 2, 
            WebkitBoxOrient: 'vertical', 
            overflow: 'hidden',
          }}
        >
          {recipe.description || '暂无简介'}
        </Typography>
        
        {/* 烹饪信息：时间、难度、评分 */}
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: 2, 
          mb: 1.5,
          flexWrap: 'wrap',
        }}>
          {/* 烹饪时间 */}
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 0.5,
            fontSize: '0.8rem',
            color: '#666',
          }}>
            <AccessTime fontSize="small" sx={{ color: '#1976d2' }} />
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              {recipe.cooking_time}分钟
            </Typography>
          </Box>
          
          {/* 难度 */}
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 0.5,
            fontSize: '0.8rem',
            color: '#666',
          }}>
            <Restaurant fontSize="small" sx={{ color: '#4caf50' }} />
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              {recipe.difficulty}
            </Typography>
          </Box>
          
          {/* 评分 */}
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 0.5,
            fontSize: '0.8rem',
          }}>
            <Star fontSize="small" sx={{ color: '#ff9800' }} />
            <Typography variant="body2" sx={{ fontWeight: 600, color: '#ff9800' }}>
              {recipe.rating || 0}
            </Typography>
          </Box>
        </Box>
        
        {/* 食谱标签 */}
        <Box sx={{ 
          display: 'flex', 
          flexWrap: 'wrap', 
          gap: 0.75,
        }}>
          {recipe.tags && recipe.tags.length > 0 ? (
            recipe.tags.map((tag, index) => (
              <Chip 
                key={index} 
                label={tag} 
                size="small" 
                sx={{
                  fontSize: '0.75rem',
                  height: '24px',
                  borderRadius: '12px',
                  backgroundColor: '#e8f5e8',
                  color: '#4caf50',
                  fontWeight: 500,
                  '&:hover': {
                    backgroundColor: '#dcedc8',
                  },
                  transition: 'background-color 0.2s ease',
                }}
              />
            ))
          ) : (
            <Typography variant="body2" color="text.disabled" sx={{ fontSize: '0.75rem' }}>
              暂无标签
            </Typography>
          )}
        </Box>
      </CardContent>
      
      {/* 操作按钮 */}
      <CardActions sx={{
        justifyContent: 'flex-start',
        p: 2.5,
        pt: 0,
        gap: 1,
        borderTop: '1px solid #f5f5f5',
      }}>
        {/* 查看详情按钮 */}
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
            fontSize: '0.875rem',
            color: '#4caf50',
            padding: '6px 14px',
            borderRadius: 1.5,
            minWidth: '80px',
            '&:hover': {
              backgroundColor: 'rgba(76, 175, 80, 0.1)',
              transform: 'translateY(-1px)',
            },
            transition: 'all 0.2s ease',
          }}
          disabled={isFavoriteLoading}
        >
          查看详情
        </Button>
        
        {/* 删除按钮（仅在食谱列表页面显示） */}
        {location.pathname === '/recipe-list' && (
          <Button
            size="small"
            startIcon={
              deleteLoading ? (
                <CircularProgress size={14} color="inherit" />
              ) : (
                <Delete fontSize="small" />
              )
            }
            onClick={handleDeleteClick}
            disabled={deleteLoading || globalLoading || isFavoriteLoading}
            sx={{
              textTransform: 'none',
              fontWeight: 600,
              fontSize: '0.875rem',
              color: '#f44336',
              padding: '6px 14px',
              borderRadius: 1.5,
              minWidth: '70px',
              '&:hover': {
                backgroundColor: 'rgba(244, 67, 54, 0.08)',
                transform: 'translateY(-1px)',
              },
              transition: 'all 0.2s ease',
            }}
          >
            删除
          </Button>
        )}
      </CardActions>
      
      {/* 删除确认模态框 */}
      <Dialog
        open={deleteModalOpen}
        onClose={handleCloseDeleteModal}
        aria-labelledby="delete-modal-title"
        disableEscapeKeyDown
      >
        <DialogTitle id="delete-modal-title">{modalTitle}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {modalMessage}
          </DialogContentText>
        </DialogContent>
        <MuiDialogActions>
          <Button 
            onClick={(e) => {
              e.stopPropagation();
              handleCloseDeleteModal();
            }} 
            sx={{ textTransform: 'none', mr: 1 }}
          >
            取消
          </Button>
          <Button 
            onClick={(e) => {
              e.stopPropagation();
              handleConfirmDelete();
            }} 
            variant="contained"
            color="error"
            sx={{ textTransform: 'none' }}
            disabled={deleteLoading}
            startIcon={deleteLoading ? <CircularProgress size={16} color="inherit" /> : undefined}
          >
            确认删除
          </Button>
        </MuiDialogActions>
      </Dialog>
      
      {/* 收藏操作消息提示 */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Card>
  );
};

export default RecipeCard;


