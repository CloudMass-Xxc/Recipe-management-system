import { apiRequest } from './api';
import {
  RecipeGenerationRequest,
  RecipeResponse,
  RecipeEnhancementRequest,
  SaveRecipeRequest,
  AIServiceStatus
} from '../types/ai';

class AIService {
  // 获取AI服务状态
  async getServiceStatus(): Promise<AIServiceStatus> {
    return apiRequest.get<AIServiceStatus>('/ai/status');
  }

  // 生成个性化食谱
  async generateRecipe(request: RecipeGenerationRequest): Promise<RecipeResponse> {
    return apiRequest.post<RecipeResponse>('/ai/generate-recipe', request);
  }

  // 增强或修改现有食谱
  async enhanceRecipe(request: RecipeEnhancementRequest): Promise<RecipeResponse> {
    return apiRequest.post<RecipeResponse>('/ai/enhance-recipe', request);
  }

  // 保存AI生成的食谱
  async saveGeneratedRecipe(request: SaveRecipeRequest): Promise<{ success: boolean; recipe_id: string; message: string }> {
    return apiRequest.post<{ success: boolean; recipe_id: string; message: string }>('/ai/save-generated-recipe', request);
  }

  // 分析食材的营养成分
  async analyzeNutrition(ingredients: Array<{ name: string; quantity: number; unit: string }>): Promise<{
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
    fiber: number;
    summary: string;
  }> {
    return apiRequest.post<{
      calories: number;
      protein: number;
      carbs: number;
      fat: number;
      fiber: number;
      summary: string;
    }>('/ai/analyze-nutrition', ingredients);
  }
}

export default new AIService();