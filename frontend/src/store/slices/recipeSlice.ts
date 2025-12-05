import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import { recipeService } from '../../services/recipe.service';
import type { Recipe, RecipeGenerateRequest, RecipeListResponse, RecipeListItem, RatingCreate } from '../../types/recipe';

// 防抖函数实现（暂时注释，因为当前未使用）
/*
function debounce<T extends (...args: any[]) => any>(func: T, wait: number) {
  let timeout: ReturnType<typeof setTimeout> | null = null;
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}
*/

// 创建请求追踪器，避免在短时间内发送相同的请求
// 使用单例模式确保在StrictMode下只存在一个实例
class RequestTracker {
  private static instance: RequestTracker;
  private pendingRequests = new Map<string, Promise<any>>();
  private requestHistory = new Map<string, number>();
  private minRequestInterval = 1000; // 最小请求间隔（毫秒）
  
  private constructor() {
    // 私有构造函数确保只能通过getInstance方法创建实例
  }
  
  public static getInstance(): RequestTracker {
    if (!RequestTracker.instance) {
      RequestTracker.instance = new RequestTracker();
    }
    return RequestTracker.instance;
  }

  // 生成请求键 - 更稳定的实现，确保相同参数生成相同的键
  private generateKey(actionType: string, payload: any): string {
    // 处理特殊情况
    if (payload === undefined || payload === null) {
      return `${actionType}:${payload}`;
    }
    
    // 为fetchRecipes生成更稳定的键
    if (actionType === 'recipes/fetch' && typeof payload === 'object') {
      const { page = 1, limit = 10, tags = [] } = payload;
      // 对tags数组排序以确保相同标签集合生成相同的键
      const sortedTags = [...tags].sort();
      return `${actionType}:page=${page}:limit=${limit}:tags=[${sortedTags.join(',')}]`;
    }
    
    // 为fetchRecipeDetail生成简单的键
    if (actionType === 'recipes/fetchDetail') {
      return `${actionType}:${payload}`;
    }
    
    // 通用情况，尝试稳定的JSON序列化
    try {
      if (typeof payload === 'object') {
        // 对对象的键进行排序，确保相同内容生成相同的字符串
        const sortedPayload = Object.keys(payload).sort().reduce((obj: any, key) => {
          obj[key] = payload[key];
          return obj;
        }, {});
        return `${actionType}:${JSON.stringify(sortedPayload)}`;
      }
      return `${actionType}:${JSON.stringify(payload)}`;
    } catch (error) {
      // 如果JSON序列化失败，使用简单的字符串表示
      return `${actionType}:${String(payload)}`;
    }
  }

  // 检查是否应该发送请求（基于时间间隔）
  shouldSendRequest(actionType: string, payload: any): boolean {
    const key = this.generateKey(actionType, payload);
    const lastRequestTime = this.requestHistory.get(key) || 0;
    const currentTime = Date.now();
    
    if (currentTime - lastRequestTime < this.minRequestInterval) {
      return false;
    }
    
    // 只有在决定发送请求时才更新时间戳
    this.requestHistory.set(key, currentTime);
    return true;
  }

  // 存储挂起的请求
  setPendingRequest(actionType: string, payload: any, promise: Promise<any>): void {
    const key = this.generateKey(actionType, payload);
    this.pendingRequests.set(key, promise);
    
    // 请求完成后清理
    promise.finally(() => {
      this.pendingRequests.delete(key);
    });
  }

  // 获取挂起的请求
  getPendingRequest(actionType: string, payload: any): Promise<any> | undefined {
    const key = this.generateKey(actionType, payload);
    return this.pendingRequests.get(key);
  }
}

// 获取请求追踪器实例（单例模式）
const requestTracker = RequestTracker.getInstance();

interface RecipeState {
  generatedRecipes: Recipe[];
  recipeList: RecipeListItem[];
  currentRecipe: Recipe | null;
  loading: boolean;
  error: string | null;
  pagination: { page: number; limit: number; total: number };
}

