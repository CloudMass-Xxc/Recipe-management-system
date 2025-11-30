import type { NutritionData, IngredientNutrition } from '../types/nutrition';
import api from './api';

export const nutritionService = {
  async calculateNutrition(ingredients: Array<{ name: string; amount: number; unit: string }>): Promise<NutritionData> {
    // 调用后端API计算营养信息
    try {
      const response = await api.post<NutritionData>('/nutrition/calculate', { ingredients });
      return response.data;
    } catch (error) {
      console.error('计算营养信息失败:', error);
      throw error;
    }
  },

  async getIngredientNutrition(ingredient: string, amount: number, unit: string): Promise<IngredientNutrition> {
    // 调用后端API获取单个食材的营养信息
    try {
      const response = await api.get<IngredientNutrition>('/nutrition/ingredient', {
        params: { name: ingredient, amount, unit }
      });
      return response.data;
    } catch (error) {
      console.error('获取食材营养信息失败:', error);
      throw error;
    }
  },

  async searchIngredients(query: string): Promise<Array<{ name: string }>> {
    // 搜索食材
    try {
      const response = await api.get<Array<{ name: string }>>('/nutrition/ingredients/search', {
        params: { query }
      });
      return response.data;
    } catch (error) {
      console.error('搜索食材失败:', error);
      throw error;
    }
  },

  async getNutritionInfo(recipeId: string): Promise<NutritionData> {
    // 获取食谱的营养信息
    try {
      const response = await api.get<NutritionData>(`/recipes/${recipeId}/nutrition`);
      return response.data;
    } catch (error) {
      console.error('获取食谱营养信息失败:', error);
      throw error;
    }
  }
};
