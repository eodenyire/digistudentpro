import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore, useUIStore } from '@/store';
import { 
  Home, 
  BookOpen, 
  MessageSquare, 
  FileText, 
  GraduationCap,
  X,
  LogOut,
  User,
  Settings
} from 'lucide-react';
import { cn } from '@/utils/helpers';

const navigationItems = [
  { name: 'Dashboard', href: '/dashboard', icon: Home },
  { name: 'DigiGuide', href: '/digiguide/careers', icon: GraduationCap },
  { name: 'DigiLab', href: '/digilab/browse', icon: BookOpen },
  { name: 'DigiChat', href: '/digichat/squads', icon: MessageSquare },
  { name: 'DigiBlog', href: '/digiblog', icon: FileText },
];

export default function Sidebar() {
  const { sidebarOpen, setSidebarOpen } = useUIStore();
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed top-0 left-0 z-40 h-screen w-64 bg-white border-r border-secondary-200 transition-transform duration-300',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between p-6 border-b border-secondary-200">
            <Link to="/dashboard" className="flex items-center gap-2">
              <GraduationCap className="text-primary-600" size={32} />
              <span className="text-xl font-bold text-secondary-900">DigiStudent</span>
            </Link>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden text-secondary-600 hover:text-secondary-900"
            >
              <X size={24} />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto p-4">
            <ul className="space-y-2">
              {navigationItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname.startsWith(item.href);
                
                return (
                  <li key={item.name}>
                    <Link
                      to={item.href}
                      className={cn(
                        'flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
                        isActive
                          ? 'bg-primary-50 text-primary-700 font-medium'
                          : 'text-secondary-600 hover:bg-secondary-50'
                      )}
                    >
                      <Icon size={20} />
                      <span>{item.name}</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </nav>

          {/* User section */}
          <div className="border-t border-secondary-200 p-4">
            <div className="flex items-center gap-3 px-4 py-2 mb-2">
              <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center">
                <User className="text-primary-600" size={20} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-secondary-900 truncate">
                  {user?.first_name} {user?.last_name}
                </p>
                <p className="text-xs text-secondary-500 truncate">{user?.role}</p>
              </div>
            </div>
            <div className="space-y-1">
              <button
                onClick={() => navigate('/profile')}
                className="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-secondary-600 hover:bg-secondary-50 transition-colors"
              >
                <Settings size={18} />
                <span className="text-sm">Settings</span>
              </button>
              <button
                onClick={() => {
                  localStorage.clear();
                  window.location.href = '/login';
                }}
                className="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-red-600 hover:bg-red-50 transition-colors"
              >
                <LogOut size={18} />
                <span className="text-sm">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}
