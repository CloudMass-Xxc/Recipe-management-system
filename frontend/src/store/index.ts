import { configureStore } from '@reduxjs/toolkit';
import recipeReducer from './slices/recipeSlice';
import userReducer from './slices/userSlice';
import nutritionReducer from './slices/nutritionSlice';

export const store = configureStore({
  reducer: {
    recipes: recipeReducer,
    user: userReducer,
    nutrition: nutritionReducer
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false
    })
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
