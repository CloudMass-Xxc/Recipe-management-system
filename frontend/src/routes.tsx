import { createBrowserRouter, Navigate, Outlet } from 'react-router-dom';
import React, { lazy } from 'react';
import { CircularProgress } from '@mui/material';
import { AuthProvider } from './hooks/useAuth';

// 使用React.lazy实现路由级别的代码分割
const RecipeGeneratePage = lazy(() => import('./pages/RecipeGenerate/RecipeGeneratePage'));
const HomePage = lazy(() => import('./pages/Home/HomePage'));
const RecipeListPage = lazy(() => import('./pages/RecipeList/RecipeListPage'));
const RecipeDetailPage = lazy(() => import('./pages/RecipeDetail/RecipeDetailPage'));
const UserProfilePage = lazy(() => import('./pages/UserProfile/UserProfilePage'));
const DietPlanPage = lazy(() => import('./pages/DietPlan/DietPlanPage'));
const FavoritesPage = lazy(() => import('./pages/Favorites/FavoritesPage'));

const LoginPage = lazy(() => import('./pages/Login/LoginPage'));
const RegisterPage = lazy(() => import('./pages/Register/RegisterPage'));

// 创建根布局组件，应用AuthProvider
const RootLayout = () => {
  return (
    <AuthProvider>
      <Outlet />
    </AuthProvider>
  );
};

// 创建带有代码分割和懒加载的路由配置
const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      {
        index: true,
        element: <React.Suspense fallback={<CircularProgress />}><HomePage /></React.Suspense>
      },
  {
      path: '/recipe-generate',
      element: <React.Suspense fallback={<CircularProgress />}><RecipeGeneratePage /></React.Suspense>
    },
  {
      path: '/recipe-list',
      element: <React.Suspense fallback={<CircularProgress />}><RecipeListPage /></React.Suspense>
    },
  {
      path: '/recipe-detail/:recipeId',
      element: <React.Suspense fallback={<CircularProgress />}><RecipeDetailPage /></React.Suspense>
    },
  {
      path: '/profile',
      element: <React.Suspense fallback={<CircularProgress />}><UserProfilePage /></React.Suspense>
    },
  {      path: '/diet-plan',
      element: <React.Suspense fallback={<CircularProgress />}><DietPlanPage /></React.Suspense>
    },
  {
      path: '/favorites',
      element: <React.Suspense fallback={<CircularProgress />}><FavoritesPage /></React.Suspense>
    },
  
      {
        path: '/login',
        element: <React.Suspense fallback={<CircularProgress />}><LoginPage /></React.Suspense>
      },
      {
        path: '/register',
        element: <React.Suspense fallback={<CircularProgress />}><RegisterPage /></React.Suspense>
      },
      {
        path: '*',
        element: <Navigate to="/" replace />
      }
    ]
  }
]);

export default router;
