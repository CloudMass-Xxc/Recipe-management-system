import { describe, it, expect, vi, beforeEach } from 'vitest';
import { 
  getFromLocalStorage, 
  setToLocalStorage, 
  removeFromLocalStorage, 
  checkForAppRestart,
  clearAuthData
} from './localStorage';

describe('localStorage utilities', () => {
  // Clear all mocks before each test
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('setToLocalStorage', () => {
    it('should set an item in localStorage', () => {
      // Mock localStorage.setItem
      const mockSetItem = vi.spyOn(global.localStorage, 'setItem');
      
      // Test data
      const key = 'testKey';
      const value = { name: 'Test', id: 1 };
      
      // Execute the function
      setToLocalStorage(key, value);
      
      // Verify it worked
      expect(mockSetItem).toHaveBeenCalledWith(key, JSON.stringify(value));
    });
  });

  describe('getFromLocalStorage', () => {
    it('should get an item from localStorage', () => {
      // Mock localStorage.getItem
      const mockGetItem = vi.spyOn(global.localStorage, 'getItem');
      
      // Test data
      const key = 'testKey';
      const value = { name: 'Test', id: 1 };
      
      // Set up the mock to return our test data
      mockGetItem.mockReturnValue(JSON.stringify(value));
      
      // Execute the function
      const result = getFromLocalStorage(key);
      
      // Verify it worked
      expect(mockGetItem).toHaveBeenCalledWith(key);
      expect(result).toEqual(value);
    });

    it('should return null if item does not exist', () => {
      // Mock localStorage.getItem to return null
      const mockGetItem = vi.spyOn(global.localStorage, 'getItem');
      mockGetItem.mockReturnValue(null);
      
      // Execute the function
      const result = getFromLocalStorage('nonExistentKey');
      
      // Verify it worked
      expect(mockGetItem).toHaveBeenCalledWith('nonExistentKey');
      expect(result).toBeNull();
    });

    it('should return null if JSON parsing fails', () => {
      // Mock localStorage.getItem to return invalid JSON
      const mockGetItem = vi.spyOn(global.localStorage, 'getItem');
      mockGetItem.mockReturnValue('invalid json');
      
      // Execute the function
      const result = getFromLocalStorage('testKey');
      
      // Verify it worked
      expect(mockGetItem).toHaveBeenCalledWith('testKey');
      expect(result).toBeNull();
    });
  });

  describe('removeFromLocalStorage', () => {
    it('should remove an item from localStorage', () => {
      // Mock localStorage.removeItem
      const mockRemoveItem = vi.spyOn(global.localStorage, 'removeItem');
      
      // Execute the function
      removeFromLocalStorage('testKey');
      
      // Verify it worked
      expect(mockRemoveItem).toHaveBeenCalledWith('testKey');
    });
  });

  describe('checkForAppRestart', () => {
    it('should check for app restart and set flag', () => {
      // Mock localStorage methods
      const mockGetItem = vi.spyOn(global.localStorage, 'getItem');
      const mockSetItem = vi.spyOn(global.localStorage, 'setItem');
      
      // Mock getItem to return null (first run)
      mockGetItem.mockReturnValue(null);
      
      // Execute the function
      const result = checkForAppRestart();
      
      // Verify it worked
      expect(mockGetItem).toHaveBeenCalledWith('app_restart_flag');
      expect(mockSetItem).toHaveBeenCalledWith('app_restart_flag', expect.any(String));
      expect(typeof result).toBe('boolean');
    });
  });

  describe('clearAuthData', () => {
    it('should clear authentication data from storage', () => {
      // Mock removeFromLocalStorage function
      const mockRemoveLocal = vi.spyOn(global.localStorage, 'removeItem');
      const mockRemoveSession = vi.spyOn(global.sessionStorage, 'removeItem');
      
      // Execute the function
      clearAuthData();
      
      // Verify it worked
      expect(mockRemoveLocal).toHaveBeenCalled();
      expect(mockRemoveSession).toHaveBeenCalled();
    });
  });
});
