// DigiBlog Module Types

export type BlogCategory =
  | 'study_hacks'
  | 'mental_health'
  | 'scholarships'
  | 'cbc_updates'
  | 'tech'
  | 'career_guidance';

export interface BlogPost {
  id: number;
  author: number;
  author_name?: string;
  author_avatar?: string;
  title: string;
  slug: string;
  content: string;
  excerpt?: string;
  featured_image?: string;
  category: BlogCategory;
  tags: string | string[];
  status?: 'draft' | 'published' | 'archived';
  is_published?: boolean;
  is_featured: boolean;
  view_count?: number;
  like_count?: number;
  comment_count?: number;
  views_count?: number;
  likes_count?: number;
  comments_count?: number;
  reading_time?: number;
  published_at?: string;
  created_at: string;
  updated_at: string;
}

export interface Comment {
  id: number;
  post: number;
  author: number;
  author_name?: string;
  author_avatar?: string;
  content: string;
  parent?: number;
  replies?: Comment[];
  like_count: number;
  is_edited: boolean;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

export interface Like {
  id: number;
  user: number;
  post?: number;
  comment?: number;
  created_at: string;
}

export interface Follow {
  id: number;
  follower: number;
  following: number;
  created_at: string;
}

export interface BlogFilters {
  category?: BlogCategory;
  tags?: string[];
  author?: number;
  search?: string;
  is_featured?: boolean;
  ordering?: 'latest' | 'popular' | 'trending';
}

export interface AuthorProfile {
  id: number;
  name: string;
  avatar?: string;
  bio?: string;
  post_count: number;
  follower_count: number;
  following_count: number;
  is_followed?: boolean;
}
