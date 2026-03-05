import { useAuthStore } from '@/store';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui';

export default function ProfilePage() {
  const { user } = useAuthStore();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-secondary-900">Profile Settings</h1>
        <p className="text-secondary-600 mt-2">Manage your account information and role details.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Account Information</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <dt className="text-sm text-secondary-500">First Name</dt>
              <dd className="text-secondary-900 font-medium">{user?.first_name || '-'}</dd>
            </div>
            <div>
              <dt className="text-sm text-secondary-500">Last Name</dt>
              <dd className="text-secondary-900 font-medium">{user?.last_name || '-'}</dd>
            </div>
            <div>
              <dt className="text-sm text-secondary-500">Email</dt>
              <dd className="text-secondary-900 font-medium">{user?.email || '-'}</dd>
            </div>
            <div>
              <dt className="text-sm text-secondary-500">Username</dt>
              <dd className="text-secondary-900 font-medium">{user?.username || '-'}</dd>
            </div>
            <div>
              <dt className="text-sm text-secondary-500">Role</dt>
              <dd className="text-secondary-900 font-medium capitalize">{user?.role || '-'}</dd>
            </div>
            <div>
              <dt className="text-sm text-secondary-500">Phone</dt>
              <dd className="text-secondary-900 font-medium">{user?.phone_number || '-'}</dd>
            </div>
          </dl>
        </CardContent>
      </Card>
    </div>
  );
}
