import { useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getBatchResults } from "../api/batches";
import InvoiceTable, { InvoiceRow } from "../components/InvoiceTable";

export default function ValidationResults() {
  const [searchParams] = useSearchParams();
  const [severityFilter, setSeverityFilter] = useState("ALL");
  const batchId = searchParams.get("batchId") ?? "";
  const resultsQuery = useQuery({
    queryKey: ["batch-results", batchId],
    queryFn: () => getBatchResults(batchId),
    enabled: Boolean(batchId),
  });

  const filteredInvoices = useMemo(() => {
    const invoices = (resultsQuery.data?.invoices ?? []) as InvoiceRow[];
    if (severityFilter === "ALL") {
      return invoices;
    }
    return invoices.filter((invoice) => invoice.errors?.some((error) => error.severity === severityFilter));
  }, [resultsQuery.data?.invoices, severityFilter]);

  return (
    <div className="card">
      <h2>Validation Results</h2>
      <p>Batch ID: <span className="code">{batchId || "Provide ?batchId=..."}</span></p>
      <div className="inline-actions">
        <label>
          Severity Filter
          <select value={severityFilter} onChange={(event) => setSeverityFilter(event.target.value)}>
            <option value="ALL">All</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>
        </label>
      </div>
      {resultsQuery.data?.degraded_messages?.length ? (
        <div className="card">
          {resultsQuery.data.degraded_messages.map((message) => (
            <div key={message} className="badge MEDIUM">{message}</div>
          ))}
        </div>
      ) : null}
      <InvoiceTable invoices={filteredInvoices} />
    </div>
  );
}
