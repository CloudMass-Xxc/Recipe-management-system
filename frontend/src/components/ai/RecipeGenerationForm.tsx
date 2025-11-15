import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Paper,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  Chip,
  IconButton,
  Alert,
  CircularProgress
} from '@mui/material';
import { Add, Delete, Send } from '@mui/icons-material';
import { RecipeGenerationRequest, DietaryPreference } from '../../types/ai';
import aiService from '../../services/aiService';
import { RecipeResponse } from '../../types/recipe';

interface RecipeGenerationFormProps {
  onRecipeGenerated: (recipe: RecipeResponse) => void;
  onError: (error: string) => void;
}

interface IngredientItem {
  name: string;
  quantity?: number;
  unit?: string;
}

const RecipeGenerationForm: React.FC<RecipeGenerationFormProps> = ({ 
  onRecipeGenerated, 
  onError 
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [title, setTitle] = useState('');
  const [cuisine, setCuisine] = useState('');
  const [mealType, setMealType] = useState<string>('');
  const [difficulty, setDifficulty] = useState<string>('');
  const [prepTimeMax, setPrepTimeMax] = useState('');
  const [cookTimeMax, setCookTimeMax] = useState('');
  const [servings, setServings] = useState('');
  const [dietaryPreferences, setDietaryPreferences] = useState<DietaryPreference[]>([]);
  const [tastePreferences, setTastePreferences] = useState<string[]>([]);
  const [excludeIngredients, setExcludeIngredients] = useState<string>('');
  const [specialRequest, setSpecialRequest] = useState('');
  const [ingredients, setIngredients] = useState<IngredientItem[]>([{ name: '' }]);
  const [caloriesMax, setCaloriesMax] = useState('');

  const handleAddIngredient = () => {
    setIngredients([...ingredients, { name: '' }]);
  };

  const handleRemoveIngredient = (index: number) => {
    const newIngredients = [...ingredients];
    newIngredients.splice(index, 1);
    setIngredients(newIngredients);
  };

  const handleIngredientChange = (index: number, field: keyof IngredientItem, value: string | number) => {
    const newIngredients = [...ingredients];
    newIngredients[index] = { ...newIngredients[index], [field]: value };
    setIngredients(newIngredients);
  };

  const handleDietaryPreferenceChange = (preference: DietaryPreference) => {
    setDietaryPreferences(prev =>
      prev.includes(preference)
        ? prev.filter(p => p !== preference)
        : [...prev, preference]
    );
  };

  const handleTastePreferenceChange = (taste: string) => {
    setTastePreferences(prev =>
      prev.includes(taste)
        ? prev.filter(t => t !== taste)
        : [...prev, taste]
    );
  };

  const validateForm = (): boolean => {
    // 检查必填字段
    if (!ingredients.some(ing => ing.name.trim())) {
      onError('请至少添加一种食材');
      return false;
    }

    // 检查所有添加的食材是否都有名称
    if (ingredients.some(ing => !ing.name.trim())) {
      onError('所有食材都必须有名称');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    
    try {
      const request: RecipeGenerationRequest = {
        title: title || undefined,
        dietary_preference: dietaryPreferences.length > 0 ? dietaryPreferences : undefined,
        ingredients: ingredients
          .filter(ing => ing.name.trim())
          .map(ing => ({
            name: ing.name,
            quantity: ing.quantity,
            unit: ing.unit
          })),
        exclude_ingredients: excludeIngredients ? excludeIngredients.split(',').map(i => i.trim()) : undefined,
        cuisine: cuisine || undefined,
        meal_type: mealType as any,
        difficulty: difficulty as any,
        prep_time_max: prepTimeMax ? parseInt(prepTimeMax) : undefined,
        cook_time_max: cookTimeMax ? parseInt(cookTimeMax) : undefined,
        servings: servings ? parseInt(servings) : undefined,
        nutritional_goal: caloriesMax ? { calories_max: parseInt(caloriesMax) } : undefined,
        taste_preferences: tastePreferences as any,
        special_request: specialRequest || undefined
      };

      const recipe = await aiService.generateRecipe(request);
      onRecipeGenerated(recipe);
    } catch (error: any) {
      onError(
        error.response?.data?.detail || 
        error.response?.data?.message || 
        '生成食谱失败，请稍后重试'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h6" gutterBottom>创建个性化食谱</Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="食谱标题（可选）"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={isLoading}
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="菜系（可选）"
              value={cuisine}
              onChange={(e) => setCuisine(e.target.value)}
              disabled={isLoading}
            />
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <FormControl fullWidth>
              <InputLabel>餐型</InputLabel>
              <Select
                value={mealType}
                label="餐型"
                onChange={(e) => setMealType(e.target.value)}
                disabled={isLoading}
              >
                <MenuItem value="">不指定</MenuItem>
                <MenuItem value="breakfast">早餐</MenuItem>
                <MenuItem value="lunch">午餐</MenuItem>
                <MenuItem value="dinner">晚餐</MenuItem>
                <MenuItem value="snack">小吃</MenuItem>
                <MenuItem value="dessert">甜点</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <FormControl fullWidth>
              <InputLabel>难度</InputLabel>
              <Select
                value={difficulty}
                label="难度"
                onChange={(e) => setDifficulty(e.target.value)}
                disabled={isLoading}
              >
                <MenuItem value="">不指定</MenuItem>
                <MenuItem value="easy">简单</MenuItem>
                <MenuItem value="medium">中等</MenuItem>
                <MenuItem value="hard">困难</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <TextField
              fullWidth
              label="份量"
              type="number"
              value={servings}
              onChange={(e) => setServings(e.target.value)}
              disabled={isLoading}
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="最大准备时间（分钟）"
              type="number"
              value={prepTimeMax}
              onChange={(e) => setPrepTimeMax(e.target.value)}
              disabled={isLoading}
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="最大烹饪时间（分钟）"
              type="number"
              value={cookTimeMax}
              onChange={(e) => setCookTimeMax(e.target.value)}
              disabled={isLoading}
            />
          </Grid>
          
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>饮食偏好</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {Object.values(DietaryPreference).map((pref) => (
                <FormControlLabel
                  key={pref}
                  control={
                    <Checkbox
                      checked={dietaryPreferences.includes(pref)}
                      onChange={() => handleDietaryPreferenceChange(pref)}
                      disabled={isLoading}
                    />
                  }
                  label={
                    pref === DietaryPreference.VEGETARIAN ? '素食' :
                    pref === DietaryPreference.VEGAN ? '纯素食' :
                    pref === DietaryPreference.GLUTEN_FREE ? '无麸质' :
                    pref === DietaryPreference.DAIRY_FREE ? '无乳制品' :
                    pref === DietaryPreference.KETO ? '生酮饮食' :
                    pref === DietaryPreference.PALEO ? '古饮食' :
                    pref === DietaryPreference.LOW_CARB ? '低碳水' :
                    pref === DietaryPreference.HIGH_PROTEIN ? '高蛋白' : '无特殊偏好'
                  }
                />
              ))}
            </Box>
          </Grid>
          
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>口味偏好</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {['sweet', 'savory', 'spicy', 'sour', 'bitter'].map((taste) => (
                <FormControlLabel
                  key={taste}
                  control={
                    <Checkbox
                      checked={tastePreferences.includes(taste)}
                      onChange={() => handleTastePreferenceChange(taste)}
                      disabled={isLoading}
                    />
                  }
                  label={
                    taste === 'sweet' ? '甜味' :
                    taste === 'savory' ? '咸鲜味' :
                    taste === 'spicy' ? '辣味' :
                    taste === 'sour' ? '酸味' : '苦味'
                  }
                />
              ))}
            </Box>
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="排除食材（用逗号分隔，可选）"
              value={excludeIngredients}
              onChange={(e) => setExcludeIngredients(e.target.value)}
              disabled={isLoading}
              helperText="例如：洋葱,大蒜,香菜"
            />
          </Grid>
          
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>营养目标</Typography>
            <TextField
              fullWidth
              label="最大热量（卡路里）"
              type="number"
              value={caloriesMax}
              onChange={(e) => setCaloriesMax(e.target.value)}
              disabled={isLoading}
            />
          </Grid>
          
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>特殊要求（可选）</Typography>
            <TextField
              fullWidth
              multiline
              rows={3}
              placeholder="例如：减少油用量，添加更多蛋白质，使用特定烹饪方法等"
              value={specialRequest}
              onChange={(e) => setSpecialRequest(e.target.value)}
              disabled={isLoading}
            />
          </Grid>
          
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>主要食材</Typography>
            {ingredients.map((ingredient, index) => (
              <Box key={index} sx={{ display: 'flex', gap: 1, mb: 2, alignItems: 'center' }}>
                <TextField
                  label="食材名称"
                  value={ingredient.name}
                  onChange={(e) => handleIngredientChange(index, 'name', e.target.value)}
                  disabled={isLoading}
                  sx={{ flex: 1 }}
                />
                <TextField
                  label="数量"
                  type="number"
                  value={ingredient.quantity || ''}
                  onChange={(e) => handleIngredientChange(index, 'quantity', e.target.value ? parseInt(e.target.value) : '')}
                  disabled={isLoading}
                  sx={{ width: 80 }}
                />
                <TextField
                  label="单位"
                  value={ingredient.unit || ''}
                  onChange={(e) => handleIngredientChange(index, 'unit', e.target.value)}
                  disabled={isLoading}
                  sx={{ width: 100 }}
                />
                <IconButton
                  onClick={() => handleRemoveIngredient(index)}
                  disabled={ingredients.length === 1 || isLoading}
                >
                  <Delete />
                </IconButton>
              </Box>
            ))}
            <Button
              startIcon={<Add />}
              onClick={handleAddIngredient}
              disabled={isLoading}
            >
              添加食材
            </Button>
          </Grid>
          
          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={isLoading}
              startIcon={isLoading ? <CircularProgress size={16} /> : <Send />}
            >
              {isLoading ? '生成中...' : '生成个性化食谱'}
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default RecipeGenerationForm;