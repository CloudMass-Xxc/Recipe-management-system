import { vi } from 'vitest';
import '@testing-library/jest-dom';

// Mock React Router
global.window = {
  ...global.window,
  location: {
    pathname: '/',
    search: '',
    hash: '',
  },
  history: {
    pushState: vi.fn(),
    replaceState: vi.fn(),
  },
} as any;

// Mock localStorage
global.localStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
} as any;

// Mock sessionStorage
global.sessionStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
} as any;

// Mock AuthService for testing
vi.mock('./services/auth.service', () => ({
  default: {
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
    refreshToken: vi.fn(),
  },
}));
