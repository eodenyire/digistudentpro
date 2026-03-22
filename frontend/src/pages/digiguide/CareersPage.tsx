import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { AlertCircle, Briefcase, CheckCircle2, DollarSign, Search, Target, TrendingUp } from 'lucide-react';
import { Card, CardContent, LoadingPage, Button } from '@/components/ui';
import { digiguideApi } from '@/api';
import { Career, ClusterRequirement } from '@/types';
import { useAuthStore } from '@/store';

function parseList(value: string | string[] | undefined): string[] {
  if (!value) return [];
  if (Array.isArray(value)) return value;
  return value
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

const gradeOptions = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'E'] as const;

const gradeScoreMap: Record<string, number> = {
  A: 12,
  'A-': 11,
  'B+': 10,
  B: 9,
  'B-': 8,
  'C+': 7,
  C: 6,
  'C-': 5,
  'D+': 4,
  D: 3,
  'D-': 2,
  E: 1,
};

type SubjectGradeMap = Record<string, string>;

interface RecommendationResult {
  career: Career;
  matchPercentage: number;
  strengths: string[];
  gaps: string[];
  meetsAllMandatory: boolean;
}

function gradeMeetsRequirement(studentGrade: string | undefined, requiredGrade: string): boolean {
  if (!studentGrade) return false;
  return (gradeScoreMap[studentGrade] ?? 0) >= (gradeScoreMap[requiredGrade] ?? 0);
}

