import apiClient from './client';
import {
  Strand,
  SubStrand,
  LearningResource,
  LearningProgress,
  Assessment,
  AssessmentAttempt,
  ResourceFilters,
  PaginatedResponse,
} from '@/types';

export const digilabApi = {
  // Strands
  getStrands: async (params?: { subject?: number; grade?: number }): Promise<Strand[]> => {
    const response = await apiClient.get('/digilab/strands/', { params });
    return response.data.results || response.data;
  },

  getStrandById: async (id: number): Promise<Strand> => {
    const response = await apiClient.get(`/digilab/strands/${id}/`);
    return response.data;
  },

  // Sub-Strands
  getSubStrands: async (strandId?: number): Promise<SubStrand[]> => {
    const params = strandId ? { strand: strandId } : {};
    const response = await apiClient.get('/digilab/sub-strands/', { params });
    return response.data.results || response.data;
  },

  getSubStrandById: async (id: number): Promise<SubStrand> => {
    const response = await apiClient.get(`/digilab/sub-strands/${id}/`);
    return response.data;
  },

  // Learning Resources
  getResources: async (filters?: ResourceFilters, page?: number): Promise<PaginatedResponse<LearningResource>> => {
    const response = await apiClient.get('/digilab/learning-resources/', {
      params: { ...filters, page },
    });
    return response.data;
  },

  getResourceById: async (id: number): Promise<LearningResource> => {
    const response = await apiClient.get(`/digilab/learning-resources/${id}/`);
    return response.data;
  },

  searchResources: async (query: string): Promise<LearningResource[]> => {
    const response = await apiClient.get('/digilab/learning-resources/', {
      params: { search: query },
    });
    return response.data.results || response.data;
  },

  getFeaturedResources: async (): Promise<LearningResource[]> => {
    const response = await apiClient.get('/digilab/learning-resources/', {
      params: { is_featured: true },
    });
    return response.data.results || response.data;
  },

  incrementResourceView: async (id: number): Promise<void> => {
    await apiClient.post(`/digilab/learning-resources/${id}/increment_view/`);
  },

  // Learning Progress
  getProgress: async (studentId?: number): Promise<LearningProgress[]> => {
    const params = studentId ? { student: studentId } : {};
    const response = await apiClient.get('/digilab/learning-progress/', { params });
    return response.data.results || response.data;
  },

  getResourceProgress: async (resourceId: number): Promise<LearningProgress> => {
    const response = await apiClient.get('/digilab/learning-progress/', {
      params: { resource: resourceId },
    });
    const results = response.data.results || response.data;
    return results[0];
  },

  updateProgress: async (
    resourceId: number,
    data: { progress_percentage?: number; time_spent?: number; completed?: boolean; notes?: string }
  ): Promise<LearningProgress> => {
    const response = await apiClient.post('/digilab/learning-progress/', {
      resource: resourceId,
      ...data,
    });
    return response.data;
  },

  toggleBookmark: async (resourceId: number): Promise<LearningProgress> => {
    const response = await apiClient.post(`/digilab/learning-progress/${resourceId}/toggle_bookmark/`);
    return response.data;
  },

  getBookmarkedResources: async (): Promise<LearningResource[]> => {
    const response = await apiClient.get('/digilab/learning-progress/', {
      params: { bookmarked: true },
    });
    return response.data.results || response.data;
  },

  // Assessments
  getAssessments: async (params?: { sub_strand?: number; difficulty_level?: string }): Promise<Assessment[]> => {
    const response = await apiClient.get('/digilab/assessments/', { params });
    return response.data.results || response.data;
  },

  getAssessmentById: async (id: number): Promise<Assessment> => {
    const response = await apiClient.get(`/digilab/assessments/${id}/`);
    return response.data;
  },

  getAssessmentQuestions: async (assessmentId: number): Promise<any[]> => {
    const response = await apiClient.get(`/digilab/assessments/${assessmentId}/questions/`);
    return response.data;
  },

  // Assessment Attempts
  getAttempts: async (studentId?: number, assessmentId?: number): Promise<AssessmentAttempt[]> => {
    const params: any = {};
    if (studentId) params.student = studentId;
    if (assessmentId) params.assessment = assessmentId;
    
    const response = await apiClient.get('/digilab/assessment-attempts/', { params });
    return response.data.results || response.data;
  },

  startAssessment: async (assessmentId: number): Promise<AssessmentAttempt> => {
    const response = await apiClient.post('/digilab/assessment-attempts/', {
      assessment: assessmentId,
      started_at: new Date().toISOString(),
    });
    return response.data;
  },

  submitAssessment: async (
    attemptId: number,
    answers: Record<string, any>
  ): Promise<AssessmentAttempt> => {
    const response = await apiClient.patch(`/digilab/assessment-attempts/${attemptId}/`, {
      answers,
      completed_at: new Date().toISOString(),
    });
    return response.data;
  },

  // Dashboard Stats
  getDashboardStats: async (): Promise<any> => {
    const response = await apiClient.get('/digilab/dashboard/stats/');
    return response.data;
  },
};
