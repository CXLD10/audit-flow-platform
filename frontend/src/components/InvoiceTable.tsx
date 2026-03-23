import ErrorBadge from "./ErrorBadge";

export type InvoiceRow = {
  id: string;
  invoice_number: string;
  supplier_gstin: string;
  total_invoice_value: string;
  state: string;
  errors?: Array<{ id: string; rule_id: string; severity: string; message: string }>;
  reconciliation_result?: { match_type: string; confidence_score: number } | null;
};

export default function InvoiceTable({ invoices }: { invoices: InvoiceRow[] }) {
  if (!invoices.length) {
    return <div className="empty-state">No invoices found for the selected batch.</div>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Invoice</th>
          <th>Supplier GSTIN</th>
          <th>Total Value</th>
          <th>State</th>
          <th>Errors</th>
          <th>Recon</th>
        </tr>
      </thead>
      <tbody>
        {invoices.map((invoice) => (
          <tr key={invoice.id}>
            <td>{invoice.invoice_number}</td>
            <td className="code">{invoice.supplier_gstin}</td>
            <td>{invoice.total_invoice_value}</td>
            <td>{invoice.state}</td>
            <td>
              {invoice.errors?.length ? (
                <div className="grid">
                  {invoice.errors.map((error) => (
                    <div key={error.id}>
                      <ErrorBadge severity={error.severity} /> {error.rule_id} — {error.message}
                    </div>
                  ))}
                </div>
              ) : (
                <span className="empty-state">Clean</span>
              )}
            </td>
            <td>
              {invoice.reconciliation_result ? `${invoice.reconciliation_result.match_type} (${invoice.reconciliation_result.confidence_score})` : "—"}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
