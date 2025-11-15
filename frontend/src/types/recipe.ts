// 营养信息接口
export interface NutritionInfo {
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fiber: number;
  sugar?: number;
  sodium?: number;
}

// 食谱配料接口
export interface Ingredient {
  id?: string;
  name: string;
  quantity: number;
  unit: string;
  notes?: string;
}

// 烹饪步骤接口
export interface CookingStep {
  id?: string;
  step_number: number;
  description: string;
  duration?: number; // 单位：分钟
}

// 食谱创建请求接口
export interface RecipeCreate {
  title: string;
  description: string;
  ingredients: Ingredient[];
  cooking_steps: CookingStep[];
  prep_time: number;
  cook_time: number;
  servings: number;
  difficulty: 'easy' | 'medium' | 'hard';
  cuisine?: string;
  meal_type?: 'breakfast' | 'lunch' | 'dinner' | 'snack' | 'dessert';
  nutrition_info: NutritionInfo;
  image_url?: string;
  tags?: string[];
  equipment?: string[];
  tips?: string[];
}

// 食谱更新请求接口
export interface RecipeUpdate {
  title?: string;
  description?: string;
  ingredients?: Ingredient[];
  cooking_steps?: CookingStep[];
  prep_time?: number;
  cook_time?: number;
  servings?: number;
  difficulty?: 'easy' | 'medium' | 'hard';
  cuisine?: string;
  meal_type?: 'breakfast' | 'lunch' | 'dinner' | 'snack' | 'dessert';
  nutrition_info?: NutritionInfo;
  image_url?: string;
  tags?: string[];
  equipment?: string[];
  tips?: string[];
}

// 食谱响应接口
export interface RecipeResponse {
  id: string;
  title: string;
  description: string;
  ingredients: Ingredient[];
  cooking_steps: CookingStep[];
  prep_time: number;
  cook_time: number;
  servings: number;
  difficulty: 'easy' | 'medium' | 'hard';
  cuisine?: string;
  meal_type?: 'breakfast' | 'lunch' | 'dinner' | 'snack' | 'dessert';
  nutrition_info: NutritionInfo;
  image_url?: string;
  tags?: string[];
  equipment?: string[];
  tips?: string[];
  created_at: string;
  updated_at: string;
  author: {
    id: string;
    username: string;
    first_name?: string;
    last_name?: string;
  };
  rating: number;
  total_ratings: number;
  is_favorite?: boolean;
  user_rating?: number;
}

// 食谱列表项接口
export interface RecipeListItem {
  id: string;
  title: string;
  description: string;
  image_url?: string;
  prep_time: number;
  cook_time: number;
  servings: number;
  difficulty: 'easy' | 'medium' | 'hard';
  rating: number;
  total_ratings: number;
  average_rating?: number;
  created_at: string;
  favorited_at?: string;
  author: {
    id: string;
    username: string;
  };
  is_favorite?: boolean;
  tags?: string[];
}

// 食谱搜索参数接口
export interface RecipeSearchParams {
  query?: string;
  tags?: string[];
  difficulty?: 'easy' | 'medium' | 'hard';
  meal_type?: 'breakfast' | 'lunch' | 'dinner' | 'snack' | 'dessert';
  cuisine?: string;
  max_prep_time?: number;
  max_cook_time?: number;
  min_rating?: number;
  author_id?: string;
  skip?: number;
  limit?: number;
  sort_by?: 'created_at' | 'rating' | 'prep_time' | 'cook_time';
  sort_order?: 'asc' | 'desc';
}

// 评分创建请求接口
export interface RatingCreate {
  score: number; // 1-5星
  comment?: string;
}

// 评分响应接口
export interface RatingResponse {
  id: string;
  user: {
    id: string;
    username: string;
  };
  recipe_id: string;
  score: number;
  comment?: string;
  created_at: string;
  updated_at: string;
}

// 收藏响应接口
export interface FavoriteResponse {
  user_id: string;
  recipe_id: string;
  created_at: string;
}

// 食谱详情页面状态接口
export interface RecipeDetailState {
  recipe: RecipeResponse | null;
  isLoading: boolean;
  error: string | null;
  isFavorite: boolean;
  userRating: number | null;
}