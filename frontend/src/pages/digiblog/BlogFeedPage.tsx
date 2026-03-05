import { useQuery } from '@tanstack/react-query';
import { digiblogApi } from '@/api';
import { Card, CardContent, LoadingPage, Button } from '@/components/ui';
import { FileText, Heart, MessageCircle, Eye, Plus, Search } from 'lucide-react';
import { useState } from 'react';
import { BlogPost, BlogCategory } from '@/types';
import { formatRelativeTime } from '@/utils/helpers';

function parseTags(tags: string | string[] | undefined): string[] {
  if (!tags) return [];
  if (Array.isArray(tags)) return tags;
  return tags
    .split(',')
    .map((tag) => tag.trim())
    .filter(Boolean);
}

export default function BlogFeedPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<BlogCategory | undefined>();

  const { data: postsData, isLoading } = useQuery({
    queryKey: ['blog-posts', searchQuery, selectedCategory],
    queryFn: () =>
      digiblogApi.getPosts({
        search: searchQuery || undefined,
        category: selectedCategory,
      }),
  });

  if (isLoading) return <LoadingPage />;

  const posts = postsData?.results || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">DigiBlog</h1>
          <p className="text-secondary-600 mt-2">Read and share educational content</p>
        </div>
        <Button className="gap-2">
          <Plus size={20} />
          Write Post
        </Button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-secondary-400" size={20} />
            <input
              type="text"
              placeholder="Search posts..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <select
            value={selectedCategory || ''}
            onChange={(e) => setSelectedCategory((e.target.value as BlogCategory) || undefined)}
            className="px-4 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">All Categories</option>
            <option value="study_hacks">Study Hacks</option>
            <option value="mental_health">Mental Health</option>
            <option value="scholarships">Scholarships</option>
            <option value="cbc_updates">CBC Updates</option>
            <option value="tech">Tech in Schools</option>
            <option value="career_guidance">Career Guidance</option>
          </select>
        </div>
      </div>

      {/* Posts List */}
      <div className="space-y-6">
        {posts.map((post: BlogPost) => (
          <Card key={post.id} hoverable>
            <CardContent className="p-0">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-0">
                {/* Image */}
                {post.featured_image && (
                  <div className="aspect-video md:aspect-auto bg-secondary-100 overflow-hidden rounded-t-lg md:rounded-l-lg md:rounded-tr-none">
                    <img
                      src={post.featured_image}
                      alt={post.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}

                {/* Content */}
                <div className={`p-6 ${post.featured_image ? 'md:col-span-2' : 'md:col-span-3'}`}>
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xs px-2 py-1 bg-primary-50 text-primary-700 rounded capitalize">
                      {post.category}
                    </span>
                    {post.is_featured && (
                      <span className="text-xs px-2 py-1 bg-yellow-50 text-yellow-700 rounded">
                        Featured
                      </span>
                    )}
                  </div>

                  <h2 className="text-2xl font-bold text-secondary-900 mb-2 hover:text-primary-600 cursor-pointer">
                    {post.title}
                  </h2>

                  <div className="flex items-center gap-4 text-sm text-secondary-600 mb-3">
                    <span>By {post.author_name || 'Anonymous'}</span>
                    <span>•</span>
                    <span>{formatRelativeTime(post.created_at)}</span>
                    {post.reading_time && (
                      <>
                        <span>•</span>
                        <span>{post.reading_time} min read</span>
                      </>
                    )}
                  </div>

                  <p className="text-secondary-600 mb-4 line-clamp-3">
                    {post.excerpt || post.content.substring(0, 200) + '...'}
                  </p>

                  {parseTags(post.tags).length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-4">
                      {parseTags(post.tags).slice(0, 5).map((tag, idx) => (
                        <span
                          key={idx}
                          className="text-xs px-2 py-1 bg-secondary-100 text-secondary-600 rounded"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  )}

                  <div className="flex items-center justify-between pt-4 border-t border-secondary-200">
                    <div className="flex items-center gap-4 text-sm text-secondary-600">
                      <span className="flex items-center gap-1">
                        <Heart size={16} />
                        {post.likes_count ?? 0}
                      </span>
                      <span className="flex items-center gap-1">
                        <MessageCircle size={16} />
                        {post.comments_count ?? 0}
                      </span>
                      <span className="flex items-center gap-1">
                        <Eye size={16} />
                        {post.views_count ?? 0}
                      </span>
                    </div>
                    <Button size="sm" variant="ghost">
                      Read More
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {posts.length === 0 && (
        <div className="text-center py-12">
          <FileText className="mx-auto text-secondary-400 mb-4" size={48} />
          <h3 className="text-lg font-medium text-secondary-900 mb-2">No posts found</h3>
          <p className="text-secondary-600">
            {searchQuery ? 'Try a different search term' : 'Be the first to write a post!'}
          </p>
        </div>
      )}
    </div>
  );
}
