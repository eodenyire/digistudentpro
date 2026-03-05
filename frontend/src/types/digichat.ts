// DigiChat Module Types

export interface Squad {
  id: number;
  name: string;
  slug: string;
  description?: string;
  topic?: string;
  avatar?: string;
  is_public: boolean;
  is_member?: boolean;
  created_by: number;
  member_count: number;
  last_message?: string;
  last_message_at?: string;
  created_at: string;
  updated_at: string;
}

export interface SquadMembership {
  id: number;
  squad: number;
  user: number;
  role: 'admin' | 'moderator' | 'member';
  joined_at: string;
  is_muted?: boolean;
}

export interface Message {
  id: number;
  squad: number;
  sender: number;
  sender_name?: string;
  sender_avatar?: string;
  content: string;
  attachments: string[];
  replied_to?: number;
  is_edited: boolean;
  is_deleted: boolean;
  reactions: Record<string, number>;
  created_at: string;
  updated_at: string;
}

export interface DirectMessage {
  id: number;
  sender: number;
  receiver: number;
  sender_name?: string;
  sender_avatar?: string;
  content: string;
  attachments: string[];
  is_read: boolean;
  is_edited: boolean;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

export interface MessageReport {
  id: number;
  message?: number;
  direct_message?: number;
  reported_by: number;
  reason: string;
  description?: string;
  status: 'pending' | 'reviewed' | 'resolved' | 'dismissed';
  created_at: string;
  updated_at: string;
}

export interface Conversation {
  id: number;
  participant: number;
  participant_name: string;
  participant_avatar?: string;
  last_message: string;
  last_message_at: string;
  unread_count: number;
  is_online?: boolean;
}

export interface ChatNotification {
  type: 'message' | 'mention' | 'squad_invite';
  squad_id?: number;
  sender: string;
  content: string;
  timestamp: string;
}
