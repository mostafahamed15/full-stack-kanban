import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginPage } from "@/components/LoginPage";

describe("LoginPage", () => {
  it("shows an error for invalid credentials", async () => {
    const onSuccess = vi.fn();
    render(<LoginPage onSuccess={onSuccess} />);

    const username = screen.getByLabelText(/username/i);
    const password = screen.getByLabelText(/password/i);
    const submit = screen.getByRole("button", { name: /sign in/i });

    await userEvent.type(username, "wrong");
    await userEvent.type(password, "wrong");
    await userEvent.click(submit);

    expect(onSuccess).not.toHaveBeenCalled();
    expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
  });
});
