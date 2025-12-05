import type { Recipe, RecipeCreate, RecipeUpdate, RecipeGenerateRequest, RecipeListResponse, RecipeSearchResponse, RatingCreate, RecipeListItem } from '../types/recipe';
import api from './api';

// 简化的食谱服务，只包含收藏相关的方法
export const recipeService = {
  // 收藏相关方法
  async addFavorite(recipeId: string): Promise<any> {
    try {
      const response = await api.post(`/recipes/${recipeId}/favorite`);
      return response.data;
    } catch (error) {
      console.error('添加收藏失败:', error);
      throw error;
    }
  },

  async removeFavorite(recipeId: string): Promise<void> {
    try {
      await api.delete(`/recipes/${recipeId}/favorite`);
    } catch (error) {
      console.error('取消收藏失败:', error);
      throw error;
    }
  },

  async isFavorite(recipeId: string): Promise<boolean> {
    try {
      const response = await api.get(`/recipes/${recipeId}/favorite`);
      return response.data.is_favorite;
    } catch (error) {
      console.error('检查收藏状态失败:', error);
      return false;
    }
  },

  async getUserFavorites(page: number = 1, limit: number = 20, params: Record<string, any> = {}): Promise<any> {
    try {
      const requestParams = { 
        page, 
        limit, 
        ...params 
      };
      const response = await api.get('/users/favorites', { params: requestParams });
      return response.data;
    } catch (error) {
      console.error('获取用户收藏列表失败:', error);
      throw error;
    }
  },

  // 其他必要的方法
  async getRecipeDetail(recipeId: string): Promise<Recipe> {
    try {
      const response = await api.get<Recipe>(`/recipes/${recipeId}`);
      return response.data;
    } catch (error) {
      console.error('获取食谱详情失败:', error);
      throw error;
    }
  },

  async getRecipes(page: number = 1, limit: number = 20, tags?: string[]): Promise<RecipeListResponse> {
    try {
      const params: Record<string, any> = { page, limit };
      if (tags && tags.length > 0) params.tags = tags;
      const response = await api.get<RecipeListResponse>('/recipes/', { params });
      return response.data;
    } catch (error: any) {
      console.error('获取食谱列表失败:', error);
      return {
        recipes: [],
        page: 1,
        limit: limit,
        total: 0
      };
    }
  },

  async generateRecipes(params: RecipeGenerateRequest): Promise<{ recipes: Recipe[] }> {
    try {
      // 转换前端参数为后端期望的格式
      const backendParams = {
        dietary_preferences: params.restrictions,
        food_likes: [], // 前端没有这个字段，暂时留空
        food_dislikes: [], // 前端没有这个字段，暂时留空
        health_conditions: [], // 前端没有这个字段，暂时留空
        nutrition_goals: [], // 前端没有这个字段，暂时留空
        cooking_time_limit: params.preferences?.cooking_time ? parseInt(params.preferences.cooking_time) : undefined,
        difficulty: params.preferences?.difficulty === '简单' ? 'easy' : 
                   params.preferences?.difficulty === '中等' ? 'medium' : 
                   params.preferences?.difficulty === '困难' ? 'hard' : undefined,
        cuisine: 'none', // 前端没有这个字段，暂时设为none
        ingredients: params.ingredients
      };
      
      console.log('发送到后端的参数:', backendParams);
      const response = await api.post<Recipe>('/ai/generate-recipe', backendParams);
      return {
        recipes: [response.data]
      };
    } catch (error: any) {
      console.error('生成食谱失败:', error);
      console.error('错误详情:', error.response?.data || error.message);
      throw error;
    }
  },

  async createRecipe(recipeData: RecipeCreate): Promise<Recipe> {
    try {
      const response = await api.post<Recipe>('/recipes', recipeData);
      return response.data;
    } catch (error) {
      console.error('创建食谱失败:', error);
      throw error;
    }
  },

  async updateRecipe(recipeId: string, recipeData: RecipeUpdate): Promise<Recipe> {
    try {
      const response = await api.put<Recipe>(`/recipes/${recipeId}`, recipeData);
      return response.data;
    } catch (error) {
      console.error('更新食谱失败:', error);
      throw error;
    }
  },

  async deleteRecipe(recipeId: string): Promise<void> {
    try {
      await api.delete(`/recipes/${recipeId}`);
    } catch (error) {
      console.error('删除食谱失败:', error);
      throw error;
    }
  },

  async searchRecipes(query?: string, cooking_time?: number, difficulty?: string, page: number = 1, limit: number = 20): Promise<RecipeSearchResponse> {
    try {
      const params: Record<string, any> = { page, limit };
      if (query) params.query = query;
      if (cooking_time) params.max_cooking_time = cooking_time;
      if (difficulty) params.difficulty = difficulty;
      
      const response = await api.get<RecipeListResponse>('/recipes', { params });
      return {
        total: response.data.total,
        recipes: response.data.recipes as unknown as Recipe[]
      };
    } catch (error) {
      console.error('搜索食谱失败:', error);
      throw error;
    }
  },

  async rateRecipe(recipeId: string, ratingData: RatingCreate): Promise<void> {
    try {
      await api.post(`/recipes/${recipeId}/rating`, ratingData);
    } catch (error) {
      console.error('评分食谱失败:', error);
      throw error;
    }
  },

  async getRecipeRatings(recipeId: string, page: number = 1, limit: number = 20): Promise<any> {
    try {
      const params = { skip: (page - 1) * limit, limit };
      const response = await api.get(`/recipes/${recipeId}/ratings`, { params });
      return response.data;
    } catch (error) {
      console.error('获取食谱评分失败:', error);
      throw error;
    }
  },

  async getUserRecipes(): Promise<RecipeListResponse> {
    try {
      const response = await api.get<RecipeListItem[]>('/recipes/user');
      return {
        recipes: response.data,
        page: 1,
        limit: response.data.length,
        total: response.data.length
      };
    } catch (error) {
      console.error('获取用户食谱列表失败:', error);
      throw error;
    }
  }
};