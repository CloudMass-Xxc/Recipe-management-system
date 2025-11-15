import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Grid,
  Divider,
  Chip,
  Alert,
  CircularProgress,
  Avatar,
  IconButton,
  Stack,
  Rating,
  Tabs,
  Tab,
  Collapse
} from '@mui/material';
import { 
  ArrowBack, 
  Clock, 
  Users, 
  ChefHat, 
  Heart, 
  Share, 
  Edit, 
  Delete, 
  Star, 
  Bookmark,
  Info,
  Home,
  ThumbsUp,
  MessageOutlined
} from '@mui/icons-material';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import recipeService from '../../services/recipeService';
import { RecipeResponse } from '../../types/recipe';

const RecipeDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  
  const [recipe, setRecipe] = useState<RecipeResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isFavorite, setIsFavorite] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [showNutritionDetails, setShowNutritionDetails] = useState(false);
  const [ratingValue, setRatingValue] = useState(0);
  const [isRatingSubmitted, setIsRatingSubmitted] = useState(false);
  const [isOwner, setIsOwner] = useState(false);

  useEffect(() => {
    if (id) {
      fetchRecipeDetails();
    }
  }, [id]);

  useEffect(() => {
    // 检查当前用户是否是食谱的所有者
    if (recipe && user && recipe.user_id === user.id) {
      setIsOwner(true);
    }
  }, [recipe, user]);

  const fetchRecipeDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await recipeService.getRecipeById(id!);
      setRecipe(data);
      setIsFavorite(data.is_favorited || false);
      setRatingValue(data.user_rating || 0);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        err.response?.data?.message || 
        '获取食谱详情失败'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleToggleFavorite = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      if (isFavorite) {
        await recipeService.removeFavorite(id!);
      } else {
        await recipeService.addFavorite(id!);
      }
      setIsFavorite(!isFavorite);
    } catch (error) {
      alert('操作失败，请稍后重试');
    }
  };

  const handleShareRecipe = () => {
    // 实现分享功能
    alert('分享功能将在后续版本中实现');
  };

  const handleSubmitRating = async (event: React.SyntheticEvent, newValue: number | null) => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    if (newValue === null) return;
    
    try {
      setRatingValue(newValue);
      await recipeService.rateRecipe(id!, { rating: newValue });
      setIsRatingSubmitted(true);
      // 更新本地的平均评分
      if (recipe) {
        const updatedRecipe = { ...recipe };
        updatedRecipe.average_rating = newValue;
        setRecipe(updatedRecipe);
      }
      // 3秒后重置提交状态
      setTimeout(() => setIsRatingSubmitted(false), 3000);
    } catch (error) {
      alert('评分失败，请稍后重试');
    }
  };

  const handleEditRecipe = () => {
    navigate(`/recipes/edit/${id}`);
  };

  const handleDeleteRecipe = async () => {
    if (window.confirm('确定要删除这个食谱吗？此操作不可撤销。')) {
      try {
        await recipeService.deleteRecipe(id!);
        navigate('/recipes');
      } catch (error) {
        alert('删除失败，请稍后重试');
      }
    }
  };

  const getDifficultyLabel = (difficulty: string): string => {
    switch (difficulty) {
      case 'easy': return '简单';
      case 'medium': return '中等';
      case 'hard': return '困难';
      default: return difficulty;
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

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !recipe) {
    return (
      <Box sx={{ maxWidth: '800px', mx: 'auto', mt: 8, p: 4 }}>
        <Alert severity="error" sx={{ mb: 4 }}>
          {error || '食谱不存在'}
        </Alert>
        <Button 
          variant="contained" 
          startIcon={<ArrowBack />}
          onClick={() => navigate('/recipes')}
        >
          返回食谱列表
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ minHeight: '100vh' }}>
      {/* 顶部导航栏 */}
      <Box sx={{ bgcolor: 'white', boxShadow: 1, position: 'sticky', top: 0, zIndex: 10 }}>
        <Box sx={{ maxWidth: '1200px', mx: 'auto', px: 4, py: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
          <IconButton onClick={() => navigate('/recipes')}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h6">食谱详情</Typography>
          <Box sx={{ flexGrow: 1 }} />
          <IconButton onClick={() => navigate('/')} color="inherit">
            <Home />
          </IconButton>
        </Box>
      </Box>

      <Box sx={{ maxWidth: '1200px', mx: 'auto', px: { xs: 2, md: 4 }, py: 6 }}>
        {/* 面包屑导航 */}
        <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', gap: 1 }}>
          <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            <Typography variant="body2" color="primary">首页</Typography>
          </Link>
          <Typography variant="body2">/</Typography>
          <Link to="/recipes" style={{ textDecoration: 'none', color: 'inherit' }}>
            <Typography variant="body2" color="primary">食谱列表</Typography>
          </Link>
          <Typography variant="body2">/</Typography>
          <Typography variant="body2" color="text.secondary">{recipe.title}</Typography>
        </Box>

        {/* 评分成功提示 */}
        {isRatingSubmitted && (
          <Alert severity="success" sx={{ mb: 4 }}>
            感谢您的评分！
          </Alert>
        )}

        {/* 食谱标题和操作按钮 */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 4, flexWrap: 'wrap', gap: 2 }}>
          <Box>
            <Typography variant="h3" gutterBottom>{recipe.title}</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Avatar sx={{ width: 32, height: 32 }}>
                  {recipe.user_name ? recipe.user_name.charAt(0).toUpperCase() : '?'}
                </Avatar>
                <Typography variant="body1">
                  {recipe.user_name || '匿名用户'}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                发布于 {new Date(recipe.created_at).toLocaleDateString()}
              </Typography>
              <Chip 
                icon={<Star fontSize="small" />}
                label={recipe.average_rating || 0}
                size="small"
                color="warning"
                sx={{ fontWeight: 'medium' }}
              />
            </Box>
          </Box>

          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {isOwner && (
              <>
                <Button 
                  startIcon={<Edit />} 
                  variant="outlined" 
                  onClick={handleEditRecipe}
                >
                  编辑
                </Button>
                <Button 
                  startIcon={<Delete />} 
                  variant="outlined" 
                  color="error"
                  onClick={handleDeleteRecipe}
                >
                  删除
                </Button>
              </>
            )}
            <IconButton 
              color={isFavorite ? "error" : "default"}
              onClick={handleToggleFavorite}
              title={isFavorite ? "取消收藏" : "收藏"}
            >
              <Heart 
                fontSize="large" 
                fill={isFavorite ? "currentColor" : "none"}
              />
            </IconButton>
            <IconButton 
              onClick={handleShareRecipe}
              title="分享"
            >
              <Share fontSize="large" />
            </IconButton>
          </Box>
        </Box>

        <Grid container spacing={6}>
          {/* 左侧内容 */}
          <Grid item xs={12} lg={8}>
            {/* 食谱图片 */}
            <Paper elevation={2} sx={{ mb: 6, overflow: 'hidden' }}>
              {recipe.image_url ? (
                <img 
                  src={recipe.image_url} 
                  alt={recipe.title} 
                  style={{ width: '100%', height: 'auto', maxHeight: '500px', objectFit: 'cover' }}
                />
              ) : (
                <Box sx={{ height: 300, bgcolor: 'grey.100', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <ChefHat fontSize="48" color="disabled" />
                </Box>
              )}
            </Paper>

            {/* 食谱描述 */}
            <Paper elevation={2} sx={{ p: 4, mb: 6 }}>
              <Typography variant="h6" gutterBottom>关于这道菜</Typography>
              <Typography variant="body1" paragraph>
                {recipe.description}
              </Typography>
            </Paper>

            {/* 标签页导航 */}
            <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 4 }}>
              <Tabs 
                value={activeTab} 
                onChange={handleTabChange}
                variant="fullWidth"
                centered
              >
                <Tab label="烹饪步骤" />
                <Tab label="食材清单" />
                <Tab label="用户评价" />
              </Tabs>
            </Box>

            {/* 标签页内容 */}
            <Box sx={{ mb: 6 }}>
              {/* 烹饪步骤 */}
              {activeTab === 0 && (
                <Paper elevation={2} sx={{ p: 4 }}>
                  {recipe.cooking_steps.map((step) => (
                    <Box key={step.id || step.step_number} sx={{ mb: 6, '&:last-child': { mb: 0 } }}>
                      <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 3 }}>
                        <Box 
                          sx={{ 
                            width: 36, 
                            height: 36, 
                            borderRadius: '50%', 
                            bgcolor: 'primary.main', 
                            color: 'white',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: 'bold',
                            flexShrink: 0
                          }}
                        >
                          {step.step_number}
                        </Box>
                        <Box sx={{ flexGrow: 1 }}>
                          <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                            {step.duration ? `步骤 ${step.step_number} (约${step.duration}分钟)` : `步骤 ${step.step_number}`}
                          </Typography>
                          <Typography variant="body1">
                            {step.description}
                          </Typography>
                        </Box>
                      </Box>
                      {step.step_number < recipe.cooking_steps.length && (
                        <Divider sx={{ mt: 6, ml: 9 }} />
                      )}
                    </Box>
                  ))}
                </Paper>
              )}

              {/* 食材清单 */}
              {activeTab === 1 && (
                <Paper elevation={2} sx={{ p: 4 }}>
                  <Grid container spacing={2}>
                    {recipe.ingredients.map((ingredient, index) => (
                      <Grid item xs={12} sm={6} key={index}>
                        <Box sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Box>
                            <Typography variant="body1" fontWeight="medium">
                              {ingredient.name}
                            </Typography>
                            {ingredient.notes && (
                              <Typography variant="caption" color="text.secondary">
                                {ingredient.notes}
                              </Typography>
                            )}
                          </Box>
                          <Typography variant="body1" color="primary.main" fontWeight="medium">
                            {ingredient.quantity} {ingredient.unit}
                          </Typography>
                        </Box>
                      </Grid>
                    ))}
                  </Grid>
                </Paper>
              )}

              {/* 用户评价 */}
              {activeTab === 2 && (
                <Paper elevation={2} sx={{ p: 4 }}>
                  <Box sx={{ mb: 4 }}>
                    <Typography variant="subtitle1" gutterBottom>您的评分</Typography>
                    <Rating
                      value={ratingValue}
                      onChange={handleSubmitRating}
                      precision={0.5}
                      size="large"
                    />
                  </Box>
                  <Divider sx={{ my: 4 }} />
                  <Typography variant="subtitle1" gutterBottom>其他用户评价</Typography>
                  {recipe.reviews && recipe.reviews.length > 0 ? (
                    <Stack spacing={3}>
                      {recipe.reviews.map((review, index) => (
                        <Box key={index} sx={{ p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                              <Avatar sx={{ width: 32, height: 32 }}>
                                {review.user_name ? review.user_name.charAt(0).toUpperCase() : '?'}
                              </Avatar>
                              <Typography variant="body1" fontWeight="medium">
                                {review.user_name || '匿名用户'}
                              </Typography>
                            </Box>
                            <Rating value={review.rating} readOnly size="small" />
                          </Box>
                          {review.comment && (
                            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                              {review.comment}
                            </Typography>
                          )}
                          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                            {new Date(review.created_at).toLocaleDateString()}
                          </Typography>
                        </Box>
                      ))}
                    </Stack>
                  ) : (
                    <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
                      暂无用户评价，成为第一个评价的人吧！
                    </Typography>
                  )}
                </Paper>
              )}
            </Box>

            {/* 小贴士和厨具 */}
            {(recipe.tips && recipe.tips.length > 0) && (
              <Paper elevation={2} sx={{ p: 4, mb: 6 }}>
                <Typography variant="h6" gutterBottom>烹饪小贴士</Typography>
                <ul>
                  {recipe.tips.map((tip, index) => (
                    <li key={index} style={{ marginBottom: '8px' }}>
                      <Typography variant="body1">• {tip}</Typography>
                    </li>
                  ))}
                </ul>
              </Paper>
            )}

            {recipe.equipment && recipe.equipment.length > 0 && (
              <Paper elevation={2} sx={{ p: 4, mb: 6 }}>
                <Typography variant="h6" gutterBottom>所需厨具</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                  {recipe.equipment.map((item, index) => (
                    <Chip key={index} label={item} variant="outlined" />
                  ))}
                </Box>
              </Paper>
            )}
          </Grid>

          {/* 右侧边栏 */}
          <Grid item xs={12} lg={4}>
            <Box sx={{ position: 'sticky', top: 100 }}>
              {/* 基本信息卡片 */}
              <Paper elevation={2} sx={{ p: 4, mb: 4 }}>
                <Typography variant="subtitle1" gutterBottom>基本信息</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                      <Clock fontSize="small" color="primary" />
                      <Typography color="text.secondary" fontSize="small">总时间</Typography>
                    </Box>
                    <Typography variant="body1" fontWeight="medium">
                      {formatTime(recipe.prep_time + recipe.cook_time)}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                      <Users fontSize="small" color="primary" />
                      <Typography color="text.secondary" fontSize="small">份量</Typography>
                    </Box>
                    <Typography variant="body1" fontWeight="medium">
                      {recipe.servings} 人份
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                      <ChefHat fontSize="small" color="primary" />
                      <Typography color="text.secondary" fontSize="small">难度</Typography>
                    </Box>
                    <Typography variant="body1" fontWeight="medium">
                      {getDifficultyLabel(recipe.difficulty)}
                    </Typography>
                  </Grid>
                  {recipe.cuisine && (
                    <Grid item xs={6}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                        <Info fontSize="small" color="primary" />
                        <Typography color="text.secondary" fontSize="small">菜系</Typography>
                      </Box>
                      <Typography variant="body1" fontWeight="medium">
                        {recipe.cuisine}
                      </Typography>
                    </Grid>
                  )}
                </Grid>

                {recipe.meal_type && (
                  <Box sx={{ mt: 3 }}>
                    <Chip 
                      label={getMealTypeLabel(recipe.meal_type)} 
                      sx={{ fontWeight: 'medium' }}
                    />
                  </Box>
                )}
              </Paper>

              {/* 营养信息卡片 */}
              <Paper elevation={2} sx={{ p: 4, mb: 4 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                  <Typography variant="subtitle1">营养信息</Typography>
                  <IconButton 
                    onClick={() => setShowNutritionDetails(!showNutritionDetails)}
                    size="small"
                  >
                    <Info fontSize="small" />
                  </IconButton>
                </Box>
                <Typography variant="h6" color="primary.main" fontWeight="bold" sx={{ mb: 2 }}>
                  {recipe.nutrition_info.calories} 卡路里
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>蛋白质</Typography>
                    <Typography variant="h6" fontWeight="medium">{recipe.nutrition_info.protein}g</Typography>
                  </Grid>
                  <Grid item xs={4}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>碳水</Typography>
                    <Typography variant="h6" fontWeight="medium">{recipe.nutrition_info.carbs}g</Typography>
                  </Grid>
                  <Grid item xs={4}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>脂肪</Typography>
                    <Typography variant="h6" fontWeight="medium">{recipe.nutrition_info.fat}g</Typography>
                  </Grid>
                </Grid>

                <Collapse in={showNutritionDetails}>
                  <Divider sx={{ my: 3 }} />
                  <Box sx={{ mt: 1 }}>
                    {recipe.nutrition_info.fiber !== undefined && (
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2">膳食纤维</Typography>
                        <Typography variant="body2">{recipe.nutrition_info.fiber}g</Typography>
                      </Box>
                    )}
                    {recipe.nutrition_info.sugar !== undefined && (
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2">糖分</Typography>
                        <Typography variant="body2">{recipe.nutrition_info.sugar}g</Typography>
                      </Box>
                    )}
                    {recipe.nutrition_info.sodium !== undefined && (
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2">钠</Typography>
                        <Typography variant="body2">{recipe.nutrition_info.sodium}mg</Typography>
                      </Box>
                    )}
                    {recipe.nutrition_info.cholesterol !== undefined && (
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2">胆固醇</Typography>
                        <Typography variant="body2">{recipe.nutrition_info.cholesterol}mg</Typography>
                      </Box>
                    )}
                  </Box>
                </Collapse>
              </Paper>

              {/* 标签卡片 */}
              {recipe.tags && recipe.tags.length > 0 && (
                <Paper elevation={2} sx={{ p: 4, mb: 4 }}>
                  <Typography variant="subtitle1" gutterBottom>标签</Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {recipe.tags.map((tag, index) => (
                      <Chip key={index} label={tag} />
                    ))}
                  </Box>
                </Paper>
              )}

              {/* 操作按钮 */}
              <Box sx={{ display: 'flex', gap: 2, flexDirection: 'column' }}>
                <Button 
                  variant="contained" 
                  fullWidth 
                  startIcon={<Bookmark />}
                  onClick={handleToggleFavorite}
                >
                  {isFavorite ? '取消收藏' : '收藏食谱'}
                </Button>
                <Button 
                  variant="outlined" 
                  fullWidth 
                  startIcon={<Share />}
                  onClick={handleShareRecipe}
                >
                  分享食谱
                </Button>
                {isAuthenticated && (
                  <Button 
                    variant="outlined" 
                    fullWidth 
                    startIcon={<ThumbsUp />}
                    onClick={() => alert('点赞功能将在后续版本中实现')}
                  >
                    点赞食谱
                  </Button>
                )}
              </Box>
            </Box>
          </Grid>
        </Grid>

        {/* 相关推荐 */}
        <Box sx={{ mt: 12 }}>
          <Typography variant="h5" gutterBottom>相关推荐</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
            可能您也会喜欢这些食谱
          </Typography>
          <Grid container spacing={3}>
            {/* 这里可以放相关推荐的食谱卡片，但目前只是占位 */}
            <Grid item xs={12} sm={6} md={4}>
              <Box sx={{ p: 4, border: '1px dashed #e0e0e0', borderRadius: 1, textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  相关推荐将在后续版本中实现
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Box>
  );
};

export default RecipeDetailPage;