import { ReactNode } from "react";
<<<<<<< HEAD

export default function RoleGuard({ children }: { children: ReactNode }) {
=======
import { useAuthStore } from "../state/authStore";
import { UserRole } from "../types";

export default function RoleGuard({ children, allow, fallback = null }: { children: ReactNode; allow: UserRole[]; fallback?: ReactNode }) {
  const role = useAuthStore((state) => state.role);
  if (!allow.includes(role)) {
    return <>{fallback}</>;
  }
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
  return <>{children}</>;
}
