// 使用type-only导入语法导入类型
import type { UserProfile, UserPreferences, UserUpdate, UserPreferencesUpdate, ShoppingListItemCreate, ShoppingListItemUpdate } from '../types/user';
import api from './api';

export const userService = {
  async getUserProfile(): Promise<UserProfile> {
    // 获取用户资料
    try {
      console.log('正在获取用户资料...');
      // 确保使用配置了完整认证处理的api实例
      const response = await api.get<UserProfile>('/users/me');
      console.log('获取用户资料成功:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('获取用户资料失败:', error);
      console.error('错误详情:', error.response?.data || error.message);
      // 重新抛出错误，让调用方知道发生了什么
      throw new Error(error.response?.data?.detail || '获取用户资料失败');
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


};
