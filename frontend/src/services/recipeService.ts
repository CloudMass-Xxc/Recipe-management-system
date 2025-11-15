import { apiRequest } from './api';
import {
  RecipeCreate,
  RecipeUpdate,
  RecipeResponse,
  RecipeListItem,
  RecipeSearchParams,
  RatingCreate,
  RatingResponse
} from '../types/recipe';

class RecipeService {
  // 创建食谱
  async createRecipe(recipeData: RecipeCreate): Promise<RecipeResponse> {
    return apiRequest.post<RecipeResponse>('/recipes', recipeData);
  }

  // 获取食谱列表
  async getRecipes(params?: RecipeSearchParams): Promise<RecipeListItem[]> {
    return apiRequest.get<RecipeListItem[]>('/recipes', { params });
  }

  // 获取单个食谱详情
  async getRecipeById(recipeId: string): Promise<RecipeResponse> {
    return apiRequest.get<RecipeResponse>(`/recipes/${recipeId}`);
  }

  // 更新食谱
  async updateRecipe(recipeId: string, recipeData: RecipeUpdate): Promise<RecipeResponse> {
    return apiRequest.put<RecipeResponse>(`/recipes/${recipeId}`, recipeData);
  }

  // 删除食谱
  async deleteRecipe(recipeId: string): Promise<void> {
    return apiRequest.delete<void>(`/recipes/${recipeId}`);
  }

  // 收藏食谱
  async favoriteRecipe(recipeId: string): Promise<{ user_id: string; recipe_id: string }> {
    return apiRequest.post<{ user_id: string; recipe_id: string }>(`/recipes/${recipeId}/favorite`);
  }

  // 取消收藏
  async unfavoriteRecipe(recipeId: string): Promise<void> {
    return apiRequest.delete<void>(`/recipes/${recipeId}/favorite`);
  }

  // 评分食谱
  async rateRecipe(recipeId: string, ratingData: RatingCreate): Promise<RatingResponse> {
    return apiRequest.post<RatingResponse>(`/recipes/${recipeId}/rating`, ratingData);
  }

  // 获取食谱评分
  async getRecipeRatings(recipeId: string, skip: number = 0, limit: number = 20): Promise<RatingResponse[]> {
    return apiRequest.get<RatingResponse[]>(`/recipes/${recipeId}/ratings`, {
      params: { skip, limit }
    });
  }

  // 获取用户收藏的食谱
  async getUserFavorites(skip: number = 0, limit: number = 20): Promise<RecipeListItem[]> {
    return apiRequest.get<RecipeListItem[]>('/recipes/user/favorites', {
      params: { skip, limit }
    });
  }

  // 搜索食谱
  async searchRecipes(searchParams: RecipeSearchParams): Promise<RecipeListItem[]> {
    return apiRequest.get<RecipeListItem[]>('/recipes', { params: searchParams });
  }

  // 获取用户创建的食谱
  async getUserRecipes(userId: string, skip: number = 0, limit: number = 20): Promise<RecipeListItem[]> {
    return apiRequest.get<RecipeListItem[]>('/recipes', {
      params: { author_id: userId, skip, limit }
    });
  }
}

export default new RecipeService();