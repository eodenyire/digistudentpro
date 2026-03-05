import { useQuery } from '@tanstack/react-query';
import { digiguideApi } from '@/api';
import { Card, CardContent, LoadingPage, Button } from '@/components/ui';
import { Search, Briefcase, TrendingUp, DollarSign } from 'lucide-react';
import { useState } from 'react';
import { Career } from '@/types';

function parseList(value: string | string[] | undefined): string[] {
  if (!value) return [];
  if (Array.isArray(value)) return value;
  return value
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

export default function CareersPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCluster, setSelectedCluster] = useState<number | undefined>();

  const { data: careersData, isLoading } = useQuery({
    queryKey: ['careers', selectedCluster, searchQuery],
    queryFn: () =>
      digiguideApi.getCareers({
        cluster: selectedCluster,
        search: searchQuery || undefined,
      }),
  });

  const { data: clusters } = useQuery({
    queryKey: ['clusters'],
    queryFn: () => digiguideApi.getClusters(),
  });

  if (isLoading) return <LoadingPage />;

  const careers = careersData?.results || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-secondary-900">Career Explorer</h1>
        <p className="text-secondary-600 mt-2">
          Discover career paths aligned with Kenya CBC curriculum
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-secondary-400" size={20} />
            <input
              type="text"
              placeholder="Search careers..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {/* Cluster Filter */}
          <select
            value={selectedCluster || ''}
            onChange={(e) => setSelectedCluster(e.target.value ? Number(e.target.value) : undefined)}
            className="px-4 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">All Clusters</option>
            {clusters?.map((cluster) => (
              <option key={cluster.id} value={cluster.id}>
                {cluster.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Careers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {careers.map((career: Career) => (
          <Card key={career.id} hoverable>
            <CardContent className="p-6">
              <div className="flex items-start gap-3 mb-4">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Briefcase className="text-primary-600" size={24} />
                </div>
                <div>
                  <h3 className="font-semibold text-secondary-900">{career.name}</h3>
                  {career.cluster_name && (
                    <p className="text-xs text-secondary-500 mt-1">{career.cluster_name}</p>
                  )}
                  {career.salary_range && (
                    <p className="text-sm text-secondary-600 flex items-center gap-1 mt-1">
                      <DollarSign size={14} />
                      {career.salary_range}
                    </p>
                  )}
                </div>
              </div>

              <p className="text-sm text-secondary-600 mb-4 line-clamp-3">
                {career.description}
              </p>

              {career.job_outlook && (
                <div className="flex items-center gap-2 text-sm mb-4">
                  <TrendingUp size={16} className="text-green-600" />
                  <span className="text-secondary-700">{career.job_outlook}</span>
                </div>
              )}

              {parseList(career.skills_needed).length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {parseList(career.skills_needed).slice(0, 3).map((skill, idx) => (
                    <span
                      key={idx}
                      className="text-xs px-2 py-1 bg-primary-50 text-primary-700 rounded"
                    >
                      {skill}
                    </span>
                  ))}
                  {parseList(career.skills_needed).length > 3 && (
                    <span className="text-xs px-2 py-1 bg-secondary-100 text-secondary-600 rounded">
                      +{parseList(career.skills_needed).length - 3} more
                    </span>
                  )}
                </div>
              )}

              <Button className="w-full" size="sm">
                View Details
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {careers.length === 0 && (
        <div className="text-center py-12">
          <Briefcase className="mx-auto text-secondary-400 mb-4" size={48} />
          <h3 className="text-lg font-medium text-secondary-900 mb-2">No careers found</h3>
          <p className="text-secondary-600">Try adjusting your search or filters</p>
        </div>
      )}
    </div>
  );
}
