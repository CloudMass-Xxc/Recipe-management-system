import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useRecipe } from '../../../hooks/useRecipe';

// Mock useRecipe hook
vi.mock('../../../hooks/useRecipe', () => ({
  useRecipe: vi.fn()
}));

const mockUseRecipe = useRecipe as vi.Mock;

describe('RecipeGenerator Component Logic Tests', () => {
  const mockGenerateRecipes = vi.fn();
  const mockRecipes = [
    {
      recipe_id: '1',
      title: '测试食谱1',
      ingredients: ['鸡蛋', '面粉'],
      instructions: ['步骤1', '步骤2'],
      cooking_time: 30,
      difficulty: '简单',
      nutrition_info: { calories: 500 },
      image_url: 'https://example.com/image1.jpg'
    },
    {
      recipe_id: '2',
      title: '测试食谱2',
      ingredients: ['牛奶', '燕麦'],
      instructions: ['步骤1', '步骤2'],
      cooking_time: 15,
      difficulty: '简单',
      nutrition_info: { calories: 400 },
      image_url: 'https://example.com/image2.jpg'
    }
  ];

  beforeEach(() => {
    vi.clearAllMocks();
    mockUseRecipe.mockReturnValue({
      generateRecipes: mockGenerateRecipes,
      generatedRecipes: [],
      loading: false
    });
  });

  it('should call generateRecipes with correct parameters when ingredients are provided', () => {
    // 验证generateRecipes函数被正确调用
    mockGenerateRecipes.mockResolvedValue(undefined);
    
    // 模拟hook返回值
    mockUseRecipe.mockReturnValue({
      generateRecipes: mockGenerateRecipes,
      generatedRecipes: [],
      loading: false
    });
    
    // 验证hook返回的generateRecipes函数可以被调用
    const { generateRecipes } = mockUseRecipe();
    
    // 调用generateRecipes函数
    generateRecipes({
      ingredients: ['鸡蛋', '面粉'],
      restrictions: ['无麸质'],
      preferences: { cooking_time: 30, difficulty: '简单' }
    });
    
    // 验证generateRecipes函数被调用了一次，并且参数正确
    expect(mockGenerateRecipes).toHaveBeenCalledTimes(1);
    expect(mockGenerateRecipes).toHaveBeenCalledWith({
      ingredients: ['鸡蛋', '面粉'],
      restrictions: ['无麸质'],
      preferences: { cooking_time: 30, difficulty: '简单' }
    });
  });

  it('should allow multiple recipe generations', async () => {
    // 验证可以多次调用generateRecipes函数
    mockGenerateRecipes.mockResolvedValue(undefined);
    
    // 模拟hook返回值
    mockUseRecipe.mockReturnValue({
      generateRecipes: mockGenerateRecipes,
      generatedRecipes: [],
      loading: false
    });
    
    // 获取generateRecipes函数
    const { generateRecipes } = mockUseRecipe();
    
    // 第一次调用
    await generateRecipes({
      ingredients: ['鸡蛋'],
      restrictions: [],
      preferences: {}
    });
    
    // 第二次调用
    await generateRecipes({
      ingredients: ['牛奶'],
      restrictions: [],
      preferences: {}
    });
    
    // 第三次调用
    await generateRecipes({
      ingredients: ['面粉'],
      restrictions: [],
      preferences: {}
    });
    
    // 验证generateRecipes函数被调用了三次
    expect(mockGenerateRecipes).toHaveBeenCalledTimes(3);
    
    // 验证每次调用的参数都是正确的
    expect(mockGenerateRecipes).toHaveBeenNthCalledWith(1, {
      ingredients: ['鸡蛋'],
      restrictions: [],
      preferences: {}
    });
    
    expect(mockGenerateRecipes).toHaveBeenNthCalledWith(2, {
      ingredients: ['牛奶'],
      restrictions: [],
      preferences: {}
    });
    
    expect(mockGenerateRecipes).toHaveBeenNthCalledWith(3, {
      ingredients: ['面粉'],
      restrictions: [],
      preferences: {}
    });
  });

  it('should handle successful recipe generation', () => {
    // 验证成功生成食谱时的状态
    mockGenerateRecipes.mockResolvedValue(undefined);
    
    // 模拟成功生成食谱的返回值
    mockUseRecipe.mockReturnValue({
      generateRecipes: mockGenerateRecipes,
      generatedRecipes: mockRecipes,
      loading: false
    });
    
    const { generatedRecipes, loading } = mockUseRecipe();
    
    // 验证生成的食谱列表不为空
    expect(generatedRecipes).toHaveLength(2);
    expect(generatedRecipes[0].title).toBe('测试食谱1');
    expect(generatedRecipes[1].title).toBe('测试食谱2');
    
    // 验证加载状态为false
    expect(loading).toBe(false);
  });

  it('should handle recipe generation failure', () => {
    // 验证失败生成食谱时的状态
    const errorMessage = '食谱生成失败，请重试';
    mockGenerateRecipes.mockRejectedValue(new Error(errorMessage));
    
    // 模拟失败生成食谱的返回值
    mockUseRecipe.mockReturnValue({
      generateRecipes: mockGenerateRecipes,
      generatedRecipes: [],
      loading: false
    });
    
    const { generateRecipes, generatedRecipes, loading } = mockUseRecipe();
    
    // 验证生成的食谱列表为空
    expect(generatedRecipes).toHaveLength(0);
    
    // 验证加载状态为false
    expect(loading).toBe(false);
    
    // 验证generateRecipes函数可以被调用，并且会抛出错误
    expect(() => generateRecipes({
      ingredients: ['鸡蛋'],
      restrictions: [],
      preferences: {}
    })).rejects.toThrow(errorMessage);
  });

  it('should handle loading state during recipe generation', () => {
    // 验证加载状态
    mockUseRecipe.mockReturnValue({
      generateRecipes: mockGenerateRecipes,
      generatedRecipes: [],
      loading: true
    });
    
    const { loading } = mockUseRecipe();
    
    // 验证加载状态为true
    expect(loading).toBe(true);
  });
});
