import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { isAuthenticated } from '@/endpoints/login';


export default function AuthorizationMiddleware({ children }) {
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
    }
  }, []);

  return children;
}