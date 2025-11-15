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
  Collapse,
  Tabs,
  Tab
} from '@mui/material';
import { Save, Share, Favorite, Star, Info, ArrowBack } from '@mui/icons-material';
import { RecipeResponse } from '../../types/recipe';
import aiService from '../../services/aiService';
import { SaveRecipeRequest } from '../../types/ai';

interface RecipeEnhancementResultProps {
  originalRecipe?: RecipeResponse;
  enhancedRecipe: RecipeResponse;
  onClose: () => void;
  onSaveSuccess?: () => void;
}

const RecipeEnhancementResult: React.FC<RecipeEnhancementResultProps> = ({ 
  originalRecipe,
  enhancedRecipe, 
  onClose,
  onSaveSuccess 
}) => {
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [showNutritionDetails, setShowNutritionDetails] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [showComparison, setShowComparison] = useState(originalRecipe !== undefined);

  const handleSaveRecipe = async () => {
    setIsSaving(true);
    setSaveSuccess(false);
    setSaveError(null);

    try {
      const request: SaveRecipeRequest = {
        generated_recipe: {
          title: enhancedRecipe.title,
          description: enhancedRecipe.description,
          ingredients: enhancedRecipe.ingredients.map(ing => ({
            name: ing.name,
            quantity: ing.quantity,
            unit: ing.unit,
            notes: ing.notes
          })),
          cooking_steps: enhancedRecipe.cooking_steps.map(step => ({
            step_number: step.step_number,
            description: step.description,
            duration: step.duration
          })),
          prep_time: enhancedRecipe.prep_time,
          cook_time: enhancedRecipe.cook_time,
          servings: enhancedRecipe.servings,
          difficulty: enhancedRecipe.difficulty,
          cuisine: enhancedRecipe.cuisine,
          meal_type: enhancedRecipe.meal_type,
          nutrition_info: enhancedRecipe.nutrition_info,
          image_url: enhancedRecipe.image_url,
          tags: enhancedRecipe.tags,
          equipment: enhancedRecipe.equipment,
          tips: enhancedRecipe.tips
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

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const getCurrentRecipe = (): RecipeResponse => {
    if (!showComparison) return enhancedRecipe;
    return activeTab === 0 ? originalRecipe! : enhancedRecipe;
  };

  const currentRecipe = getCurrentRecipe();

  const renderComparisonTabs = () => {
    if (!showComparison) return null;
    
    return (
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs 
          value={activeTab} 
          onChange={handleTabChange}
          variant="fullWidth"
          centered
        >
          <Tab label="原始食谱" />
          <Tab label="增强后食谱" />
        </Tabs>
      </Box>
    );
  };

  return (
    <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <IconButton 
            onClick={() => {
              if (showComparison && activeTab === 1) {
                setActiveTab(0);
              } else {
                onClose();
              }
            }}
          >
            <ArrowBack />
          </IconButton>
          <Typography variant="h4" gutterBottom>{currentRecipe.title}</Typography>
        </Box>
        {showComparison && (
          <Button 
            onClick={() => setShowComparison(false)}
            variant="text"
            size="small"
          >
            隐藏对比
          </Button>
        )}
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

      {renderComparisonTabs()}

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Card elevation={0} sx={{ mb: 3 }}>
            {currentRecipe.image_url ? (
              <CardMedia
                component="img"
                height="300"
                image={currentRecipe.image_url}
                alt={currentRecipe.title}
                sx={{ objectFit: 'cover' }}
              />
            ) : (
              <Box sx={{ height: 300, bgcolor: 'grey.100', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography color="text.secondary">暂无图片</Typography>
              </Box>
            )}
          </Card>

          <Typography variant="body1" paragraph>{currentRecipe.description}</Typography>

          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>烹饪步骤</Typography>
            {currentRecipe.cooking_steps.map((step) => (
              <Box key={step.id || step.step_number} sx={{ mb: 3 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                  步骤 {step.step_number}{step.duration ? ` (约${step.duration}分钟)` : ''}:
                </Typography>
                <Typography variant="body1" sx={{ pl: 3 }}>{step.description}</Typography>
              </Box>
            ))}
          </Box>

          {currentRecipe.tips && currentRecipe.tips.length > 0 && (
            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" gutterBottom>烹饪小贴士</Typography>
              <ul>
                {currentRecipe.tips.map((tip, index) => (
                  <li key={index}>
                    <Typography variant="body1">{tip}</Typography>
                  </li>
                ))}
              </ul>
            </Box>
          )}

          {currentRecipe.equipment && currentRecipe.equipment.length > 0 && (
            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" gutterBottom>所需厨具</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {currentRecipe.equipment.map((item, index) => (
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
                    <Typography>{getDifficultyLabel(currentRecipe.difficulty)}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography color="text.secondary">份量</Typography>
                    <Typography>{currentRecipe.servings} 人份</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography color="text.secondary">准备时间</Typography>
                    <Typography>{currentRecipe.prep_time} 分钟</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography color="text.secondary">烹饪时间</Typography>
                    <Typography>{currentRecipe.cook_time} 分钟</Typography>
                  </Grid>
                  {currentRecipe.cuisine && (
                    <Grid item xs={6}>
                      <Typography color="text.secondary">菜系</Typography>
                      <Typography>{currentRecipe.cuisine}</Typography>
                    </Grid>
                  )}
                  {currentRecipe.meal_type && (
                    <Grid item xs={6}>
                      <Typography color="text.secondary">餐型</Typography>
                      <Typography>{getMealTypeLabel(currentRecipe.meal_type)}</Typography>
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
                  {currentRecipe.nutrition_info.calories} 卡路里
                </Typography>
                <Collapse in={showNutritionDetails}>
                  <Divider sx={{ my: 1 }} />
                  <Grid container spacing={1}>
                    <Grid item xs={6}>
                      <Typography color="text.secondary" fontSize="small">蛋白质</Typography>
                      <Typography>{currentRecipe.nutrition_info.protein}g</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography color="text.secondary" fontSize="small">碳水化合物</Typography>
                      <Typography>{currentRecipe.nutrition_info.carbs}g</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography color="text.secondary" fontSize="small">脂肪</Typography>
                      <Typography>{currentRecipe.nutrition_info.fat}g</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography color="text.secondary" fontSize="small">纤维素</Typography>
                      <Typography>{currentRecipe.nutrition_info.fiber}g</Typography>
                    </Grid>
                    {currentRecipe.nutrition_info.sugar !== undefined && (
                      <Grid item xs={6}>
                        <Typography color="text.secondary" fontSize="small">糖</Typography>
                        <Typography>{currentRecipe.nutrition_info.sugar}g</Typography>
                      </Grid>
                    )}
                    {currentRecipe.nutrition_info.sodium !== undefined && (
                      <Grid item xs={6}>
                        <Typography color="text.secondary" fontSize="small">钠</Typography>
                        <Typography>{currentRecipe.nutrition_info.sodium}mg</Typography>
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
                  {currentRecipe.ingredients.map((ingredient, index) => (
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

            {currentRecipe.tags && currentRecipe.tags.length > 0 && (
              <Card elevation={2} sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>标签</Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {currentRecipe.tags.map((tag, index) => (
                      <Chip key={index} label={tag} />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            )}

            <CardActions sx={{ flexDirection: 'column', gap: 2 }}>
              {(!showComparison || activeTab === 1) && (
                <Button
                  variant="contained"
                  fullWidth
                  startIcon={<Save />}
                  onClick={handleSaveRecipe}
                  disabled={isSaving}
                >
                  {isSaving ? <CircularProgress size={16} /> : '保存增强食谱'}
                </Button>
              )}
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

export default RecipeEnhancementResult;