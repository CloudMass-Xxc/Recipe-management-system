import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Card, 
  CardContent, 
  CardMedia, 
  Button, 
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Divider
} from '@mui/material';
import { useNavigate } from 'react-router-dom';


interface Recipe {
  id: string;
  title: string;
  description: string;
  cookTime: string;
  difficulty: string;
  image: string;
  isVegetarian: boolean;
  isBeginnerFriendly: boolean;
}

const MyRecipesPage: React.FC = () => {
  const navigate = useNavigate();
  const [userRecipes, setUserRecipes] = useState<Recipe[]>([
    {
      id: '101',
      title: '我的私房炒面',
      description: '我自己研发的炒面配方，味道独特。',
      cookTime: '25分钟',
      difficulty: '中等',
      image: 'https://via.placeholder.com/400x300?text=我的私房炒面',
      isVegetarian: false,
      isBeginnerFriendly: false,
    },
    {
      id: '102',
      title: '创意蔬菜沙拉',
      description: '混合多种蔬菜和特制酱料的健康沙拉。',
      cookTime: '15分钟',
      difficulty: '简单',
      image: 'https://via.placeholder.com/400x300?text=创意蔬菜沙拉',
      isVegetarian: true,
      isBeginnerFriendly: true,
    },
    {
      id: '103',
      title: '香煎牛排配黑椒酱',
      description: '外焦里嫩的牛排，搭配自制黑椒酱。',
      cookTime: '35分钟',
      difficulty: '中等',
      image: 'https://via.placeholder.com/400x300?text=香煎牛排配黑椒酱',
      isVegetarian: false,
      isBeginnerFriendly: false,
    },
  ]);
  
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [editingRecipe, setEditingRecipe] = useState<Recipe | null>(null);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [deletingRecipeId, setDeletingRecipeId] = useState<string | null>(null);

  const handleRecipeClick = (recipeId: string) => {
    navigate(`/recipe/${recipeId}`);
  };

  const handleEditRecipe = (recipe: Recipe) => {
    setEditingRecipe(recipe);
    setOpenEditDialog(true);
  };

  const handleDeleteRecipe = (recipeId: string) => {
    setDeletingRecipeId(recipeId);
    setOpenDeleteDialog(true);
  };

  const confirmDeleteRecipe = () => {
    if (deletingRecipeId) {
      setUserRecipes(prevRecipes => prevRecipes.filter(recipe => recipe.id !== deletingRecipeId));
      setOpenDeleteDialog(false);
      setDeletingRecipeId(null);
    }
  };

  const handleSaveEdit = () => {
    // 保存编辑后的食谱
    if (editingRecipe) {
      setUserRecipes(prevRecipes => 
        prevRecipes.map(recipe => 
          recipe.id === editingRecipe.id ? editingRecipe : recipe
        )
      );
      setOpenEditDialog(false);
      setEditingRecipe(null);
    }
  };

  const handleBack = () => {
    navigate('/profile');
  };

  const handleCreateRecipe = () => {
    navigate('/recipe/generate');
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Button onClick={handleBack} sx={{ mr: 2 }}>
            返回
          </Button>
          <Typography variant="h4" component="h1">
            我的食谱
          </Typography>
        </Box>
        <Button 
            variant="contained" 
            onClick={handleCreateRecipe}
          >
            创建新食谱
          </Button>
      </Box>

      {userRecipes.length === 0 ? (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            您还没有创建任何食谱
          </Typography>
          <Button 
            variant="contained" 
            onClick={handleCreateRecipe}
          >
            开始创建
          </Button>
        </Box>
      ) : (
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          {userRecipes.map((recipe) => (
            <Box sx={{ width: { xs: '100%', sm: 'calc(50% - 12px)', md: 'calc(33.333% - 12px)' } }} key={recipe.id}>
              <Card 
                elevation={2} 
                sx={{ 
                  height: '100%', 
                  display: 'flex', 
                  flexDirection: 'column',
                  '&:hover': { boxShadow: 3 }
                }}
              >
                <Box sx={{ position: 'relative' }}>
                  <CardMedia
                    component="img"
                    height="180"
                    image={recipe.image}
                    alt={recipe.title}
                    sx={{ objectFit: 'cover' }}
                  />
                  <Box sx={{ position: 'absolute', bottom: 8, left: 8, display: 'flex', gap: 1 }}>
                    {recipe.isVegetarian && (
                      <Chip 
                        label="素食" 
                        size="small" 
                        sx={{ bgcolor: '#4caf50', color: 'white' }}
                      />
                    )}
                    {recipe.isBeginnerFriendly && (
                      <Chip 
                        label="适合新手" 
                        size="small" 
                        sx={{ bgcolor: '#2196f3', color: 'white' }}
                      />
                    )}
                  </Box>
                </Box>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" component="h3" gutterBottom>
                    {recipe.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {recipe.description}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                    <Chip 
                      label={recipe.cookTime} 
                      size="small" 
                      variant="outlined"
                    />
                    <Chip 
                      label={recipe.difficulty} 
                      size="small" 
                      variant="outlined"
                    />
                  </Box>
                </CardContent>
                <Box sx={{ p: 2, borderTop: '1px solid rgba(0, 0, 0, 0.1)' }}>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button 
                      variant="outlined" 
                      fullWidth
                      onClick={() => handleRecipeClick(recipe.id)}
                      sx={{ flexGrow: 1 }}
                    >
                      查看详情
                    </Button>
                    <Button 
                        variant="text" 
                        onClick={() => handleEditRecipe(recipe)}
                        sx={{ minWidth: '40px', p: 1 }}
                      >
                        编辑
                      </Button>
                      <Button 
                        variant="text" 
                        onClick={() => handleDeleteRecipe(recipe.id)}
                        sx={{ minWidth: '40px', p: 1, color: 'error.main' }}
                      >
                        删除
                      </Button>
                  </Box>
                </Box>
              </Card>
            </Box>
          ))}
        </Box>
      )}

      {/* 编辑食谱对话框 */}
      <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)}>
        <DialogTitle>编辑食谱</DialogTitle>
        <DialogContent>
          {editingRecipe && (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <TextField
                label="食谱名称"
                value={editingRecipe.title}
                onChange={(e) => setEditingRecipe({ ...editingRecipe, title: e.target.value })}
                fullWidth
              />
              <TextField
                label="描述"
                value={editingRecipe.description}
                onChange={(e) => setEditingRecipe({ ...editingRecipe, description: e.target.value })}
                fullWidth
                multiline
                rows={3}
              />
              <Divider />
              <Typography variant="subtitle2">食谱标签</Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip
                  label="素食"
                  onClick={() => setEditingRecipe({ ...editingRecipe, isVegetarian: !editingRecipe.isVegetarian })}
                  color={editingRecipe.isVegetarian ? "success" : "default"}
                  variant={editingRecipe.isVegetarian ? "filled" : "outlined"}
                />
                <Chip
                  label="适合新手"
                  onClick={() => setEditingRecipe({ ...editingRecipe, isBeginnerFriendly: !editingRecipe.isBeginnerFriendly })}
                  color={editingRecipe.isBeginnerFriendly ? "primary" : "default"}
                  variant={editingRecipe.isBeginnerFriendly ? "filled" : "outlined"}
                />
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditDialog(false)}>取消</Button>
          <Button onClick={handleSaveEdit} variant="contained">保存</Button>
        </DialogActions>
      </Dialog>

      {/* 删除确认对话框 */}
      <Dialog open={openDeleteDialog} onClose={() => setOpenDeleteDialog(false)}>
        <DialogTitle>确认删除</DialogTitle>
        <DialogContent>
          <Typography>确定要删除这个食谱吗？此操作无法撤销。</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDeleteDialog(false)}>取消</Button>
          <Button onClick={confirmDeleteRecipe} color="error">删除</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default MyRecipesPage;