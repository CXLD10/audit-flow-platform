import { useQuery } from "@tanstack/react-query";
import { listInvoices } from "../api/invoices";

export function useInvoices(batchId: string, page: number, pageSize: number) {
  return useQuery({
    queryKey: ["invoices", batchId, page, pageSize],
    queryFn: () => listInvoices(batchId, page, pageSize),
    enabled: Boolean(batchId),
    placeholderData: (previous) => previous,
  });
}