const initialState: RecipeState = {
  generatedRecipes: [],
  recipeList: [],
  currentRecipe: null,
  loading: false,
  error: null,
  pagination: { page: 1, limit: 10, total: 0 }
};

export const generateRecipes = createAsyncThunk(
  'recipes/generate',
  async (params: RecipeGenerateRequest, { rejectWithValue }) => {
    try {
      const response = await recipeService.generateRecipes(params);
      // 返回完整的Recipe对象数组
      return response.recipes;
    } catch (error: any) {
      console.error('生成食谱失败:', error);
      return rejectWithValue(error.response?.data || error.message || '生成食谱失败');
    }
  }
);

// 添加一个简单的内存缓存，用于存储最近的请求结果
// 使用全局变量确保在StrictMode下只存在一个缓存实例
let recentRequests: Map<string, { timestamp: number; result: any }> = new Map();
let CACHE_DURATION = 2000; // 缓存持续时间（毫秒）

// 初始化缓存（确保在StrictMode下只初始化一次）
if (typeof window !== 'undefined' && !window.__RECIPE_CACHE_INITIALIZED__) {
  recentRequests = new Map();
  window.__RECIPE_CACHE_INITIALIZED__ = true;
}

// 扩展Window接口以避免TypeScript错误
declare global {
  interface Window {
    __RECIPE_CACHE_INITIALIZED__?: boolean;
  }
}

export const fetchRecipes = createAsyncThunk(
  'recipes/fetch',
  async (params: { page?: number; limit?: number; tags?: string[] }, { rejectWithValue }) => {
    try {
      const { page = 1, limit = 10, tags = [] } = params;
      
      // 生成缓存键
      const sortedTags = [...tags].sort();
      const cacheKey = `fetchRecipes:page=${page}:limit=${limit}:tags=[${sortedTags.join(',')}]`;
      
      // 检查是否有缓存的结果
      const cached = recentRequests.get(cacheKey);
      const now = Date.now();
      
      if (cached && (now - cached.timestamp) < CACHE_DURATION) {
        console.log('使用缓存的食谱列表数据');
        return cached.result;
      }
      
      // 检查是否应该发送请求或是否已有挂起的相同请求
      const pendingRequest = requestTracker.getPendingRequest('recipes/fetch', params);
      
      if (pendingRequest) {
        // 如果已有相同的挂起请求，直接返回该请求
        console.log('使用挂起的食谱列表请求');
        return await pendingRequest;
      }
      
      if (!requestTracker.shouldSendRequest('recipes/fetch', params)) {
        // 如果请求太频繁，抛出错误或返回空数据
        console.log('请求过于频繁，拒绝发送食谱列表请求');
        return rejectWithValue('Request too frequent');
      }
      
      console.log('发送新的食谱列表请求:', params);
      
      // 发送新请求并跟踪
      const responsePromise = recipeService.getRecipes(params.page, params.limit, params.tags);
      requestTracker.setPendingRequest('recipes/fetch', params, responsePromise);
      
      const response = await responsePromise;
      
      // 缓存结果
      recentRequests.set(cacheKey, { timestamp: now, result: response });
      
      return response;
    } catch (error: any) {
      console.error('获取食谱列表失败:', error);
      return rejectWithValue(error.response?.data?.detail || '获取食谱失败');
    }
  }
);

