import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getBatch, getBatchResults } from "../api/batches";
import { resolveInvoice } from "../api/invoices";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import FilterBar from "../components/FilterBar";
import InvoiceTable from "../components/InvoiceTable";
import { useInvoices } from "../hooks/useInvoices";
import { useAuthStore } from "../state/authStore";
import { Severity } from "../types";

const PAGE_SIZE = 100;

export default function ValidationResults() {
  const [searchParams] = useSearchParams();
  const batchId = searchParams.get("batchId") ?? "";
  const role = useAuthStore((state) => state.role);
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [severityFilter, setSeverityFilter] = useState<Severity | "ALL">("ALL");
  const [search, setSearch] = useState("");
  const invoicesQuery = useInvoices(batchId, page, PAGE_SIZE);
  const batchSummaryQuery = useQuery({ queryKey: ["batch-results-summary", batchId], queryFn: () => getBatchResults(batchId), enabled: Boolean(batchId) });
  const batchMetaQuery = useQuery({ queryKey: ["batch-meta", batchId], queryFn: () => getBatch(batchId), enabled: Boolean(batchId) });

  const resolveMutation = useMutation({
    mutationFn: (invoiceId: string) => resolveInvoice(invoiceId),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["invoices", batchId] });
      await queryClient.invalidateQueries({ queryKey: ["batch-results-summary", batchId] });
    },
  });

  const filteredInvoices = useMemo(() => {
    const rows = invoicesQuery.data?.items ?? [];
    return rows.filter((invoice) => {
      const severityMatch = severityFilter === "ALL" || invoice.errors.some((error) => error.severity === severityFilter);
      const searchMatch = !search || invoice.invoice_number.toLowerCase().includes(search.toLowerCase()) || invoice.supplier_gstin.includes(search);
      return severityMatch && searchMatch;
    });
  }, [invoicesQuery.data?.items, severityFilter, search]);

  if (!batchId) {
    return <EmptyState title="Batch ID required" description="Open this page with ?batchId=<uuid> to review validation results." />;
  }

  if (invoicesQuery.error) {
    return <ErrorState message={(invoicesQuery.error as Error).message} />;
  }

  return (
    <div className="grid">
      <section className="card">
        <div className="inline-actions spread">
          <div>
            <h2>Validation Results</h2>
            <p>{batchMetaQuery.data?.filename ?? "Batch"} — {batchMetaQuery.data?.status ?? "Loading…"}</p>
          </div>
          <div className="summary-grid compact">
            <div><strong>Invoices</strong><span>{batchMetaQuery.data?.total_invoices ?? 0}</span></div>
            <div><strong>Errors</strong><span>{batchMetaQuery.data?.error_count ?? 0}</span></div>
          </div>
        </div>
        {batchSummaryQuery.data?.degraded_messages?.map((message) => <div key={message} className="warning-banner">{message}</div>)}
        <FilterBar onReset={() => { setSeverityFilter("ALL"); setSearch(""); setPage(1); }}>
          <label>
            Severity
            <select value={severityFilter} onChange={(event) => setSeverityFilter(event.target.value as Severity | "ALL")}>
              <option value="ALL">All severities</option>
              <option value="CRITICAL">Critical</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
          </label>
          <label>
            Search
            <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Invoice number or GSTIN" />
          </label>
        </FilterBar>
        <InvoiceTable invoices={filteredInvoices} loading={invoicesQuery.isLoading} canResolve={role !== "CLIENT"} onResolve={(invoiceId) => resolveMutation.mutate(invoiceId)} />
        <div className="inline-actions spread">
          <div>Page {page}</div>
          <div className="inline-actions">
            <button className="secondary" disabled={page === 1} onClick={() => setPage((current) => current - 1)}>Previous</button>
            <button className="secondary" disabled={(invoicesQuery.data?.items.length ?? 0) < PAGE_SIZE} onClick={() => setPage((current) => current + 1)}>Next</button>
          </div>
        </div>
      </section>
    </div>
  );
}
