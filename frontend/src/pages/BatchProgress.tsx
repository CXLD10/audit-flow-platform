import { useMemo } from "react";
import { NavLink, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getBatch } from "../api/batches";
import ErrorBadge from "../components/ErrorBadge";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import ProgressBar from "../components/ProgressBar";
import { useBatchProgress } from "../hooks/useBatchProgress";

export default function BatchProgress() {
  const [searchParams] = useSearchParams();
  const batchId = searchParams.get("batchId") ?? "";
  const progressQuery = useBatchProgress(batchId);
  const batchQuery = useQuery({ queryKey: ["batch", batchId], queryFn: () => getBatch(batchId), enabled: Boolean(batchId) });

  const stageOrder = ["PARSING", "NORMALIZATION", "ENTITY_RESOLUTION", "VALIDATION", "GSTN_VERIFICATION", "RECONCILIATION", "PRIORITIZATION"];
  const currentStageIndex = useMemo(() => stageOrder.indexOf(progressQuery.data?.stage ?? "PARSING"), [progressQuery.data?.stage]);

  if (!batchId) {
    return <EmptyState title="Batch ID required" description="Open this page with ?batchId=<uuid> to start polling progress." />;
  }

  if (progressQuery.error) {
    return <ErrorState message={(progressQuery.error as Error).message} />;
  }

  const progress = progressQuery.data;

  return (
    <div className="grid">
      <section className="card">
        <div className="inline-actions spread">
          <div>
            <h2>Batch Progress</h2>
            <p className="code">{batchId}</p>
          </div>
          <ErrorBadge severity={(progress?.status === "FAILED" ? "CRITICAL" : progress?.status === "COMPLETE" ? "CLEAN" : "MEDIUM") as "CRITICAL" | "MEDIUM" | "CLEAN"} />
        </div>
        <div className="grid">
          <div><strong>File:</strong> {batchQuery.data?.filename ?? "Loading…"}</div>
          <div><strong>Stage:</strong> {progress?.stage ?? "Queued"}</div>
          <div><strong>Processed:</strong> {progress?.processed ?? 0} / {progress?.total ?? 0}</div>
          <ProgressBar pct={progress?.pct ?? 0} />
        </div>
        {progress?.degraded ? <div className="warning-banner">GSTN verification is degraded. The batch continues with reduced confidence instead of failing.</div> : null}
        {progress?.error_message ? <ErrorState message={progress.error_message} /> : null}
      </section>
      <section className="card">
        <h3>Stage Timeline</h3>
        <div className="stage-strip">
          {stageOrder.map((stage, index) => {
            const active = index <= currentStageIndex;
            return <div key={stage} className={`stage-chip ${active ? "active" : ""}`}>{stage}</div>;
          })}
        </div>
        {progress?.status === "COMPLETE" ? (
          <div className="inline-actions">
            <NavLink to={`/validation?batchId=${batchId}`}>Open validation results</NavLink>
            <NavLink to={`/reconciliation?batchId=${batchId}`}>Open reconciliation results</NavLink>
            <NavLink to={`/export?batchId=${batchId}`}>Export reports</NavLink>
          </div>
        ) : null}
      </section>
    </div>
  );
}
