import { vi } from 'vitest';
import '@testing-library/jest-dom';

// Define the storage interface matching the native Storage API
interface StorageMock {
  getItem: (key: string) => string | null;
  setItem: (key: string, value: string) => void;
  removeItem: (key: string) => void;
  clear: () => void;
  length: number;
  key: (index: number) => string | null;
}

// Create a mock storage implementation with internal data store
function createMockStorage(): StorageMock {
  const storage: Record<string, string> = {};
  
  return {
    getItem: vi.fn<StorageMock['getItem']>((key) => storage[key] || null),
    setItem: vi.fn<StorageMock['setItem']>((key, value) => {
      storage[key] = value;
    }),
    removeItem: vi.fn<StorageMock['removeItem']>((key) => {
      delete storage[key];
    }),
    clear: vi.fn<StorageMock['clear']>(() => {
      Object.keys(storage).forEach(key => delete storage[key]);
    }),
    get length() {
      return Object.keys(storage).length;
    },
    key: vi.fn<StorageMock['key']>((index) => {
      const keys = Object.keys(storage);
      return keys[index] || null;
    }),
  };
}

// Mock localStorage
globalThis.localStorage = createMockStorage();

// Mock sessionStorage
globalThis.sessionStorage = createMockStorage();

// Mock AuthService for testing
vi.mock('./services/auth.service', () => ({
  default: {
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
    refreshToken: vi.fn(),
  },
}));
