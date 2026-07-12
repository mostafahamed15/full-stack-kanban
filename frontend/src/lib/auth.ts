const AUTH_KEY = "kanban-authenticated";

const isBrowser = () => typeof window !== "undefined";

export const isAuthenticated = () => {
  return isBrowser() && localStorage.getItem(AUTH_KEY) === "true";
};

export const login = (username: string, password: string) => {
  const validUser = username === "user" && password === "password";
  if (validUser && isBrowser()) {
    localStorage.setItem(AUTH_KEY, "true");
  }
  return validUser;
};

export const logout = () => {
  if (isBrowser()) {
    localStorage.removeItem(AUTH_KEY);
  }
};
