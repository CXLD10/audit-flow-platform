import { ReactNode } from "react";
import { useAuthStore } from "../state/authStore";

export default function RoleGuard({ children, allow }: { children: ReactNode; allow: string[] }) {
  const role = useAuthStore((state) => state.role);
  if (!allow.includes(role)) {
    return null;
  }
  return <>{children}</>;
}
