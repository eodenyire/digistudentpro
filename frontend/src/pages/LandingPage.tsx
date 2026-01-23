import { Link } from 'react-router-dom';
import { Button } from '@/components/ui';
import { GraduationCap, BookOpen, MessageSquare, FileText, ArrowRight } from 'lucide-react';

export default function LandingPage() {
  const features = [
    {
      icon: GraduationCap,
      title: 'DigiGuide',
      description: 'Career guidance aligned with Kenya CBC curriculum. Get personalized recommendations based on your performance.',
    },
    {
      icon: BookOpen,
      title: 'DigiLab',
      description: 'Access comprehensive learning resources, interactive content, and assessments for all subjects.',
    },
    {
      icon: MessageSquare,
      title: 'DigiChat',
      description: 'Connect with peers and mentors through squad chats and direct messaging.',
    },
    {
      icon: FileText,
      title: 'DigiBlog',
      description: 'Read and share educational content, tips, and experiences with the community.',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      {/* Navbar */}
      <nav className="border-b border-secondary-200 bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <GraduationCap className="text-primary-600" size={32} />
            <span className="text-xl font-bold text-secondary-900">DigiStudentPro</span>
          </div>
          <div className="flex items-center gap-4">
            <Link to="/login">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link to="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-secondary-900 mb-6">
            Your Complete <span className="text-primary-600">EdTech Platform</span> for Kenya CBC
          </h1>
          <p className="text-xl text-secondary-600 mb-8">
            Comprehensive learning resources, career guidance, and community support for students, mentors, and parents.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/register">
              <Button size="lg" className="gap-2">
                Start Learning <ArrowRight size={20} />
              </Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="outline">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-3xl font-bold text-center text-secondary-900 mb-12">
          Everything You Need to Succeed
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <div
                key={feature.title}
                className="bg-white rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                  <Icon className="text-primary-600" size={24} />
                </div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-secondary-600">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="bg-primary-600 rounded-2xl p-12 text-white">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">10,000+</div>
              <div className="text-primary-100">Learning Resources</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">500+</div>
              <div className="text-primary-100">Career Paths</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">50,000+</div>
              <div className="text-primary-100">Active Students</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-secondary-900 mb-4">
            Ready to Start Your Learning Journey?
          </h2>
          <p className="text-xl text-secondary-600 mb-8">
            Join thousands of students achieving their academic and career goals.
          </p>
          <Link to="/register">
            <Button size="lg" className="gap-2">
              Create Free Account <ArrowRight size={20} />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-secondary-200 bg-white">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-secondary-600">
            <p>Kenya CBC Education Platform</p>
            <p className="mt-2">© 2024 DigiStudentPro. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
