import React, { useState } from 'react';
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
  Card,
  CardContent,
  CardMedia,
  CardActions,
  IconButton,
  Collapse
} from '@mui/material';
import { Save, Share, Favorite, Star, Info } from '@mui/icons-material';
import { RecipeResponse } from '../../types/recipe';
import aiService from '../../services/aiService';
import { SaveRecipeRequest } from '../../types/ai';

interface RecipeGenerationResultProps {
  recipe: RecipeResponse;
  onClose: () => void;
  onSaveSuccess?: () => void;
}

const RecipeGenerationResult: React.FC<RecipeGenerationResultProps> = ({ 
  recipe, 
  onClose,
  onSaveSuccess 
}) => {
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [showNutritionDetails, setShowNutritionDetails] = useState(false);

  const handleSaveRecipe = async () => {
    setIsSaving(true);
    setSaveSuccess(false);
    setSaveError(null);

    try {
      const request: SaveRecipeRequest = {
        generated_recipe: {
          title: recipe.title,
          description: recipe.description,
          ingredients: recipe.ingredients.map(ing => ({
            name: ing.name,
            quantity: ing.quantity,
            unit: ing.unit,
            notes: ing.notes
          })),
          cooking_steps: recipe.cooking_steps.map(step => ({
            step_number: step.step_number,
            description: step.description,
            duration: step.duration
          })),
          prep_time: recipe.prep_time,
          cook_time: recipe.cook_time,
          servings: recipe.servings,
          difficulty: recipe.difficulty,
          cuisine: recipe.cuisine,
          meal_type: recipe.meal_type,
          nutrition_info: recipe.nutrition_info,
          image_url: recipe.image_url,
          tags: recipe.tags,
          equipment: recipe.equipment,
          tips: recipe.tips
        },
        save_as_draft: false
      };

      await aiService.saveGeneratedRecipe(request);
      setSaveSuccess(true);
      if (onSaveSuccess) {
        onSaveSuccess();
      }
      // 3秒后隐藏成功提示
      setTimeout(() => {
        setSaveSuccess(false);
      }, 3000);
    } catch (error: any) {
      setSaveError(
        error.response?.data?.detail || 
        error.response?.data?.message || 
        '保存食谱失败，请稍后重试'
      );
    } finally {
      setIsSaving(false);
    }
  };

  const handleShareRecipe = () => {
    // 实现分享功能
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

  return (
    <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Typography variant="h4" gutterBottom>{recipe.title}</Typography>
        <Button onClick={onClose} color="inherit" variant="text">关闭</Button>
      </Box>

      {saveSuccess && (
        <Alert severity="success" sx={{ mb: 3 }}>
          食谱保存成功！
        </Alert>
      )}

      {saveError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {saveError}
        </Alert>
      )}

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Card elevation={0} sx={{ mb: 3 }}>
            {recipe.image_url ? (
              <CardMedia
                component="img"
                height="300"
                image={recipe.image_url}
                alt={recipe.title}
                sx={{ objectFit: 'cover' }}
              />
            ) : (
              <Box sx={{ height: 300, bgcolor: 'grey.100', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography color="text.secondary">暂无图片</Typography>
              </Box>
            )}
          </Card>

          <Typography variant="body1" paragraph>{recipe.description}</Typography>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>烹饪步骤</Typography>
            {recipe.cooking_steps.map((step) => (
              <Box key={step.id || step.step_number} sx={{ mb: 3 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                  步骤 {step.step_number}{step.duration ? ` (约${step.duration}分钟)` : ''}:
                </Typography>
                <Typography variant="body1" sx={{ pl: 3 }}>{step.description}</Typography>
              </Box>
            ))}
          </Box>

          {recipe.tips && recipe.tips.length > 0 && (
            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" gutterBottom>烹饪小贴士</Typography>
              <ul>
                {recipe.tips.map((tip, index) => (
                  <li key={index}>
                    <Typography variant="body1">{tip}</Typography>
                  </li>
                ))}
              </ul>
            </Box>
          )}

          {recipe.equipment && recipe.equipment.length > 0 && (
            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" gutterBottom>所需厨具</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {recipe.equipment.map((item, index) => (
                  <Chip key={index} label={item} />
                ))}
              </Box>
            </Box>
          )}
        </Grid>

        <Grid item xs={12} md={4}>
          <Box sx={{ position: 'sticky', top: 20 }}>
            <Card elevation={2} sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>基本信息</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography color="text.secondary">难度</Typography>
                    <Typography>{getDifficultyLabel(recipe.difficulty)}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography color="text.secondary">份量</Typography>
                    <Typography>{recipe.servings} 人份</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography color="text.secondary">准备时间</Typography>
                    <Typography>{recipe.prep_time} 分钟</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography color="text.secondary">烹饪时间</Typography>
                    <Typography>{recipe.cook_time} 分钟</Typography>
                  </Grid>
                  {recipe.cuisine && (
                    <Grid item xs={6}>
                      <Typography color="text.secondary">菜系</Typography>
                      <Typography>{recipe.cuisine}</Typography>
                    </Grid>
                  )}
                  {recipe.meal_type && (
                    <Grid item xs={6}>
                      <Typography color="text.secondary">餐型</Typography>
                      <Typography>{getMealTypeLabel(recipe.meal_type)}</Typography>
                    </Grid>
                  )}
                </Grid>
              </CardContent>
            </Card>

            <Card elevation={2} sx={{ mb: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="subtitle1">营养信息</Typography>
                  <IconButton onClick={() => setShowNutritionDetails(!showNutritionDetails)}>
                    <Info fontSize="small" />
                  </IconButton>
                </Box>
                <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                  {recipe.nutrition_info.calories} 卡路里
                </Typography>
                <Collapse in={showNutritionDetails}>
                  <Divider sx={{ my: 1 }} />
                  <Grid container spacing={1}>
                    <Grid item xs={6}>
                      <Typography color="text.secondary" fontSize="small">蛋白质</Typography>
                      <Typography>{recipe.nutrition_info.protein}g</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography color="text.secondary" fontSize="small">碳水化合物</Typography>
                      <Typography>{recipe.nutrition_info.carbs}g</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography color="text.secondary" fontSize="small">脂肪</Typography>
                      <Typography>{recipe.nutrition_info.fat}g</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography color="text.secondary" fontSize="small">纤维素</Typography>
                      <Typography>{recipe.nutrition_info.fiber}g</Typography>
                    </Grid>
                    {recipe.nutrition_info.sugar !== undefined && (
                      <Grid item xs={6}>
                        <Typography color="text.secondary" fontSize="small">糖</Typography>
                        <Typography>{recipe.nutrition_info.sugar}g</Typography>
                      </Grid>
                    )}
                    {recipe.nutrition_info.sodium !== undefined && (
                      <Grid item xs={6}>
                        <Typography color="text.secondary" fontSize="small">钠</Typography>
                        <Typography>{recipe.nutrition_info.sodium}mg</Typography>
                      </Grid>
                    )}
                  </Grid>
                </Collapse>
              </CardContent>
            </Card>

            <Card elevation={2} sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>食材清单</Typography>
                <ul sx={{ pl: 2 }}>
                  {recipe.ingredients.map((ingredient, index) => (
                    <li key={index} style={{ marginBottom: '8px' }}>
                      <Typography variant="body2">
                        {ingredient.quantity} {ingredient.unit} {ingredient.name}
                        {ingredient.notes && ` (${ingredient.notes})`}
                      </Typography>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            {recipe.tags && recipe.tags.length > 0 && (
              <Card elevation={2} sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>标签</Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {recipe.tags.map((tag, index) => (
                      <Chip key={index} label={tag} />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            )}

            <CardActions sx={{ flexDirection: 'column', gap: 2 }}>
              <Button
                variant="contained"
                fullWidth
                startIcon={<Save />}
                onClick={handleSaveRecipe}
                disabled={isSaving}
              >
                {isSaving ? <CircularProgress size={16} /> : '保存食谱'}
              </Button>
              <Button
                variant="outlined"
                fullWidth
                startIcon={<Share />}
                onClick={handleShareRecipe}
              >
                分享食谱
              </Button>
              <Button
                variant="text"
                fullWidth
                startIcon={<Favorite />}
                onClick={() => alert('收藏功能将在后续版本中实现')}
              >
                收藏食谱
              </Button>
            </CardActions>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default RecipeGenerationResult;