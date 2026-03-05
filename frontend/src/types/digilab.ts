// DigiLab Module Types

export type ResourceType = 'video' | 'document' | 'interactive' | 'audio' | 'pdf';
export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced';

export interface Strand {
  id: number;
  subject: number;
  grade: number;
  name: string;
  code: string;
  description?: string;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface SubStrand {
  id: number;
  strand: number;
  name: string;
  code: string;
  description?: string;
  order: number;
  learning_outcomes: string[];
  created_at: string;
  updated_at: string;
}

export interface LearningResource {
  id: number;
  sub_strand: number;
  title: string;
  description?: string;
  resource_type: ResourceType;
  content_url?: string;
  file?: string;
  thumbnail?: string;
  difficulty?: DifficultyLevel;
  duration?: number;
  duration_minutes?: number;
  difficulty_level: DifficultyLevel;
  tags: string[];
  is_featured: boolean;
  view_count: number;
  views_count?: number;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface LearningProgress {
  id: number;
  student: number;
  resource: number;
  progress_percentage: number;
  completed: boolean;
  time_spent: number;
  last_accessed: string;
  notes?: string;
  bookmarked: boolean;
  created_at: string;
  updated_at: string;
}

export interface Assessment {
  id: number;
  sub_strand: number;
  title: string;
  description?: string;
  difficulty_level: DifficultyLevel;
  time_limit?: number;
  passing_score: number;
  total_marks: number;
  is_published: boolean;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface Question {
  id: number;
  assessment: number;
  question_text: string;
  question_type: 'multiple_choice' | 'true_false' | 'short_answer';
  options?: string[];
  correct_answer: string;
  explanation?: string;
  marks: number;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface AssessmentAttempt {
  id: number;
  assessment: number;
  student: number;
  score: number;
  percentage: number;
  passed: boolean;
  time_taken: number;
  answers: Record<string, any>;
  started_at: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface ResourceFilters {
  subject?: number;
  grade?: number;
  strand?: number;
  resource_type?: ResourceType;
  difficulty?: DifficultyLevel;
  difficulty_level?: DifficultyLevel;
  search?: string;
  is_featured?: boolean;
}
