import { useQuery } from "@tanstack/react-query";
import { useSearchParams } from "react-router-dom";
import { getBatchResults } from "../api/batches";

export default function ReconciliationResults() {
  const [searchParams] = useSearchParams();
  const batchId = searchParams.get("batchId") ?? "";
  const resultsQuery = useQuery({
    queryKey: ["reconciliation-results", batchId],
    queryFn: () => getBatchResults(batchId),
    enabled: Boolean(batchId),
  });

  const invoices = (resultsQuery.data?.invoices ?? []) as Array<Record<string, any>>;
  const summary = invoices.reduce<Record<string, number>>((acc, invoice) => {
    const matchType = invoice.reconciliation_result?.match_type ?? "UNAVAILABLE";
    acc[matchType] = (acc[matchType] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <div className="card">
      <h2>Reconciliation Results</h2>
      <div className="grid three">
        {Object.entries(summary).map(([matchType, count]) => (
          <div className="card" key={matchType}>
            <strong>{matchType}</strong>
            <div>{count} invoices</div>
          </div>
        ))}
      </div>
      <table>
        <thead>
          <tr>
            <th>Invoice</th>
            <th>Supplier GSTIN</th>
            <th>Match Type</th>
            <th>Confidence</th>
          </tr>
        </thead>
        <tbody>
          {invoices.map((invoice) => (
            <tr key={invoice.id}>
              <td>{invoice.invoice_number}</td>
              <td className="code">{invoice.supplier_gstin}</td>
              <td>{invoice.reconciliation_result?.match_type ?? "—"}</td>
              <td>{invoice.reconciliation_result?.confidence_score ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
