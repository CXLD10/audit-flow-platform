import { useQuery } from "@tanstack/react-query";
import { listInvoices } from "../api/invoices";

export function useInvoices(batchId: string) {
  return useQuery({
    queryKey: ["invoices", batchId],
    queryFn: () => listInvoices(batchId),
    enabled: Boolean(batchId),
  });
}
