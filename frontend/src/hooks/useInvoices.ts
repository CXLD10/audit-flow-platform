<<<<<<< HEAD
export function useInvoices() {
  return [];
=======
import { useQuery } from "@tanstack/react-query";
import { listInvoices } from "../api/invoices";

export function useInvoices(batchId: string, page: number, pageSize: number) {
  return useQuery({
    queryKey: ["invoices", batchId, page, pageSize],
    queryFn: () => listInvoices(batchId, page, pageSize),
    enabled: Boolean(batchId),
    placeholderData: (previous) => previous,
  });
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
