<<<<<<< HEAD
export function login() {
  return Promise.resolve(null);
=======
import { apiClient } from "./client";
import { AuthUser } from "../types";

export type LoginPayload = {
  email: string;
  password: string;
};

export async function login(payload: LoginPayload) {
  const response = await apiClient.post<{ access_token: string; token_type: string }>("/auth/login", payload);
  return response.data;
}

export async function getMe() {
  const response = await apiClient.get<AuthUser>("/auth/me");
  return response.data;
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
