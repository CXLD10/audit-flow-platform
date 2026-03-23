<<<<<<< HEAD
export function listInvoices() {
  return Promise.resolve([]);
=======
import { apiClient } from "./client";
import { InvoiceRecord, PaginatedInvoices } from "../types";

export async function listInvoices(batchId: string, page = 1, pageSize = 100) {
  const response = await apiClient.get<PaginatedInvoices>(`/invoices`, { params: { batch_id: batchId, page, page_size: pageSize } });
  return response.data;
}

export async function getInvoice(invoiceId: string) {
  const response = await apiClient.get<InvoiceRecord>(`/invoices/${invoiceId}`);
  return response.data;
}

export async function resolveInvoice(invoiceId: string) {
  const response = await apiClient.patch<InvoiceRecord>(`/invoices/${invoiceId}/resolve`, { acknowledge: true });
  return response.data;
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
