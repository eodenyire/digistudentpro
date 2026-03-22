import apiClient from './client';
import { User, LoginData, RegisterData, LoginResponse, AuthTokens } from '@/types';

export const authApi = {
  // Login
  login: async (credentials: LoginData): Promise<LoginResponse> => {
    const response = await apiClient.post('/auth/jwt/create/', credentials);
    const tokens: AuthTokens = response.data;
    
    // Store tokens
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    
    // Get user details
    const userResponse = await apiClient.get('/auth/users/me/');
    const user: User = userResponse.data;
    localStorage.setItem('user', JSON.stringify(user));
    
    return { tokens, user };
  },

  // Register
  register: async (data: RegisterData): Promise<User> => {
    const response = await apiClient.post('/auth/users/', data);
    return response.data;
  },

  // Logout
  logout: async (): Promise<void> => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  // Get current user
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/auth/users/me/');
    return response.data;
  },

  // Update user profile
  updateProfile: async (id: number, data: Partial<User>): Promise<User> => {
    const response = await apiClient.patch(`/auth/users/${id}/`, data);
    return response.data;
  },

  // Refresh token
  refreshToken: async (refresh: string): Promise<AuthTokens> => {
    const response = await apiClient.post('/auth/jwt/refresh/', { refresh });
    return response.data;
  },

  // Verify token
  verifyToken: async (token: string): Promise<boolean> => {
    try {
      await apiClient.post('/auth/jwt/verify/', { token });
      return true;
    } catch {
      return false;
    }
  },

  // Request password reset
  resetPassword: async (email: string): Promise<void> => {
    await apiClient.post('/auth/users/reset_password/', { email });
  },

  // Confirm password reset
  confirmPasswordReset: async (uid: string, token: string, new_password: string): Promise<void> => {
    await apiClient.post('/auth/users/reset_password_confirm/', {
      uid,
      token,
      new_password,
    });
  },
};
