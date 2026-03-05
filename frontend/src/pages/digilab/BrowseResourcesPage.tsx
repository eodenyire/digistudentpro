import { useQuery } from '@tanstack/react-query';
import { digilabApi, digiguideApi } from '@/api';
import { Card, CardContent, LoadingPage, Button } from '@/components/ui';
import { BookOpen, Video, FileText, Search } from 'lucide-react';
import { useState } from 'react';
import { LearningResource, ResourceType, DifficultyLevel } from '@/types';

export default function BrowseResourcesPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSubject, setSelectedSubject] = useState<number | undefined>();
  const [selectedType, setSelectedType] = useState<ResourceType | undefined>();
  const [selectedDifficulty, setSelectedDifficulty] = useState<DifficultyLevel | undefined>();

  const { data: resourcesData, isLoading } = useQuery({
    queryKey: ['resources', searchQuery, selectedSubject, selectedType, selectedDifficulty],
    queryFn: () =>
      digilabApi.getResources({
        search: searchQuery || undefined,
        subject: selectedSubject,
        resource_type: selectedType,
        difficulty: selectedDifficulty,
      }),
  });

  const { data: subjects } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => digiguideApi.getSubjects(),
  });

  if (isLoading) return <LoadingPage />;

  const resources = resourcesData?.results || [];

  const getResourceIcon = (type: ResourceType) => {
    switch (type) {
      case 'video':
        return Video;
      case 'document':
      case 'pdf':
        return FileText;
      default:
        return BookOpen;
    }
  };

  const getDifficultyColor = (level: DifficultyLevel) => {
    switch (level) {
      case 'beginner':
        return 'bg-green-100 text-green-700';
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-700';
      case 'advanced':
        return 'bg-red-100 text-red-700';
      default:
        return 'bg-secondary-100 text-secondary-700';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-secondary-900">Browse Learning Resources</h1>
        <p className="text-secondary-600 mt-2">
          Access comprehensive study materials for all subjects
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <div className="space-y-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-secondary-400" size={20} />
            <input
              type="text"
              placeholder="Search resources..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Subject Filter */}
            <select
              value={selectedSubject || ''}
              onChange={(e) => setSelectedSubject(e.target.value ? Number(e.target.value) : undefined)}
              className="px-4 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All Subjects</option>
              {subjects?.map((subject) => (
                <option key={subject.id} value={subject.id}>
                  {subject.name}
                </option>
              ))}
            </select>

            {/* Type Filter */}
            <select
              value={selectedType || ''}
              onChange={(e) => setSelectedType((e.target.value as ResourceType) || undefined)}
              className="px-4 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All Types</option>
              <option value="video">Video</option>
              <option value="document">Document</option>
              <option value="pdf">PDF</option>
              <option value="interactive">Interactive</option>
            </select>

            {/* Difficulty Filter */}
            <select
              value={selectedDifficulty || ''}
              onChange={(e) => setSelectedDifficulty((e.target.value as DifficultyLevel) || undefined)}
              className="px-4 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All Levels</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
        </div>
      </div>

      {/* Resources Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {resources.map((resource: LearningResource) => {
          const Icon = getResourceIcon(resource.resource_type);
          
          return (
            <Card key={resource.id} hoverable>
              <CardContent className="p-0">
                {resource.thumbnail && (
                  <div className="aspect-video bg-secondary-100 rounded-t-lg overflow-hidden">
                    <img
                      src={resource.thumbnail}
                      alt={resource.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}
                
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                      <Icon className="text-primary-600" size={20} />
                    </div>
                    <div className="flex-1">
                      <span className={`text-xs px-2 py-1 rounded ${getDifficultyColor(resource.difficulty || resource.difficulty_level || 'beginner')}`}>
                        {resource.difficulty || resource.difficulty_level || 'beginner'}
                      </span>
                    </div>
                  </div>

                  <h3 className="font-semibold text-secondary-900 mb-2 line-clamp-2">
                    {resource.title}
                  </h3>
                  
                  <p className="text-sm text-secondary-600 mb-4 line-clamp-2">
                    {resource.description}
                  </p>

                  <div className="flex items-center justify-between text-sm text-secondary-500 mb-4">
                    <span className="capitalize">{resource.resource_type}</span>
                    {(resource.duration || resource.duration_minutes) && (
                      <span>{resource.duration || resource.duration_minutes} min</span>
                    )}
                    <span>{resource.view_count || resource.views_count || 0} views</span>
                  </div>

                  <Button className="w-full" size="sm">
                    View Resource
                  </Button>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {resources.length === 0 && (
        <div className="text-center py-12">
          <BookOpen className="mx-auto text-secondary-400 mb-4" size={48} />
          <h3 className="text-lg font-medium text-secondary-900 mb-2">No resources found</h3>
          <p className="text-secondary-600">Try adjusting your search or filters</p>
        </div>
      )}
    </div>
  );
}
