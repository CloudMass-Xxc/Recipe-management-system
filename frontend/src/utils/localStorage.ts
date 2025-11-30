// localStorage.ts - 安全的存储操作工具，支持系统重启检测

// 应用重启检测标记
const APP_RESTART_FLAG = 'app_restart_flag';
const CURRENT_VERSION = '1.0.0'; // 应用版本，可用于强制清除旧数据

/**
 * 检查并处理应用重启
 * @returns boolean 是否是应用重启
 */
export const checkForAppRestart = (): boolean => {
  try {
    const storedFlag = localStorage.getItem(APP_RESTART_FLAG);
    const currentFlag = `${CURRENT_VERSION}_${Date.now()}`;
    
    // 如果没有存储的标记或标记格式不正确，说明是新启动
    if (!storedFlag || !storedFlag.includes(CURRENT_VERSION)) {
      // 更新重启标记
      localStorage.setItem(APP_RESTART_FLAG, currentFlag);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error('Error checking for app restart:', error);
    return true; // 出错时默认按重启处理，确保安全
  }
};

/**
 * 安全地从localStorage获取数据
 * @param key 存储键名
 * @returns 存储的数据，如果不存在或发生错误则返回null
 */
export const getFromLocalStorage = <T>(key: string): T | null => {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  } catch (error) {
    console.error(`Error getting ${key} from localStorage:`, error);
    return null;
  }
};

/**
 * 安全地向localStorage存储数据
 * @param key 存储键名
 * @param value 要存储的数据
 */
export const setToLocalStorage = <T>(key: string, value: T): void => {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error(`Error setting ${key} to localStorage:`, error);
  }
};

/**
 * 安全地从localStorage删除数据
 * @param key 存储键名
 */
export const removeFromLocalStorage = (key: string): void => {
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.error(`Error removing ${key} from localStorage:`, error);
  }
};

/**
 * 清除所有localStorage数据
 */
export const clearLocalStorage = (): void => {
  try {
    localStorage.clear();
  } catch (error) {
    console.error('Error clearing localStorage:', error);
  }
};

/**
 * 安全地从sessionStorage获取数据
 * @param key 存储键名
 * @returns 存储的数据，如果不存在或发生错误则返回null
 */
export const getFromSessionStorage = <T>(key: string): T | null => {
  try {
    const item = sessionStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  } catch (error) {
    console.error(`Error getting ${key} from sessionStorage:`, error);
    return null;
  }
};

/**
 * 安全地向sessionStorage存储数据
 * @param key 存储键名
 * @param value 要存储的数据
 */
export const setToSessionStorage = <T>(key: string, value: T): void => {
  try {
    sessionStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error(`Error setting ${key} to sessionStorage:`, error);
  }
};

/**
 * 安全地从sessionStorage删除数据
 * @param key 存储键名
 */
export const removeFromSessionStorage = (key: string): void => {
  try {
    sessionStorage.removeItem(key);
  } catch (error) {
    console.error(`Error removing ${key} from sessionStorage:`, error);
  }
};

/**
 * 清除所有sessionStorage数据
 */
export const clearSessionStorage = (): void => {
  try {
    sessionStorage.clear();
  } catch (error) {
    console.error('Error clearing sessionStorage:', error);
  }
};

/**
 * 清除所有认证相关数据
 */
export const clearAuthData = (): void => {
  try {
    // 清除localStorage中的认证数据
    removeFromLocalStorage('user');
    removeFromLocalStorage('refresh_token');
    
    // 清除sessionStorage中的认证数据
    removeFromSessionStorage('access_token');
    
    console.log('Authentication data cleared successfully');
  } catch (error) {
    console.error('Error clearing auth data:', error);
  }
};
