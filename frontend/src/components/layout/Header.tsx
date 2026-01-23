import { Menu, Bell, Search } from 'lucide-react';
import { useUIStore } from '@/store';

export default function Header() {
  const { toggleSidebar } = useUIStore();

  return (
    <header className="sticky top-0 z-30 bg-white border-b border-secondary-200">
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-4">
          <button
            onClick={toggleSidebar}
            className="lg:hidden text-secondary-600 hover:text-secondary-900"
          >
            <Menu size={24} />
          </button>

          {/* Search bar */}
          <div className="hidden md:flex items-center gap-2 px-4 py-2 bg-secondary-50 rounded-lg w-96">
            <Search size={18} className="text-secondary-400" />
            <input
              type="text"
              placeholder="Search resources, careers, posts..."
              className="bg-transparent border-none outline-none text-sm flex-1"
            />
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <button className="relative p-2 text-secondary-600 hover:text-secondary-900 hover:bg-secondary-50 rounded-lg transition-colors">
            <Bell size={20} />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
          </button>
        </div>
      </div>
    </header>
  );
}
