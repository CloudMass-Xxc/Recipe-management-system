import api from './api';

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

interface RecipeFilter {
  isVegetarian?: boolean;
  isBeginnerFriendly?: boolean;
  difficulty?: string;
  searchTerm?: string;
}

interface RecipeGenerateParams {
  dietary_preferences?: string[];
  food_likes?: string[];
  food_dislikes?: string[];
  health_conditions?: string[];
  nutrition_goals?: string[];
  cooking_time_limit?: number;
  difficulty?: string;
  cuisine?: string;
}

const PLACEHOLDER_IMG = (title: string) =>
  `https://via.placeholder.com/400x300?text=${encodeURIComponent(title)}`;

const formatCookTime = (minutes?: number) =>
  typeof minutes === 'number' && minutes > 0 ? `${minutes}分钟` : '未知';

const formatIngredient = (ingredient: any): string => {
  if (!ingredient) return '未指定食材';
  const name = ingredient.name || ingredient.ingredient_name || '未命名食材';
  const quantity = ingredient.quantity ?? ingredient.amount;
  const unit = ingredient.unit || '';
  const note = ingredient.note || '';
  const quantityText = quantity ? `${quantity}${unit}` : '';
  return [name, quantityText, note].filter(Boolean).join(' ');
};

const formatInstructions = (instructions?: string[] | string): string[] => {
  if (!instructions) return [];
  if (Array.isArray(instructions)) {
    return instructions.filter((step) => !!step && step.trim().length > 0);
  }
  return instructions
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
};

const normalizeRecipeSummary = (recipe: any): Recipe => {
  const id = recipe.recipe_id || recipe.id;
  const title = recipe.title || '未命名食谱';
  const tags: string[] = recipe.tags || [];
  return {
    id,
    title,
    description: recipe.description || '',
    cookTime: formatCookTime(recipe.cooking_time),
    difficulty: recipe.difficulty || 'unknown',
    image: recipe.image_url || recipe.image || PLACEHOLDER_IMG(title),
    isVegetarian: recipe.is_vegetarian ?? tags.includes('素食'),
    isBeginnerFriendly:
      recipe.is_beginner_friendly ??
      (tags.includes('新手') ||
       recipe.difficulty === 'easy' ||
       recipe.difficulty === '简单'),
  };
};

const normalizeRecipeDetail = (recipe: any): RecipeDetail => {
  const summary = normalizeRecipeSummary(recipe);
  const nutrition = recipe.nutrition_info || {};
  const ingredientsSource = recipe.ingredients || [];
  return {
    ...summary,
    ingredients: ingredientsSource.map((item: any) => formatIngredient(item)),
    instructions: formatInstructions(recipe.instructions),
    servings: recipe.servings || recipe.serving || 1,
    calories: nutrition.calories || recipe.calories || 0,
    tags: recipe.tags || [],
    isFavorite: recipe.is_favorite || false,
  };
};

class RecipeAPI {
  // 获取食谱列表
  static async getRecipes(filter?: RecipeFilter): Promise<Recipe[]> {
    try {
      // 构建查询参数
      const params: Record<string, unknown> = {};

      if (filter) {
        if (filter.isVegetarian === true) {
          params.tags = '素食';
        }
        if (filter.isBeginnerFriendly === true) {
          params.difficulty = 'easy';
        }
        if (filter.difficulty) {
          params.difficulty = filter.difficulty;
        }
        if (filter.searchTerm) {
          params.query = filter.searchTerm;
        }
      }

      const response = await api.get('/recipes', { params });
      return Array.isArray(response) ? response.map(normalizeRecipeSummary) : [];
    } catch (error) {
      console.error('获取食谱列表失败:', error);
      throw error;
    }
  }

  // 获取食谱详情
  static async getRecipeById(recipeId: string): Promise<RecipeDetail> {
    try {
      const response = await api.get(`/recipes/${recipeId}`);
      return normalizeRecipeDetail(response);
    } catch (error) {
      console.error(`获取食谱详情失败 (ID: ${recipeId}):`, error);
      throw error;
    }
  }

  // 生成食谱
  static async generateRecipe(params: RecipeGenerateParams = {}): Promise<RecipeDetail> {
    try {
      const payload = {
        dietary_preferences: params.dietary_preferences || [],
        food_likes: params.food_likes || [],
        food_dislikes: params.food_dislikes || [],
        health_conditions: params.health_conditions || [],
        nutrition_goals: params.nutrition_goals || [],
        cooking_time_limit: params.cooking_time_limit,
        difficulty: params.difficulty,
        cuisine: params.cuisine,
      };

      const response = await api.post('/ai/generate-recipe', payload);
      return normalizeRecipeDetail(response);
    } catch (error) {
      console.error('生成食谱失败:', error);
      throw error;
    }
  }

  // 添加到收藏
  static async addToFavorites(recipeId: string): Promise<void> {
    try {
      await api.post(`/recipes/${recipeId}/favorite`);
    } catch (error) {
      console.error(`添加收藏失败 (ID: ${recipeId}):`, error);
      throw error;
    }
  }

  // 移除收藏
  static async removeFromFavorites(recipeId: string): Promise<void> {
    try {
      await api.delete(`/recipes/${recipeId}/favorite`);
    } catch (error) {
      console.error(`移除收藏失败 (ID: ${recipeId}):`, error);
      throw error;
    }
  }

  // 获取用户收藏的食谱
  static async getFavoriteRecipes(): Promise<Recipe[]> {
    try {
      const response = await api.get('/recipes/user/favorites');
      return Array.isArray(response) ? response.map((recipe: any) => normalizeRecipeSummary(recipe.recipe || recipe)) : [];
    } catch (error) {
      console.error('获取收藏食谱失败:', error);
      throw error;
    }
  }

  // 获取用户创建的食谱
  static async getUserRecipes(): Promise<Recipe[]> {
    try {
      const response = await api.get('/recipes/user');
      return Array.isArray(response) ? response.map(normalizeRecipeSummary) : [];
    } catch (error) {
      console.error('获取用户食谱失败:', error);
      throw error;
    }
  }
}

// 导出类
export default RecipeAPI;

// 导出静态方法作为模块函数
export const getRecipes = RecipeAPI.getRecipes;
export const getRecipeById = RecipeAPI.getRecipeById;
export const generateRecipe = RecipeAPI.generateRecipe;
export const addToFavorites = RecipeAPI.addToFavorites;
export const removeFromFavorites = RecipeAPI.removeFromFavorites;
export const getFavoriteRecipes = RecipeAPI.getFavoriteRecipes;
export const getUserRecipes = RecipeAPI.getUserRecipes;