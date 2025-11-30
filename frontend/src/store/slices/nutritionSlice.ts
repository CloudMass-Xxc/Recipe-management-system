import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import { nutritionService } from '../../services/nutrition.service';
import type { NutritionData, IngredientNutrition } from '../../types/nutrition';

interface NutritionState {
  nutritionData: NutritionData | null;
  ingredientNutrition: IngredientNutrition | null;
  loading: boolean;
  error: string | null;
}

const initialState: NutritionState = {
  nutritionData: null,
  ingredientNutrition: null,
  loading: false,
  error: null
};

export const calculateNutrition = createAsyncThunk(
  'nutrition/calculate',
  async (ingredients: any[], { rejectWithValue }) => {
    try {
      const nutrition = await nutritionService.calculateNutrition(ingredients);
      return nutrition;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || '计算营养成分失败');
    }
  }
);

export const getIngredientNutrition = createAsyncThunk(
  'nutrition/getIngredientNutrition',
  async (params: { name: string; amount: number; unit: string }, { rejectWithValue }) => {
    try {
      const nutrition = await nutritionService.getIngredientNutrition(params.name, params.amount, params.unit);
      return nutrition;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || '获取食材营养信息失败');
    }
  }
);

const nutritionSlice = createSlice({
  name: 'nutrition',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearNutritionData: (state) => {
      state.nutritionData = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Calculate Nutrition
      .addCase(calculateNutrition.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(calculateNutrition.fulfilled, (state, action: PayloadAction<NutritionData>) => {
        state.loading = false;
        state.nutritionData = action.payload;
        state.error = null;
      })
      .addCase(calculateNutrition.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Get Ingredient Nutrition
      .addCase(getIngredientNutrition.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getIngredientNutrition.fulfilled, (state, action: PayloadAction<IngredientNutrition>) => {
        state.loading = false;
        state.ingredientNutrition = action.payload;
        state.error = null;
      })
      .addCase(getIngredientNutrition.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Clear error
      .addCase(clearError, (state) => {
        state.error = null;
      })
      // Clear nutrition data
      .addCase(clearNutritionData, (state) => {
        state.nutritionData = null;
      });
  }
});

export const { clearError, clearNutritionData } = nutritionSlice.actions;
export default nutritionSlice.reducer;
