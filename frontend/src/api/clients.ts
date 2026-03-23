import { apiClient } from "./client";
import { ClientRecord } from "../types";

export async function listClients(page = 1, pageSize = 100) {
  const response = await apiClient.get<ClientRecord[]>("/clients", { params: { page, page_size: pageSize } });
  return response.data;
}

export async function createClient(payload: { gstin: string; legal_name: string }) {
  const response = await apiClient.post<ClientRecord>("/clients", payload);
  return response.data;
}
