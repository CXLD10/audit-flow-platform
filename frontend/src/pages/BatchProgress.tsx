import { useSearchParams } from "react-router-dom";
import ProgressBar from "../components/ProgressBar";
import { useBatchProgress } from "../hooks/useBatchProgress";

export default function BatchProgress() {
  const [searchParams] = useSearchParams();
  const batchId = searchParams.get("batchId") ?? "";
  const progressQuery = useBatchProgress(batchId);
  const progress = progressQuery.data;

  return (
    <div className="card">
      <h2>Batch Progress</h2>
      <p>Batch ID: <span className="code">{batchId || "Provide ?batchId=... in the URL"}</span></p>
      {progress ? (
        <div className="grid">
          <div>
            <strong>Stage:</strong> {progress.stage}
          </div>
          <ProgressBar pct={progress.pct} />
          <div>{progress.processed} processed out of {progress.total} rows.</div>
          <div>Status: <strong>{progress.status}</strong></div>
          {progress.degraded ? <div className="badge MEDIUM">Running in degraded mode due to external dependency failure.</div> : null}
          {progress.error_message ? <div className="badge CRITICAL">{progress.error_message}</div> : null}
        </div>
      ) : (
        <div className="empty-state">Waiting for a batch ID and progress data.</div>
      )}
    </div>
  );
}
