// User and Authentication Types
export type UserRole = 'student' | 'mentor' | 'parent' | 'teacher' | 'admin';

export interface User {
  id: number;
  username: string;
  email: string;
  phone_number?: string;
  role: UserRole;
  first_name: string;
  last_name: string;
  date_of_birth?: string;
  profile_picture?: string;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface StudentProfile {
  id: number;
  user: number;
  grade?: number;
  education_level?: number;
  career_aspiration?: string;
  parental_consent: boolean;
  guardian?: number;
  created_at: string;
  updated_at: string;
}

export interface MentorProfile {
  id: number;
  user: number;
  bio?: string;
  expertise_areas: string[];
  verification_status: 'pending' | 'verified' | 'rejected';
  badge?: string;
  rating: number;
  total_students: number;
  created_at: string;
  updated_at: string;
}

export interface ParentGuardianProfile {
  id: number;
  user: number;
  relationship_type: string;
  students: number[];
  created_at: string;
  updated_at: string;
}

// Auth Response Types
export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  tokens: AuthTokens;
  user: User;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  date_of_birth?: string;
  phone_number?: string;
}

export interface LoginData {
  email: string;
  password: string;
}
