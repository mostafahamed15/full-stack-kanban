'use client';

import { useState } from 'react';

type AiChatPanelProps = {
  onBoardUpdate: (nextBoard: {
    columns: Array<{ id: string; title: string; cardIds: string[] }>;
    cards: Record<string, { id: string; title: string; details: string }>;
  }) => void;
};

export const AiChatPanel = ({ onBoardUpdate }: AiChatPanelProps) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<
    Array<{ role: 'user' | 'assistant'; content: string }>
  >([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!input.trim()) {
      return;
    }

    const nextMessage = input.trim();
    setMessages((prev) => [...prev, { role: 'user', content: nextMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: nextMessage }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Unable to contact AI');
      }

      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: data.message },
      ]);
      if (data.applied && data.board) {
        onBoardUpdate(data.board);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content:
            error instanceof Error ? error.message : 'Unable to contact AI',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <aside className="rounded-[28px] border border-[var(--stroke)] bg-white/80 p-5 shadow-[var(--shadow)] backdrop-blur">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.25em] text-[var(--gray-text)]">
            AI assistant
          </p>
          <h2 className="mt-1 text-lg font-semibold text-[var(--navy-dark)]">
            Ask for board changes
          </h2>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="mt-4 flex flex-col gap-3">
        <textarea
          value={input}
          onChange={(event) => setInput(event.target.value)}
          rows={4}
          placeholder="Try: add a card for sprint planning"
          className="w-full rounded-2xl border border-[var(--stroke)] bg-[var(--surface)] px-4 py-3 text-sm outline-none"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="rounded-2xl bg-[var(--primary-blue)] px-4 py-3 text-sm font-semibold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isLoading ? 'Thinking…' : 'Send'}
        </button>
      </form>

      <div className="mt-4 flex max-h-[260px] flex-col gap-2 overflow-auto">
        {messages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={`rounded-2xl px-3 py-2 text-sm ${message.role === 'user' ? 'bg-[var(--surface)] text-[var(--navy-dark)]' : 'bg-[var(--surface-strong)] text-[var(--gray-text)]'}`}
          >
            {message.content}
          </div>
        ))}
      </div>
    </aside>
  );
};
