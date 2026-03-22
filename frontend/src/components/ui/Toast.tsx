import { useEffect } from 'react';
import { useUIStore } from '@/store';
import { cn } from '@/utils/helpers';
import { X } from 'lucide-react';

export default function Toast() {
  const { notifications, removeNotification } = useUIStore();

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-md">
      {notifications.map((notification) => (
        <ToastItem
          key={notification.id}
          {...notification}
          onClose={() => removeNotification(notification.id)}
        />
      ))}
    </div>
  );
}

interface ToastItemProps {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  onClose: () => void;
}

function ToastItem({ type, title, message, onClose }: ToastItemProps) {
  useEffect(() => {
    const timer = setTimeout(onClose, 5000);
    return () => clearTimeout(timer);
  }, [onClose]);

  const styles = {
    success: 'bg-green-50 border-green-500 text-green-900',
    error: 'bg-red-50 border-red-500 text-red-900',
    warning: 'bg-yellow-50 border-yellow-500 text-yellow-900',
    info: 'bg-blue-50 border-blue-500 text-blue-900',
  };

  const iconStyles = {
    success: 'text-green-500',
    error: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500',
  };

  return (
    <div
      className={cn(
        'flex items-start gap-3 p-4 rounded-lg border-l-4 shadow-lg animate-in slide-in-from-right',
        styles[type]
      )}
    >
      <div className="flex-1">
        <h4 className="font-semibold">{title}</h4>
        <p className="text-sm mt-1 opacity-90">{message}</p>
      </div>
      <button
        onClick={onClose}
        className={cn('p-1 rounded hover:bg-black/10 transition-colors', iconStyles[type])}
      >
        <X size={18} />
      </button>
    </div>
  );
}
