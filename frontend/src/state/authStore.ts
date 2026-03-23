import { create } from "zustand";

type AuthState = {
  tenantId: string;
  token: string;
  role: string;
  email: string;
  setAuth: (payload: Partial<Pick<AuthState, "tenantId" | "token" | "role" | "email">>) => void;
  clearAuth: () => void;
};

export const useAuthStore = create<AuthState>((set) => ({
  tenantId: "00000000-0000-0000-0000-000000000001",
  token: "",
  role: "CA",
  email: "",
  setAuth: (payload) => set((state) => ({ ...state, ...payload })),
  clearAuth: () => set({ token: "", role: "CA", email: "" }),
}));
