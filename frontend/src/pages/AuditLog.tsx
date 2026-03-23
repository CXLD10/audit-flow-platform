<<<<<<< HEAD
export default function AuditLog() {
  return <div>Audit log page scaffolded for later frontend phases.</div>;
=======
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { apiClient } from "../api/client";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import FilterBar from "../components/FilterBar";
import RoleGuard from "../components/RoleGuard";
import { AuditLogRecord } from "../types";

async function listAuditLogs(page: number, pageSize: number) {
  const response = await apiClient.get<AuditLogRecord[]>("/admin/audit-logs", { params: { page, page_size: pageSize } });
  return response.data;
}

export default function AuditLog() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const query = useQuery({ queryKey: ["audit-logs", page], queryFn: () => listAuditLogs(page, 100) });
  const rows = (query.data ?? []).filter((log) => !search || log.action_type.toLowerCase().includes(search.toLowerCase()) || log.entity_type.toLowerCase().includes(search.toLowerCase()));

  return (
    <RoleGuard allow={["ADMIN"]} fallback={<ErrorState message="Audit log access is restricted to administrators." />}>
      <div className="card">
        <h2>Audit Log</h2>
        <FilterBar onReset={() => setSearch("")}>
          <label>
            Search
            <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Action or entity type" />
          </label>
        </FilterBar>
        {query.error ? <ErrorState message={(query.error as Error).message} /> : null}
        {rows.length ? (
          <div className="table-shell">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Action</th>
                  <th>Entity</th>
                  <th>Entity ID</th>
                  <th>Created At</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((log) => (
                  <tr key={log.id}>
                    <td>{log.action_type}</td>
                    <td>{log.entity_type}</td>
                    <td className="code">{log.entity_id}</td>
                    <td>{new Date(log.created_at).toLocaleString("en-IN")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : <EmptyState title="No audit events found" description="Change the page or clear the current search term." />}
        <div className="inline-actions spread">
          <div>Page {page}</div>
          <div className="inline-actions">
            <button className="secondary" disabled={page === 1} onClick={() => setPage((current) => current - 1)}>Previous</button>
            <button className="secondary" disabled={(query.data?.length ?? 0) < 100} onClick={() => setPage((current) => current + 1)}>Next</button>
          </div>
        </div>
      </div>
    </RoleGuard>
  );
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
