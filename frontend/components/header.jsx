// components/Header.jsx

import React, { useState, useEffect } from "react";
import { supabase } from "./src/pages/supabaseClient";
import { Auth } from "@supabase/auth-ui-react";
import { ThemeSupa } from "@supabase/auth-ui-shared";

export default function Header() {
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(false);

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => setUser(user));

    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user || null);
    });

    return () => {
      listener?.subscription.unsubscribe();
    };
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    setUser(null);
  };

  return (
    <header className="flex justify-between items-center px-6 py-4 border-b shadow-sm">
      <div className="text-xl font-semibold text-blue-700">RAGaaS</div>

      {user ? (
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600">Hello, {user.email}</span>
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-3 py-1 rounded"
          >
            Logout
          </button>
        </div>
      ) : (
        <>
          <button
            onClick={() => setShowLogin(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Login
          </button>

          {showLogin && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
              <div className="bg-white p-6 rounded shadow-lg max-w-md w-full">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-lg font-semibold">Login</h2>
                  <button
                    onClick={() => setShowLogin(false)}
                    className="text-gray-500 hover:text-gray-800"
                  >
                    ×
                  </button>
                </div>
                <Auth
                  supabaseClient={supabase}
                  providers={["google"]}
                  appearance={{ theme: ThemeSupa }}
                  theme="default"
                />
              </div>
            </div>
          )}
        </>
      )}
    </header>
  );
}
