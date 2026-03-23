import { useQuery } from "@tanstack/react-query";
import { getBatchProgress } from "../api/batches";

export function useBatchProgress(batchId: string) {
  return useQuery({
    queryKey: ["batch-progress", batchId],
    queryFn: () => getBatchProgress(batchId),
    enabled: Boolean(batchId),
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return status === "COMPLETE" || status === "FAILED" ? false : 2000;
    },
  });
}
