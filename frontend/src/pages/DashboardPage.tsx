import { useAuthStore } from '@/store';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui';
import { BookOpen, Trophy, MessageSquare, TrendingUp, Clock, Target } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { digiblogApi, digichatApi, digiguideApi, digilabApi } from '@/api';
import { formatRelativeTime } from '@/utils/helpers';

export default function DashboardPage() {
  const { user } = useAuthStore();

  const { data: careersData } = useQuery({
    queryKey: ['dashboard-careers'],
    queryFn: () => digiguideApi.getCareers(),
  });

  const { data: resourcesData } = useQuery({
    queryKey: ['dashboard-resources'],
    queryFn: () => digilabApi.getResources(),
  });

  const { data: postsData } = useQuery({
    queryKey: ['dashboard-posts'],
    queryFn: () => digiblogApi.getPosts(),
  });

  const { data: squadsData } = useQuery({
    queryKey: ['dashboard-squads'],
    queryFn: () => digichatApi.getSquads(),
  });

  const resourceCount = resourcesData?.count ?? 0;
  const careerCount = careersData?.count ?? 0;
  const postCount = postsData?.count ?? 0;
  const squadCount = squadsData?.count ?? 0;

  const recentResources = resourcesData?.results?.slice(0, 3) ?? [];
  const topCareers = careersData?.results?.slice(0, 3) ?? [];

  const stats = [
    {
      label: 'Resources Available',
      value: String(resourceCount),
      icon: BookOpen,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      label: 'Careers Available',
      value: String(careerCount),
      icon: Trophy,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      label: 'Published Posts',
      value: String(postCount),
      icon: Clock,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
    {
      label: 'Active Squads',
      value: String(squadCount),
      icon: Target,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
    },
  ];

  const quickActions = [
    {
      title: 'Explore Careers',
      description:
        careerCount > 0
          ? `Discover ${careerCount} career paths based on your interests`
          : 'Discover career paths based on your interests',
      href: '/digiguide/careers',
      icon: Target,
      color: 'bg-primary-600',
    },
    {
      title: 'Browse Resources',
      description:
        resourceCount > 0
          ? `Access ${resourceCount} learning resources and assessments`
          : 'Access learning materials and assessments',
      href: '/digilab/browse',
      icon: BookOpen,
      color: 'bg-blue-600',
    },
    {
      title: 'Join Squads',
      description:
        squadCount > 0
          ? `Connect with peers in ${squadCount} active squads`
          : 'Connect with peers and mentors',
      href: '/digichat/squads',
      icon: MessageSquare,
      color: 'bg-green-600',
    },
    {
      title: 'Read Blogs',
      description:
        postCount > 0
          ? `Stay updated with ${postCount} published posts`
          : 'Stay updated with educational content',
      href: '/digiblog',
      icon: TrendingUp,
      color: 'bg-purple-600',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div>
        <h1 className="text-3xl font-bold text-secondary-900">
          Welcome back, {user?.first_name}! 👋
        </h1>
        <p className="text-secondary-600 mt-2">
          Here's what's happening with your learning journey today.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.label}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-secondary-600">{stat.label}</p>
                    <p className="text-3xl font-bold text-secondary-900 mt-2">
                      {stat.value}
                    </p>
                  </div>
                  <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                    <Icon className={stat.color} size={24} />
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-secondary-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action) => {
            const Icon = action.icon;
            return (
              <Link key={action.title} to={action.href}>
                <Card hoverable className="h-full">
                  <CardContent className="p-6">
                    <div className={`w-12 h-12 rounded-lg ${action.color} flex items-center justify-center mb-4`}>
                      <Icon className="text-white" size={24} />
                    </div>
                    <h3 className="font-semibold text-secondary-900 mb-2">
                      {action.title}
                    </h3>
                    <p className="text-sm text-secondary-600">{action.description}</p>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recent Resources</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentResources.length === 0 && (
                <p className="text-sm text-secondary-600">No resources available yet.</p>
              )}
              {recentResources.map((resource) => (
                <div key={resource.id} className="flex items-center gap-4 p-3 bg-secondary-50 rounded-lg">
                  <div className="w-12 h-12 bg-primary-100 rounded flex items-center justify-center">
                    <BookOpen className="text-primary-600" size={20} />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-secondary-900">{resource.title}</p>
                    <p className="text-sm text-secondary-600 capitalize">
                      {resource.resource_type} • {resource.difficulty || resource.difficulty_level || 'beginner'}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Career Highlights</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {topCareers.length === 0 && (
                <p className="text-sm text-secondary-600">No careers available yet.</p>
              )}
              {topCareers.map((career) => (
                <div key={career.id} className="flex items-center gap-4 p-3 bg-secondary-50 rounded-lg">
                  <div className="w-12 h-12 bg-green-100 rounded flex items-center justify-center">
                    <Trophy className="text-green-600" size={20} />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-secondary-900">{career.name}</p>
                    <p className="text-sm text-secondary-600">
                      {career.cluster_name || 'General'}
                    </p>
                  </div>
                  {career.created_at && (
                    <span className="text-xs text-secondary-500">{formatRelativeTime(career.created_at)}</span>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
