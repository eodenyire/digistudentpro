import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  BookOpen,
  ClipboardCheck,
  ExternalLink,
  FileText,
  Headphones,
  Image as ImageIcon,
  Search,
  Video,
} from 'lucide-react';
import { Card, CardContent, LoadingPage, Button } from '@/components/ui';
import { digilabApi, digiguideApi } from '@/api';
import { useUIStore } from '@/store';
import { LearningResource, ResourceType, DifficultyLevel } from '@/types';

const SAMPLE_PDF_PATH = '/samples/sample-study-note.pdf';
const BACKEND_ORIGIN = import.meta.env.VITE_BACKEND_ORIGIN || 'http://localhost:8000';

function normalizeMediaUrl(url?: string): string | undefined {
  if (!url) return undefined;
  if (url.startsWith('http://') || url.startsWith('https://')) return url;
  if (url.startsWith('/media/')) return `${BACKEND_ORIGIN}${url}`;
  if (url.startsWith('media/')) return `${BACKEND_ORIGIN}/${url}`;
  if (url.startsWith('/')) return url;
  return `${BACKEND_ORIGIN}/${url}`;
}

function isImageUrl(url?: string): boolean {
  if (!url) return false;
  return /\.(jpg|jpeg|png|gif|webp|svg)(\?.*)?$/i.test(url);
}

function isDirectVideoUrl(url?: string): boolean {
  if (!url) return false;
  return /\.(mp4|webm|ogg)(\?.*)?$/i.test(url);
}

function isDirectAudioUrl(url?: string): boolean {
  if (!url) return false;
  return /\.(mp3|wav|ogg|m4a)(\?.*)?$/i.test(url);
}

function stripHtml(value: string): string {
  return value.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
}

function getResourceUrl(resource: LearningResource): string | undefined {
  const fileUrl = normalizeMediaUrl(resource.file);
  if (fileUrl) return fileUrl;

  const externalUrl = normalizeMediaUrl(resource.external_url);
  if (externalUrl) return externalUrl;

  if (resource.resource_type === 'pdf' || resource.resource_type === 'text') {
    return SAMPLE_PDF_PATH;
  }

  return undefined;
}

export default function BrowseResourcesPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSubject, setSelectedSubject] = useState<number | undefined>();
  const [selectedType, setSelectedType] = useState<ResourceType | undefined>();
  const [selectedDifficulty, setSelectedDifficulty] = useState<DifficultyLevel | undefined>();

  const { addNotification } = useUIStore();

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
      case 'audio':
        return Headphones;
      case 'pdf':
      case 'text':
        return FileText;
      case 'assessment':
        return ClipboardCheck;
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

  const getActionLabel = (resourceType: ResourceType) => {
    switch (resourceType) {
      case 'video':
        return 'Watch Video';
      case 'audio':
        return 'Play Audio';
      case 'pdf':
        return 'Open PDF';
      case 'text':
        return 'Read Notes';
      case 'assessment':
        return 'Open Assessment';
      default:
        return 'Open Resource';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-secondary-900">Browse Learning Resources</h1>
        <p className="text-secondary-600 mt-2">
          Access videos, text notes, audio content, PDFs, assessments, and visual resources.
        </p>
      </div>

      <div className="bg-white rounded-lg p-6 shadow-sm">
        <div className="space-y-4">
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

            <select
              value={selectedType || ''}
              onChange={(e) => setSelectedType((e.target.value as ResourceType) || undefined)}
              className="px-4 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All Types</option>
              <option value="video">Video</option>
              <option value="text">Text Notes</option>
              <option value="audio">Audio</option>
              <option value="pdf">PDF</option>
              <option value="assessment">Assessment</option>
            </select>

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

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {resources.map((resource: LearningResource) => {
          const Icon = getResourceIcon(resource.resource_type);
          const resourceUrl = getResourceUrl(resource);
          const thumbnailUrl = normalizeMediaUrl(resource.thumbnail);
          const difficulty = resource.difficulty || resource.difficulty_level || 'beginner';
          const plainTextPreview = resource.content ? stripHtml(resource.content).slice(0, 180) : '';

          return (
            <Card key={resource.id} hoverable>
              <CardContent className="p-0">
                {thumbnailUrl && (
                  <div className="aspect-video bg-secondary-100 rounded-t-lg overflow-hidden">
                    <img
                      src={thumbnailUrl}
                      alt={resource.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}

                <div className="p-6 space-y-3">
                  <div className="flex items-center gap-2">
                    <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                      <Icon className="text-primary-600" size={20} />
                    </div>
                    <div className="flex-1">
                      <span className={`text-xs px-2 py-1 rounded ${getDifficultyColor(difficulty)}`}>
                        {difficulty}
                      </span>
                    </div>
                  </div>

                  <h3 className="font-semibold text-secondary-900 line-clamp-2">{resource.title}</h3>

                  <p className="text-sm text-secondary-600 line-clamp-2">{resource.description}</p>

                  {resource.resource_type === 'audio' && resourceUrl && isDirectAudioUrl(resourceUrl) && (
                    <audio controls className="w-full">
                      <source src={resourceUrl} />
                    </audio>
                  )}

                  {resource.resource_type === 'video' && resourceUrl && isDirectVideoUrl(resourceUrl) && (
                    <video controls className="w-full rounded-lg bg-black/90" preload="none">
                      <source src={resourceUrl} />
                    </video>
                  )}

                  {!thumbnailUrl && isImageUrl(resourceUrl) && resourceUrl && (
                    <div className="rounded-lg overflow-hidden border border-secondary-200">
                      <img src={resourceUrl} alt={resource.title} className="w-full h-40 object-cover" />
                    </div>
                  )}

                  {resource.resource_type === 'text' && plainTextPreview && (
                    <div className="rounded-lg border border-secondary-200 bg-secondary-50 p-3 text-sm text-secondary-700">
                      {plainTextPreview}...
                    </div>
                  )}

                  <div className="flex items-center justify-between text-sm text-secondary-500">
                    <span className="capitalize">{resource.resource_type}</span>
                    {(resource.duration || resource.duration_minutes) && (
                      <span>{resource.duration || resource.duration_minutes} min</span>
                    )}
                    <span>{resource.view_count || resource.views_count || 0} views</span>
                  </div>

                  {resourceUrl ? (
                    <a href={resourceUrl} target="_blank" rel="noreferrer" className="block">
                      <Button className="w-full" size="sm">
                        {getActionLabel(resource.resource_type)}
                        <ExternalLink size={14} className="ml-2" />
                      </Button>
                    </a>
                  ) : (
                    <Button
                      className="w-full"
                      size="sm"
                      variant="outline"
                      onClick={() =>
                        addNotification({
                          type: 'info',
                          title: 'Resource Not Yet Available',
                          message: 'This resource is listed but file/media content has not been uploaded yet.',
                        })
                      }
                    >
                      Coming Soon
                    </Button>
                  )}

                  {!resourceUrl && resource.resource_type === 'pdf' && (
                    <a href={SAMPLE_PDF_PATH} target="_blank" rel="noreferrer" className="text-xs text-primary-600 hover:underline inline-flex items-center gap-1">
                      <ImageIcon size={12} />
                      Open sample PDF preview
                    </a>
                  )}
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
