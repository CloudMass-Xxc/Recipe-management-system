// AI服务状态接口
export interface AIServiceStatus {
  status: 'online' | 'offline' | 'degraded';
  provider: 'openai' | 'anthropic' | 'custom';
  version: string;
  uptime: number; // 单位：秒
  error?: string;
}

// 饮食偏好枚举
export enum DietaryPreference {
  VEGETARIAN = 'vegetarian',
  VEGAN = 'vegan',
  GLUTEN_FREE = 'gluten_free',
  DAIRY_FREE = 'dairy_free',
  KETO = 'keto',
  PALEO = 'paleo',
  LOW_CARB = 'low_carb',
  HIGH_PROTEIN = 'high_protein',
  NONE = 'none'
}

// 食谱生成请求接口
export interface RecipeGenerationRequest {
  title?: string;
  dietary_preference?: DietaryPreference | DietaryPreference[];
  ingredients?: Array<{ name: string; quantity?: number; unit?: string }>;
  exclude_ingredients?: string[];
  cuisine?: string;
  meal_type?: 'breakfast' | 'lunch' | 'dinner' | 'snack' | 'dessert';
  difficulty?: 'easy' | 'medium' | 'hard';
  prep_time_max?: number;
  cook_time_max?: number;
  servings?: number;
  nutritional_goal?: {
    calories_max?: number;
    protein_min?: number;
    carbs_max?: number;
    fat_max?: number;
  };
  taste_preferences?: Array<'sweet' | 'savory' | 'spicy' | 'sour' | 'bitter'>;
  special_request?: string;
}

// 食谱增强请求接口
export interface RecipeEnhancementRequest {
  recipe_id?: string;
  original_recipe?: {
    title: string;
    description: string;
    ingredients: Array<{ name: string; quantity: number; unit: string }>;
    cooking_steps: Array<{ step_number: number; description: string }>;
    prep_time: number;
    cook_time: number;
    servings: number;
    difficulty: 'easy' | 'medium' | 'hard';
  };
  enhancement_type: 'more_healthy' | 'more_flavorful' | 'reduce_time' | 'increase_yield' | 'substitute_ingredient' | 'custom';
  substitute_from?: string;
  substitute_to?: string;
  custom_request?: string;
  dietary_preference?: DietaryPreference | DietaryPreference[];
}

// 保存生成食谱请求接口
export interface SaveRecipeRequest {
  generated_recipe: {
    title: string;
    description: string;
    ingredients: Array<{ name: string; quantity: number; unit: string; notes?: string }>;
    cooking_steps: Array<{ step_number: number; description: string; duration?: number }>;
    prep_time: number;
    cook_time: number;
    servings: number;
    difficulty: 'easy' | 'medium' | 'hard';
    cuisine?: string;
    meal_type?: 'breakfast' | 'lunch' | 'dinner' | 'snack' | 'dessert';
    nutrition_info: {
      calories: number;
      protein: number;
      carbs: number;
      fat: number;
      fiber: number;
    };
    image_url?: string;
    tags?: string[];
    equipment?: string[];
    tips?: string[];
  };
  save_as_draft?: boolean;
}

// 营养分析响应接口
export interface NutritionAnalysisResponse {
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fiber: number;
  sugar?: number;
  sodium?: number;
  summary: string;
  health_impact: {
    balanced: boolean;
    concerns: string[];
    recommendations: string[];
  };
}

// AI食谱生成状态接口
export interface RecipeGenerationStatus {
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number; // 0-100
  recipe?: RecipeResponse;
  error?: string;
}

// 从recipe.ts导入RecipeResponse类型
export type { RecipeResponse } from './recipe';