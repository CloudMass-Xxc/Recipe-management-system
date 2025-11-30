
import type { Recipe, RecipeCreate, RecipeUpdate, RecipeGenerateRequest, RecipeListResponse, RecipeSearchResponse, RatingCreate, RecipeListItem } from '../types/recipe';
import api from './api';

// 添加简单的缓存机制，避免重复请求
interface CacheItem {
  data: any;
  timestamp: number;
  expiry: number;
}

class RequestCache {
  private cache = new Map<string, CacheItem>();
  private defaultExpiry = 30000; // 默认30秒过期

  // 获取缓存项
  get(key: string): any | null {
    const item = this.cache.get(key);
    if (!item) return null;

    // 检查是否过期
    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }

    return item.data;
  }

  // 设置缓存项
  set(key: string, data: any, expiryMs?: number): void {
    const expiry = Date.now() + (expiryMs || this.defaultExpiry);
    this.cache.set(key, { data, timestamp: Date.now(), expiry });
  }

  // 删除缓存项
  delete(key: string): void {
    this.cache.delete(key);
  }

  // 清除所有缓存
  clear(): void {
    this.cache.clear();
  }

  // 生成缓存键
  generateKey(prefix: string, ...args: any[]): string {
    return `${prefix}:${JSON.stringify(args)}`;
  }
}

// 创建全局缓存实例
const cache = new RequestCache();

