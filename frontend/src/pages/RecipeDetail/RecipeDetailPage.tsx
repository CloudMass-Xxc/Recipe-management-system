import React, { useEffect, useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Rating, 
  Button, 
  Chip, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText,
  Divider,
  IconButton,
  Collapse,
  useMediaQuery,
  useTheme,
  CircularProgress
} from '@mui/material';
import { 
  ArrowBack, 

  Share, 
  AccessTime, 
  Star, 
  Info, 
  Restaurant,
  ExpandMore, 
  ExpandLess, 
  CheckCircle,
  Timer,
  People
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import Layout from '../../components/layout/Layout';
import { useRecipe } from '../../hooks/useRecipe';

// 推荐食谱数据 - 与HomePage保持一致
const recommendedRecipes = [
  {
    recipe_id: 'recommended-1',
    title: '健康早餐燕麦粥',
    image_url: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
    cooking_time: 15,
    time: '15分钟',
    difficulty: '简单',
    rating: 4.8,
    tags: ['健康', '早餐', '快速'],
    description: '营养丰富的早餐燕麦粥，富含膳食纤维和蛋白质，为您的一天提供充足能量。',
    instructions: [
      '将1杯燕麦片放入碗中',
      '加入2杯热水或热牛奶，搅拌',
      '静置2-3分钟，让燕麦片充分吸收水分',
      '根据个人口味添加蜂蜜、水果或坚果',
      '搅拌即可享用'
    ],
    servings: 1,
    ingredients: [
      { name: '燕麦片', quantity: '1', unit: '杯' },
      { name: '牛奶或水', quantity: '2', unit: '杯' },
      { name: '蜂蜜', quantity: '1', unit: '汤匙' },
      { name: '蓝莓', quantity: '1/2', unit: '杯' },
      { name: '核桃', quantity: '5', unit: '颗' }
    ],
    nutrition_info: {
      calories: 320,
      protein: 12,
      carbs: 45,
      fat: 10,
      fiber: 8
    }
  },
  {
    recipe_id: 'recommended-2',
    title: '番茄鸡蛋面',
    image_url: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
    cooking_time: 20,
    time: '20分钟',
    difficulty: '简单',
    rating: 4.6,
    tags: ['家常菜', '午餐', '快速'],
    description: '经典的中式家常菜，酸甜可口，营养均衡，制作简单快捷。',
    instructions: [
      '将面条放入沸水中煮熟，捞出过冷水备用',
      '鸡蛋打散，加入少许盐调味',
      '热锅倒油，倒入鸡蛋液炒熟盛起',
      '锅中再倒入少许油，放入番茄块炒软',
      '加入炒好的鸡蛋，翻炒均匀',
      '加入盐、糖、生抽调味',
      '将番茄鸡蛋卤浇在面条上即可'
    ],
    servings: 1,
    ingredients: [
      { name: '面条', quantity: '100', unit: '克' },
      { name: '鸡蛋', quantity: '2', unit: '个' },
      { name: '番茄', quantity: '2', unit: '个' },
      { name: '盐', quantity: '1/2', unit: '茶匙' },
      { name: '糖', quantity: '1', unit: '茶匙' },
      { name: '生抽', quantity: '1', unit: '汤匙' },
      { name: '油', quantity: '2', unit: '汤匙' }
    ],
    nutrition_info: {
      calories: 450,
      protein: 15,
      carbs: 60,
      fat: 18,
      fiber: 3
    }
  },
  {
    recipe_id: 'recommended-3',
    title: '红烧肉',
    image_url: 'https://images.unsplash.com/photo-1563245372-127f94260939?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
    cooking_time: 60,
    time: '60分钟',
    difficulty: '中等',
    rating: 4.9,
    tags: ['家常菜', '晚餐', '经典'],
    description: '传统中式经典菜肴，肥而不腻，色泽红亮，口感软糯香甜。',
    instructions: [
      '将五花肉切成2厘米见方的块状',
      '锅中放入清水，将肉块冷水下锅焯水',
      '撇去浮沫，将肉块捞出备用',
      '热锅倒油，放入冰糖小火炒至融化呈焦糖色',
      '放入焯好的肉块翻炒上色',
      '加入料酒、生抽、老抽、姜片和葱段',
      '倒入热水，没过肉块',
      '大火烧开后转小火慢炖40分钟',
      '最后大火收汁即可'
    ],
    servings: 4,
    ingredients: [
      { name: '五花肉', quantity: '500', unit: '克' },
      { name: '冰糖', quantity: '30', unit: '克' },
      { name: '料酒', quantity: '2', unit: '汤匙' },
      { name: '生抽', quantity: '2', unit: '汤匙' },
      { name: '老抽', quantity: '1', unit: '汤匙' },
      { name: '姜片', quantity: '3', unit: '片' },
      { name: '葱段', quantity: '2', unit: '根' },
      { name: '盐', quantity: '1', unit: '茶匙' }
    ],
    nutrition_info: {
      calories: 580,
      protein: 22,
      carbs: 18,
      fat: 50,
      fiber: 1
    }
  },
  {
    recipe_id: 'recommended-4',
    title: '蔬菜沙拉',
    image_url: 'https://images.unsplash.com/photo-1511690656952-34342bb7c2F5?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
    cooking_time: 10,
    time: '10分钟',
    difficulty: '简单',
    rating: 4.5,
    tags: ['健康', '低卡', '快速'],
    description: '清爽健康的蔬菜沙拉，富含维生素和膳食纤维，是减肥健身的理想选择。',
    instructions: [
      '将生菜洗净撕成小块',
      '黄瓜、番茄洗净切片',
      '紫甘蓝洗净切丝',
      '将所有蔬菜放入大碗中',
      '调制沙拉酱：橄榄油、柠檬汁、盐、黑胡椒混合',
      '将沙拉酱淋在蔬菜上',
      '撒上坚果碎，轻轻拌匀即可'
    ],
    servings: 1,
    ingredients: [
      { name: '生菜', quantity: '1', unit: '颗' },
      { name: '黄瓜', quantity: '1', unit: '根' },
      { name: '番茄', quantity: '1', unit: '个' },
      { name: '紫甘蓝', quantity: '1/4', unit: '个' },
      { name: '橄榄油', quantity: '1', unit: '汤匙' },
      { name: '柠檬汁', quantity: '1', unit: '汤匙' },
      { name: '盐', quantity: '1/4', unit: '茶匙' },
      { name: '黑胡椒', quantity: '少许', unit: '' },
      { name: '核桃碎', quantity: '1', unit: '汤匙' }
    ],
    nutrition_info: {
      calories: 180,
      protein: 5,
      carbs: 12,
      fat: 14,
      fiber: 8
    }
  }
];

const RecipeDetailPage: React.FC = () => {
  const { recipeId } = useParams<{ recipeId: string }>();
  const navigate = useNavigate();
  const { fetchRecipeDetail, currentRecipe, loading, error, clearError, getGeneratedRecipeById, setGeneratedRecipeDetail } = useRecipe();
  const [expandedSection, setExpandedSection] = useState<string | null>(null);
  const [checkedIngredients, setCheckedIngredients] = useState<number[]>([]);
  const [isImageLoaded, setIsImageLoaded] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  // 优先从推荐食谱中查找，然后从生成的食谱列表中查找，如果都找不到再从数据库获取
  useEffect(() => {
    console.log('RecipeDetailPage useEffect触发:', {
      recipeId,
      currentRecipe: currentRecipe?.recipe_id,
      timestamp: Date.now()
    });
    if (recipeId) {
      clearError();
      
      // 1. 首先尝试从推荐食谱中查找（以'recommended-'开头的ID）
      if (recipeId.startsWith('recommended-')) {
        const recommendedRecipe = recommendedRecipes.find(recipe => recipe.recipe_id === recipeId);
        
        if (recommendedRecipe) {
          // 只有当currentRecipe为空或ID不匹配时才设置，避免无限循环
          if (!currentRecipe || currentRecipe.recipe_id !== recommendedRecipe.recipe_id) {
            // 直接使用推荐食谱的完整数据
            setGeneratedRecipeDetail(recommendedRecipe);
          }
          return; // 找到推荐食谱后直接返回
        }
      }
      
      // 2. 尝试从生成的食谱中查找
      const generatedRecipe = getGeneratedRecipeById(recipeId);
      
      if (generatedRecipe) {
        // 直接使用生成的食谱的完整数据，而不是创建简化对象
        // 确保生成的食谱包含所有必要字段
        const fullRecipe = {
          ...generatedRecipe,
          recipe_id: generatedRecipe.recipe_id,
          cooking_time: typeof generatedRecipe.cooking_time === 'string' ? parseInt(generatedRecipe.cooking_time) || 0 : (generatedRecipe.cooking_time || 0),
          servings: generatedRecipe.servings || 1,
          author_id: generatedRecipe.author_id || 'ai-generated',
          author_name: generatedRecipe.author_name || 'AI生成',
          created_at: generatedRecipe.created_at || new Date().toISOString(),
          updated_at: generatedRecipe.updated_at || new Date().toISOString(),
          // 确保ingredients和instructions字段存在且类型正确
          ingredients: generatedRecipe.ingredients || [],
          instructions: generatedRecipe.instructions || [],
          // 确保nutrition_info字段存在
          nutrition_info: generatedRecipe.nutrition_info || {
            nutrition_id: '',
            recipe_id: generatedRecipe.recipe_id,
            calories: 0,
            protein: 0,
            carbs: 0,
            fat: 0,
            fiber: 0
          }
        };
        
        // 只有当currentRecipe为空或ID不匹配时才设置，避免无限循环
        if (!currentRecipe || currentRecipe.recipe_id !== fullRecipe.recipe_id) {
          // 使用新的action直接设置生成的食谱详情到Redux状态
          setGeneratedRecipeDetail(fullRecipe);
        }
      } else {
        // 3. 如果没有找到推荐食谱或生成的食谱，从数据库获取
        // 只有当currentRecipe为空或ID不匹配时才获取，避免无限循环
        if (!currentRecipe || currentRecipe.recipe_id !== recipeId) {
          fetchRecipeDetail(recipeId);
        }
      }
    }
  }, [recipeId, currentRecipe, fetchRecipeDetail, getGeneratedRecipeById, setGeneratedRecipeDetail, clearError]);

  // 当食谱数据加载完成后，记录instructions的数量
  useEffect(() => {
    if (currentRecipe && currentRecipe.instructions) {
      console.log('=== RecipeDetailPage: 食谱加载完成 ===');
      console.log('食谱标题:', currentRecipe.title);
      console.log('instructions数组长度:', currentRecipe.instructions.length);
      console.log('instructions类型:', typeof currentRecipe.instructions);
      console.log('instructions是否为数组:', Array.isArray(currentRecipe.instructions));
      console.log('instructions内容:', currentRecipe.instructions);
      console.log('=== RecipeDetailPage: 渲染烹饪步骤 ===');
      console.log('instructions.map执行前，instructions:', currentRecipe.instructions || []);
      console.log('instructions.map执行前，是否为数组:', Array.isArray(currentRecipe.instructions));
    }
  }, [currentRecipe]);

  // 处理食材勾选
  const handleIngredientToggle = (index: number) => {
    setCheckedIngredients(prev => 
      prev.includes(index) 
        ? prev.filter(i => i !== index)
        : [...prev, index]
    );
  };

  // 处理区域展开/折叠
  const handleSectionToggle = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section);
  };



  if (loading || !currentRecipe) {
    return (
      <Layout>
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '50vh',
          flexDirection: 'column',
          gap: 2
        }}>
          {error ? (
            <Box sx={{ textAlign: 'center', maxWidth: 400, p: 3 }}>
              <Typography variant="h6" color="error" sx={{ mb: 2 }}>
                {error}
              </Typography>
              <Button
                variant="contained"
                onClick={() => recipeId && fetchRecipeDetail(recipeId)}
                sx={{ backgroundColor: '#4caf50' }}
              >
                重试
              </Button>
            </Box>
          ) : (
            <>
              <CircularProgress size={60} sx={{ color: '#4caf50' }} />
              <Typography variant="h6" sx={{ mt: 2 }}>正在加载美味食谱...</Typography>
            </>
          )}
        </Box>
      </Layout>
    );
  }



  return (
    <Layout>
      {/* 顶部导航和标题 */}
      <Box sx={{ mb: 4 }}>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate(-1)}
          sx={{ 
            mb: 2,
            textTransform: 'none',
            fontWeight: 600,
            color: '#4caf50',
            '&:hover': {
              backgroundColor: 'rgba(76, 175, 80, 0.1)'
            }
          }}
        >
          返回
        </Button>
        
        <Typography 
          variant="h3" 
          sx={{ 
            fontWeight: 'bold', 
            color: '#333', 
            mb: 2,
            lineHeight: 1.2,
            fontSize: { xs: '1.75rem', md: '2.5rem' }
          }}
        >
          {currentRecipe.title}
        </Typography>
        
        {/* 食谱基本信息标签 */}
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: 2, 
          mb: 3,
          flexWrap: 'wrap'
        }}>
          <Rating 
            value={0} 
            precision={0.5} 
            readOnly 
            sx={{
              '& .MuiRating-iconFilled': {
                color: '#ff9800',
              },
              '& .MuiRating-iconEmpty': {
                color: '#e0e0e0',
              },
            }}
          />
          <Typography variant="body2" color="text.secondary">
            (0)
          </Typography>
          
          <Chip
            label={currentRecipe.difficulty}
            size="small"
            sx={{ 
              backgroundColor: '#e8f5e8', 
              color: '#388e3c',
              fontWeight: 600,
              borderRadius: 1.5
            }}
          />
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <AccessTime fontSize="small" sx={{ color: '#666' }} />
            <Typography variant="body2" color="text.secondary">
              {currentRecipe.cooking_time}分钟
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <People fontSize="small" sx={{ color: '#666' }} />
            <Typography variant="body2" color="text.secondary">
              {currentRecipe.servings}人份
            </Typography>
          </Box>
        </Box>
        
        {/* 食谱标签 */}
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.75, mb: 3 }}>
          {currentRecipe.tags?.map((tag, index) => (
            <Chip 
              key={index} 
              label={tag} 
              size="small" 
              variant="outlined" 
              sx={{ 
                fontSize: '0.75rem',
                borderRadius: 1.5,
                borderColor: '#4caf50',
                color: '#4caf50',
                '&:hover': {
                  backgroundColor: 'rgba(76, 175, 80, 0.05)'
                }
              }}
            />
          ))}
        </Box>
        
        {/* 食谱描述 */}
        {currentRecipe.description && (
          <Paper sx={{ 
            p: 3, 
            borderRadius: 2, 
            mb: 3,
            backgroundColor: '#f9f9f9',
            transition: 'transform 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
            }
          }}>
            <Typography variant="body1" color="text.primary" sx={{ lineHeight: 1.6 }}>
              {currentRecipe.description}
            </Typography>
          </Paper>
        )}
      </Box>

      {/* 主内容区域 */}
      <Box sx={{ 
        display: 'flex', 
        flexDirection: { xs: 'column', md: 'row' }, 
        gap: 4,
        mb: 4
      }}>
        {/* 左侧：食谱图片和营养信息 */}
        <Box sx={{ flex: '1 1 100%', md: '0 0 40%' }}>
          {/* 食谱主图 */}
          <Paper sx={{ 
            overflow: 'hidden', 
            borderRadius: 2,
            boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
            transition: 'transform 0.3s ease, box-shadow 0.3s ease',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: '0 8px 24px rgba(0,0,0,0.15)'
            }
          }}>
            <Box sx={{ position: 'relative', width: '100%', height: isMobile ? 250 : 400 }}>
              {!isImageLoaded && (
                <Box sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  backgroundColor: '#f0f0f0'
                }}>
                  <CircularProgress sx={{ color: '#4caf50' }} />
                </Box>
              )}
              <img
                src={currentRecipe.image_url || 'https://picsum.photos/600/400?random=detail'}
                alt={currentRecipe.title}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  transition: 'opacity 0.5s ease',
                  opacity: isImageLoaded ? 1 : 0
                }}
                onLoad={() => setIsImageLoaded(true)}
                loading="lazy"
              />
            </Box>
          </Paper>

          {/* 烹饪信息概览 */}
          <Box sx={{ 
            mt: 3, 
            p: 3, 
            borderRadius: 2,
            backgroundColor: '#f9f9f9'
          }}>
            <Typography variant="h6" sx={{ 
              fontWeight: 'bold', 
              mb: 2, 
              display: 'flex', 
              alignItems: 'center', 
              gap: 1,
              color: '#333'
            }}>
              <Timer sx={{ color: '#4caf50' }} />
              烹饪概览
            </Typography>
            
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Box sx={{ 
                flex: 1,
                textAlign: 'center', 
                p: 2, 
                backgroundColor: '#fff', 
                borderRadius: 1.5,
                boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
              }}>
                <Typography variant="body2" color="text.secondary">烹饪时间</Typography>
                <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#4caf50' }}>
                  {currentRecipe.cooking_time}分钟
                </Typography>
              </Box>
              <Box sx={{ 
                flex: 1,
                textAlign: 'center', 
                p: 2, 
                backgroundColor: '#fff', 
                borderRadius: 1.5,
                boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
              }}>
                <Typography variant="body2" color="text.secondary">份量</Typography>
                <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#4caf50' }}>
                  {currentRecipe.servings}人
                </Typography>
              </Box>
            </Box>
          </Box>

          {/* 营养信息 */}
          <Paper sx={{ 
            mt: 3, 
            p: 3, 
            borderRadius: 2,
            transition: 'transform 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
            }
          }}>
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              mb: 2
            }}>
              <Typography variant="h6" sx={{ 
                fontWeight: 'bold', 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                color: '#333'
              }}>
                <Info sx={{ color: '#4caf50' }} />
                营养信息
              </Typography>
              <IconButton 
                size="small"
                onClick={() => handleSectionToggle('nutrition')}
              >
                {expandedSection === 'nutrition' ? <ExpandLess /> : <ExpandMore />}
              </IconButton>
            </Box>
            
            <Collapse in={expandedSection === 'nutrition' || expandedSection === null}>
              <Box sx={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(2, 1fr)', 
                gap: 2
              }}>
                <Box sx={{ 
                  textAlign: 'center', 
                  p: 2, 
                  backgroundColor: '#f5f5f5', 
                  borderRadius: 1.5,
                  transition: 'transform 0.2s ease',
                  '&:hover': {
                    transform: 'scale(1.02)',
                    backgroundColor: '#e8f5e8'
                  }
                }}>
                  <Typography variant="body2" color="text.secondary">卡路里</Typography>
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                    {currentRecipe.nutrition_info?.calories || 0} kcal
                  </Typography>
                </Box>
                <Box sx={{ 
                  textAlign: 'center', 
                  p: 2, 
                  backgroundColor: '#f5f5f5', 
                  borderRadius: 1.5,
                  transition: 'transform 0.2s ease',
                  '&:hover': {
                    transform: 'scale(1.02)',
                    backgroundColor: '#e8f5e8'
                  }
                }}>
                  <Typography variant="body2" color="text.secondary">蛋白质</Typography>
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                    {currentRecipe.nutrition_info?.protein || 0} g
                  </Typography>
                </Box>
                <Box sx={{ 
                  textAlign: 'center', 
                  p: 2, 
                  backgroundColor: '#f5f5f5', 
                  borderRadius: 1.5,
                  transition: 'transform 0.2s ease',
                  '&:hover': {
                    transform: 'scale(1.02)',
                    backgroundColor: '#e8f5e8'
                  }
                }}>
                  <Typography variant="body2" color="text.secondary">碳水化合物</Typography>
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                    {currentRecipe.nutrition_info?.carbs || 0} g
                  </Typography>
                </Box>
                <Box sx={{ 
                  textAlign: 'center', 
                  p: 2, 
                  backgroundColor: '#f5f5f5', 
                  borderRadius: 1.5,
                  transition: 'transform 0.2s ease',
                  '&:hover': {
                    transform: 'scale(1.02)',
                    backgroundColor: '#e8f5e8'
                  }
                }}>
                  <Typography variant="body2" color="text.secondary">脂肪</Typography>
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                    {currentRecipe.nutrition_info?.fat || 0} g
                  </Typography>
                </Box>
                {currentRecipe.nutrition_info?.fiber !== undefined && (
                  <Box sx={{ 
                    textAlign: 'center', 
                    p: 2, 
                    backgroundColor: '#f5f5f5', 
                    borderRadius: 1.5,
                    gridColumn: 'span 2',
                    transition: 'transform 0.2s ease',
                    '&:hover': {
                      transform: 'scale(1.02)',
                      backgroundColor: '#e8f5e8'
                    }
                  }}>
                    <Typography variant="body2" color="text.secondary">膳食纤维</Typography>
                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                      {currentRecipe.nutrition_info.fiber} g
                    </Typography>
                  </Box>
                )}
              </Box>
            </Collapse>
          </Paper>
        </Box>

        {/* 右侧：食材和步骤 */}
        <Box sx={{ flex: '1 1 100%', md: '0 0 60%' }}>
          {/* 食材列表 */}
          <Paper sx={{ 
            p: 3, 
            borderRadius: 2, 
            mb: 3,
            transition: 'transform 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
            }
          }}>
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              mb: 2
            }}>
              <Typography variant="h6" sx={{ 
                fontWeight: 'bold', 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                color: '#333'
              }}>
                <Restaurant sx={{ color: '#4caf50' }} />
                食材
              </Typography>
              <Typography variant="caption" color="text.secondary">
                已准备 {checkedIngredients.length}/{currentRecipe.ingredients?.length || 0}
              </Typography>
            </Box>
            
            <List sx={{ padding: 0 }}>
              {(currentRecipe.ingredients || []).map((ingredient, index) => (
                <React.Fragment key={index}>
                  <ListItem 
                    sx={{ 
                      padding: '12px 0',
                      borderRadius: 1,
                      transition: 'background-color 0.2s ease',
                      '&:hover': {
                        backgroundColor: 'rgba(76, 175, 80, 0.05)'
                      }
                    }}
                  >
                    <ListItemIcon sx={{ minWidth: 40 }}>
                      <IconButton 
                        size="small" 
                        onClick={() => handleIngredientToggle(index)}
                        sx={{ 
                          color: checkedIngredients.includes(index) ? '#4caf50' : '#bdbdbd',
                          '&:hover': {
                            backgroundColor: 'rgba(76, 175, 80, 0.1)'
                          }
                        }}
                      >
                        {checkedIngredients.includes(index) ? <CheckCircle /> : <Box sx={{ width: 20, height: 20, borderRadius: '50%', border: '2px solid #bdbdbd' }} />}
                      </IconButton>
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography 
                          variant="body1" 
                          sx={{
                            fontWeight: checkedIngredients.includes(index) ? 600 : 400,
                            textDecoration: checkedIngredients.includes(index) ? 'line-through' : 'none',
                            color: checkedIngredients.includes(index) ? '#757575' : 'inherit'
                          }}
                        >
                          {ingredient.name}
                        </Typography>
                      }
                      secondary={
                        <Typography variant="body2" color="text.secondary">
                          {ingredient.quantity} {ingredient.unit || ''}
                        </Typography>
                      }
                    />
                  </ListItem>
                  {index < (currentRecipe.ingredients?.length || 0) - 1 && (
                    <Divider sx={{ margin: '4px 0' }} />
                  )}
                </React.Fragment>
              ))}
            </List>
          </Paper>

          {/* 烹饪步骤 */}
          <Paper sx={{ 
            p: 3, 
            borderRadius: 2,
            transition: 'transform 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
            }
          }}>
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              mb: 3
            }}>
              <Typography variant="h6" sx={{ 
                fontWeight: 'bold', 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                color: '#333'
              }}>
                <Star sx={{ color: '#4caf50' }} />
                烹饪步骤
              </Typography>
              <IconButton 
                size="small"
                onClick={() => handleSectionToggle('instructions')}
              >
                {expandedSection === 'instructions' ? <ExpandLess /> : <ExpandMore />}
              </IconButton>
            </Box>
            
            <Collapse in={expandedSection === 'instructions' || expandedSection === null}>
              <Box sx={{ 
                display: 'flex',
                flexDirection: 'column',
                gap: 3
              }}>
                {(currentRecipe.instructions || []).map((step, index) => {
                  // console.log(`步骤${index + 1}:`, step); // 暂时注释掉，避免返回void
                  return (
                    <Box 
                      key={index} 
                      sx={{
                        display: 'flex',
                        gap: 2,
                        padding: 2,
                        borderRadius: 1.5,
                        backgroundColor: '#f9f9f9',
                        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                        '&:hover': {
                          transform: 'translateX(4px)',
                          boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
                        }
                      }}
                    >
                      {/* 步骤序号 */}
                      <Box sx={{
                        minWidth: 40,
                        height: 40,
                        borderRadius: '50%',
                        backgroundColor: '#4caf50',
                        color: 'white',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        fontWeight: 'bold',
                        fontSize: '1.125rem',
                        flexShrink: 0
                      }}>
                        {index + 1}
                      </Box>
                      
                      {/* 步骤内容 */}
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="body1" sx={{ 
                          fontWeight: 600, 
                          mb: 1,
                          color: '#333'
                        }}>
                          步骤 {index + 1}
                        </Typography>
                        <Typography variant="body2" color="text.primary" sx={{ lineHeight: 1.6 }}>
                          {step.trim()}
                        </Typography>
                      </Box>
                    </Box>
                  );
                })}
              </Box>
            </Collapse>
          </Paper>

          {/* 操作按钮 */}
          <Box sx={{ 
            mt: 3, 
            display: 'flex', 
            gap: 2,
            flexDirection: { xs: 'column', sm: 'row' }
          }}>
            <Button
              variant="contained"
              sx={{ 
                flexGrow: 1, 
                backgroundColor: '#4caf50',
                textTransform: 'none',
                fontWeight: 600,
                padding: '12px 24px',
                borderRadius: 2,
                '&:hover': {
                  backgroundColor: '#388e3c',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 4px 12px rgba(76, 175, 80, 0.3)'
                },
                transition: 'all 0.3s ease'
              }}
            >
              收藏
            </Button>
            <Button
              variant="outlined"
              startIcon={<Share />}
              sx={{ 
                flexGrow: 1,
                textTransform: 'none',
                fontWeight: 600,
                padding: '12px 24px',
                borderRadius: 2,
                borderColor: '#4caf50',
                color: '#4caf50',
                '&:hover': {
                  backgroundColor: 'rgba(76, 175, 80, 0.05)',
                  borderColor: '#388e3c',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 4px 12px rgba(76, 175, 80, 0.2)'
                },
                transition: 'all 0.3s ease'
              }}
            >
              分享
            </Button>
          </Box>
        </Box>
      </Box>
    </Layout>
  );
};

export default RecipeDetailPage;