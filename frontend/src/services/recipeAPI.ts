// import api from './api'; // 暂时注释，使用模拟数据

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
  ingredients: string[];
  dietaryRestrictions?: string[];
  cuisineType?: string;
  cookTime?: string;
  difficulty?: string;
}

class RecipeAPI {
  // 获取食谱列表
  static async getRecipes(filter?: RecipeFilter): Promise<Recipe[]> {
    try {
      // 模拟食谱数据
      const mockRecipes: Recipe[] = [
        {
          id: '1',
          title: '健康蔬菜炒饭',
          description: '营养丰富的蔬菜炒饭，适合素食者。',
          cookTime: '20分钟',
          difficulty: '简单',
          image: 'https://via.placeholder.com/400x300?text=健康蔬菜炒饭',
          isVegetarian: true,
          isBeginnerFriendly: true,
        },
        {
          id: '2',
          title: '香煎三文鱼',
          description: '美味的香煎三文鱼配时蔬。',
          cookTime: '30分钟',
          difficulty: '中等',
          image: 'https://via.placeholder.com/400x300?text=香煎三文鱼',
          isVegetarian: false,
          isBeginnerFriendly: false,
        },
        {
          id: '3',
          title: '番茄鸡蛋面',
          description: '经典的家常菜，简单又美味。',
          cookTime: '15分钟',
          difficulty: '简单',
          image: 'https://via.placeholder.com/400x300?text=番茄鸡蛋面',
          isVegetarian: false,
          isBeginnerFriendly: true,
        },
        {
          id: '4',
          title: '素食沙拉',
          description: '新鲜的蔬菜沙拉，健康又清爽。',
          cookTime: '10分钟',
          difficulty: '简单',
          image: 'https://via.placeholder.com/400x300?text=素食沙拉',
          isVegetarian: true,
          isBeginnerFriendly: true,
        },
      ];

      // 应用过滤条件
      let filteredRecipes = [...mockRecipes];
      
      if (filter) {
        if (filter.isVegetarian !== undefined) {
          filteredRecipes = filteredRecipes.filter(r => r.isVegetarian === filter.isVegetarian);
        }
        if (filter.isBeginnerFriendly !== undefined) {
          filteredRecipes = filteredRecipes.filter(r => r.isBeginnerFriendly === filter.isBeginnerFriendly);
        }
        if (filter.difficulty) {
          filteredRecipes = filteredRecipes.filter(r => r.difficulty === filter.difficulty);
        }
        if (filter.searchTerm) {
          const searchLower = filter.searchTerm.toLowerCase();
          filteredRecipes = filteredRecipes.filter(r => 
            r.title.toLowerCase().includes(searchLower) || 
            r.description.toLowerCase().includes(searchLower)
          );
        }
      }

      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 500));
      
