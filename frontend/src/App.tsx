import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Layout
import { AppLayout } from './components/layout';
import ProtectedRoute from './components/ProtectedRoute';
import { Toast } from './components/ui';

// Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import CareersPage from './pages/digiguide/CareersPage';
import BrowseResourcesPage from './pages/digilab/BrowseResourcesPage';
import SquadsPage from './pages/digichat/SquadsPage';
import BlogFeedPage from './pages/digiblog/BlogFeedPage';

// Create QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Toast />
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected Routes */}
          <Route element={<ProtectedRoute />}>
            <Route element={<AppLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              
              {/* DigiGuide Routes */}
              <Route path="/digiguide/careers" element={<CareersPage />} />
              
              {/* DigiLab Routes */}
              <Route path="/digilab/browse" element={<BrowseResourcesPage />} />
              
              {/* DigiChat Routes */}
              <Route path="/digichat/squads" element={<SquadsPage />} />
              
              {/* DigiBlog Routes */}
              <Route path="/digiblog" element={<BlogFeedPage />} />
            </Route>
          </Route>

          {/* Catch all */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
