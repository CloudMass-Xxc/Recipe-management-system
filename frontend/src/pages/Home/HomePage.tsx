import React, { useMemo } from 'react';
import { Box, Typography, Button, Card } from '@mui/material';
import { LocalFireDepartment as RecipeIcon, Search, Favorite as HeartIcon, Event as CalendarIcon, ArrowRight, TrendingUp, Shield, Group as UsersIcon, Star } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import Layout from '../../components/layout/Layout';
import RecipeCard from '../../components/recipe/RecipeCard/RecipeCard';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  // 快速操作按钮数据 - 使用useMemo缓存
  const quickActions = useMemo(() => [
    { title: '生成食谱', icon: <RecipeIcon />, path: '/recipe-generate', color: '#4caf50', bgColor: '#e8f5e8' },
    { title: '浏览食谱', icon: <Search />, path: '/recipe-list', color: '#2196f3', bgColor: '#e3f2fd' },
    { title: '我的收藏', icon: <HeartIcon />, path: '/favorites', color: '#f44336', bgColor: '#ffebee' },
    { title: '饮食计划', icon: <CalendarIcon />, path: '/diet-plan', color: '#ff9800', bgColor: '#fff3e0' },
  ], []);

  // 推荐食谱数据 - 固定存储在前端，包含完整详细信息 - 使用useMemo缓存
  const recommendedRecipes = useMemo(() => [
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
        '加入2杯热水或热牛奶，搅拌均匀',
        '静置2-3分钟，让燕麦片充分吸收水分',
        '根据个人口味添加蜂蜜、水果或坚果',
        '搅拌均匀即可享用'
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
      image_url: 'https://images.unsplash.com/photo-1511690656952-34342bb7c2f5?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
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
  ], []);

  // 系统优势数据 - 使用useMemo缓存
  const systemAdvantages = useMemo(() => [
    {
      icon: <RecipeIcon />,
      title: '智能食谱生成',
      description: '基于AI算法，根据您的食材、偏好和健康需求，智能生成个性化食谱',
      color: '#4caf50'
    },
    {
      icon: <Search />,
      title: '丰富的食谱库',
      description: '拥有超过10,000+种食谱，涵盖各种菜系和饮食需求',
      color: '#2196f3'
    },
    {
      icon: <CalendarIcon />,
      title: '个性化饮食计划',
      description: '制定个性化饮食计划，帮助您实现健康目标',
      color: '#ff9800'
    },
    {
      icon: <Shield />,
      title: '健康饮食管理',
      description: '提供营养成分分析，帮助您更好地管理饮食健康',
      color: '#9c27b0'
    },
    {
      icon: <HeartIcon />,
      title: '收藏与分享',
      description: '收藏喜爱的食谱，与朋友分享您的烹饪成果',
      color: '#f44336'
    },
    {
      icon: <UsersIcon />,
      title: '社区互动',
      description: '加入烹饪社区，交流经验，发现更多美食灵感',
      color: '#00bcd4'
    }
  ], []);

  // 系统统计数据 - 使用useMemo缓存
  const stats = useMemo(() => [
    { label: '食谱数量', value: '10,000+', icon: <RecipeIcon />, color: '#4caf50' },
    { label: '活跃用户', value: '50,000+', icon: <UsersIcon />, color: '#2196f3' },
    { label: '每日生成', value: '1,000+', icon: <TrendingUp />, color: '#ff9800' },
    { label: '五星评价', value: '98%', icon: <Star />, color: '#f44336' },
  ], []);

  return (
    <Layout>
      {/* 顶部横幅 */}
      <Box sx={{
        width: '100%',
        mb: 8,
        p: { xs: 3, md: 8 },
        borderRadius: 4,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        boxShadow: '0 8px 32px rgba(102, 126, 234, 0.4)',
        overflow: 'hidden',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        minHeight: { xs: '300px', md: '450px' },
      }}>
        {/* 装饰元素 */}
        <Box sx={{
          position: 'absolute',
          top: '-50%',
          right: '-10%',
          width: '80%',
          height: '200%',
          backgroundColor: 'rgba(255,255,255,0.1)',
          borderRadius: '50%',
          zIndex: 0,
        }} />
        <Box sx={{
          position: 'absolute',
          bottom: '-30%',
          left: '-10%',
          width: '60%',
          height: '150%',
          backgroundColor: 'rgba(255,255,255,0.05)',
          borderRadius: '50%',
          zIndex: 0,
        }} />

        {/* 内容 */}
        <Box sx={{ position: 'relative', zIndex: 1, maxWidth: '800px', mx: 'auto', width: '100%' }}>
          <Typography variant="h2" sx={{ 
            fontWeight: 800, 
            mb: 3,
            fontSize: { xs: '1.75rem', sm: '2.25rem', md: '3rem' },
            lineHeight: 1.2,
            wordWrap: 'break-word',
          }}>
            发现您的专属食谱
          </Typography>
          <Typography variant="h6" sx={{ 
            mb: 5,
            fontSize: { xs: '1rem', md: '1.25rem' },
            opacity: 0.95,
            maxWidth: { md: '60%' },
            lineHeight: 1.6,
          }}>
            根据您的食材、饮食偏好和健康需求，智能生成个性化食谱，让烹饪变得简单又有趣
          </Typography>
          <Box sx={{ 
            display: 'flex', 
            gap: 3, 
            flexWrap: 'wrap',
            '& > button': {
              borderRadius: 3,
              textTransform: 'none',
              fontWeight: 600,
              padding: { xs: '10px 24px', md: '14px 32px' },
              fontSize: { xs: '0.9rem', md: '1rem' },
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            }
          }}>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/recipe-generate')}
              sx={{
                backgroundColor: 'white',
                color: '#667eea',
                '&:hover': {
                  backgroundColor: '#f5f5f5',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 6px 16px rgba(0,0,0,0.2)',
                },
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              }}
            >
              立即开始生成
            </Button>
            <Button
              variant="outlined"
              size="large"
              onClick={() => navigate('/recipe-list')}
              sx={{
                borderColor: 'white',
                color: 'white',
                borderWidth: 2,
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.1)',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 6px 16px rgba(0,0,0,0.2)',
                },
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              }}
            >
              浏览食谱库
            </Button>
          </Box>
        </Box>
      </Box>

      {/* 快速操作区域 */}
      <Box sx={{ mb: 10 }}>
        <Typography variant="h4" sx={{ 
          fontWeight: 700, 
          mb: 5,
          color: '#333',
          fontSize: { xs: '1.75rem', md: '2.5rem' },
          textAlign: 'center',
        }}>
          快速操作
        </Typography>
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: {
            xs: 'repeat(2, 1fr)',
            sm: 'repeat(4, 1fr)'
          },
          gap: { xs: 2, sm: 4 }
        }}>
          {quickActions.map((action, index) => (
            <Card
            key={index}
            onClick={() => navigate(action.path)}
            sx={{
              height: { xs: '120px', sm: '160px' },
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              gap: 1.5,
              backgroundColor: action.bgColor,
              borderRadius: 3,
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
              '&:hover': {
                transform: 'translateY(-8px)',
                boxShadow: '0 12px 32px rgba(0,0,0,0.2)',
              },
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              cursor: 'pointer',
              border: `1px solid ${action.color}20`,
            }}
            >
              <Box sx={{ 
                fontSize: '2.5rem', 
                color: action.color,
                transition: 'transform 0.3s ease',
                '&:hover': {
                  transform: 'scale(1.1)',
                }
              }}>
                {action.icon}
              </Box>
              <Typography variant="body1" sx={{ 
                color: action.color,
                fontWeight: 600,
                fontSize: { xs: '0.9rem', md: '1rem' }
              }}>
                {action.title}
              </Typography>
            </Card>
          ))}
        </Box>
      </Box>

      {/* 推荐食谱区域 */}
      <Box sx={{ mb: 10 }}>
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          mb: 5, 
          flexWrap: 'wrap', 
          gap: 2
        }}>
          <Typography variant="h4" sx={{ 
            fontWeight: 700, 
            color: '#333',
            fontSize: { xs: '1.75rem', md: '2.5rem' }
          }}>
            推荐食谱
          </Typography>
          <Button
            variant="contained"
            onClick={() => navigate('/recipe-list')}
            endIcon={<ArrowRight />}
            sx={{
              backgroundColor: '#667eea',
              color: 'white',
              borderRadius: 3,
              textTransform: 'none',
              fontWeight: 600,
              padding: '10px 24px',
              fontSize: { xs: '0.875rem', md: '1rem' },
              boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)',
              '&:hover': {
                backgroundColor: '#5a6fd8',
                transform: 'translateY(-2px)',
                boxShadow: '0 6px 16px rgba(102, 126, 234, 0.4)',
              },
              transition: 'all 0.3s ease',
            }}
          >
            查看全部
          </Button>
        </Box>
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: {
            xs: '1fr',
            sm: 'repeat(2, 1fr)',
            lg: 'repeat(4, 1fr)' 
          },
          gap: { xs: 2, sm: 4 }
        }}>
          {recommendedRecipes.map((recipe) => (
            <RecipeCard 
              key={recipe.recipe_id} 
              recipe={{
                ...recipe,
                author_id: 'system',
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString(),
                author_name: '系统推荐'
              }} 
            />
          ))}
        </Box>
      </Box>

      {/* 系统优势区域 */}
      <Box sx={{ 
        mb: 10, 
        p: { xs: 4, md: 10 }, 
        borderRadius: 4, 
        backgroundColor: '#f8f9fa',
        position: 'relative',
        overflow: 'hidden',
      }}>
        {/* 背景装饰 */}
        <Box sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundImage: 'radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(76, 175, 80, 0.1) 0%, transparent 50%)',
          zIndex: 0,
        }} />
        
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Typography variant="h4" sx={{ 
            fontWeight: 700, 
            mb: 8,
            textAlign: 'center',
            color: '#333',
            fontSize: { xs: '1.75rem', md: '2.5rem' }
          }}>
            为什么选择我们
          </Typography>
          <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: {
            xs: 'repeat(1, 1fr)',
            sm: 'repeat(2, 1fr)',
            lg: 'repeat(3, 1fr)'
          },
          gap: { xs: 3, sm: 5 }
        }}>
            {systemAdvantages.map((advantage, index) => (
              <Card key={index} sx={{ 
                p: 3,
                borderRadius: 3,
                boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                backgroundColor: 'white',
                '&:hover': {
                  transform: 'translateY(-5px)',
                  boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
                },
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                border: `1px solid ${advantage.color}15`,
              }}>
                <Box sx={{ 
                  width: { xs: '60px', sm: '70px' }, 
                  height: { xs: '60px', sm: '70px' }, 
                  marginBottom: { xs: '1rem', sm: '1.5rem' }, 
                  borderRadius: '50%', 
                  backgroundColor: `${advantage.color}15`, 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  fontSize: { xs: '1.5rem', sm: '2rem' },
                  color: advantage.color,
                }}>
                  {advantage.icon}
                </Box>
                <Typography variant="h6" sx={{ 
                  fontWeight: 700, 
                  mb: 1.5, 
                  color: '#333' 
                }}>
                  {advantage.title}
                </Typography>
                <Typography variant="body2" sx={{ 
                  color: '#666',
                  lineHeight: 1.6,
                }}>
                  {advantage.description}
                </Typography>
              </Card>
            ))}
          </Box>
        </Box>
      </Box>

      {/* 系统统计区域 */}
      <Box sx={{ mb: 10 }}>
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: {
            xs: 'repeat(2, 1fr)',
            md: 'repeat(4, 1fr)'
          },
          gap: { xs: 2, sm: 4 }
        }}>
          {stats.map((stat, index) => (
            <Card key={index} sx={{ 
              p: 3, 
              borderRadius: 3,
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
              textAlign: 'center',
              backgroundColor: 'white',
              borderTop: `4px solid ${stat.color}`,
              '&:hover': {
                transform: 'translateY(-5px)',
                boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
              },
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            }}>
              <Box sx={{ 
                fontSize: '2rem', 
                color: stat.color,
                mb: 1.5,
              }}>
                {stat.icon}
              </Box>
              <Typography variant="h3" sx={{ 
                fontWeight: 800, 
                color: stat.color,
                mb: 0.5,
                fontSize: { xs: '1.75rem', md: '2.5rem' }
              }}>
                {stat.value}
              </Typography>
              <Typography variant="body1" sx={{ 
                color: '#666', 
                fontWeight: 600,
                fontSize: { xs: '0.9rem', md: '1rem' }
              }}>
                {stat.label}
              </Typography>
            </Card>
          ))}
        </Box>
      </Box>

      {/* 行动召唤区域 */}
      <Box sx={{
        p: { xs: 5, md: 12 },
        borderRadius: 4,
        background: 'linear-gradient(135deg, #4caf50 0%, #388e3c 100%)',
        color: 'white',
        textAlign: 'center',
        boxShadow: '0 8px 32px rgba(76, 175, 80, 0.4)',
        position: 'relative',
        overflow: 'hidden',
        mb: 4,
      }}>
        {/* 背景装饰 */}
        <Box sx={{
          position: 'absolute',
          top: '-50%',
          right: '-20%',
          width: '80%',
          height: '200%',
          backgroundColor: 'rgba(255,255,255,0.1)',
          borderRadius: '50%',
        }} />
        <Box sx={{
          position: 'absolute',
          bottom: '-30%',
          left: '-10%',
          width: '60%',
          height: '150%',
          backgroundColor: 'rgba(255,255,255,0.05)',
          borderRadius: '50%',
        }} />
        
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Typography variant="h4" sx={{ 
            fontWeight: 700, 
            mb: 2,
            fontSize: { xs: '1.75rem', md: '2.5rem' }
          }}>
            准备好开始您的烹饪之旅了吗？
          </Typography>
          <Typography variant="body1" sx={{ 
            mb: 4,
            fontSize: { xs: '1rem', md: '1.25rem' },
            opacity: 0.95,
            maxWidth: { md: '60%' },
            mx: 'auto',
            lineHeight: 1.6,
          }}>
            加入我们，发现更多美味食谱，让烹饪变得简单又有趣
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/recipe-generate')}
            sx={{
              backgroundColor: 'white',
              color: '#4caf50',
              borderRadius: 3,
              textTransform: 'none',
              fontWeight: 700,
              padding: { xs: '12px 32px', md: '14px 40px' },
              fontSize: { xs: '1rem', md: '1.125rem' },
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
              '&:hover': {
                backgroundColor: '#f5f5f5',
                transform: 'translateY(-3px)',
                boxShadow: '0 8px 24px rgba(0,0,0,0.2)',
              },
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            }}
          >
            立即开始
          </Button>
        </Box>
      </Box>
    </Layout>
  );
};

// 使用React.memo避免不必要的重新渲染
export default React.memo(HomePage);
