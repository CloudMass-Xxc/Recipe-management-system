import { useDispatch, useSelector } from 'react-redux';
import { useCallback } from 'react';
import type { RootState, AppDispatch } from '../store';
import { 
  generateRecipes, 
  fetchRecipes, 
  fetchRecipeDetail, 
  searchRecipes, 
  favoriteRecipe, 
  unfavoriteRecipe, 
  rateRecipe,
  addToMyRecipes,
  deleteRecipe,
  clearGeneratedRecipes,
  clearError,
  setGeneratedRecipeDetail 
} from '../store/slices/recipeSlice';
import type { RecipeGenerateRequest, RatingCreate } from '../types/recipe';

export const useRecipe = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { generatedRecipes, recipeList, currentRecipe, loading, error, pagination } = useSelector((state: RootState) => state.recipes);

  const handleGenerateRecipes = useCallback((params: RecipeGenerateRequest) => {
    return dispatch(generateRecipes(params)).unwrap();
  }, [dispatch]);

  const handleFetchRecipes = useCallback((page: number = 1, limit: number = 10, tags?: string[]) => {
    try {
      // 直接传递参数给fetchRecipes action
      return dispatch(fetchRecipes({ page, limit, tags })).unwrap();
    } catch (error) {
      console.error('获取食谱列表失败:', error);
      throw error;
    }
  }, [dispatch]);

  const handleFetchRecipeDetail = useCallback((recipeId: string) => {
    return dispatch(fetchRecipeDetail(recipeId)).unwrap();
  }, [dispatch]);

  // 获取当前生成的食谱详情（从generatedRecipes中查找）
  const getGeneratedRecipeById = useCallback((recipeId: string) => {
    return generatedRecipes.find(recipe => recipe.recipe_id === recipeId) || null;
  }, [generatedRecipes]);

  const handleSearchRecipes = useCallback((query?: string, cooking_time?: number, difficulty?: string, page: number = 1, limit: number = 10) => {
    return dispatch(searchRecipes({ query, cooking_time, difficulty, page, limit })).unwrap();
  }, [dispatch]);

  const handleFavoriteRecipe = useCallback((recipeId: string) => {
    return dispatch(favoriteRecipe(recipeId)).unwrap();
  }, [dispatch]);

  const handleUnfavoriteRecipe = useCallback((recipeId: string) => {
    return dispatch(unfavoriteRecipe(recipeId)).unwrap();
  }, [dispatch]);

  const handleRateRecipe = useCallback((recipeId: string, ratingData: RatingCreate) => {
    return dispatch(rateRecipe({ recipeId, ratingData })).unwrap();
  }, [dispatch]);

  const handleAddToMyRecipes = useCallback((recipe: any) => {
    return dispatch(addToMyRecipes(recipe)).unwrap();
  }, [dispatch]);

  const handleClearGeneratedRecipes = useCallback(() => {
    dispatch(clearGeneratedRecipes());
  }, [dispatch]);

  const handleClearError = useCallback(() => {
    dispatch(clearError());
  }, [dispatch]);

  const handleSetGeneratedRecipeDetail = useCallback((recipe: any) => {
    return dispatch(setGeneratedRecipeDetail(recipe));
  }, [dispatch]);

  const handleDeleteRecipe = useCallback((recipeId: string) => {
    return dispatch(deleteRecipe(recipeId)).unwrap();
  }, [dispatch]);

  return {
    generatedRecipes,
    recipeList,
    currentRecipe,
    loading,
    error,
    pagination,
    generateRecipes: handleGenerateRecipes,
    fetchRecipes: handleFetchRecipes,
    fetchRecipeDetail: handleFetchRecipeDetail,
    searchRecipes: handleSearchRecipes,
    favoriteRecipe: handleFavoriteRecipe,
    unfavoriteRecipe: handleUnfavoriteRecipe,
    rateRecipe: handleRateRecipe,
    addToMyRecipes: handleAddToMyRecipes,
    deleteRecipe: handleDeleteRecipe,
    clearGeneratedRecipes: handleClearGeneratedRecipes,
    clearError: handleClearError,
    getGeneratedRecipeById,
    setGeneratedRecipeDetail: handleSetGeneratedRecipeDetail
  };
};
