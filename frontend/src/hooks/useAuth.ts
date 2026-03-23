import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { getMe, LoginPayload, login } from "../api/auth";
import { useAuthStore } from "../state/authStore";

export function useAuth() {
  const store = useAuthStore();
  const queryClient = useQueryClient();

  const meQuery = useQuery({
    queryKey: ["me", store.token],
    queryFn: getMe,
    enabled: Boolean(store.token),
  });

  const loginMutation = useMutation({
    mutationFn: async (payload: LoginPayload) => {
      const token = await login(payload);
      store.setSession({ token: token.access_token });
      const profile = await queryClient.fetchQuery({ queryKey: ["me", token.access_token], queryFn: getMe });
      store.setSession({ profile });
      return { token, profile };
    },
  });

  return {
    ...store,
    profile: meQuery.data,
    isProfileLoading: meQuery.isLoading,
    login: loginMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    loginError: loginMutation.error,
    logout: store.clearAuth,
  };
}
