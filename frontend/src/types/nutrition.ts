export interface NutritionData {
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
}

export interface IngredientNutrition {
  name: string;
  amount: number;
  unit: string;
  nutrition: NutritionData;
}