export const recipeService = {
  async generateRecipes(params: RecipeGenerateRequest): Promise<{ recipes: Recipe[] }> {
    try {
      // 调用真实的后端API
      const response = await api.post<Recipe>('/ai/generate-recipe', params);
      
      // 直接返回完整的Recipe对象，不进行转换
      return {
        recipes: [response.data]
      };
    } catch (error: any) {
      console.error('生成食谱失败:', error);
      throw error;
    }
  },

  async createRecipe(recipeData: RecipeCreate): Promise<Recipe> {
    // 创建新食谱
    try {
      const response = await api.post<Recipe>('/recipes', recipeData);
      return response.data;
    } catch (error) {
      console.error('创建食谱失败:', error);
      throw error;
    }
  },

  async getRecipes(page: number = 1, limit: number = 20, tags?: string[]): Promise<RecipeListResponse> {
    try {
      // 生成缓存键
      const cacheKey = cache.generateKey('recipes', page, limit, tags);
      
      // 检查缓存
      const cachedData = cache.get(cacheKey);
      if (cachedData) {
        console.log('使用缓存的食谱列表数据');
        return cachedData;
      }
      
      // 从后端API获取真实的公共食谱列表
      const params: Record<string, any> = { page, limit };
      if (tags && tags.length > 0) params.tags = tags;
      
      console.log('发送食谱列表请求:', params);
      
      // 添加请求超时设置，避免请求挂起
      const timeoutPromise = new Promise<RecipeListResponse>((_, reject) => {
        setTimeout(() => {
          reject(new Error('请求超时: 后端API响应时间超过30秒'));
        }, 30000); // 30秒超时
      });
      
      // 使用Promise.race来实现超时控制
      const response = await Promise.race([
        api.get<RecipeListResponse>('/recipes/', { params }),
        timeoutPromise
      ]) as any;
      
      // 添加数据验证，确保返回的数据结构符合预期
      if (!response?.data || !Array.isArray(response.data.recipes)) {
        console.error('获取食谱列表失败: 返回数据结构不符合预期', response?.data);
        // 返回默认的空列表，避免前端崩溃
        const defaultResult = {
          recipes: [],
          page: 1,
          limit: limit,
          total: 0
        };
        cache.set(cacheKey, defaultResult, 5000); // 错误结果缓存5秒
        return defaultResult;
      }
      
      // 缓存成功的响应
      cache.set(cacheKey, response.data);
      return response.data;
    } catch (error: any) {
      console.error('获取食谱列表失败:', error);
      
      // 发生错误时返回默认的空列表，避免前端崩溃
      const defaultResult = {
        recipes: [],
        page: 1,
        limit: limit,
        total: 0
      };
      return defaultResult;
    }
  },

  async getUserRecipes(): Promise<RecipeListResponse> {
    // 获取当前用户的食谱列表
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
  },

  async getRecipeDetail(recipeId: string): Promise<Recipe> {
    // 获取食谱详情
    try {
      // 生成缓存键
      const cacheKey = cache.generateKey('recipeDetail', recipeId);
      
      // 检查缓存
      const cachedData = cache.get(cacheKey);
      if (cachedData) {
        console.log('使用缓存的食谱详情数据:', recipeId);
        return cachedData;
      }
      
      console.log('发送食谱详情请求:', recipeId);
      
      const response = await api.get<Recipe>(`/recipes/${recipeId}`);
      
      // 确保instructions是数组类型 - 使用类型断言解决TypeScript编译错误
      if (response.data.instructions) {
        if (Array.isArray(response.data.instructions)) {
          // 如果已经是数组，确保每个元素都是字符串并过滤空元素
          response.data.instructions = response.data.instructions
            .filter((step: any) => typeof step === 'string' && step.trim())
            .map((step: string) => step.trim());
        } else if (typeof response.data.instructions === 'string') {
          // 如果是字符串，按换行符分割成数组
          // 使用类型断言告诉TypeScript这是一个字符串
          const instructionsStr = response.data.instructions as string;
          response.data.instructions = instructionsStr.split('\n').filter((step: string) => step.trim());
        } else {
          // 如果是其他类型，转换为空数组
          response.data.instructions = [];
        }
      } else {
        // 如果instructions不存在，设置为空数组
        response.data.instructions = [];
      }
      
      // 缓存成功的响应
      cache.set(cacheKey, response.data);
      return response.data;
    } catch (error) {
      console.error('获取食谱详情失败:', error);
      throw error;
    }
  },

  async updateRecipe(recipeId: string, recipeData: RecipeUpdate): Promise<Recipe> {
    // 更新食谱
    try {
      const response = await api.put<Recipe>(`/recipes/${recipeId}`, recipeData);
      return response.data;
    } catch (error) {
      console.error('更新食谱失败:', error);
      throw error;
    }
  },

  async deleteRecipe(recipeId: string): Promise<void> {
    // 删除食谱
    try {
      await api.delete(`/recipes/${recipeId}`);
    } catch (error) {
      console.error('删除食谱失败:', error);
      throw error;
    }
  },

  async searchRecipes(query?: string, cooking_time?: number, difficulty?: string, page: number = 1, limit: number = 20): Promise<RecipeSearchResponse> {
    // 搜索食谱
    try {
      const params: Record<string, any> = { skip: (page - 1) * limit, limit };
      if (query) params.query = query;
      if (cooking_time) params.max_cooking_time = cooking_time;
      if (difficulty) params.difficulty = difficulty;
      
      const response = await api.get<RecipeListItem[]>('/recipes', { params });
      return {
        total: response.data.length,
        recipes: response.data as unknown as Recipe[]
      };
    } catch (error) {
      console.error('搜索食谱失败:', error);
      throw error;
    }
  },

  async favoriteRecipe(recipeId: string): Promise<void> {
    // 收藏食谱
    try {
      await api.post(`/recipes/${recipeId}/favorite`);
    } catch (error) {
      console.error('收藏食谱失败:', error);
      throw error;
    }
  },

  async unfavoriteRecipe(recipeId: string): Promise<void> {
    // 取消收藏食谱
    try {
      await api.delete(`/recipes/${recipeId}/favorite`);
    } catch (error) {
      console.error('取消收藏食谱失败:', error);
      throw error;
    }
  },

  async rateRecipe(recipeId: string, ratingData: RatingCreate): Promise<void> {
    // 评分食谱
    try {
      await api.post(`/recipes/${recipeId}/rating`, ratingData);
    } catch (error) {
      console.error('评分食谱失败:', error);
      throw error;
    }
  },

  async getRecipeRatings(recipeId: string, page: number = 1, limit: number = 20): Promise<any> {
    // 获取食谱评分列表
    try {
      const params = { skip: (page - 1) * limit, limit };
      const response = await api.get(`/recipes/${recipeId}/ratings`, { params });
      return response.data;
    } catch (error) {
      console.error('获取食谱评分失败:', error);
      throw error;
    }
  }
};