export default function CareersPage() {
  const { user } = useAuthStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCluster, setSelectedCluster] = useState<number | undefined>();

  const [studentId, setStudentId] = useState('');
  const [subjectGrades, setSubjectGrades] = useState<SubjectGradeMap>({});
  const [recommendations, setRecommendations] = useState<RecommendationResult[]>([]);

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

  const requirementSubjects = useMemo(() => {
    const subjectSet = new Set<string>();
    (clusters || []).forEach((cluster) => {
      (cluster.requirements || []).forEach((requirement) => {
        subjectSet.add(requirement.subject_name);
      });
    });
    return Array.from(subjectSet).sort((a, b) => a.localeCompare(b));
  }, [clusters]);

  const handleGradeChange = (subjectName: string, grade: string) => {
    setSubjectGrades((prev) => ({
      ...prev,
      [subjectName]: grade,
    }));
  };

  const clearPerformanceInputs = () => {
    setStudentId('');
    setSubjectGrades({});
    setRecommendations([]);
  };

  const generateRecommendations = () => {
    const enteredGrades = Object.entries(subjectGrades).filter(([, grade]) => grade);
    if (enteredGrades.length === 0) {
      setRecommendations([]);
      return;
    }

    const clusterRequirements = new Map<number, ClusterRequirement[]>();
    (clusters || []).forEach((cluster) => {
      clusterRequirements.set(cluster.id, cluster.requirements || []);
    });

    const calculated = careers
      .map((career) => {
        const requirements = clusterRequirements.get(career.cluster ?? -1) || [];

        if (requirements.length === 0) {
          return {
            career,
            matchPercentage: 0,
            strengths: [],
            gaps: ['No cluster requirements found for this career yet.'],
            meetsAllMandatory: false,
          } as RecommendationResult;
        }

        let earnedWeight = 0;
        let totalWeight = 0;
        let meetsAllMandatory = true;
        const strengths: string[] = [];
        const gaps: string[] = [];

        requirements.forEach((requirement) => {
          const weight = requirement.is_mandatory ? 2 : 1;
          totalWeight += weight;

          const studentGrade = subjectGrades[requirement.subject_name];
          const meets = gradeMeetsRequirement(studentGrade, requirement.minimum_grade);

          if (meets) {
            earnedWeight += weight;
            strengths.push(`${requirement.subject_name}: ${studentGrade} (meets ${requirement.minimum_grade})`);
          } else {
            gaps.push(
              `${requirement.subject_name}: ${studentGrade || 'not entered'} (requires ${requirement.minimum_grade})`
            );
            if (requirement.is_mandatory) {
              meetsAllMandatory = false;
            }
          }
        });

        const matchPercentage = totalWeight > 0 ? Math.round((earnedWeight / totalWeight) * 100) : 0;

        return {
          career,
          matchPercentage,
          strengths,
          gaps,
          meetsAllMandatory,
        } as RecommendationResult;
      })
      .sort((a, b) => b.matchPercentage - a.matchPercentage)
      .slice(0, 6);

    setRecommendations(calculated);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-secondary-900">Career Explorer</h1>
        <p className="text-secondary-600 mt-2">
          Discover career paths aligned with Kenya CBC curriculum.
        </p>
      </div>

      <Card>
        <CardContent className="p-6 space-y-5">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold text-secondary-900 flex items-center gap-2">
                <Target className="text-primary-600" size={20} />
                Performance-Based Career Prediction
              </h2>
              <p className="text-sm text-secondary-600 mt-1">
                Enter student performance and instantly compare against KUCCPS cluster criteria.
              </p>
            </div>
            {user?.role === 'teacher' && (
              <span className="text-xs px-2 py-1 rounded bg-green-50 text-green-700">Teacher Mode</span>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-secondary-700 mb-1">Student ID</label>
              <input
                type="text"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                placeholder="e.g. STU-001"
                className="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div className="bg-secondary-50 rounded-lg p-3 text-sm text-secondary-700">
              {studentId
                ? `Predicting recommendations for Student ID: ${studentId}`
                : 'Tip: Add a student ID so teachers can track whose scores were used.'}
            </div>
          </div>

          {requirementSubjects.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-secondary-800 mb-3">Subject Grades</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {requirementSubjects.map((subjectName) => (
                  <div key={subjectName}>
                    <label className="block text-xs text-secondary-600 mb-1">{subjectName}</label>
                    <select
                      value={subjectGrades[subjectName] || ''}
                      onChange={(e) => handleGradeChange(subjectName, e.target.value)}
                      className="w-full px-3 py-2 border border-secondary-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      <option value="">Not entered</option>
                      {gradeOptions.map((grade) => (
                        <option key={grade} value={grade}>
                          {grade}
                        </option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="flex gap-3">
            <Button onClick={generateRecommendations}>Predict Careers</Button>
            <Button variant="outline" onClick={clearPerformanceInputs}>
              Clear Inputs
            </Button>
          </div>

          {recommendations.length > 0 && (
            <div className="space-y-3 pt-2">
              <h3 className="text-sm font-semibold text-secondary-900">Recommended Careers</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {recommendations.map((result) => (
                  <div key={result.career.id} className="border border-secondary-200 rounded-lg p-4 bg-white">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="font-semibold text-secondary-900">{result.career.name}</p>
                        <p className="text-xs text-secondary-600 mt-1">
                          {result.career.cluster_name || 'General Cluster'}
                        </p>
                      </div>
                      <span
                        className={`text-xs px-2 py-1 rounded ${
                          result.matchPercentage >= 75
                            ? 'bg-green-100 text-green-700'
                            : result.matchPercentage >= 50
                            ? 'bg-yellow-100 text-yellow-700'
                            : 'bg-red-100 text-red-700'
                        }`}
                      >
                        {result.matchPercentage}% match
                      </span>
                    </div>

                    <div className="mt-3 space-y-2 text-sm">
                      <p className="flex items-center gap-2 text-secondary-700">
                        {result.meetsAllMandatory ? (
                          <CheckCircle2 size={16} className="text-green-600" />
                        ) : (
                          <AlertCircle size={16} className="text-yellow-600" />
                        )}
                        {result.meetsAllMandatory
                          ? 'All mandatory subjects meet minimum grade.'
                          : 'Some mandatory subjects are below required grade.'}
                      </p>

                      {result.strengths.length > 0 && (
                        <p className="text-xs text-green-700">Strengths: {result.strengths.slice(0, 2).join(' | ')}</p>
                      )}
                      {result.gaps.length > 0 && (
                        <p className="text-xs text-red-700">Gaps: {result.gaps.slice(0, 2).join(' | ')}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      <div className="bg-white rounded-lg p-6 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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

              <p className="text-sm text-secondary-600 mb-4 line-clamp-3">{career.description}</p>

              {career.job_outlook && (
                <div className="flex items-center gap-2 text-sm mb-4">
                  <TrendingUp size={16} className="text-green-600" />
                  <span className="text-secondary-700">{career.job_outlook}</span>
                </div>
              )}

              {parseList(career.skills_needed).length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {parseList(career.skills_needed)
                    .slice(0, 3)
                    .map((skill, idx) => (
                      <span key={idx} className="text-xs px-2 py-1 bg-primary-50 text-primary-700 rounded">
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
