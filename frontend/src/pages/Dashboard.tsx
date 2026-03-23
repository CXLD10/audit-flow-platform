<<<<<<< HEAD
export default function Dashboard() {
  return <div>Dashboard scaffolded for later frontend phases.</div>;
=======
import { useMemo } from "react";
import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getBatch, getBatchProgress } from "../api/batches";
import EmptyState from "../components/EmptyState";
import ErrorBadge from "../components/ErrorBadge";

export default function Dashboard() {
  const [searchParams] = useSearchParams();
  const batchId = searchParams.get("batchId") ?? "";
  const batchQuery = useQuery({ queryKey: ["batch-summary", batchId], queryFn: () => getBatch(batchId), enabled: Boolean(batchId) });
  const progressQuery = useQuery({ queryKey: ["batch-progress-summary", batchId], queryFn: () => getBatchProgress(batchId), enabled: Boolean(batchId) });

  const metrics = useMemo(
    () => [
      { label: "Selected Batch", value: batchId || "None" },
      { label: "Status", value: batchQuery.data?.status ?? "No batch selected" },
      { label: "Invoices", value: batchQuery.data?.total_invoices ?? 0 },
      { label: "Errors", value: batchQuery.data?.error_count ?? 0 },
    ],
    [batchId, batchQuery.data],
  );

  return (
    <div className="grid">
      <section className="card">
        <h2>Workspace Overview</h2>
        <p>Use the query string <span className="code">?batchId=&lt;uuid&gt;</span> in dashboard-linked pages to inspect an active upload batch end-to-end.</p>
      </section>
      <section className="grid four-up">
        {metrics.map((metric) => (
          <div className="metric-card" key={metric.label}>
            <div className="metric-label">{metric.label}</div>
            <div className="metric-value">{String(metric.value)}</div>
          </div>
        ))}
      </section>
      <section className="grid two">
        <div className="card">
          <h3>Pipeline</h3>
          <ol className="timeline">
            <li>Upload</li>
            <li>Parsing</li>
            <li>Normalization</li>
            <li>Entity Resolution</li>
            <li>Validation</li>
            <li>GSTN Verification</li>
            <li>Reconciliation</li>
            <li>Review & Export</li>
          </ol>
        </div>
        <div className="card">
          <h3>Current Batch Snapshot</h3>
          {batchId ? (
            <div className="grid">
              <div><strong>Filename:</strong> {batchQuery.data?.filename ?? "Loading…"}</div>
              <div><strong>Progress stage:</strong> {progressQuery.data?.stage ?? "—"}</div>
              <div><strong>Progress:</strong> {progressQuery.data?.pct ?? 0}%</div>
              <div><ErrorBadge severity={(progressQuery.data?.status === "FAILED" ? "CRITICAL" : progressQuery.data?.status === "COMPLETE" ? "CLEAN" : "MEDIUM") as "CRITICAL" | "MEDIUM" | "CLEAN"} /></div>
            </div>
          ) : (
            <EmptyState title="No batch selected" description="Open a recent batch in the progress, validation, reconciliation, or export pages to inspect it here." />
          )}
        </div>
      </section>
    </div>
  );
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
