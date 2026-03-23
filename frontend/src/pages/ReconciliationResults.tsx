<<<<<<< HEAD
export default function ReconciliationResults() {
  return <div>Reconciliation results page scaffolded for later frontend phases.</div>;
=======
import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useSearchParams } from "react-router-dom";
import { getBatch, getBatchResults } from "../api/batches";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import FilterBar from "../components/FilterBar";
import InvoiceTable from "../components/InvoiceTable";
import { useInvoices } from "../hooks/useInvoices";
import { MatchType } from "../types";

const PAGE_SIZE = 100;

export default function ReconciliationResults() {
  const [searchParams] = useSearchParams();
  const batchId = searchParams.get("batchId") ?? "";
  const [page, setPage] = useState(1);
  const [matchFilter, setMatchFilter] = useState<MatchType | "ALL">("ALL");
  const [search, setSearch] = useState("");
  const invoicesQuery = useInvoices(batchId, page, PAGE_SIZE);
  const batchMetaQuery = useQuery({ queryKey: ["batch-meta", batchId], queryFn: () => getBatch(batchId), enabled: Boolean(batchId) });
  const batchResultsQuery = useQuery({ queryKey: ["batch-summary", batchId], queryFn: () => getBatchResults(batchId), enabled: Boolean(batchId) });

  const filteredInvoices = useMemo(() => {
    const rows = invoicesQuery.data?.items ?? [];
    return rows.filter((invoice) => {
      const currentMatch = invoice.reconciliation_result?.match_type ?? "UNMATCHED";
      const matchOk = matchFilter === "ALL" || currentMatch === matchFilter;
      const searchOk = !search || invoice.invoice_number.toLowerCase().includes(search.toLowerCase()) || invoice.supplier_gstin.includes(search);
      return matchOk && searchOk;
    });
  }, [invoicesQuery.data?.items, matchFilter, search]);

  const summary = useMemo(() => {
    const counts: Record<string, number> = { EXACT: 0, FUZZY: 0, HEURISTIC: 0, UNMATCHED: 0 };
    (batchResultsQuery.data?.invoices ?? []).forEach((invoice) => {
      const matchType = invoice.reconciliation_result?.match_type ?? "UNMATCHED";
      counts[matchType] = (counts[matchType] ?? 0) + 1;
    });
    return counts;
  }, [batchResultsQuery.data?.invoices]);

  if (!batchId) {
    return <EmptyState title="Batch ID required" description="Open this page with ?batchId=<uuid> to inspect reconciliation results." />;
  }
  if (invoicesQuery.error) {
    return <ErrorState message={(invoicesQuery.error as Error).message} />;
  }

  return (
    <div className="grid">
      <section className="card">
        <div className="inline-actions spread">
          <div>
            <h2>Reconciliation Results</h2>
            <p>{batchMetaQuery.data?.filename ?? "Batch"}</p>
          </div>
          <div className="summary-grid compact">
            {Object.entries(summary).map(([matchType, count]) => (
              <div key={matchType}><strong>{matchType}</strong><span>{count}</span></div>
            ))}
          </div>
        </div>
        <FilterBar onReset={() => { setMatchFilter("ALL"); setSearch(""); setPage(1); }}>
          <label>
            Match Type
            <select value={matchFilter} onChange={(event) => setMatchFilter(event.target.value as MatchType | "ALL")}>
              <option value="ALL">All matches</option>
              <option value="EXACT">Exact</option>
              <option value="FUZZY">Fuzzy</option>
              <option value="HEURISTIC">Heuristic</option>
              <option value="UNMATCHED">Unmatched</option>
            </select>
          </label>
          <label>
            Search
            <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Invoice number or GSTIN" />
          </label>
        </FilterBar>
        <InvoiceTable invoices={filteredInvoices} loading={invoicesQuery.isLoading} matchMode />
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
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
