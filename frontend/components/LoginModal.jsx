// frontend/components/LoginModal.jsx
import { useEffect } from 'react';
import { Auth } from '@supabase/auth-ui-react';
import { supabase } from '../supabaseClient';
import { ThemeSupa } from '@supabase/auth-ui-shared';

export default function LoginModal({ open, onClose }) {
  useEffect(() => {
    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session) onClose();
    });

    return () => {
      listener.subscription.unsubscribe();
    };
  }, [onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-md shadow-lg">
        <button onClick={onClose} className="text-sm float-right">✖</button>
        <Auth
          supabaseClient={supabase}
          providers={['google']}
          appearance={{ theme: ThemeSupa }}
        />
      </div>
    </div>
  );
}