export const fetchRecipeDetail = createAsyncThunk(
  'recipes/fetchDetail',
  async (recipeId: string, { rejectWithValue }) => {
    try {
      // 生成缓存键
      const cacheKey = `fetchRecipeDetail:${recipeId}`;
      
      // 检查是否有缓存的结果
      const cached = recentRequests.get(cacheKey);
      const now = Date.now();
      
      if (cached && (now - cached.timestamp) < CACHE_DURATION) {
        console.log('使用缓存的食谱详情数据:', recipeId);
        return cached.result;
      }
      
      // 检查是否应该发送请求或是否已有挂起的相同请求
      const pendingRequest = requestTracker.getPendingRequest('recipes/fetchDetail', recipeId);
      
      if (pendingRequest) {
        // 如果已有相同的挂起请求，直接返回该请求的结果
        console.log('使用挂起的食谱详情请求:', recipeId);
        return await pendingRequest;
      }
      
      if (!requestTracker.shouldSendRequest('recipes/fetchDetail', recipeId)) {
        // 如果请求太频繁，抛出错误或返回空数据
        console.log('请求过于频繁，拒绝发送食谱详情请求:', recipeId);
        return rejectWithValue('Request too frequent');
      }
      
      console.log('发送新的食谱详情请求:', recipeId);
      
      // 发送新请求并跟踪
      const responsePromise = recipeService.getRecipeDetail(recipeId);
      requestTracker.setPendingRequest('recipes/fetchDetail', recipeId, responsePromise);
      
      const response = await responsePromise;
      
      // 确保instructions是数组类型 - 使用类型断言解决TypeScript编译错误
      if (response.instructions) {
        if (Array.isArray(response.instructions)) {
          // 如果已经是数组，确保每个元素都是字符串并过滤空元素
          response.instructions = response.instructions
            .filter((step: any) => typeof step === 'string' && step.trim())
            .map((step: string) => step.trim());
        } else if (typeof response.instructions === 'string') {
          // 如果是字符串，按换行符分割成数组
          // 使用类型断言告诉TypeScript这是一个字符串
          const instructionsStr = response.instructions as string;
          response.instructions = instructionsStr.split('\n').filter((step: string) => step.trim());
        } else {
          // 如果是其他类型，转换为空数组
          response.instructions = [];
        }
      } else {
        // 如果instructions不存在，设置为空数组
        response.instructions = [];
      }
      
      // 缓存结果
      recentRequests.set(cacheKey, { timestamp: now, result: response });
      
      return response;
    } catch (error: any) {
      console.error('获取食谱详情失败:', error);
      return rejectWithValue(error.response?.data?.detail || '获取食谱详情失败');
    }
  }
);

export const searchRecipes = createAsyncThunk(
  'recipes/search',
  async (params: { query?: string; cooking_time?: number; difficulty?: string; page?: number; limit?: number }, { rejectWithValue }) => {
    try {
      const response = await recipeService.searchRecipes(params.query, params.cooking_time, params.difficulty, params.page, params.limit);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || '搜索食谱失败');
    }
  }
);



export const rateRecipe = createAsyncThunk(
  'recipes/rate',
  async (params: { recipeId: string; ratingData: RatingCreate }, { rejectWithValue }) => {
    try {
      await recipeService.rateRecipe(params.recipeId, params.ratingData);
      return { recipeId: params.recipeId, rating: params.ratingData };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || '评分失败');
    }
  }
);

export const addToMyRecipes = createAsyncThunk(
  'recipes/addToMyRecipes',
  async (recipe: RecipeListItem, { rejectWithValue }) => {
    try {
      // 使用createRecipe方法将生成的食谱添加到我的食谱中
      const newRecipe = await recipeService.createRecipe(recipe as unknown as any);
      return newRecipe;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || '添加到我的食谱失败');
    }
  }
);

export const deleteRecipe = createAsyncThunk(
  'recipes/delete',
  async (recipeId: string, { rejectWithValue }) => {
    try {
      await recipeService.deleteRecipe(recipeId);
      return recipeId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || '删除食谱失败');
    }
  }
);

