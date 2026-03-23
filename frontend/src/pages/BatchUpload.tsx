import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadBatch } from "../api/batches";
import { listClients } from "../api/clients";
import FileUploader from "../components/FileUploader";

export default function BatchUpload() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [clientGstin, setClientGstin] = useState("");
  const [returnPeriod, setReturnPeriod] = useState("");

  const clientsQuery = useQuery({ queryKey: ["clients"], queryFn: listClients });
  const uploadMutation = useMutation({
    mutationFn: () => {
      if (!file || !clientGstin) {
        throw new Error("Client GSTIN and file are required");
      }
      return uploadBatch({ file, clientGstin, returnPeriod: returnPeriod || undefined });
    },
    onSuccess: (data) => {
      navigate(`/progress?batchId=${data.batch_id}`);
    },
  });

  return (
    <div className="card">
      <h2>Upload Invoice Batch</h2>
      <p>Accepted formats: CSV, XLSX, XLS. The API returns immediately after object storage upload and Celery enqueue.</p>
      <div className="grid two">
        <label>
          Client GSTIN
          <select value={clientGstin} onChange={(event) => setClientGstin(event.target.value)}>
            <option value="">Select a client</option>
            {clientsQuery.data?.map((client) => (
              <option key={client.id} value={client.gstin}>{client.legal_name} — {client.gstin}</option>
            ))}
          </select>
        </label>
        <label>
          Return Period
          <input type="date" value={returnPeriod} onChange={(event) => setReturnPeriod(event.target.value)} />
        </label>
      </div>
      <div className="card">
        <FileUploader onChange={setFile} />
        <p>{file ? `Selected file: ${file.name}` : "No file selected yet."}</p>
      </div>
      <div className="inline-actions">
        <button disabled={uploadMutation.isPending} onClick={() => uploadMutation.mutate()}>
          {uploadMutation.isPending ? "Uploading..." : "Upload and Process"}
        </button>
      </div>
      {uploadMutation.error ? <p className="badge CRITICAL">{(uploadMutation.error as Error).message}</p> : null}
    </div>
  );
}