      return filteredRecipes;
    } catch (error) {
      console.error('获取食谱列表失败:', error);
      throw error;
    }
  }

  // 获取食谱详情
  static async getRecipeById(recipeId: string): Promise<RecipeDetail> {
    try {
      // 模拟食谱详情数据
      const mockRecipeDetail: RecipeDetail = {
        id: recipeId,
        title: '健康蔬菜炒饭',
        description: '这是一道营养丰富的蔬菜炒饭，使用新鲜蔬菜和优质大米制作。',
        ingredients: [
          '大米 1碗',
          '胡萝卜 1根',
          '青豆 50g',
          '玉米粒 50g',
          '鸡蛋 2个',
          '葱 2根',
          '盐 适量',
          '生抽 1勺',
          '食用油 2勺'
        ],
        instructions: [
          '将胡萝卜洗净切丁，葱切末备用。',
          '热锅下油，炒香葱花。',
          '加入胡萝卜丁炒至变色。',
          '打入鸡蛋，快速翻炒成小块。',
          '加入米饭，用中火翻炒均匀。',
          '加入青豆和玉米粒，继续翻炒。',
          '加入生抽和盐调味，翻炒均匀即可出锅。'
        ],
        cookTime: '20分钟',
        difficulty: '简单',
        servings: 2,
        calories: 350,
        image: 'https://via.placeholder.com/800x500?text=健康蔬菜炒饭',
        tags: ['素食', '快手菜', '家常菜'],
        isFavorite: false,
        isVegetarian: true,
        isBeginnerFriendly: true,
      };

      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 300));
      
      return mockRecipeDetail;
    } catch (error) {
      console.error(`获取食谱详情失败 (ID: ${recipeId}):`, error);
      throw error;
    }
  }

  // 生成食谱
  static async generateRecipe(params: RecipeGenerateParams): Promise<RecipeDetail> {
    try {
      // 模拟生成的食谱数据
      const mockGeneratedRecipe: RecipeDetail = {
        id: Date.now().toString(),
        title: '定制食谱 - ' + (params.ingredients?.join('、') || '家常菜'),
        description: '根据您的需求生成的个性化食谱。',
        ingredients: params.ingredients || ['米饭', '鸡蛋', '蔬菜'],
        instructions: [
          '准备所有食材。',
          '按照步骤烹饪。',
          '完成后享用美食。'
        ],
        cookTime: params.cookTime || '25分钟',
        difficulty: params.difficulty || '中等',
        servings: 2,
        calories: 400,
        image: 'https://via.placeholder.com/800x500?text=Generated+Recipe',
        tags: params.dietaryRestrictions || [],
        isFavorite: false,
        isVegetarian: params.dietaryRestrictions?.includes('vegetarian') || false,
        isBeginnerFriendly: params.difficulty === '简单',
      };

      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      return mockGeneratedRecipe;
    } catch (error) {
      console.error('生成食谱失败:', error);
      throw error;
    }
  }

  // 添加到收藏
  static async addToFavorites(recipeId: string): Promise<void> {
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 300));
      console.log(`添加收藏成功: ${recipeId}`);
    } catch (error) {
      console.error(`添加收藏失败 (ID: ${recipeId}):`, error);
      throw error;
    }
  }

  // 移除收藏
  static async removeFromFavorites(recipeId: string): Promise<void> {
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 300));
      console.log(`移除收藏成功: ${recipeId}`);
    } catch (error) {
      console.error(`移除收藏失败 (ID: ${recipeId}):`, error);
      throw error;
    }
  }

  // 获取用户收藏的食谱
  static async getFavoriteRecipes(): Promise<Recipe[]> {
    try {
      // 模拟收藏的食谱数据
      const mockFavorites: Recipe[] = [
        {
          id: '1',
          title: '健康蔬菜炒饭',
          description: '营养丰富的蔬菜炒饭，适合素食者。',
          cookTime: '20分钟',
          difficulty: '简单',
          image: 'https://via.placeholder.com/400x300?text=健康蔬菜炒饭',
          isVegetarian: true,
          isBeginnerFriendly: true,
        },
        {
          id: '3',
          title: '番茄鸡蛋面',
          description: '经典的家常菜，简单又美味。',
          cookTime: '15分钟',
          difficulty: '简单',
          image: 'https://via.placeholder.com/400x300?text=番茄鸡蛋面',
          isVegetarian: false,
          isBeginnerFriendly: true,
        },
      ];

      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 500));
      
      return mockFavorites;
    } catch (error) {
      console.error('获取收藏食谱失败:', error);
      throw error;
    }
  }

  // 获取用户创建的食谱
  static async getUserRecipes(): Promise<Recipe[]> {
    try {
      // 模拟用户创建的食谱数据
      const mockUserRecipes: Recipe[] = [
        {
          id: '101',
          title: '我的私房炒面',
          description: '我自己研发的炒面配方，味道独特。',
          cookTime: '25分钟',
          difficulty: '中等',
          image: 'https://via.placeholder.com/400x300?text=我的私房炒面',
          isVegetarian: false,
          isBeginnerFriendly: false,
        },
        {
          id: '102',
          title: '创意蔬菜沙拉',
          description: '混合多种蔬菜和特制酱料的健康沙拉。',
          cookTime: '15分钟',
          difficulty: '简单',
          image: 'https://via.placeholder.com/400x300?text=创意蔬菜沙拉',
          isVegetarian: true,
          isBeginnerFriendly: true,
        },
      ];

      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 500));
      
      return mockUserRecipes;
    } catch (error) {
      console.error('获取用户食谱失败:', error);
      throw error;
    }
  }
}

export default RecipeAPI;