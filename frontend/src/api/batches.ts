import { apiClient } from "./client";

export async function uploadBatch(payload: { file: File; clientGstin: string; returnPeriod?: string }) {
  const formData = new FormData();
  formData.append("file", payload.file);
  formData.append("client_gstin", payload.clientGstin);
  if (payload.returnPeriod) {
    formData.append("return_period", payload.returnPeriod);
  }
  const response = await apiClient.post("/batches/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data as { batch_id: string; status: string };
}

export async function getBatchProgress(batchId: string) {
  const response = await apiClient.get(`/batches/${batchId}/progress`);
  return response.data as {
    stage: string;
    pct: number;
    processed: number;
    total: number;
    status: string;
    error_message?: string;
    degraded?: boolean;
  };
}

export async function getBatchResults(batchId: string) {
  const response = await apiClient.get(`/batches/${batchId}/results`);
  return response.data as {
    batch: {
      id: string;
      status: string;
      filename: string;
      error_count: number;
      total_invoices: number;
      completed_at?: string | null;
    };
    invoices: Array<Record<string, unknown>>;
    errors: Array<Record<string, unknown>>;
    degraded_messages: string[];
  };
}

export function getExportUrl(batchId: string, type = "validation") {
  const url = new URL(`${apiClient.defaults.baseURL}/batches/${batchId}/export`);
  url.searchParams.set("type", type);
  return url.toString();
}
