import { describe, it, expect, vi, beforeEach } from 'vitest';
import AuthService from './auth.service';
import api from '../utils/api';
import { getFromLocalStorage, setToLocalStorage, removeFromLocalStorage } from '../utils/localStorage';

// Mock the api module
vi.mock('../utils/api', () => ({
  default: {
    post: vi.fn(),
    delete: vi.fn(),
  },
}));

// Mock the localStorage utility functions
vi.mock('../utils/localStorage', () => ({
  getFromLocalStorage: vi.fn(),
  setToLocalStorage: vi.fn(),
  removeFromLocalStorage: vi.fn(),
  clearAuthData: vi.fn(),
}));

// Mock sessionStorage globally
vi.spyOn(global.sessionStorage, 'getItem');
vi.spyOn(global.sessionStorage, 'setItem');
vi.spyOn(global.sessionStorage, 'removeItem');

describe('AuthService', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
  });

  describe('login', () => {
    it('should successfully login and store tokens and user data', async () => {
      // Mock data
      const mockResponse = {
        user_id: '1',
        username: 'testuser',
        email: 'test@example.com',
        phone: '1234567890',
        access_token: 'mock-access-token',
        refresh_token: 'mock-refresh-token'
      };

      // Mock API response
      api.post.mockResolvedValueOnce({ data: mockResponse });

      // Execute login
      const result = await AuthService.login('testuser', 'password123');

      // Verify API call
      expect(api.post).toHaveBeenCalledWith('/auth/login', {
        username: 'testuser',
        password: 'password123'
      });
      expect(api.post).toHaveBeenCalledTimes(1);

      // Verify storage operations
      expect(setToLocalStorage).toHaveBeenCalledWith('user', {
        user_id: '1',
        username: 'testuser',
        email: 'test@example.com',
        phone: '1234567890'
      });
      expect(sessionStorage.setItem).toHaveBeenCalledWith('access_token', 'mock-access-token');
      expect(sessionStorage.setItem).toHaveBeenCalledWith('refresh_token', 'mock-refresh-token');

      // Verify return value
      expect(result).toEqual(mockResponse);
    });

    it('should throw error when login fails', async () => {
      // Mock API error
      api.post.mockRejectedValueOnce(new Error('Invalid credentials'));

      // Execute login and verify error
      await expect(AuthService.login('testuser', 'wrongpassword')).rejects.toThrow('Invalid credentials');

      // Verify API call
      expect(api.post).toHaveBeenCalledWith('/auth/login', {
        username: 'testuser',
        password: 'wrongpassword'
      });
    });
  });

  describe('register', () => {
    it('should successfully register new user', async () => {
      // Mock data
      const mockResponse = {
        user_id: '1',
        username: 'newuser',
        email: 'new@example.com',
        phone: '0987654321'
      };

      // Mock API response
      api.post.mockResolvedValueOnce({ data: mockResponse });

      // Execute registration
      const result = await AuthService.register(
        'newuser',
        'new@example.com',
        '0987654321',
        'password123'
      );

      // Verify API call
      expect(api.post).toHaveBeenCalledWith('/auth/register', {
        username: 'newuser',
        email: 'new@example.com',
        phone: '0987654321',
        password: 'password123'
      });
      expect(api.post).toHaveBeenCalledTimes(1);

      // Verify return value
      expect(result).toEqual(mockResponse);
    });

    it('should throw error when registration fails', async () => {
      // Mock API error
      api.post.mockRejectedValueOnce(new Error('Username already exists'));

      // Execute registration and verify error
      await expect(AuthService.register(
        'existinguser',
        'existing@example.com',
        '1234567890',
        'password123'
      )).rejects.toThrow('Username already exists');

      // Verify API call
      expect(api.post).toHaveBeenCalledWith('/auth/register', {
        username: 'existinguser',
        email: 'existing@example.com',
        phone: '1234567890',
        password: 'password123'
      });
    });
  });

  describe('logout', () => {
    it('should successfully logout and clear tokens and user data', async () => {
      // Mock refresh token in session storage
      sessionStorage.getItem.mockReturnValue('mock-refresh-token');

      // Mock successful API response
      api.delete.mockResolvedValueOnce({});

      // Execute logout
      await AuthService.logout();

      // Verify API call
      expect(api.delete).toHaveBeenCalledWith('/auth/logout', {
        data: { refresh_token: 'mock-refresh-token' }
      });
      expect(api.delete).toHaveBeenCalledTimes(1);

      // Verify credentials are cleared
      expect(sessionStorage.removeItem).toHaveBeenCalledWith('access_token');
      expect(sessionStorage.removeItem).toHaveBeenCalledWith('refresh_token');
      expect(removeFromLocalStorage).toHaveBeenCalledWith('user');
    });

    it('should handle logout failure', async () => {
      // Mock refresh token in session storage
      sessionStorage.getItem.mockReturnValue('mock-refresh-token');

      // Mock API failure
      api.delete.mockRejectedValueOnce(new Error('Logout failed'));

      // Execute logout and verify error
      await expect(AuthService.logout()).rejects.toThrow('Logout failed');

      // Verify API call
      expect(api.delete).toHaveBeenCalledWith('/auth/logout', {
        data: { refresh_token: 'mock-refresh-token' }
      });

      // Verify credentials are still cleared even on failure
      expect(sessionStorage.removeItem).toHaveBeenCalledWith('access_token');
      expect(sessionStorage.removeItem).toHaveBeenCalledWith('refresh_token');
      expect(removeFromLocalStorage).toHaveBeenCalledWith('user');
    });

    it('should handle logout without refresh token', async () => {
      // Mock no refresh token in session storage
      sessionStorage.getItem.mockReturnValue(null);

      // Execute logout
      await AuthService.logout();

      // Verify API call is not made
      expect(api.delete).not.toHaveBeenCalled();

      // Verify credentials are still cleared
      expect(sessionStorage.removeItem).toHaveBeenCalledWith('access_token');
      expect(sessionStorage.removeItem).toHaveBeenCalledWith('refresh_token');
      expect(removeFromLocalStorage).toHaveBeenCalledWith('user');
    });
  });

  describe('refreshToken', () => {
    it('should successfully refresh access token', async () => {
      // Mock refresh token in session storage
      sessionStorage.getItem.mockReturnValue('mock-refresh-token');

      // Mock successful API response
      const mockNewToken = {
        access_token: 'new-access-token'
      };
      api.post.mockResolvedValueOnce({ data: mockNewToken });

      // Execute token refresh
      const newToken = await AuthService.refreshToken();

      // Verify API call was made correctly
      expect(api.post).toHaveBeenCalledWith('/auth/refresh', {
        refresh_token: 'mock-refresh-token'
      });
      expect(api.post).toHaveBeenCalledTimes(1);

      // Verify new token was saved
      expect(sessionStorage.setItem).toHaveBeenCalledWith('access_token', 'new-access-token');

      // Verify return value
      expect(newToken).toBe('new-access-token');
    });

    it('should throw error when refresh token is not available', async () => {
      // Mock no refresh token in session storage
      sessionStorage.getItem.mockReturnValue(null);

      // Execute token refresh and verify error
      await expect(AuthService.refreshToken()).rejects.toThrow('No refresh token available');

      // Verify API call is not made
      expect(api.post).not.toHaveBeenCalled();
    });

    it('should throw error when token refresh API fails', async () => {
      // Mock refresh token in session storage
      sessionStorage.getItem.mockReturnValue('mock-refresh-token');

      // Mock API failure
      api.post.mockRejectedValueOnce(new Error('Refresh token expired'));

      // Execute token refresh and verify error
      await expect(AuthService.refreshToken()).rejects.toThrow('Refresh token expired');

      // Verify API call
      expect(api.post).toHaveBeenCalledWith('/auth/refresh', {
        refresh_token: 'mock-refresh-token'
      });
    });
  });
});
