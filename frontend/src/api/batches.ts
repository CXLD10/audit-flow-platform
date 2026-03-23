<<<<<<< HEAD
export function listBatches() {
  return Promise.resolve([]);
=======
import { apiClient } from "./client";
import { BatchProgress, BatchRecord, BatchResultsResponse } from "../types";

export async function uploadBatch(payload: { file: File; clientGstin: string; returnPeriod?: string }) {
  const formData = new FormData();
  formData.append("file", payload.file);
  formData.append("client_gstin", payload.clientGstin);
  if (payload.returnPeriod) {
    formData.append("return_period", payload.returnPeriod);
  }
  const response = await apiClient.post<{ batch_id: string; status: string }>("/batches/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function getBatch(batchId: string) {
  const response = await apiClient.get<BatchRecord>(`/batches/${batchId}`);
  return response.data;
}

export async function getBatchProgress(batchId: string) {
  const response = await apiClient.get<BatchProgress>(`/batches/${batchId}/progress`);
  return response.data;
}

export async function getBatchResults(batchId: string) {
  const response = await apiClient.get<BatchResultsResponse>(`/batches/${batchId}/results`);
  return response.data;
}

export async function downloadBatchExport(batchId: string, type: "validation" | "gstr1") {
  const response = await apiClient.get<Blob>(`/batches/${batchId}/export`, {
    params: { type },
    responseType: "blob",
  });
  const blob = new Blob([response.data], { type: response.headers["content-type"] });
  const filename = /filename="([^"]+)"/.exec(response.headers["content-disposition"] ?? "")?.[1] ?? `batch-${batchId}-${type}`;
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
