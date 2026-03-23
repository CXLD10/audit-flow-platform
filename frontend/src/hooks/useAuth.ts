import { useMutation, useQuery } from "@tanstack/react-query";
import { getMe, login, LoginPayload } from "../api/auth";
import { useAuthStore } from "../state/authStore";

export function useAuth() {
  const store = useAuthStore();

  const meQuery = useQuery({
    queryKey: ["me", store.token],
    queryFn: getMe,
    enabled: Boolean(store.token),
  });

  const loginMutation = useMutation({
    mutationFn: (payload: LoginPayload) => login(payload),
    onSuccess: (data) => {
      store.setAuth({ token: data.access_token });
    },
  });

  return {
    ...store,
    profile: meQuery.data,
    isProfileLoading: meQuery.isLoading,
    login: loginMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    loginError: loginMutation.error,
  };
}
