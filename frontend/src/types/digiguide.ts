// DigiGuide Module Types

export interface EducationLevel {
  id: number;
  name: string;
  description?: string;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface Grade {
  id: number;
  education_level: number;
  name: string;
  description?: string;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface Subject {
  id: number;
  name: string;
  code: string;
  description?: string;
  icon?: string;
  color?: string;
  education_level?: number;
  created_at: string;
  updated_at: string;
}

export interface Cluster {
  id: number;
  name: string;
  code: string;
  description?: string;
  subjects: number[];
  created_at: string;
  updated_at: string;
}

export interface Career {
  id: number;
  name: string;
  description?: string;
  cluster?: number;
  cluster_name?: string;
  clusters?: number[];
  required_subjects: number[];
  minimum_grades: Record<string, string>;
  salary_range?: string;
  job_outlook?: string;
  required_qualifications?: string;
  skills_needed: string | string[];
  career_path?: string;
  work_environment?: string;
  created_at: string;
  updated_at: string;
}

export interface AcademicRecord {
  id: number;
  student: number;
  subject: number;
  grade: string;
  marks?: number;
  term: string;
  year: number;
  comments?: string;
  created_at: string;
  updated_at: string;
}

export interface CareerPrediction {
  id: number;
  student: number;
  career: number;
  match_score: number;
  strengths: string[];
  improvement_areas: string[];
  predicted_success_rate: number;
  recommendations: string[];
  created_at: string;
  updated_at: string;
}

export interface SubjectPerformance {
  subject: Subject;
  current_grade: string;
  marks: number;
  trend: 'improving' | 'stable' | 'declining';
  recommendations: string[];
}

export interface CareerRecommendation {
  career: Career;
  match_percentage: number;
  required_grades: Record<string, string>;
  current_grades: Record<string, string>;
  gaps: string[];
  strengths: string[];
}
