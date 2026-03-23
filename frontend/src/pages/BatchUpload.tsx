import { useMutation, useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadBatch } from "../api/batches";
import { listClients } from "../api/clients";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import FileUploader from "../components/FileUploader";
import { useAuthStore } from "../state/authStore";

export default function BatchUpload() {
  const navigate = useNavigate();
  const role = useAuthStore((state) => state.role);
  const [file, setFile] = useState<File | null>(null);
  const [clientGstin, setClientGstin] = useState("");
  const [returnPeriod, setReturnPeriod] = useState("");
  const clientsQuery = useQuery({ queryKey: ["clients", 1], queryFn: () => listClients(1, 100), enabled: role !== "CLIENT" });

  const uploadMutation = useMutation({
    mutationFn: async () => {
      if (!file || !clientGstin) {
        throw new Error("Client GSTIN and file are required before upload.");
      }
      return uploadBatch({ file, clientGstin, returnPeriod: returnPeriod || undefined });
    },
    onSuccess: (data) => {
      navigate(`/progress?batchId=${data.batch_id}`);
    },
  });

  const selectedClient = useMemo(
    () => clientsQuery.data?.find((client) => client.gstin === clientGstin),
    [clientGstin, clientsQuery.data],
  );

  return (
    <div className="grid two">
      <section className="card">
        <h2>Upload Invoice Batch</h2>
        <p>Upload purchase invoices for deterministic GST validation and reconciliation. The UI never waits for processing; it redirects to the live progress screen immediately after enqueue.</p>
        <div className="grid">
          {role === "CLIENT" ? (
            <label>
              Client GSTIN
              <input value={clientGstin} onChange={(event) => setClientGstin(event.target.value.toUpperCase())} placeholder="Enter your GSTIN" maxLength={15} />
            </label>
          ) : (
            <label>
              Client GSTIN
              <select value={clientGstin} onChange={(event) => setClientGstin(event.target.value)}>
                <option value="">Select a client</option>
                {clientsQuery.data?.map((client) => (
                  <option key={client.id} value={client.gstin}>{client.legal_name} — {client.gstin}</option>
                ))}
              </select>
            </label>
          )}
          <label>
            Return Period
            <input type="date" value={returnPeriod} onChange={(event) => setReturnPeriod(event.target.value)} />
          </label>
          <label>
            Invoice File
            <FileUploader onChange={setFile} />
          </label>
          <div className="file-meta">{file ? `Selected file: ${file.name}` : "Choose a CSV or Excel file up to 50MB."}</div>
        </div>
        <div className="inline-actions">
          <button disabled={uploadMutation.isPending} onClick={() => uploadMutation.mutate()}>{uploadMutation.isPending ? "Uploading…" : "Upload and Start Processing"}</button>
        </div>
        {uploadMutation.error ? <ErrorState message={(uploadMutation.error as Error).message} /> : null}
      </section>
      <section className="card">
        <h2>Upload Checklist</h2>
        <ul className="checklist">
          <li>Headers may be on a later row; the parser auto-detects them.</li>
          <li>Files are processed in 1,000-row chunks in the worker.</li>
          <li>Raw files are stored under a tenant-prefixed object path.</li>
          <li>GSTN verification may degrade gracefully without failing the batch.</li>
        </ul>
        {selectedClient ? (
          <div className="info-panel">
            <strong>Selected client:</strong>
            <div>{selectedClient.legal_name}</div>
            <div className="code">{selectedClient.gstin}</div>
          </div>
        ) : (
          <EmptyState title="No client selected" description="Choose a client GSTIN or enter one manually if you are signed in as a client user." />
        )}
      </section>
    </div>
  );
}
