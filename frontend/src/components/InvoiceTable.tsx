import { Fragment, memo, useMemo, useState } from "react";
import ErrorBadge from "./ErrorBadge";
import EmptyState from "./EmptyState";
import { InvoiceRecord } from "../types";
import { formatCurrency, formatDate } from "../utils/formatters";

export type InvoiceTableProps = {
  invoices: InvoiceRecord[];
  onResolve?: (invoiceId: string) => void;
  canResolve?: boolean;
  loading?: boolean;
  matchMode?: boolean;
};

function severityForInvoice(invoice: InvoiceRecord): "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "CLEAN" {
  const severities = invoice.errors.map((error) => error.severity);
  if (severities.includes("CRITICAL")) return "CRITICAL";
  if (severities.includes("HIGH")) return "HIGH";
  if (severities.includes("MEDIUM")) return "MEDIUM";
  if (severities.includes("LOW")) return "LOW";
  return "CLEAN";
}

function InvoiceTableComponent({ invoices, onResolve, canResolve = false, loading = false, matchMode = false }: InvoiceTableProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const rows = useMemo(
    () => invoices.map((invoice) => ({ ...invoice, displaySeverity: severityForInvoice(invoice) })),
    [invoices],
  );

  if (loading) {
    return <div className="empty-panel">Loading invoice rows…</div>;
  }

  if (!rows.length) {
    return <EmptyState title="No invoices to show" description="Try a different batch, filter, or page selection." />;
  }

  return (
    <div className="table-shell">
      <table className="data-table">
        <thead>
          <tr>
            <th>Invoice</th>
            <th>Date</th>
            <th>Supplier GSTIN</th>
            <th>Total</th>
            <th>Severity</th>
            <th>State</th>
            <th>{matchMode ? "Match" : "Errors"}</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((invoice) => {
            const expanded = expandedId === invoice.id;
            return (
              <Fragment key={invoice.id}>
                <tr className={`severity-row ${invoice.displaySeverity}`}>
                  <td>
                    <button className="link-button" onClick={() => setExpandedId(expanded ? null : invoice.id)}>
                      {invoice.invoice_number}
                    </button>
                  </td>
                  <td>{formatDate(invoice.invoice_date)}</td>
                  <td className="code">{invoice.supplier_gstin}</td>
                  <td>{formatCurrency(invoice.total_invoice_value)}</td>
                  <td><ErrorBadge severity={invoice.displaySeverity} /></td>
                  <td>{invoice.state}</td>
                  <td>
                    {matchMode
                      ? invoice.reconciliation_result
                        ? `${invoice.reconciliation_result.match_type} (${invoice.reconciliation_result.confidence_score})`
                        : "Not reconciled"
                      : invoice.errors.length}
                  </td>
                  <td>
                    {canResolve && onResolve && invoice.state === "RECONCILED" ? (
                      <button className="secondary" onClick={() => onResolve(invoice.id)}>Mark Resolved</button>
                    ) : (
                      <span className="empty-state">—</span>
                    )}
                  </td>
                </tr>
                {expanded ? (
                  <tr className="expanded-row">
                    <td colSpan={8}>
                      <div className="expanded-grid">
                        <div>
                          <strong>Recipient GSTIN</strong>
                          <div className="code">{invoice.recipient_gstin}</div>
                        </div>
                        <div>
                          <strong>HSN/SAC</strong>
                          <div>{invoice.hsn_sac_code}</div>
                        </div>
                        <div>
                          <strong>GSTN Status</strong>
                          <div>{invoice.gstn_verification_status ?? "—"}</div>
                        </div>
                        <div>
                          <strong>Taxable Value</strong>
                          <div>{formatCurrency(invoice.taxable_value)}</div>
                        </div>
                        {invoice.errors.length ? (
                          <div className="expanded-errors">
                            <strong>Validation Errors</strong>
                            {invoice.errors.map((error) => (
                              <div key={error.id} className="error-item">
                                <ErrorBadge severity={error.severity} />
                                <div>
                                  <div><strong>{error.rule_id}</strong> — {error.message}</div>
                                  <div className="error-meta">Field: {error.field_name} | Actual: {error.actual_value} | Expected: {error.expected_value}</div>
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div className="expanded-errors clean-state">
                            <strong>No validation errors</strong>
                          </div>
                        )}
                      </div>
                    </td>
                  </tr>
                ) : null}
              </Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

const InvoiceTable = memo(InvoiceTableComponent);
export default InvoiceTable;
