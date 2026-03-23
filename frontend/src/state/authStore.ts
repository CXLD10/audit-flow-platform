import { create } from "zustand";
import { AuthUser, UserRole } from "../types";

type AuthState = {
  tenantId: string;
  token: string;
  role: UserRole;
  email: string;
  userId: string;
  setSession: (payload: { token?: string; tenantId?: string; profile?: AuthUser }) => void;
  clearAuth: () => void;
};

export const useAuthStore = create<AuthState>((set) => ({
  tenantId: "00000000-0000-0000-0000-000000000001",
  token: "",
  role: "CA",
  email: "",
  userId: "",
  setSession: ({ token, tenantId, profile }) =>
    set((state) => ({
      ...state,
      token: token ?? state.token,
      tenantId: tenantId ?? state.tenantId,
      role: profile?.role ?? state.role,
      email: profile?.email ?? state.email,
      userId: profile?.id ?? state.userId,
    })),
  clearAuth: () => set({ token: "", role: "CA", email: "", userId: "", tenantId: "00000000-0000-0000-0000-000000000001" }),
}));
