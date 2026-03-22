import apiClient from './client';
import {
  Squad,
  SquadMembership,
  Message,
  DirectMessage,
  Conversation,
  PaginatedResponse,
} from '@/types';

export const digichatApi = {
  // Squads (Group Chats)
  getSquads: async (page?: number): Promise<PaginatedResponse<Squad>> => {
    const response = await apiClient.get('/digichat/squads/', { params: { page } });
    return response.data;
  },

  getSquadById: async (identifier: number | string): Promise<Squad> => {
    const response = await apiClient.get(`/digichat/squads/${identifier}/`);
    return response.data;
  },

  createSquad: async (data: {
    name: string;
    description?: string;
    topic?: string;
    is_public?: boolean;
  }): Promise<Squad> => {
    const response = await apiClient.post('/digichat/squads/', data);
    return response.data;
  },

  updateSquad: async (id: number, data: Partial<Squad>): Promise<Squad> => {
    const response = await apiClient.patch(`/digichat/squads/${id}/`, data);
    return response.data;
  },

  deleteSquad: async (id: number): Promise<void> => {
    await apiClient.delete(`/digichat/squads/${id}/`);
  },

  joinSquad: async (slug: string): Promise<SquadMembership> => {
    const response = await apiClient.post(`/digichat/squads/${slug}/join/`);
    return response.data;
  },

  leaveSquad: async (slug: string): Promise<void> => {
    await apiClient.post(`/digichat/squads/${slug}/leave/`);
  },

  // Squad Memberships
  getSquadMembers: async (squadId: number): Promise<SquadMembership[]> => {
    const response = await apiClient.get('/digichat/memberships/', {
      params: { squad: squadId },
    });
    return response.data.results || response.data;
  },

  updateMemberRole: async (
    membershipId: number,
    role: 'admin' | 'moderator' | 'member'
  ): Promise<SquadMembership> => {
    const response = await apiClient.patch(`/digichat/memberships/${membershipId}/`, { role });
    return response.data;
  },

  removeMember: async (membershipId: number): Promise<void> => {
    await apiClient.delete(`/digichat/memberships/${membershipId}/`);
  },

  // Squad Messages
  getSquadMessages: async (squadId: number, page?: number): Promise<PaginatedResponse<Message>> => {
    const response = await apiClient.get('/digichat/messages/', {
      params: { squad: squadId, page },
    });
    return response.data;
  },

  sendSquadMessage: async (squadId: number, content: string, replyTo?: number): Promise<Message> => {
    const response = await apiClient.post('/digichat/messages/', {
      squad: squadId,
      content,
      replied_to: replyTo,
    });
    return response.data;
  },

  updateMessage: async (id: number, content: string): Promise<Message> => {
    const response = await apiClient.patch(`/digichat/messages/${id}/`, {
      content,
      is_edited: true,
    });
    return response.data;
  },

  deleteMessage: async (id: number): Promise<void> => {
    await apiClient.delete(`/digichat/messages/${id}/`);
  },

  addReaction: async (messageId: number, emoji: string): Promise<Message> => {
    const response = await apiClient.post(`/digichat/messages/${messageId}/react/`, { emoji });
    return response.data;
  },

  // Direct Messages
  getConversations: async (): Promise<Conversation[]> => {
    const response = await apiClient.get('/digichat/conversations/');
    return response.data;
  },

  getDirectMessages: async (userId: number, page?: number): Promise<PaginatedResponse<DirectMessage>> => {
    const response = await apiClient.get('/digichat/direct-messages/', {
      params: { user: userId, page },
    });
    return response.data;
  },

  sendDirectMessage: async (receiverId: number, content: string): Promise<DirectMessage> => {
    const response = await apiClient.post('/digichat/direct-messages/', {
      receiver: receiverId,
      content,
    });
    return response.data;
  },

  markAsRead: async (messageId: number): Promise<void> => {
    await apiClient.patch(`/digichat/direct-messages/${messageId}/`, { is_read: true });
  },

  deleteDirectMessage: async (id: number): Promise<void> => {
    await apiClient.delete(`/digichat/direct-messages/${id}/`);
  },

  // Search
  searchSquads: async (query: string): Promise<Squad[]> => {
    const response = await apiClient.get('/digichat/squads/', {
      params: { search: query },
    });
    return response.data.results || response.data;
  },

  searchMessages: async (squadId: number, query: string): Promise<Message[]> => {
    const response = await apiClient.get('/digichat/messages/', {
      params: { squad: squadId, search: query },
    });
    return response.data.results || response.data;
  },
};
