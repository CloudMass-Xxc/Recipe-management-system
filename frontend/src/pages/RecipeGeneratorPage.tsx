import React, { useState } from 'react';
import { Box, Typography, TextField, Button, FormControl, InputLabel, Select, MenuItem, Container, Paper, Divider, useMediaQuery, useTheme } from '@mui/material';

interface RecipePreference {
  ingredients: string;
  dietaryRestriction: string;
  cuisine: string;
  cookTime: string;
  difficulty: string;
}

const RecipeGeneratorPage: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  const [preferences, setPreferences] = useState<RecipePreference>({
    ingredients: '',
    dietaryRestriction: '',
    cuisine: '',
    cookTime: '',
    difficulty: '',
  });
  const [generatedRecipe, setGeneratedRecipe] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 处理表单输入变化
  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>, fieldName?: string) => {
    const name = fieldName || event.target.name;
    const value = event.target.value;
    setPreferences(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // 处理Select组件变化
  const handleSelectChange = (event: any, value: React.ReactNode) => {
    const name = event.target?.name || event.target?.id || event.currentTarget?.name;
    setPreferences(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleGenerate = async () => {
    try {
      setLoading(true);
      console.log('生成食谱请求:', preferences);
      
      // 准备请求数据
      const requestData = {
        dietary_preferences: preferences.dietaryRestriction ? [preferences.dietaryRestriction] : [],
        food_likes: preferences.ingredients ? preferences.ingredients.split(',').map(item => item.trim()) : [],
        food_dislikes: [],
        health_conditions: [],
        nutrition_goals: [],
        cooking_time_limit: preferences.cookTime === 'quick' ? 30 : preferences.cookTime === 'medium' ? 45 : undefined,
        difficulty: preferences.difficulty,
        cuisine: preferences.cuisine || 'none' // 添加菜系参数
      };
      
      // 发送实际的API请求
      const response = await fetch('http://localhost:8000/ai/generate-recipe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify(requestData)
      });
      
      if (!response.ok) {
        throw new Error(`API请求失败: ${response.status}`);
      }
      
      const recipeData = await response.json();
      // 转换后端返回的数据格式以匹配前端期望的格式
      const formattedRecipe = {
        id: recipeData.title || 'generated-recipe',
        title: recipeData.title,
        description: recipeData.description,
        ingredients: recipeData.ingredients.map((ing: any) => `${ing.quantity} ${ing.unit} ${ing.name}`),
        instructions: recipeData.instructions,
        cookTime: `${recipeData.cooking_time}分钟`,
        difficulty: getDifficultyText(recipeData.difficulty),
        image: `https://via.placeholder.com/400x300?text=${encodeURIComponent(recipeData.title)}`
      };
      
      setGeneratedRecipe(formattedRecipe);
      setLoading(false);
    } catch (error) {
      console.error('生成食谱失败:', error);
      setError('生成食谱失败，请稍后重试');
      setLoading(false);
    }
  };
  
  // 辅助函数：将难度枚举转换为中文显示
  const getDifficultyText = (difficulty: string): string => {
    const difficultyMap: Record<string, string> = {
      'easy': '简单',
      'medium': '中等',
      'hard': '困难'
    };
    return difficultyMap[difficulty] || difficulty;
  };

  return (
    <Container maxWidth={isMobile ? "sm" : "md"} sx={{ p: { xs: 1, sm: 2 } }}>
      {/* 表单卡片 */}
      <Paper 
        elevation={isMobile ? 1 : 3} 
        sx={{ 
          p: { xs: 3, sm: 4 }, 
          mb: 4,
          borderRadius: 2,
          transition: 'transform 0.2s',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: isMobile ? theme.shadows[1] : theme.shadows[4],
            transition: 'transform 0.2s, box-shadow 0.2s'
          }
        }}
      >
        {/* 页面标题 */}
        <Box sx={{ textAlign: { xs: 'center', sm: 'left' } }}>
          <Typography 
            variant={isMobile ? "h5" : "h4"} 
            component="h1" 
            gutterBottom
            sx={{ fontWeight: 700, color: theme.palette.primary.main }}
          >
            生成个性化食谱
          </Typography>
          <Typography 
            variant="body1" 
            gutterBottom
            sx={{ 
              color: theme.palette.text.secondary, 
              maxWidth: { xs: '100%', md: '90%' },
              margin: '0 auto'
            }}
          >
            输入您的偏好，我们将为您生成完美的食谱
          </Typography>
        </Box>
        
        {/* 表单区域 */}
        <Box sx={{ mt: { xs: 3, sm: 4 } }}>
          {/* 食材输入框 */}
          <Box sx={{ mb: { xs: 3, sm: 4 } }}>
            <TextField
              fullWidth
              label="喜欢的食材（用逗号分隔）"
              name="ingredients"
              value={preferences.ingredients}
              onChange={handleChange}
              multiline
              rows={isMobile ? 2 : 3}
              variant="outlined"
              size={isMobile ? "small" : "medium"}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderRadius: 1.5,
                  },
                }
              }}
            />
          </Box>
          
          {/* 筛选选项 - 响应式网格布局 */}
          <Box 
            sx={{ 
              display: 'grid', 
              gridTemplateColumns: { 
                xs: '1fr', 
                sm: '1fr', 
                md: '1fr 1fr' 
              }, 
              gap: { xs: 2, sm: 3 }, 
              mb: { xs: 3, sm: 4 }
            }}
          >
            {/* 饮食限制 */}
            <FormControl 
              fullWidth 
              variant="outlined"
              size={isMobile ? "small" : "medium"}
              sx={{ 
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderRadius: 1.5,
                  },
                }
              }}
            >
              <InputLabel>饮食限制</InputLabel>
              <Select
                name="dietaryRestriction"
                value={preferences.dietaryRestriction}
                onChange={handleSelectChange}
                label="饮食限制"
              >
                <MenuItem value="">(无)</MenuItem>
                <MenuItem value="vegetarian">素食</MenuItem>
                <MenuItem value="vegan">纯素食</MenuItem>
                <MenuItem value="glutenFree">无麸质</MenuItem>
                <MenuItem value="dairyFree">无乳糖</MenuItem>
              </Select>
            </FormControl>
            
            {/* 菜系 */}
            <FormControl 
              fullWidth 
              variant="outlined"
              size={isMobile ? "small" : "medium"}
              sx={{ 
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderRadius: 1.5,
                  },
                }
              }}
            >
              <InputLabel>菜系</InputLabel>
              <Select
                name="cuisine"
                value={preferences.cuisine}
                onChange={handleSelectChange}
                label="菜系"
              >
                <MenuItem value="">(无)</MenuItem>
                <MenuItem value="chinese">中餐</MenuItem>
                <MenuItem value="western">西餐</MenuItem>
                <MenuItem value="japanese">日料</MenuItem>
                <MenuItem value="korean">韩餐</MenuItem>
              </Select>
            </FormControl>
            
            {/* 烹饪时间 */}
            <FormControl 
              fullWidth 
              variant="outlined"
              size={isMobile ? "small" : "medium"}
              sx={{ 
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderRadius: 1.5,
                  },
                }
              }}
            >
              <InputLabel>烹饪时间</InputLabel>
              <Select
                name="cookTime"
                value={preferences.cookTime}
                onChange={handleSelectChange}
                label="烹饪时间"
              >
                <MenuItem value="">(无)</MenuItem>
                <MenuItem value="quick">快速（30分钟内）</MenuItem>
                <MenuItem value="medium">中等（30-60分钟）</MenuItem>
                <MenuItem value="long">较长（60分钟以上）</MenuItem>
              </Select>
            </FormControl>
            
            {/* 难度 */}
            <FormControl 
              fullWidth 
              variant="outlined"
              size={isMobile ? "small" : "medium"}
              sx={{ 
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderRadius: 1.5,
                  },
                }
              }}
            >
              <InputLabel>难度</InputLabel>
              <Select
                name="difficulty"
                value={preferences.difficulty}
                onChange={handleSelectChange}
                label="难度"
              >
                <MenuItem value="">(无)</MenuItem>
                <MenuItem value="easy">简单</MenuItem>
                <MenuItem value="medium">中等</MenuItem>
                <MenuItem value="hard">困难</MenuItem>
              </Select>
            </FormControl>
          </Box>
          
          {/* 生成按钮 */}
          <Button
            variant="contained"
            fullWidth
            onClick={handleGenerate}
            disabled={loading}
            size={isMobile ? "medium" : "large"}
            sx={{ 
              py: { xs: 1.25, sm: 1.5 },
              borderRadius: 2,
              fontWeight: 600,
              transition: 'transform 0.2s',
              '&:hover': {
                transform: 'translateY(-1px)',
                transition: 'transform 0.2s',
              },
              '&:active': {
                transform: 'translateY(0)',
              }
            }}
          >
            {loading ? '生成中...' : '生成食谱'}
          </Button>
        </Box>
      </Paper>
        
      {/* 生成的食谱展示 - 添加响应式设计 */}
      {generatedRecipe && (
        <Paper 
          elevation={isMobile ? 1 : 3} 
          sx={{ 
            p: { xs: 3, sm: 4 },
            borderRadius: 2,
            mt: 2,
            transition: 'opacity 0.5s, transform 0.5s',
            opacity: 1,
            transform: 'translateY(0)'
          }}
        >
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Typography 
              variant={isMobile ? "h5" : "h4"} 
              component="h2" 
              gutterBottom
              sx={{ fontWeight: 700, color: theme.palette.primary.main }}
            >
              {generatedRecipe.title}
            </Typography>
          </Box>
          
          <Divider sx={{ mb: { xs: 3, sm: 4 } }} />
          
          {/* 食谱图片 */}
          <Box 
            sx={{ 
              mb: { xs: 3, sm: 4 }, 
              overflow: 'hidden',
              borderRadius: 2,
              boxShadow: theme.shadows[2]
            }}
          >
            <img
              src={generatedRecipe.image}
              alt={generatedRecipe.title}
              style={{ 
                width: '100%', 
                height: 'auto',
                transition: 'transform 0.3s'
              }}
            />
          </Box>
          
          {/* 食谱详情 */}
          <Box 
            sx={{ 
              mb: { xs: 3, sm: 4 },
              display: 'grid',
              gap: 4
            }}
          >
            {/* 描述 */}
            <Box>
              <Typography 
                variant="subtitle1" 
                fontWeight="bold"
                gutterBottom
                sx={{ color: theme.palette.primary.dark }}
              >
                描述
              </Typography>
              <Box 
                sx={{ 
                  p: 2, 
                  bgcolor: theme.palette.background.default,
                  borderRadius: 1.5,
                  boxShadow: 'inset 0 0 0 1px rgba(0,0,0,0.05)'
                }}
              >
                <Typography>{generatedRecipe.description}</Typography>
              </Box>
            </Box>
            
            {/* 配料 */}
            <Box>
              <Typography 
                variant="subtitle1" 
                fontWeight="bold"
                gutterBottom
                sx={{ color: theme.palette.primary.dark }}
              >
                配料
              </Typography>
              <Box 
                sx={{ 
                  p: 2, 
                  bgcolor: theme.palette.background.default,
                  borderRadius: 1.5,
                  boxShadow: 'inset 0 0 0 1px rgba(0,0,0,0.05)'
                }}
              >
                <Box 
                  sx={{ 
                    display: 'grid', 
                    gridTemplateColumns: { 
                      xs: '1fr', 
                      sm: 'repeat(auto-fill, minmax(150px, 1fr))' 
                    },
                    gap: { xs: 1, sm: 2 }
                  }}
                >
                  {generatedRecipe.ingredients.map((ingredient: string, index: number) => (
                    <Box 
                      key={index} 
                      sx={{ 
                        display: 'flex', 
                        alignItems: 'center', 
                        gap: 1,
                        bgcolor: theme.palette.background.paper,
                        p: 1,
                        borderRadius: 1,
                        boxShadow: theme.shadows[0]
                      }}
                    >
                      <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: theme.palette.primary.main }} />
                      <Typography variant="body2">{ingredient}</Typography>
                    </Box>
                  ))}
                </Box>
              </Box>
            </Box>
            
            {/* 步骤 */}
            <Box>
              <Typography 
                variant="subtitle1" 
                fontWeight="bold"
                gutterBottom
                sx={{ color: theme.palette.primary.dark }}
              >
                步骤
              </Typography>
              <Box 
                sx={{ 
                  p: 2, 
                  bgcolor: theme.palette.background.default,
                  borderRadius: 1.5,
                  boxShadow: 'inset 0 0 0 1px rgba(0,0,0,0.05)'
                }}
              >
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: { xs: 2, sm: 3 } }}>
                  {generatedRecipe.instructions.map((instruction: string, index: number) => (
                    <Box 
                      key={index} 
                      sx={{ 
                        display: 'flex', 
                        gap: 2,
                        alignItems: { xs: 'flex-start', sm: 'flex-start' }
                      }}
                    >
                      <Box 
                        sx={{
                          display: 'flex',
                          justifyContent: 'center',
                          alignItems: 'center',
                          minWidth: 28,
                          height: 28,
                          borderRadius: '50%',
                          bgcolor: theme.palette.primary.main,
                          color: 'white',
                          fontWeight: 600,
                          fontSize: '0.875rem',
                          mt: { xs: 0.25, sm: 0 }
                        }}
                      >
                        {index + 1}
                      </Box>
                      <Typography variant="body1">{instruction}</Typography>
                    </Box>
                  ))}
                </Box>
              </Box>
            </Box>
          </Box>
        </Paper>
      )}
      </Container>
  );
};

export default RecipeGeneratorPage;