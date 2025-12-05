// 营养信息类型
export interface NutritionInfoBase {
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fiber?: number;
  sugar?: number;
  sodium?: number;
  additional_nutrients?: Record<string, any>;
}

// 营养信息响应类型
export interface NutritionInfoResponse extends NutritionInfoBase {
  nutrition_id: number;
  recipe_id: string;
}

// 简化的食材信息（用于食谱创建）
export interface SimpleIngredient {
  name: string;
  quantity: number;
  unit?: string;
}

// 食谱配料响应类型
export interface RecipeIngredient {
  recipe_ingredient_id?: number;
  recipe_id: string;
  ingredient_id: number;
  ingredient_name?: string;
  quantity: number;
  unit?: string;
  note?: string;
}

// 食谱基础类型
export interface RecipeBase {
  title: string;
  description?: string;
  cooking_time: number;
  servings: number;
  difficulty: string;
  ingredients?: SimpleIngredient[];
  tags?: string[];
  image_url?: string;
}

// 食谱创建类型
export interface RecipeCreate extends RecipeBase {
  instructions: string[];
  nutrition_info?: NutritionInfoBase;
}

// 食谱更新类型
export interface RecipeUpdate {
  title?: string;
  description?: string;
  instructions?: string[];
  cooking_time?: number;
  servings?: number;
  difficulty?: string;
  ingredients?: SimpleIngredient[];
  tags?: string[];
  image_url?: string;
  nutrition_info?: NutritionInfoBase;
}

// 食谱响应类型
export interface Recipe {
  recipe_id: string;
  title: string;
  description?: string;
  instructions: string[];
  cooking_time: number;
  servings: number;
  difficulty: string;
  cuisine?: string;
  tags?: string[];
  image_url?: string;
  nutrition_info?: NutritionInfoResponse;
  author_id: string;
  author_name?: string;
  created_at: string;
  updated_at: string;
  ingredients?: SimpleIngredient[];
  rating?: number;
}

// 食谱列表项类型（简化版）
export interface RecipeListItem {
  recipe_id: string;
  title: string;
  description?: string;
  cuisine?: string;
  cooking_time: number;
  difficulty: string;
  created_at: string;
  image_url?: string;
  author_name?: string;
  tags?: string[];
  rating?: number;
}

// 食谱生成请求类型
export interface RecipeGenerateRequest {
  ingredients: string[];
  restrictions: string[];
  preferences?: {
    cooking_time?: string;
    difficulty?: string;
    flavor?: string;
  };
}

// 食谱生成响应类型
export interface RecipeGenerateResponse {
  recipes: Recipe[];
}

// 食谱列表响应类型
export interface RecipeListResponse {
  recipes: RecipeListItem[];
  page: number;
  limit: number;
  total: number;
}

// 食谱搜索参数类型
export interface RecipeSearchParams {
  query?: string;
  tags?: string[];
  difficulty?: string;
  max_cooking_time?: number;
  ingredients_include?: string[];
  ingredients_exclude?: string[];
}

// 食谱搜索响应类型
export interface RecipeSearchResponse {
  total: number;
  recipes: Recipe[];
}



// 评分创建类型
export interface RatingCreate {
  score: number;
  comment?: string;
  recipe_id?: string;
}

// 评分响应类型
export interface RatingResponse {
  rating_id: number;
  user_id: string;
  recipe_id: string;
  score: number;
  comment?: string;
  user_name?: string;
  created_at: string;
}

// 收藏响应类型
export interface FavoriteResponse {
  favorite_id: number;
  user_id: string;
  recipe_id: string;
  recipe: RecipeListItem;
  created_at: string;
}

// 收藏状态响应类型
export interface FavoriteStatusResponse {
  is_favorite: boolean;
}

// 用户收藏列表响应类型
export interface UserFavoritesResponse {
  recipes: RecipeListItem[];
  page: number;
  limit: number;
  total: number;
}
