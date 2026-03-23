<<<<<<< HEAD
export default function ExportPage() {
  return <div>Export page scaffolded for later frontend phases.</div>;
=======
import { useMutation } from "@tanstack/react-query";
import { useSearchParams } from "react-router-dom";
import { downloadBatchExport } from "../api/batches";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import RoleGuard from "../components/RoleGuard";

export default function ExportPage() {
  const [searchParams] = useSearchParams();
  const batchId = searchParams.get("batchId") ?? "";
  const exportMutation = useMutation({
    mutationFn: ({ type }: { type: "validation" | "gstr1" }) => downloadBatchExport(batchId, type),
  });

  if (!batchId) {
    return <EmptyState title="Batch ID required" description="Open this page with ?batchId=<uuid> so the frontend can call the authenticated export endpoint." />;
  }

  return (
    <RoleGuard allow={["CA", "ADMIN"]} fallback={<ErrorState message="Only CA and Admin users can export reports." />}>
      <div className="card">
        <h2>Export Reports</h2>
        <p>Exports use the authenticated backend endpoint so JWT-protected downloads work correctly for validation workbooks and draft GSTR-1 files.</p>
        <p>Batch ID: <span className="code">{batchId}</span></p>
        <div className="inline-actions">
          <button onClick={() => exportMutation.mutate({ type: "validation" })}>Download Validation Report</button>
          <button className="secondary" onClick={() => exportMutation.mutate({ type: "gstr1" })}>Download Draft GSTR-1</button>
        </div>
        {exportMutation.error ? <ErrorState message={(exportMutation.error as Error).message} /> : null}
      </div>
    </RoleGuard>
  );
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
