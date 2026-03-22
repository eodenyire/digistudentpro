// Common Types

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  detail?: string;
  message?: string;
  errors?: Record<string, string[]>;
}

export interface SelectOption {
  value: string | number;
  label: string;
}

export interface Notification {
  id: number;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  read: boolean;
  created_at: string;
}

export interface DashboardStats {
  total_resources: number;
  completed_resources: number;
  total_assessments: number;
  passed_assessments: number;
  study_time: number;
  streak_days: number;
}

// Re-export all types
export * from './auth';
export * from './digiguide';
export * from './digilab';
export * from './digichat';
export * from './digiblog';
