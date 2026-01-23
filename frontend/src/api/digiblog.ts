import apiClient from './client';
import {
  BlogPost,
  Comment,
  Like,
  Follow,
  BlogFilters,
  AuthorProfile,
  PaginatedResponse,
} from '@/types';

export const digiblogApi = {
  // Blog Posts
  getPosts: async (filters?: BlogFilters, page?: number): Promise<PaginatedResponse<BlogPost>> => {
    const response = await apiClient.get('/digiblog/posts/', {
      params: { ...filters, page },
    });
    return response.data;
  },

  getPostById: async (id: number): Promise<BlogPost> => {
    const response = await apiClient.get(`/digiblog/posts/${id}/`);
    return response.data;
  },

  getPostBySlug: async (slug: string): Promise<BlogPost> => {
    const response = await apiClient.get('/digiblog/posts/', {
      params: { slug },
    });
    const results = response.data.results || response.data;
    return results[0];
  },

  createPost: async (data: {
    title: string;
    content: string;
    excerpt?: string;
    category: string;
    tags?: string[];
    featured_image?: File;
  }): Promise<BlogPost> => {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined) {
        if (Array.isArray(value)) {
          value.forEach(item => formData.append(key, item));
        } else {
          formData.append(key, value);
        }
      }
    });

    const response = await apiClient.post('/digiblog/posts/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  updatePost: async (id: number, data: Partial<BlogPost>): Promise<BlogPost> => {
    const response = await apiClient.patch(`/digiblog/posts/${id}/`, data);
    return response.data;
  },

  deletePost: async (id: number): Promise<void> => {
    await apiClient.delete(`/digiblog/posts/${id}/`);
  },

  publishPost: async (id: number): Promise<BlogPost> => {
    const response = await apiClient.post(`/digiblog/posts/${id}/publish/`);
    return response.data;
  },

  incrementViewCount: async (id: number): Promise<void> => {
    await apiClient.post(`/digiblog/posts/${id}/increment_views/`);
  },

  // Comments
  getComments: async (postId: number): Promise<Comment[]> => {
    const response = await apiClient.get('/digiblog/comments/', {
      params: { post: postId },
    });
    return response.data.results || response.data;
  },

  createComment: async (postId: number, content: string, parentId?: number): Promise<Comment> => {
    const response = await apiClient.post('/digiblog/comments/', {
      post: postId,
      content,
      parent: parentId,
    });
    return response.data;
  },

  updateComment: async (id: number, content: string): Promise<Comment> => {
    const response = await apiClient.patch(`/digiblog/comments/${id}/`, {
      content,
      is_edited: true,
    });
    return response.data;
  },

  deleteComment: async (id: number): Promise<void> => {
    await apiClient.delete(`/digiblog/comments/${id}/`);
  },

  // Likes
  likePost: async (postId: number): Promise<Like> => {
    const response = await apiClient.post('/digiblog/likes/', { post: postId });
    return response.data;
  },

  unlikePost: async (likeId: number): Promise<void> => {
    await apiClient.delete(`/digiblog/likes/${likeId}/`);
  },

  likeComment: async (commentId: number): Promise<Like> => {
    const response = await apiClient.post('/digiblog/likes/', { comment: commentId });
    return response.data;
  },

  getPostLikes: async (postId: number): Promise<Like[]> => {
    const response = await apiClient.get('/digiblog/likes/', {
      params: { post: postId },
    });
    return response.data.results || response.data;
  },

  // Follows
  followUser: async (userId: number): Promise<Follow> => {
    const response = await apiClient.post('/digiblog/follows/', { following: userId });
    return response.data;
  },

  unfollowUser: async (followId: number): Promise<void> => {
    await apiClient.delete(`/digiblog/follows/${followId}/`);
  },

  getFollowers: async (userId: number): Promise<Follow[]> => {
    const response = await apiClient.get('/digiblog/follows/', {
      params: { following: userId },
    });
    return response.data.results || response.data;
  },

  getFollowing: async (userId: number): Promise<Follow[]> => {
    const response = await apiClient.get('/digiblog/follows/', {
      params: { follower: userId },
    });
    return response.data.results || response.data;
  },

  // Author Profile
  getAuthorProfile: async (userId: number): Promise<AuthorProfile> => {
    const response = await apiClient.get(`/digiblog/authors/${userId}/`);
    return response.data;
  },

  getAuthorPosts: async (userId: number, page?: number): Promise<PaginatedResponse<BlogPost>> => {
    const response = await apiClient.get('/digiblog/posts/', {
      params: { author: userId, page },
    });
    return response.data;
  },

  // Featured & Trending
  getFeaturedPosts: async (): Promise<BlogPost[]> => {
    const response = await apiClient.get('/digiblog/posts/', {
      params: { is_featured: true },
    });
    return response.data.results || response.data;
  },

  getTrendingPosts: async (): Promise<BlogPost[]> => {
    const response = await apiClient.get('/digiblog/posts/trending/');
    return response.data;
  },
};
