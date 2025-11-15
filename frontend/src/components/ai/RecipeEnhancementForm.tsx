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
  FormControlLabel,
  Checkbox,
  Alert,
  CircularProgress
} from '@mui/material';
import { Send } from '@mui/icons-material';
import { RecipeEnhancementRequest, DietaryPreference } from '../../types/ai';
import aiService from '../../services/aiService';
import { RecipeResponse } from '../../types/recipe';

interface RecipeEnhancementFormProps {
  onRecipeEnhanced: (recipe: RecipeResponse) => void;
  onError: (error: string) => void;
  existingRecipe?: RecipeResponse;
}

const RecipeEnhancementForm: React.FC<RecipeEnhancementFormProps> = ({ 
  onRecipeEnhanced, 
  onError,
  existingRecipe
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [enhancementType, setEnhancementType] = useState<string>('');
  const [substituteFrom, setSubstituteFrom] = useState('');
  const [substituteTo, setSubstituteTo] = useState('');
  const [customRequest, setCustomRequest] = useState('');
  const [dietaryPreferences, setDietaryPreferences] = useState<DietaryPreference[]>([]);

  const handleDietaryPreferenceChange = (preference: DietaryPreference) => {
    setDietaryPreferences(prev =>
      prev.includes(preference)
        ? prev.filter(p => p !== preference)
        : [...prev, preference]
    );
  };

  const validateForm = (): boolean => {
    if (!enhancementType) {
      onError('请选择增强类型');
      return false;
    }

    if (enhancementType === 'substitute_ingredient') {
      if (!substituteFrom.trim()) {
        onError('请输入要替换的食材');
        return false;
      }
      if (!substituteTo.trim()) {
        onError('请输入替换成的食材');
        return false;
      }
    }

    if (enhancementType === 'custom' && !customRequest.trim()) {
      onError('请输入自定义增强要求');
      return false;
    }

    if (!existingRecipe && !customRequest) {
      onError('请提供要增强的食谱信息');
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
      const request: RecipeEnhancementRequest = {
        recipe_id: existingRecipe?.id,
        original_recipe: existingRecipe ? {
          title: existingRecipe.title,
          description: existingRecipe.description,
          ingredients: existingRecipe.ingredients.map(ing => ({
            name: ing.name,
            quantity: ing.quantity,
            unit: ing.unit
          })),
          cooking_steps: existingRecipe.cooking_steps.map(step => ({
            step_number: step.step_number,
            description: step.description
          })),
          prep_time: existingRecipe.prep_time,
          cook_time: existingRecipe.cook_time,
          servings: existingRecipe.servings,
          difficulty: existingRecipe.difficulty
        } : undefined,
        enhancement_type: enhancementType as any,
        substitute_from: substituteFrom || undefined,
        substitute_to: substituteTo || undefined,
        custom_request: customRequest || undefined,
        dietary_preference: dietaryPreferences.length > 0 ? dietaryPreferences : undefined
      };

      const recipe = await aiService.enhanceRecipe(request);
      onRecipeEnhanced(recipe);
    } catch (error: any) {
      onError(
        error.response?.data?.detail || 
        error.response?.data?.message || 
        '增强食谱失败，请稍后重试'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const getEnhancementTypeLabel = (type: string): string => {
    switch (type) {
      case 'more_healthy': return '更健康';
      case 'more_flavorful': return '更美味';
      case 'reduce_time': return '减少制作时间';
      case 'increase_yield': return '增加份量';
      case 'substitute_ingredient': return '替换食材';
      case 'custom': return '自定义';
      default: return '';
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h6" gutterBottom>增强现有食谱</Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <FormControl fullWidth>
              <InputLabel>增强类型</InputLabel>
              <Select
                value={enhancementType}
                label="增强类型"
                onChange={(e) => setEnhancementType(e.target.value)}
                disabled={isLoading}
              >
                <MenuItem value="more_healthy">更健康</MenuItem>
                <MenuItem value="more_flavorful">更美味</MenuItem>
                <MenuItem value="reduce_time">减少制作时间</MenuItem>
                <MenuItem value="increase_yield">增加份量</MenuItem>
                <MenuItem value="substitute_ingredient">替换食材</MenuItem>
                <MenuItem value="custom">自定义</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          {enhancementType === 'substitute_ingredient' && (
            <>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="要替换的食材"
                  value={substituteFrom}
                  onChange={(e) => setSubstituteFrom(e.target.value)}
                  disabled={isLoading}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="替换成的食材"
                  value={substituteTo}
                  onChange={(e) => setSubstituteTo(e.target.value)}
                  disabled={isLoading}
                />
              </Grid>
            </>
          )}
          
          {(enhancementType === 'custom' || !existingRecipe) && (
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="自定义要求"
                placeholder="详细描述您希望如何增强或修改这个食谱"
                value={customRequest}
                onChange={(e) => setCustomRequest(e.target.value)}
                disabled={isLoading}
              />
            </Grid>
          )}
          
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>饮食偏好限制</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {Object.values(DietaryPreference).filter(pref => pref !== DietaryPreference.NONE).map((pref) => (
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
                    pref === DietaryPreference.LOW_CARB ? '低碳水' : '高蛋白'
                  }
                />
              ))}
            </Box>
          </Grid>
          
          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={isLoading}
              startIcon={isLoading ? <CircularProgress size={16} /> : <Send />}
            >
              {isLoading ? '增强中...' : `增强食谱（${getEnhancementTypeLabel(enhancementType)}）`}
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default RecipeEnhancementForm;