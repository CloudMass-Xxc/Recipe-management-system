// 食谱生成请求类型
export interface RecipeGenerationRequest {
  food_likes: string[];
  food_dislikes: string[];
  dietary_preferences: string[];
  health_conditions: string[];
  nutrition_goals: string[];
  cooking_time_limit: number;
  difficulty: string;
  cuisine: string;
}

// 食谱响应类型
export interface RecipeResponse {
  title: string;
  description?: string;
  ingredients: string[];
  instructions: string[];
  cooking_time: number;
  preparation_time: number;
  difficulty: string;
  nutritional_info?: {
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
  };
  tips?: string[];
  servings?: number;
}

// 食谱基本信息类型
export interface Recipe {
  id: string;
  title: string;
  description?: string;
  cookTime: string;
  difficulty: string;
  image?: string;
  isVegetarian?: boolean;
  isBeginnerFriendly?: boolean;
  ingredients?: string[];
  instructions?: string[];
  servings?: number;
  calories?: number;
  tags?: string[];
  isFavorite?: boolean;
}
