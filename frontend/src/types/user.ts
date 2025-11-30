// 用户基础类型
export interface UserBase {
  username: string;
  email: string;
  phone?: string;
}

// 用户创建类型
export interface UserCreate extends UserBase {
  password: string;
  display_name?: string;
}

// 用户登录类型
export interface UserLogin {
  identifier: string;
  password: string;
}

// 用户响应类型
export interface UserResponse extends UserBase {
  user_id: string;
  display_name?: string;
  created_at: string;
  updated_at?: string;
}

// 用户更新类型
export interface UserUpdate {
  display_name?: string;
  phone?: string;
}

// 用户资料类型
export interface UserProfile extends UserResponse {
  avatar_url?: string;
  bio?: string;
  diet_preferences?: {
    ingredients: string[];
    restrictions: string[];
    preferences: {
      cooking_time?: string;
      difficulty?: string;
      flavor?: string;
    };
  };
  is_active?: boolean;
  is_superuser?: boolean;
}

// 用户偏好设置类型
export interface UserPreferences {
  ingredients: string[];
  restrictions: string[];
  preferences: {
    cooking_time?: string;
    difficulty?: string;
    flavor?: string;
  };
}

// 用户偏好设置更新类型
export interface UserPreferencesUpdate {
  ingredients?: string[];
  restrictions?: string[];
  preferences?: {
    cooking_time?: string;
    difficulty?: string;
    flavor?: string;
  };
}

// 密码更新类型
export interface PasswordUpdate {
  old_password: string;
  new_password: string;
}

// 购物清单项目类型
export interface ShoppingListItem {
  id: string;
  name: string;
  quantity: string;
  unit: string;
  is_checked: boolean;
  created_at: string;
}

// 购物清单项目创建类型
export interface ShoppingListItemCreate {
  name: string;
  quantity: string;
  unit: string;
}

// 购物清单项目更新类型
export interface ShoppingListItemUpdate {
  name?: string;
  quantity?: string;
  unit?: string;
  is_checked?: boolean;
}