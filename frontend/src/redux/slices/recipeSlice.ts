import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

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

interface RecipeDetail extends Recipe {
  ingredients: string[];
  instructions: string[];
  servings: number;
  calories: number;
  tags: string[];
  isFavorite: boolean;
}

interface RecipeState {
  recipes: Recipe[];
  currentRecipe: RecipeDetail | null;
  isLoading: boolean;
  error: string | null;
  favorites: string[];
}

const initialState: RecipeState = {
  recipes: [],
  currentRecipe: null,
  isLoading: false,
  error: null,
  favorites: [],
};

// 模拟获取食谱列表
export const fetchRecipes = createAsyncThunk(
  'recipes/fetchRecipes',
  async () => {
    return new Promise<Recipe[]>((resolve) => {
      setTimeout(() => {
        resolve([
          {
            id: '1',
            title: '健康蔬菜炒饭',
            description: '营养丰富的蔬菜炒饭，适合素食者。',
            cookTime: '20分钟',
            difficulty: '简单',
            image: 'https://via.placeholder.com/400x300?text=健康蔬菜炒饭',
            isVegetarian: true,
            isBeginnerFriendly: true,
          },
          {
            id: '2',
            title: '香煎三文鱼',
            description: '美味的香煎三文鱼配时蔬。',
            cookTime: '30分钟',
            difficulty: '中等',
            image: 'https://via.placeholder.com/400x300?text=香煎三文鱼',
            isVegetarian: false,
            isBeginnerFriendly: false,
          },
          {
            id: '3',
            title: '番茄鸡蛋面',
            description: '经典的家常菜，简单又美味。',
            cookTime: '15分钟',
            difficulty: '简单',
            image: 'https://via.placeholder.com/400x300?text=番茄鸡蛋面',
            isVegetarian: false,
            isBeginnerFriendly: true,
          },
          {
            id: '4',
            title: '素食沙拉',
            description: '新鲜的蔬菜沙拉，健康又清爽。',
            cookTime: '10分钟',
            difficulty: '简单',
            image: 'https://via.placeholder.com/400x300?text=素食沙拉',
            isVegetarian: true,
            isBeginnerFriendly: true,
          },
        ]);
      }, 800);
    });
  }
);

// 模拟获取食谱详情
export const fetchRecipeDetail = createAsyncThunk(
  'recipes/fetchRecipeDetail',
  async (recipeId: string) => {
    return new Promise<RecipeDetail>((resolve) => {
      setTimeout(() => {
        resolve({
          id: recipeId,
          title: '健康蔬菜炒饭',
          description: '这是一道营养丰富的蔬菜炒饭，使用新鲜蔬菜和优质大米制作。',
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
          image: 'https://via.placeholder.com/800x500?text=健康蔬菜炒饭',
          tags: ['素食', '快手菜', '家常菜'],
          isFavorite: false,
          isVegetarian: true,
          isBeginnerFriendly: true,
        });
      }, 500);
    });
  }
);

const recipeSlice = createSlice({
  name: 'recipes',
  initialState,
  reducers: {
    toggleFavorite: (state, action: PayloadAction<string>) => {
      const recipeId = action.payload;
      const index = state.favorites.indexOf(recipeId);
      if (index > -1) {
        state.favorites.splice(index, 1);
      } else {
        state.favorites.push(recipeId);
      }
      
      // 更新当前食谱的收藏状态
      if (state.currentRecipe?.id === recipeId) {
        state.currentRecipe.isFavorite = !state.currentRecipe.isFavorite;
      }
    },
    clearCurrentRecipe: (state) => {
      state.currentRecipe = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // 获取食谱列表
      .addCase(fetchRecipes.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchRecipes.fulfilled, (state, action: PayloadAction<Recipe[]>) => {
        state.isLoading = false;
        state.recipes = action.payload;
      })
      .addCase(fetchRecipes.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || '获取食谱列表失败';
      })
      // 获取食谱详情
      .addCase(fetchRecipeDetail.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchRecipeDetail.fulfilled, (state, action: PayloadAction<RecipeDetail>) => {
        state.isLoading = false;
        // 检查是否在收藏列表中
        const isFavorite = state.favorites.includes(action.payload.id);
        state.currentRecipe = { ...action.payload, isFavorite };
      })
      .addCase(fetchRecipeDetail.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || '获取食谱详情失败';
      });
  },
});

export const { toggleFavorite, clearCurrentRecipe, clearError } = recipeSlice.actions;
export default recipeSlice.reducer;