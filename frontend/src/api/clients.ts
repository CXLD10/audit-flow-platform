import { apiClient } from "./client";
<<<<<<< HEAD

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
=======
import { ClientRecord } from "../types";

export async function listClients(page = 1, pageSize = 100) {
  const response = await apiClient.get<ClientRecord[]>("/clients", { params: { page, page_size: pageSize } });
  return response.data;
}

export async function createClient(payload: { gstin: string; legal_name: string }) {
  const response = await apiClient.post<ClientRecord>("/clients", payload);
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
  return response.data;
}
