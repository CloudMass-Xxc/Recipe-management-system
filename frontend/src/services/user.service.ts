// 使用type-only导入语法导入类型
import type { UserProfile, UserPreferences, UserUpdate, UserPreferencesUpdate, ShoppingListItemCreate, ShoppingListItemUpdate } from '../types/user';
import api from './api';

export const userService = {
  async getUserProfile(): Promise<UserProfile> {
    // 获取用户资料
    try {
      const response = await api.get<UserProfile>('/users/me');
      return response.data;
    } catch (error) {
      console.error('获取用户资料失败:', error);
      throw error;
    }
  },

  async updateUserProfile(profileData: UserUpdate): Promise<UserProfile> {
    // 更新用户资料
    try {
      const response = await api.put<UserProfile>('/users/me', profileData);
      return response.data;
    } catch (error) {
      console.error('更新用户资料失败:', error);
      throw error;
    }
  },

  async updateUserPreferences(preferences: UserPreferencesUpdate): Promise<UserPreferences> {
    // 更新用户偏好
    try {
      const response = await api.put<UserPreferences>('/users/preferences', preferences);
      return response.data;
    } catch (error) {
      console.error('更新用户偏好失败:', error);
      throw error;
    }
  },

  async addToShoppingList(item: ShoppingListItemCreate): Promise<UserPreferences> {
    // 添加购物清单项目
    try {
      const response = await api.post<UserPreferences>('/users/shopping-list', item);
      return response.data;
    } catch (error) {
      console.error('添加购物清单项目失败:', error);
      throw error;
    }
  },

  async updateShoppingList(itemId: string, updates: ShoppingListItemUpdate): Promise<UserPreferences> {
    // 更新购物清单项目
    try {
      const response = await api.put<UserPreferences>(`/users/shopping-list/${itemId}`, updates);
      return response.data;
    } catch (error) {
      console.error('更新购物清单项目失败:', error);
      throw error;
    }
  },

  async removeFromShoppingList(itemId: string): Promise<UserPreferences> {
    // 删除购物清单项目
    try {
      const response = await api.delete<UserPreferences>(`/users/shopping-list/${itemId}`);
      return response.data;
    } catch (error) {
      console.error('删除购物清单项目失败:', error);
      throw error;
    }
  },

  async getFavorites(page: number = 1, limit: number = 20): Promise<any> {
    // 获取收藏的食谱
    try {
      const params = { skip: (page - 1) * limit, limit };
      const response = await api.get('/users/favorites', { params });
      return response.data;
    } catch (error) {
      console.error('获取收藏食谱失败:', error);
      throw error;
    }
  },

  async toggleFavorite(recipeId: string): Promise<{ is_favorite: boolean }> {
    // 切换收藏状态
    try {
      const response = await api.post<{ is_favorite: boolean }>(`/recipes/${recipeId}/favorite`);
      return response.data;
    } catch (error) {
      console.error('切换收藏状态失败:', error);
      throw error;
    }
  },

  async isFavorite(recipeId: string): Promise<{ is_favorite: boolean }> {
    // 检查是否已收藏
    try {
      const response = await api.get<{ is_favorite: boolean }>(`/recipes/${recipeId}/favorite`);
      return response.data;
    } catch (error) {
      console.error('检查收藏状态失败:', error);
      throw error;
    }
  }
};
