import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import { userService } from '../../services/user.service';
import type { UserProfile, UserPreferences } from '../../types/user';
import { getFromLocalStorage, setToLocalStorage, removeFromLocalStorage } from '../../utils/localStorage';

interface UserState {
  profile: UserProfile | null;
  preferences: UserPreferences | null;
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  profile: getFromLocalStorage<UserProfile>('userProfile'),
  preferences: getFromLocalStorage<UserPreferences>('userPreferences'),
  loading: false,
  error: null
};

export const fetchProfile = createAsyncThunk(
  'user/fetchProfile',
  async (_, { rejectWithValue }) => {
    try {
      const profile = await userService.getUserProfile();
      return profile;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || '获取用户资料失败');
    }
  }
);

export const updateProfile = createAsyncThunk(
  'user/updateProfile',
  async (profileData: Partial<UserProfile>, { rejectWithValue }) => {
    try {
      const updatedProfile = await userService.updateUserProfile(profileData);
      return updatedProfile;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || '更新用户资料失败');
    }
  }
);

export const updatePreferences = createAsyncThunk(
  'user/updatePreferences',
  async (preferences: UserPreferences, { rejectWithValue }) => {
    try {
      const updatedPreferences = await userService.updateUserPreferences(preferences);
      return updatedPreferences;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || '更新偏好设置失败');
    }
  }
);



const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Profile
      .addCase(fetchProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProfile.fulfilled, (state, action: PayloadAction<UserProfile>) => {
        state.loading = false;
        state.profile = action.payload;
        state.error = null;
        setToLocalStorage('userProfile', action.payload);
      })
      .addCase(fetchProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Update Profile
      .addCase(updateProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateProfile.fulfilled, (state, action: PayloadAction<UserProfile>) => {
        state.loading = false;
        state.profile = action.payload;
        state.error = null;
        setToLocalStorage('userProfile', action.payload);
      })
      .addCase(updateProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Update Preferences
      .addCase(updatePreferences.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updatePreferences.fulfilled, (state, action: PayloadAction<UserPreferences>) => {
        state.loading = false;
        state.preferences = action.payload;
        state.error = null;
        setToLocalStorage('userPreferences', action.payload);
      })
      .addCase(updatePreferences.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })

      // Clear error
      .addCase(clearError, (state) => {
        state.error = null;
      })
      // Handle logout
      .addCase('auth/logout/fulfilled', (state) => {
        state.profile = null;
        state.preferences = null;
        removeFromLocalStorage('userProfile');
        removeFromLocalStorage('userPreferences');
      });
  }
});

export const { clearError } = userSlice.actions;
export default userSlice.reducer;
