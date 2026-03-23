import { apiClient } from "./client";

export type LoginPayload = {
  email: string;
  password: string;
};

export async function login(payload: LoginPayload) {
  const response = await apiClient.post("/auth/login", payload);
  return response.data as { access_token: string; token_type: string };
}

export async function getMe() {
  const response = await apiClient.get("/auth/me");
  return response.data as { id: string; tenant_id: string; email: string; role: string; created_at: string };
}
