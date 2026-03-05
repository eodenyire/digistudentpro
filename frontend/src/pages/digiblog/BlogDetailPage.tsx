import { useQuery } from '@tanstack/react-query';
import { Link, useParams } from 'react-router-dom';
import { digiblogApi } from '@/api';
import { Button, Card, CardContent, LoadingPage } from '@/components/ui';
import { ArrowLeft, Calendar, Eye, Heart, MessageCircle } from 'lucide-react';
import { formatRelativeTime } from '@/utils/helpers';

function parseTags(tags: string | string[] | undefined): string[] {
  if (!tags) return [];
  if (Array.isArray(tags)) return tags;
  return tags
    .split(',')
    .map((tag) => tag.trim())
    .filter(Boolean);
}

export default function BlogDetailPage() {
  const { slug } = useParams<{ slug: string }>();

  const { data: post, isLoading, isError } = useQuery({
    queryKey: ['blog-post', slug],
    queryFn: () => digiblogApi.getPostBySlug(slug ?? ''),
    enabled: Boolean(slug),
  });

  if (isLoading) return <LoadingPage />;

  if (isError || !post) {
    return (
      <div className="space-y-6">
        <Link
          to="/digiblog"
          className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700"
        >
          <ArrowLeft size={18} />
          Back to DigiBlog
        </Link>

        <Card>
          <CardContent className="p-8 text-center">
            <h1 className="text-2xl font-bold text-secondary-900 mb-2">Post not found</h1>
            <p className="text-secondary-600 mb-6">
              This post may have been removed or the link is incorrect.
            </p>
            <Link to="/digiblog">
              <Button>Return to Blog Feed</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  const tags = parseTags(post.tags);

  return (
    <div className="space-y-6">
      <Link
        to="/digiblog"
        className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700"
      >
        <ArrowLeft size={18} />
        Back to DigiBlog
      </Link>

      <Card>
        {post.featured_image && (
          <div className="w-full max-h-[420px] overflow-hidden rounded-t-lg bg-secondary-100">
            <img src={post.featured_image} alt={post.title} className="w-full h-full object-cover" />
          </div>
        )}

        <CardContent className="p-6 md:p-8">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-xs px-2 py-1 bg-primary-50 text-primary-700 rounded capitalize">
              {post.category}
            </span>
            {post.is_featured && (
              <span className="text-xs px-2 py-1 bg-yellow-50 text-yellow-700 rounded">Featured</span>
            )}
          </div>

          <h1 className="text-3xl font-bold text-secondary-900 mb-4">{post.title}</h1>

          <div className="flex flex-wrap items-center gap-3 text-sm text-secondary-600 mb-6">
            <span>By {post.author_name || 'Anonymous'}</span>
            <span>•</span>
            <span className="inline-flex items-center gap-1">
              <Calendar size={14} />
              {formatRelativeTime(post.created_at)}
            </span>
            <span>•</span>
            <span className="inline-flex items-center gap-1">
              <Eye size={14} />
              {post.views_count ?? 0}
            </span>
            <span className="inline-flex items-center gap-1">
              <Heart size={14} />
              {post.likes_count ?? 0}
            </span>
            <span className="inline-flex items-center gap-1">
              <MessageCircle size={14} />
              {post.comments_count ?? 0}
            </span>
          </div>

          {post.excerpt && (
            <p className="text-lg text-secondary-700 mb-6 border-l-4 border-primary-200 pl-4">
              {post.excerpt}
            </p>
          )}

          <div className="text-secondary-800 whitespace-pre-wrap leading-7">{post.content}</div>

          {tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-8 pt-6 border-t border-secondary-200">
              {tags.map((tag) => (
                <span
                  key={tag}
                  className="text-xs px-2 py-1 bg-secondary-100 text-secondary-700 rounded"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
