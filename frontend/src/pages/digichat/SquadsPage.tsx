import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { MessageSquare, Users, Plus, Search, LogIn, LogOut } from 'lucide-react';
import { Card, CardContent, LoadingPage, Button } from '@/components/ui';
import { digichatApi } from '@/api';
import { useUIStore } from '@/store';
import { Squad } from '@/types';
import { formatRelativeTime } from '@/utils/helpers';

export default function SquadsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const queryClient = useQueryClient();
  const { addNotification } = useUIStore();

  const { data: squadsData, isLoading } = useQuery({
    queryKey: ['squads'],
    queryFn: () => digichatApi.getSquads(),
  });

  const joinSquadMutation = useMutation({
    mutationFn: (slug: string) => digichatApi.joinSquad(slug),
    onSuccess: () => {
      addNotification({
        type: 'success',
        title: 'Joined Squad',
        message: 'You have joined the squad successfully.',
      });
      queryClient.invalidateQueries({ queryKey: ['squads'] });
    },
    onError: () => {
      addNotification({
        type: 'error',
        title: 'Join Failed',
        message: 'Could not join this squad at the moment.',
      });
    },
  });

  const leaveSquadMutation = useMutation({
    mutationFn: (slug: string) => digichatApi.leaveSquad(slug),
    onSuccess: () => {
      addNotification({
        type: 'info',
        title: 'Left Squad',
        message: 'You have left the squad.',
      });
      queryClient.invalidateQueries({ queryKey: ['squads'] });
    },
    onError: () => {
      addNotification({
        type: 'error',
        title: 'Leave Failed',
        message: 'Could not leave this squad at the moment.',
      });
    },
  });

  if (isLoading) return <LoadingPage />;

  const squads = squadsData?.results || [];
  const filteredSquads = squads.filter((squad: Squad) =>
    squad.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const isBusy = joinSquadMutation.isPending || leaveSquadMutation.isPending;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Squads</h1>
          <p className="text-secondary-600 mt-2">Join group chats and connect with peers</p>
        </div>
        <Button className="gap-2">
          <Plus size={20} />
          Create Squad
        </Button>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-secondary-400" size={20} />
        <input
          type="text"
          placeholder="Search squads..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredSquads.map((squad: Squad) => {
          const joined = Boolean(squad.is_member);
          return (
            <Card key={squad.id} hoverable>
              <CardContent className="p-6">
                <div className="flex items-start gap-3 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-primary-400 to-primary-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    {squad.avatar ? (
                      <img src={squad.avatar} alt={squad.name} className="w-full h-full object-cover rounded-lg" />
                    ) : (
                      <MessageSquare className="text-white" size={24} />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-secondary-900 truncate">{squad.name}</h3>
                    <div className="flex items-center gap-2 text-sm text-secondary-600 mt-1">
                      <Users size={14} />
                      <span>{squad.member_count} members</span>
                    </div>
                  </div>
                </div>

                {squad.description && (
                  <p className="text-sm text-secondary-600 mb-4 line-clamp-2">{squad.description}</p>
                )}

                {squad.topic && (
                  <div className="mb-4">
                    <span className="text-xs px-2 py-1 bg-primary-50 text-primary-700 rounded">{squad.topic}</span>
                  </div>
                )}

                {squad.last_message && (
                  <div className="mb-4 p-3 bg-secondary-50 rounded-lg">
                    <p className="text-sm text-secondary-700 line-clamp-2">{squad.last_message}</p>
                    {squad.last_message_at && (
                      <p className="text-xs text-secondary-500 mt-1">{formatRelativeTime(squad.last_message_at)}</p>
                    )}
                  </div>
                )}

                {joined ? (
                  <Button
                    className="w-full"
                    size="sm"
                    variant="outline"
                    disabled={isBusy}
                    onClick={() => leaveSquadMutation.mutate(squad.slug)}
                  >
                    <LogOut size={16} className="mr-2" />
                    Leave Squad
                  </Button>
                ) : (
                  <Button
                    className="w-full"
                    size="sm"
                    disabled={isBusy}
                    onClick={() => joinSquadMutation.mutate(squad.slug)}
                  >
                    <LogIn size={16} className="mr-2" />
                    Join Squad
                  </Button>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {filteredSquads.length === 0 && (
        <div className="text-center py-12">
          <MessageSquare className="mx-auto text-secondary-400 mb-4" size={48} />
          <h3 className="text-lg font-medium text-secondary-900 mb-2">No squads found</h3>
          <p className="text-secondary-600">
            {searchQuery ? 'Try a different search term' : 'Create your first squad to get started'}
          </p>
        </div>
      )}
    </div>
  );
}
