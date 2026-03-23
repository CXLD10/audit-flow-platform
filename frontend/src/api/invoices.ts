import { apiClient } from "./client";

export async function listInvoices(batchId: string) {
  const response = await apiClient.get(`/invoices`, { params: { batch_id: batchId } });
  return response.data as { items: Array<Record<string, unknown>>; total: number };
}

export async function resolveInvoice(invoiceId: string) {
  const response = await apiClient.patch(`/invoices/${invoiceId}/resolve`, { acknowledge: true });
  return response.data;
}
