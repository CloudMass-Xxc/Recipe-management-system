import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import RecipeAPI from '../../services/recipeAPI';

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

// 获取食谱列表，支持筛选参数
export const fetchRecipes = createAsyncThunk(
  'recipes/fetchRecipes',
  async (filters?: {
    vegetarian?: boolean;
    beginner_friendly?: boolean;
    difficulty?: string;
    search?: string;
  }) => {
    const recipes = await RecipeAPI.getRecipes(filters);
    return recipes;
  }
);

// 获取食谱详情
export const fetchRecipeDetail = createAsyncThunk(
  'recipes/fetchRecipeDetail',
  async (recipeId: string) => {
    const recipe = await RecipeAPI.getRecipeById(recipeId);
    return recipe;
  }
);

// 生成个性化食谱
export const generatePersonalizedRecipe = createAsyncThunk(
  'recipes/generatePersonalized',
  async (params: {
    dietary_preferences?: string[];
    food_likes?: string[];
    food_dislikes?: string[];
    health_conditions?: string[];
    nutrition_goals?: string[];
    cooking_time_limit?: number;
    difficulty?: string;
    cuisine?: string;
  }) => {
    const recipe = await RecipeAPI.generateRecipe(params);
    return recipe;
  }
);

// 添加到收藏
export const addToFavorites = createAsyncThunk(
  'recipes/addToFavorites',
  async (recipeId: string) => {
    await RecipeAPI.addToFavorites(recipeId);
    return recipeId;
  }
);

// 从收藏中移除
export const removeFromFavorites = createAsyncThunk(
  'recipes/removeFromFavorites',
  async (recipeId: string) => {
    await RecipeAPI.removeFromFavorites(recipeId);
    return recipeId;
  }
);

// 获取收藏的食谱
export const fetchFavoriteRecipes = createAsyncThunk(
  'recipes/fetchFavoriteRecipes',
  async () => {
    const recipes = await RecipeAPI.getFavoriteRecipes();
    return recipes;
  }
);

// 获取用户的食谱
export const fetchUserRecipes = createAsyncThunk(
  'recipes/fetchUserRecipes',
  async () => {
    const recipes = await RecipeAPI.getUserRecipes();
    return recipes;
  }
);

const recipeSlice = createSlice({
  name: 'recipes',
  initialState,
  reducers: {
    clearCurrentRecipe: (state) => {
      state.currentRecipe = null;
    },
    clearError: (state) => {
      state.error = null;
    },
    setFavorites: (state, action: PayloadAction<string[]>) => {
      state.favorites = action.payload;
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
        state.currentRecipe = action.payload;
      })
      .addCase(fetchRecipeDetail.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || '获取食谱详情失败';
      })
      // 生成个性化食谱
      .addCase(generatePersonalizedRecipe.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(generatePersonalizedRecipe.fulfilled, (state, action: PayloadAction<RecipeDetail>) => {
        state.isLoading = false;
        state.currentRecipe = action.payload;
      })
      .addCase(generatePersonalizedRecipe.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || '生成个性化食谱失败';
      })
      // 添加到收藏
      .addCase(addToFavorites.fulfilled, (state, action: PayloadAction<string>) => {
        const recipeId = action.payload;
        if (!state.favorites.includes(recipeId)) {
          state.favorites.push(recipeId);
        }
        if (state.currentRecipe?.id === recipeId) {
          state.currentRecipe.isFavorite = true;
        }
      })
      // 从收藏中移除
      .addCase(removeFromFavorites.fulfilled, (state, action: PayloadAction<string>) => {
        const recipeId = action.payload;
        const index = state.favorites.indexOf(recipeId);
        if (index > -1) {
          state.favorites.splice(index, 1);
        }
        if (state.currentRecipe?.id === recipeId) {
          state.currentRecipe.isFavorite = false;
        }
      })
      // 获取收藏的食谱
      .addCase(fetchFavoriteRecipes.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchFavoriteRecipes.fulfilled, (state, action: PayloadAction<Recipe[]>) => {
        state.isLoading = false;
        state.recipes = action.payload;
      })
      .addCase(fetchFavoriteRecipes.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || '获取收藏食谱失败';
      })
      // 获取用户的食谱
      .addCase(fetchUserRecipes.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchUserRecipes.fulfilled, (state, action: PayloadAction<Recipe[]>) => {
        state.isLoading = false;
        state.recipes = action.payload;
      })
      .addCase(fetchUserRecipes.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || '获取用户食谱失败';
      });
  },
});

export const { clearCurrentRecipe, clearError, setFavorites } = recipeSlice.actions;
export default recipeSlice.reducer;