import apiClient from './client';
import {
  EducationLevel,
  Grade,
  Subject,
  Cluster,
  Career,
  AcademicRecord,
  CareerPrediction,
  PaginatedResponse,
} from '@/types';

export const digiguideApi = {
  // Education Levels
  getEducationLevels: async (): Promise<EducationLevel[]> => {
    const response = await apiClient.get('/digiguide/education-levels/');
    return response.data.results || response.data;
  },

  // Grades
  getGrades: async (educationLevelId?: number): Promise<Grade[]> => {
    const params = educationLevelId ? { education_level: educationLevelId } : {};
    const response = await apiClient.get('/digiguide/grades/', { params });
    return response.data.results || response.data;
  },

  getGradeById: async (id: number): Promise<Grade> => {
    const response = await apiClient.get(`/digiguide/grades/${id}/`);
    return response.data;
  },

  // Subjects
  getSubjects: async (params?: { education_level?: number; grade?: number }): Promise<Subject[]> => {
    const response = await apiClient.get('/digiguide/subjects/', { params });
    return response.data.results || response.data;
  },

  getSubjectById: async (id: number): Promise<Subject> => {
    const response = await apiClient.get(`/digiguide/subjects/${id}/`);
    return response.data;
  },

  // Clusters
  getClusters: async (): Promise<Cluster[]> => {
    const response = await apiClient.get('/digiguide/clusters/');
    return response.data.results || response.data;
  },

  getClusterById: async (id: number): Promise<Cluster> => {
    const response = await apiClient.get(`/digiguide/clusters/${id}/`);
    return response.data;
  },

  // Careers
  getCareers: async (params?: {
    cluster?: number;
    subject?: number;
    search?: string;
  }): Promise<PaginatedResponse<Career>> => {
    const response = await apiClient.get('/digiguide/careers/', { params });
    return response.data;
  },

  getCareerById: async (id: number): Promise<Career> => {
    const response = await apiClient.get(`/digiguide/careers/${id}/`);
    return response.data;
  },

  searchCareers: async (query: string): Promise<Career[]> => {
    const response = await apiClient.get('/digiguide/careers/', {
      params: { search: query },
    });
    return response.data.results || response.data;
  },

  // Academic Records
  getAcademicRecords: async (studentId?: number): Promise<AcademicRecord[]> => {
    const params = studentId ? { student: studentId } : {};
    const response = await apiClient.get('/digiguide/academic-records/', { params });
    return response.data.results || response.data;
  },

  createAcademicRecord: async (data: Omit<AcademicRecord, 'id' | 'created_at' | 'updated_at'>): Promise<AcademicRecord> => {
    const response = await apiClient.post('/digiguide/academic-records/', data);
    return response.data;
  },

  updateAcademicRecord: async (id: number, data: Partial<AcademicRecord>): Promise<AcademicRecord> => {
    const response = await apiClient.patch(`/digiguide/academic-records/${id}/`, data);
    return response.data;
  },

  deleteAcademicRecord: async (id: number): Promise<void> => {
    await apiClient.delete(`/digiguide/academic-records/${id}/`);
  },

  // Career Predictions
  getCareerPredictions: async (studentId?: number): Promise<CareerPrediction[]> => {
    const params = studentId ? { student: studentId } : {};
    const response = await apiClient.get('/digiguide/career-predictions/', { params });
    return response.data.results || response.data;
  },

  generateCareerPrediction: async (studentId: number): Promise<CareerPrediction[]> => {
    const response = await apiClient.post('/digiguide/career-predictions/generate/', {
      student_id: studentId,
    });
    return response.data;
  },

  // Performance Analytics
  getPerformanceAnalytics: async (studentId: number): Promise<any> => {
    const response = await apiClient.get(`/digiguide/students/${studentId}/performance/`);
    return response.data;
  },
};
