import React, { useState } from 'react';
import { Box, Button, Typography, Paper, Alert, CircularProgress } from '@mui/material';
import { LocalFireDepartment as FireIcon } from '@mui/icons-material';
import IngredientInput from '../IngredientInput/IngredientInput';
import RestrictionSelector from '../RestrictionSelector/RestrictionSelector';
import PreferenceSettings, { type Preferences } from '../PreferenceSettings/PreferenceSettings';
import RecipeCard from '../RecipeCard/RecipeCard';
import { useRecipe } from '../../../hooks/useRecipe';

interface RecipeGeneratorProps {
  initialIngredients?: string[];
  initialRestrictions?: string[];
  initialPreferences?: Preferences;
}

const RecipeGenerator: React.FC<RecipeGeneratorProps> = ({ 
  initialIngredients = [],
  initialRestrictions = [],
  initialPreferences = {}
}) => {
  console.log('RecipeGenerator component is rendering');
  const [ingredients, setIngredients] = useState<string[]>(initialIngredients);
  const [restrictions, setRestrictions] = useState<string[]>(initialRestrictions);
  const [preferences, setPreferences] = useState<Preferences>(initialPreferences);
  const [error, setError] = useState<string | null>(null);
  const { generateRecipes, generatedRecipes, loading, favoriteRecipe } = useRecipe();
  
  console.log('RecipeGenerator state:', { ingredients, restrictions, preferences, generatedRecipes, loading, error });

  const handleGenerate = async () => {
    console.log('Generate recipes button clicked with:', { ingredients, restrictions, preferences });
    if (ingredients.length === 0) {
      setError('请至少添加一种食材');
      return;
    }
    
    setError(null);
    try {
      await generateRecipes({
        ingredients,
        restrictions,
        preferences
      });
      console.log('Recipes generated successfully');
    } catch (err: any) {
      setError(err.message || '食谱生成失败，请重试');
      console.error('生成食谱失败:', err);
    }
  };

  const handleAddIngredient = (ingredient: string) => {
    setIngredients([...ingredients, ingredient]);
  };

  const handleRemoveIngredient = (index: number) => {
    const newIngredients = [...ingredients];
    newIngredients.splice(index, 1);
    setIngredients(newIngredients);
  };

  // 移除了保存到我的食谱功能，因为现在生成的食谱会自动保存到公共列表

  const handleFavorite = async (recipeId: string) => {
    try {
      await favoriteRecipe(recipeId);
      // 可以添加成功提示
      console.log('食谱已收藏');
    } catch (err) {
      console.error('收藏食谱失败:', err);
      setError('收藏食谱失败');
    }
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Paper sx={{ p: 4, borderRadius: 3, backgroundColor: '#ffffff', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 4 }}>
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#333', display: 'flex', alignItems: 'center', gap: 1 }}>
            <FireIcon sx={{ color: '#ff5722' }} />
            生成个性化食谱
          </Typography>
        </Box>
        
        {error && (
          <Alert
            severity="error"
            sx={{ mb: 3 }}
          >
            {error}
          </Alert>
        )}
        
        <IngredientInput
          ingredients={ingredients}
          onAddIngredient={handleAddIngredient}
          onRemoveIngredient={handleRemoveIngredient}
        />
        
        <RestrictionSelector
          restrictions={restrictions}
          onRestrictionChange={setRestrictions}
        />
        
        <PreferenceSettings
          preferences={preferences}
          onPreferenceChange={setPreferences}
        />
        
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Button 
            variant="contained"
            size="large"
            onClick={handleGenerate}
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <FireIcon />}
            sx={{
              fontSize: '1.1rem',
              padding: '10px 40px',
              backgroundColor: '#4caf50',
              '&:hover': {
                backgroundColor: '#388e3c',
              },
              borderRadius: 2,
              textTransform: 'none',
              fontWeight: 'bold',
            }}
          >
            {loading ? '正在生成食谱...' : '开始生成食谱'}
          </Button>
        </Box>
      </Paper>

      {/* 生成的食谱展示 */}
      {generatedRecipes.length > 0 ? (
        <Paper sx={{ p: 4, borderRadius: 3, backgroundColor: '#ffffff', boxShadow: '0 4px 12px rgba(0,0,0,0.08)', mt: 4 }}>
          <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#333', mb: 3 }}>
            生成的食谱
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
              {/* 调试日志 */}
            {generatedRecipes.map((recipe) => (
              <Box key={recipe.recipe_id} sx={{ flex: '1 1 300px', maxWidth: { xs: '100%', sm: 'calc(50% - 12px)', md: 'calc(33.333% - 16px)' } }}>
                <RecipeCard 
                  recipe={recipe} 
                  onFavorite={handleFavorite}
                />
              </Box>
            ))}
          </Box>
        </Paper>
      ) : loading === false && generatedRecipes.length === 0 ? (
        <Paper sx={{ p: 6, borderRadius: 3, backgroundColor: '#ffffff', boxShadow: '0 4px 12px rgba(0,0,0,0.08)', mt: 4, textAlign: 'center' }}>
          <Typography variant="h6" sx={{ color: '#666', mb: 2 }}>
            还没有生成食谱
          </Typography>
          <Typography variant="body1" sx={{ color: '#999' }}>
            添加食材并点击"开始生成食谱"按钮，获取个性化的食谱推荐
          </Typography>
        </Paper>
      ) : null}
    </Box>
  );
};

export default RecipeGenerator;
