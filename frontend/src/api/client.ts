<<<<<<< HEAD
export const apiClient = {
  baseUrl: "/api/v1",
};
=======
import axios from "axios";
import { useAuthStore } from "../state/authStore";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const { token, tenantId } = useAuthStore.getState();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.headers["X-Tenant-Id"] = tenantId;
  return config;
});
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
