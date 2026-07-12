"use client";

import { useState } from "react";
import { login } from "@/lib/auth";

export const LoginPage = ({ onSuccess }: { onSuccess: () => void }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (login(username, password)) {
      onSuccess();
      return;
    }
    setError("Invalid credentials. Use user / password.");
  };

  return (
    <main className="min-h-screen bg-[var(--surface)] px-6 py-12">
      <div className="mx-auto max-w-md rounded-[32px] border border-[var(--stroke)] bg-white/90 p-10 shadow-[var(--shadow)]">
        <h1 className="text-3xl font-semibold text-[var(--navy-dark)]">Sign in</h1>
        <p className="mt-3 text-sm text-[var(--gray-text)]">
          Use the dummy credentials to access the board.
        </p>
        <form onSubmit={handleSubmit} className="mt-8 flex flex-col gap-4">
          <label className="space-y-2 text-sm font-medium text-[var(--navy-dark)]">
            <span>Username</span>
            <input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              className="w-full rounded-xl border border-[var(--stroke)] bg-[var(--surface)] px-4 py-3 outline-none"
              autoComplete="username"
              required
            />
          </label>
          <label className="space-y-2 text-sm font-medium text-[var(--navy-dark)]">
            <span>Password</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="w-full rounded-xl border border-[var(--stroke)] bg-[var(--surface)] px-4 py-3 outline-none"
              autoComplete="current-password"
              required
            />
          </label>
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <button
            type="submit"
            className="rounded-full bg-[var(--primary-blue)] px-4 py-3 text-sm font-semibold text-white transition hover:brightness-110"
          >
            Sign in
          </button>
        </form>
      </div>
    </main>
  );
};