const recipeSlice = createSlice({
  name: 'recipes',
  initialState,
  reducers: {
    clearGeneratedRecipes: (state) => {
      state.generatedRecipes = [];
    },
    clearError: (state) => {
      state.error = null;
    },
    setGeneratedRecipeDetail: (state, action: PayloadAction<Recipe>) => {
      state.loading = false;
      state.currentRecipe = action.payload;
      state.error = null;
    }
  },
  extraReducers: (builder) => {
      builder
        // 生成食谱
        .addCase(generateRecipes.pending, (state) => {
          state.loading = true;
          state.error = null;
        })
        .addCase(generateRecipes.fulfilled, (state, action) => {
          state.loading = false;
          state.generatedRecipes = action.payload;
          state.error = null;
          
          // 将生成的食谱自动添加到用户食谱列表中
          action.payload.forEach(recipe => {
            // 检查食谱是否已存在于列表中
            const exists = state.recipeList.some(r => r.recipe_id === recipe.recipe_id);
            if (!exists) {
              // 将Recipe对象转换为RecipeListItem类型
              const recipeListItem: RecipeListItem = {
                recipe_id: recipe.recipe_id,
                title: recipe.title,
                description: recipe.description || '',
                cuisine: recipe.cuisine || '',
                cooking_time: Number(recipe.cooking_time) || 0,
                difficulty: recipe.difficulty,
                created_at: recipe.created_at || new Date().toISOString(),
                image_url: recipe.image_url || '',
                author_name: recipe.author_name || 'AI',
                tags: recipe.tags || []
              };
              state.recipeList.push(recipeListItem);
            }
          });
        })
      .addCase(generateRecipes.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch Recipes
      .addCase(fetchRecipes.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRecipes.fulfilled, (state, action: PayloadAction<RecipeListResponse>) => {
        state.loading = false;
        
        // 更新状态 - 使用生成的食谱替换现有列表
        state.recipeList = action.payload.recipes;
        
        state.pagination = {
          page: action.payload.page,
          limit: action.payload.limit,
          total: action.payload.total
        };
        state.error = null;
      })
      .addCase(fetchRecipes.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch Recipe Detail
      .addCase(fetchRecipeDetail.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRecipeDetail.fulfilled, (state, action: PayloadAction<Recipe>) => {
        state.loading = false;
        state.currentRecipe = action.payload;
        state.error = null;
      })
      .addCase(fetchRecipeDetail.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })

      // Clear error
      .addCase(clearError, (state) => {
        state.error = null;
      })
      // Add To My Recipes
      .addCase(addToMyRecipes.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addToMyRecipes.fulfilled, (state, action) => {
        state.loading = false;
        // 将新添加的食谱添加到recipeList中，确保类型匹配
        const newRecipeListItem: RecipeListItem = {
          recipe_id: action.payload.recipe_id,
          title: action.payload.title,
          description: action.payload.description || '',
          cuisine: action.payload.cuisine || '',
          cooking_time: Number(action.payload.cooking_time) || 0,
          difficulty: action.payload.difficulty,
          created_at: action.payload.created_at,
          image_url: action.payload.image_url || '',
          author_name: action.payload.author_name || '',
          tags: action.payload.tags
        };
        state.recipeList = [...state.recipeList, newRecipeListItem];
        state.error = null;
      })
      .addCase(addToMyRecipes.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // 删除食谱
      .addCase(deleteRecipe.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteRecipe.fulfilled, (state, action) => {
        state.loading = false;
        const recipeId = action.payload;
        // 从食谱列表中移除删除的食谱
        state.recipeList = state.recipeList.filter(recipe => recipe.recipe_id !== recipeId);
        // 如果当前食谱被删除，清除当前食谱
        if (state.currentRecipe && state.currentRecipe.recipe_id === recipeId) {
          state.currentRecipe = null;
        }
        // 从生成的食谱中也移除
        state.generatedRecipes = state.generatedRecipes.filter(recipe => recipe.recipe_id !== recipeId);
        state.error = null;
      })
      .addCase(deleteRecipe.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  }
});

export const { clearGeneratedRecipes, clearError, setGeneratedRecipeDetail } = recipeSlice.actions;
export default recipeSlice.reducer;
