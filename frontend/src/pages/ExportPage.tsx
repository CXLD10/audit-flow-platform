import { useState } from "react";
import { getExportUrl } from "../api/batches";
import RoleGuard from "../components/RoleGuard";

export default function ExportPage() {
  const [batchId, setBatchId] = useState("");

  return (
    <RoleGuard allow={["CA", "ADMIN"]}>
      <div className="card">
        <h2>Export Reports</h2>
        <label>
          Batch ID
          <input value={batchId} onChange={(event) => setBatchId(event.target.value)} placeholder="Enter batch UUID" />
        </label>
        <div className="inline-actions">
          <a href={getExportUrl(batchId, "validation")} target="_blank" rel="noreferrer"><button disabled={!batchId}>Validation Report</button></a>
          <a href={getExportUrl(batchId, "gstr1")} target="_blank" rel="noreferrer"><button className="secondary" disabled={!batchId}>Draft GSTR-1</button></a>
        </div>
      </div>
    </RoleGuard>
  );
}
