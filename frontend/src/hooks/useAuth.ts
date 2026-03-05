import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { authApi } from '@/api';
import { useAuthStore } from '@/store';
import { LoginData, RegisterData } from '@/types';
import { useNavigate } from 'react-router-dom';
import { useUIStore } from '@/store';

export function useLogin() {
  const navigate = useNavigate();
  const { setUser, setTokens } = useAuthStore();
  const { addNotification } = useUIStore();

  return useMutation({
    mutationFn: (credentials: LoginData) => authApi.login(credentials),
    onSuccess: (data) => {
      setUser(data.user);
      setTokens(data.tokens.access, data.tokens.refresh);
      addNotification({
        type: 'success',
        title: 'Login Successful',
        message: `Welcome back, ${data.user.first_name}!`,
      });
      navigate('/dashboard');
    },
    onError: (error: any) => {
      addNotification({
        type: 'error',
        title: 'Login Failed',
        message: error.message || 'Invalid credentials',
      });
    },
  });
}

export function useRegister() {
  const navigate = useNavigate();
  const { addNotification } = useUIStore();

  return useMutation({
    mutationFn: (data: RegisterData) => authApi.register(data),
    onSuccess: () => {
      addNotification({
        type: 'success',
        title: 'Registration Successful',
        message: 'Please log in with your credentials',
      });
      navigate('/login');
    },
    onError: (error: any) => {
      addNotification({
        type: 'error',
        title: 'Registration Failed',
        message: error.message || 'Failed to register',
      });
    },
  });
}

export function useLogout() {
  const navigate = useNavigate();
  const { clearAuth } = useAuthStore();
  const { addNotification } = useUIStore();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => authApi.logout(),
    onSuccess: () => {
      clearAuth();
      queryClient.clear();
      addNotification({
        type: 'info',
        title: 'Logged Out',
        message: 'You have been logged out successfully',
      });
      navigate('/login');
    },
  });
}

export function useCurrentUser() {
  const { user } = useAuthStore();

  return useQuery({
    queryKey: ['currentUser'],
    queryFn: () => authApi.getCurrentUser(),
    enabled: !!user,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

export function useUpdateProfile() {
  const queryClient = useQueryClient();
  const { updateUser } = useAuthStore();
  const { addNotification } = useUIStore();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      authApi.updateProfile(id, data),
    onSuccess: (data) => {
      updateUser(data);
      queryClient.invalidateQueries({ queryKey: ['currentUser'] });
      addNotification({
        type: 'success',
        title: 'Profile Updated',
        message: 'Your profile has been updated successfully',
      });
    },
    onError: () => {
      addNotification({
        type: 'error',
        title: 'Update Failed',
        message: 'Failed to update profile',
      });
    },
  });
}
