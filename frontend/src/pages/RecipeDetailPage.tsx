import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography, Container, Paper, Button, Chip, Divider, IconButton, useMediaQuery, useTheme, Alert } from '@mui/material';
import { useAppDispatch, useAppSelector } from '../redux/hooks';
import { addToFavorites, removeFromFavorites, fetchRecipeDetail } from '../redux/slices/recipeSlice';
import RecipeAPI from '../services/recipeAPI';

interface Recipe {
  id: string;
  title: string;
  description: string;
  ingredients: string[];
  instructions: string[];
  cookTime: string;
  difficulty: string;
  servings: number;
  calories: number;
  image: string;
  tags: string[];
  isFavorite: boolean;
}

const RecipeDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const dispatch = useAppDispatch();
  const { currentRecipe, isLoading, error } = useAppSelector((state) => state.recipes);
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(true);
  const [favoriteError, setFavoriteError] = useState<string | null>(null);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState<boolean>(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  useEffect(() => {
    const fetchRecipeDetail = async () => {
      try {
        setLoading(true);
        if (id) {
          // 调用Redux的fetchRecipeDetail action获取食谱详情
          await dispatch(fetchRecipeDetail(id));
        } else {
          // 模拟数据（当没有id时）
          const mockRecipe: Recipe = {
            id: '1',
            title: '健康蔬菜炒饭',
            description: '这是一道营养丰富的蔬菜炒饭，使用新鲜蔬菜和优质大米制作。适合素食者，也是一道快速便捷的家常菜。',
            ingredients: [
              '大米 1碗',
              '胡萝卜 1根',
              '青豆 50g',
              '玉米粒 50g',
              '鸡蛋 2个',
              '葱 2根',
              '盐 适量',
              '生抽 1勺',
              '食用油 2勺'
            ],
            instructions: [
              '将胡萝卜洗净切丁，葱切末备用。',
              '热锅下油，炒香葱花。',
              '加入胡萝卜丁炒至变色。',
              '打入鸡蛋，快速翻炒成小块。',
              '加入米饭，用中火翻炒均匀。',
              '加入青豆和玉米粒，继续翻炒。',
              '加入生抽和盐调味，翻炒均匀即可出锅。'
            ],
            cookTime: '20分钟',
            difficulty: '简单',
            servings: 2,
            calories: 350,
            image: 'https://placehold.co/800x500?text=健康蔬菜炒饭',
            tags: ['素食', '快手菜', '家常菜'],
            isFavorite: false
          };
          setRecipe(mockRecipe);
        }
      } catch (error) {
        console.error('获取食谱详情失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipeDetail();
  }, [id, dispatch]);

  // 当currentRecipe从Redux更新时，更新本地状态
  useEffect(() => {
    if (currentRecipe) {
      setRecipe(currentRecipe);
    }
  }, [currentRecipe]);

  const handleFavoriteToggle = async () => {
    if (recipe && id) {
      try {
        setFavoriteError(null);
        if (recipe.isFavorite) {
          // 从收藏中移除
          await dispatch(removeFromFavorites(id));
        } else {
          // 添加到收藏
          await dispatch(addToFavorites(id));
        }
      } catch (error) {
        console.error('操作收藏失败:', error);
        setFavoriteError(recipe.isFavorite ? '取消收藏失败，请重试' : '添加收藏失败，请重试');
        // 3秒后自动清除错误提示
        setTimeout(() => setFavoriteError(null), 3000);
      }
    }
  };

  const handleSaveToMyRecipes = async () => {
    if (recipe) {
      try {
        setSaveError(null);
        setSaveSuccess(false);
        
        // 准备保存到我的食谱的数据
        const recipeData = {
          title: recipe.title,
          description: recipe.description,
          instructions: recipe.instructions,
          cooking_time: parseInt(recipe.cookTime) || 0,
          difficulty: recipe.difficulty,
          servings: recipe.servings,
          ingredients: recipe.ingredients.map(ing => {
            // 尝试解析食材字符串，提取名称、数量和单位
            const match = ing.match(/^(.*?)\s+(\d+(?:\.\d+)?)\s*(.*?)$/);
            if (match) {
              return {
                name: match[1].trim(),
                quantity: parseFloat(match[2]),
                unit: match[3].trim()
              };
            }
            return {
              name: ing.trim(),
              quantity: 1,
              unit: ''
            };
          }),
          tags: recipe.tags,
          nutrition_info: {
            calories: recipe.calories,
            protein: 0,
            carbs: 0,
            fat: 0,
            fiber: 0
          }
        };
        
        // 调用API保存食谱
        await RecipeAPI.saveGeneratedRecipe(recipeData);
        
        setSaveSuccess(true);
        // 3秒后自动清除成功提示
        setTimeout(() => setSaveSuccess(false), 3000);
      } catch (error) {
        console.error('保存食谱失败:', error);
        setSaveError('添加到我的食谱失败，请重试');
        // 3秒后自动清除错误提示
        setTimeout(() => setSaveError(null), 3000);
      }
    }
  };

  const handleShare = () => {
    // 模拟分享功能
    console.log('分享食谱:', recipe?.id);
    alert('分享链接已复制到剪贴板！');
  };

  if ((loading || isLoading) || !recipe) {
    return (
      <Container>
        <Typography variant="h6" align="center" sx={{ py: 4 }}>
          加载中...
        </Typography>
      </Container>
    );
  }

  // 显示错误信息
  if (error) {
    return (
      <Container>
        <Alert severity="error" sx={{ my: 4 }}>
          {error}
        </Alert>
        <Button
          component="a"
          href="/recipes"
          variant="contained"
        >
          返回食谱列表
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
        <Box sx={{ mb: 4, pt: 3 }}>
          <Button
            component="a"
            href="/recipes"
            sx={{ mb: 2 }}
            size={isMobile ? "small" : "medium"}
          >
            返回食谱列表
          </Button>
        </Box>

        <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 3, mb: 3 }}>
            <Box sx={{ width: { xs: '100%', sm: '50%' }, position: 'relative' }}>
              <img
                src={recipe.image}
                alt={recipe.title}
                style={{ width: '100%', height: 'auto', borderRadius: 8 }}
              />
              <Box sx={{ position: 'absolute', top: { xs: 8, sm: 16 }, right: { xs: 8, sm: 16 }, display: 'flex', gap: { xs: 1, sm: 2 } }}>
              <IconButton
                onClick={handleFavoriteToggle}
                sx={{ 
                  bgcolor: 'white', 
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.8)' },
                  minWidth: 'auto',
                  p: isMobile ? 1 : 1.5
                }}
              >
                {/* <FavoriteIcon color={recipe.isFavorite ? "error" : "action"} /> */}
                <span style={{ fontSize: isMobile ? '0.75rem' : '0.875rem' }}>{recipe.isFavorite ? "已收藏" : "收藏"}</span>
              </IconButton>
              <IconButton
                onClick={handleShare}
                sx={{ 
                  bgcolor: 'white', 
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.8)' },
                  minWidth: 'auto',
                  p: isMobile ? 1 : 1.5
                }}
              >
                {/* <ShareIcon color="action" /> */}
                <span style={{ fontSize: isMobile ? '0.75rem' : '0.875rem' }}>分享</span>
              </IconButton>
            </Box>
          </Box>
          <Box sx={{ width: { xs: '100%', sm: '50%' } }}>
            <Typography 
              variant={isMobile ? "h4" : "h3"} 
              component="h1" 
              gutterBottom
              sx={{ wordBreak: 'break-word' }}
            >
              {recipe.title}
            </Typography>
          </Box>
        </Box>

          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
            {recipe.tags.map(tag => (
              <Chip key={tag} label={tag} color="primary" variant="outlined" />
            ))}
          </Box>

          <Divider sx={{ mb: 3 }} />

          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" fontWeight="bold">描述：</Typography>
            <Typography variant="body1" paragraph>
              {recipe.description}
            </Typography>
          </Box>

          <Box sx={{ 
            display: 'grid', 
            gridTemplateColumns: { xs: '1fr 1fr', md: '1fr 1fr 1fr' }, 
            gap: 3, 
            mb: 4 
          }}>
            <Paper elevation={0} sx={{ p: 2, textAlign: 'center', border: '1px solid #e0e0e0' }}>
              <Typography variant="h6" color="primary">{recipe.cookTime}</Typography>
              <Typography variant="body2">烹饪时间</Typography>
            </Paper>
            <Paper elevation={0} sx={{ p: 2, textAlign: 'center', border: '1px solid #e0e0e0' }}>
              <Typography variant="h6" color="primary">{recipe.difficulty}</Typography>
              <Typography variant="body2">难度</Typography>
            </Paper>
            <Paper elevation={0} sx={{ p: 2, textAlign: 'center', border: '1px solid #e0e0e0' }}>
              <Typography variant="h6" color="primary">{recipe.servings} 人份</Typography>
              <Typography variant="body2">份量</Typography>
            </Paper>
          </Box>

          <Divider sx={{ mb: 3 }} />

          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>配料：</Typography>
            <ul style={{ paddingLeft: 20 }}>
              {recipe.ingredients.map((ingredient, index) => (
                <li key={index} style={{ marginBottom: 8 }}>
                  <Typography>{ingredient}</Typography>
                </li>
              ))}
            </ul>
          </Box>

          <Divider sx={{ mb: 3 }} />

          <Box>
            <Typography variant="h6" gutterBottom>烹饪步骤：</Typography>
            <ol style={{ paddingLeft: 20 }}>
              {recipe.instructions.map((instruction, index) => (
                <li key={index} style={{ marginBottom: 12 }}>
                  <Typography variant="body1">
                    <span style={{ fontWeight: 'bold', marginRight: 8 }}>{index + 1}.</span>
                    {instruction}
                  </Typography>
                </li>
              ))}
            </ol>
          </Box>

          <Box sx={{ mt: 4, p: 3, bgcolor: 'grey.50', borderRadius: 2 }}>
            <Typography variant="subtitle1" color="text.secondary" gutterBottom>
              营养信息（每份）：{recipe.calories} 卡路里
            </Typography>
            <Typography variant="body2" color="text.secondary">
              注：营养信息仅供参考，实际数值可能因食材和烹饪方法略有不同。
            </Typography>
          </Box>
        </Paper>
        
        {/* 操作提示 */}
        <Box sx={{ display: 'flex', gap: 2, mt: 4, mb: 2 }}>
          <Button 
            variant="contained" 
            color="primary" 
            onClick={handleSaveToMyRecipes}
            fullWidth
          >
            添加到我的食谱
          </Button>
          <Button 
            variant="outlined" 
            color="secondary" 
            onClick={handleFavoriteToggle}
            fullWidth
          >
            {recipe.isFavorite ? '取消收藏' : '添加到我的收藏'}
          </Button>
        </Box>
        
        {/* 错误和成功提示 */}
        {(favoriteError || saveError || saveSuccess) && (
          <Box sx={{ mt: 2 }}>
            {favoriteError && (
              <Alert severity="error">
                {favoriteError}
              </Alert>
            )}
            {saveError && (
              <Alert severity="error">
                {saveError}
              </Alert>
            )}
            {saveSuccess && (
              <Alert severity="success">
                成功添加到我的食谱！
              </Alert>
            )}
          </Box>
        )}
      </Container>
    );
  };

export default RecipeDetailPage;