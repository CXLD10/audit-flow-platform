import { ReactNode } from "react";
import { useAuthStore } from "../state/authStore";
import { UserRole } from "../types";

export default function RoleGuard({ children, allow, fallback = null }: { children: ReactNode; allow: UserRole[]; fallback?: ReactNode }) {
  const role = useAuthStore((state) => state.role);
  if (!allow.includes(role)) {
    return <>{fallback}</>;
  }
  return <>{children}</>;
}
