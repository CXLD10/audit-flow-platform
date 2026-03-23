import { apiClient } from "./client";

export async function listClients() {
  const response = await apiClient.get("/clients");
  return response.data as Array<{
    id: string;
    gstin: string;
    legal_name: string;
    created_at: string;
  }>;
}

export async function createClient(payload: { gstin: string; legal_name: string }) {
  const response = await apiClient.post("/clients", payload);
  return response.data;
}
