import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useRegister } from '@/hooks';
import { Button, Input } from '@/components/ui';
import { GraduationCap } from 'lucide-react';

const registerSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  password_confirm: z.string(),
  role: z.enum(['student', 'mentor', 'parent']),
}).refine((data) => data.password === data.password_confirm, {
  message: "Passwords don't match",
  path: ['password_confirm'],
});

type RegisterFormData = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      role: 'student',
    },
  });

  const registerMutation = useRegister();

  const onSubmit = (data: RegisterFormData) => {
    registerMutation.mutate(data);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        {/* Logo and Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center">
              <GraduationCap className="text-white" size={32} />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-secondary-900">Join DigiStudentPro</h1>
          <p className="text-secondary-600 mt-2">Create your account to get started</p>
        </div>

        {/* Register Form */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Input
                label="First Name"
                {...register('first_name')}
                error={errors.first_name?.message}
                placeholder="John"
              />

              <Input
                label="Last Name"
                {...register('last_name')}
                error={errors.last_name?.message}
                placeholder="Doe"
              />
            </div>

            <Input
              label="Username"
              {...register('username')}
              error={errors.username?.message}
              placeholder="johndoe"
            />

            <Input
              label="Email"
              type="email"
              {...register('email')}
              error={errors.email?.message}
              placeholder="john@example.com"
            />

            <div>
              <label className="block text-sm font-medium text-secondary-700 mb-1">
                I am a
              </label>
              <div className="grid grid-cols-3 gap-4">
                <label className="flex items-center gap-2 p-3 border-2 border-secondary-200 rounded-lg cursor-pointer hover:border-primary-500 has-[:checked]:border-primary-600 has-[:checked]:bg-primary-50">
                  <input
                    type="radio"
                    value="student"
                    {...register('role')}
                    className="text-primary-600"
                  />
                  <span className="text-sm font-medium">Student</span>
                </label>
                <label className="flex items-center gap-2 p-3 border-2 border-secondary-200 rounded-lg cursor-pointer hover:border-primary-500 has-[:checked]:border-primary-600 has-[:checked]:bg-primary-50">
                  <input
                    type="radio"
                    value="mentor"
                    {...register('role')}
                    className="text-primary-600"
                  />
                  <span className="text-sm font-medium">Mentor</span>
                </label>
                <label className="flex items-center gap-2 p-3 border-2 border-secondary-200 rounded-lg cursor-pointer hover:border-primary-500 has-[:checked]:border-primary-600 has-[:checked]:bg-primary-50">
                  <input
                    type="radio"
                    value="parent"
                    {...register('role')}
                    className="text-primary-600"
                  />
                  <span className="text-sm font-medium">Parent</span>
                </label>
              </div>
              {errors.role && (
                <p className="mt-1 text-sm text-red-600">{errors.role.message}</p>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Input
                label="Password"
                type="password"
                {...register('password')}
                error={errors.password?.message}
                placeholder="••••••••"
              />

              <Input
                label="Confirm Password"
                type="password"
                {...register('password_confirm')}
                error={errors.password_confirm?.message}
                placeholder="••••••••"
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              isLoading={registerMutation.isPending}
            >
              Create Account
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-secondary-600">
              Already have an account?{' '}
              <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
