import { fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, afterEach, describe, expect, it, vi } from 'vitest';
import { KanbanBoard } from '@/components/KanbanBoard';
import { initialData, type BoardData } from '@/lib/kanban';

const getFirstColumn = () => screen.getAllByTestId(/column-/i)[0];

const createResponse = (body: BoardData) => ({
  ok: true,
  json: async () => body,
});

describe('KanbanBoard', () => {
  const fetchMock = vi.fn();

  beforeEach(() => {
    vi.stubGlobal('fetch', fetchMock);
    fetchMock.mockImplementation((input: RequestInfo | URL) => {
      const url = typeof input === 'string' ? input : input.toString();

      if (url.includes('/api/board')) {
        if (
          fetchMock.mock.calls.filter(([callUrl]) => callUrl === url).length ===
          0
        ) {
          return Promise.resolve(createResponse(initialData));
        }

        return Promise.resolve(createResponse(initialData));
      }

      return Promise.resolve({
        ok: false,
        json: async () => ({ detail: 'not found' }),
      });
    });
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    fetchMock.mockReset();
  });

  it('loads the board from the backend on mount', async () => {
    render(<KanbanBoard />);

    expect(fetchMock).toHaveBeenCalledWith('/api/board');
    expect(await screen.findByText('Align roadmap themes')).toBeInTheDocument();
  });

  it('renames a column', async () => {
    render(<KanbanBoard />);
    const column = getFirstColumn();
    const input = within(column).getByLabelText('Column title');
    fireEvent.change(input, { target: { value: '' } });
    fireEvent.change(input, { target: { value: 'New Name' } });
    expect(input).toHaveValue('New Name');
  });

  it('adds and removes a card', async () => {
    render(<KanbanBoard />);
    const column = getFirstColumn();
    const addButton = within(column).getByRole('button', {
      name: /add a card/i,
    });
    await userEvent.click(addButton);

    const titleInput = within(column).getByPlaceholderText(/card title/i);
    await userEvent.type(titleInput, 'New card');
    const detailsInput = within(column).getByPlaceholderText(/details/i);
    await userEvent.type(detailsInput, 'Notes');

    await userEvent.click(
      within(column).getByRole('button', { name: /add card/i }),
    );

    expect(within(column).getByText('New card')).toBeInTheDocument();

    const deleteButton = within(column).getByRole('button', {
      name: /delete new card/i,
    });
    await userEvent.click(deleteButton);

    expect(within(column).queryByText('New card')).not.toBeInTheDocument();
  });

  it('persists board changes to the backend', async () => {
    render(<KanbanBoard />);
    await screen.findByText('Align roadmap themes');

    const column = getFirstColumn();
    const input = within(column).getByLabelText('Column title');
    await userEvent.clear(input);
    await userEvent.type(input, 'Renamed');

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/board',
      expect.objectContaining({ method: 'PATCH' }),
    );
  });
});
