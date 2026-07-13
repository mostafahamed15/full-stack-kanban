'use client';

import { useEffect, useState } from 'react';
import { KanbanBoard } from '@/components/KanbanBoard';
import { LoginPage } from '@/components/LoginPage';
import { isAuthenticated, logout } from '@/lib/auth';

export default function Home() {
  const [authenticated, setAuthenticated] = useState(false);
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    setAuthenticated(isAuthenticated());
    setInitialized(true);
  }, []);

  if (!initialized) {
    return null;
  }

  if (!authenticated) {
    return <LoginPage onSuccess={() => setAuthenticated(true)} />;
  }

  return (
    <div>
      <div className="absolute right-6 top-6">
        <button
          type="button"
          onClick={() => {
            logout();
            setAuthenticated(false);
          }}
          className="rounded-full border border-[var(--stroke)] bg-white/90 px-4 py-2 text-sm font-semibold text-[var(--navy-dark)] shadow-[var(--shadow)] transition hover:bg-[var(--surface)]"
        >
          Logout
        </button>
      </div>
      <KanbanBoard />
    </div>
  );
}
