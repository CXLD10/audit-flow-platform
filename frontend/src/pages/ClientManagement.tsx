<<<<<<< HEAD
export default function ClientManagement() {
  return <div>Client management page scaffolded for later frontend phases.</div>;
=======
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { FormEvent, useMemo, useState } from "react";
import { createClient, listClients } from "../api/clients";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import FilterBar from "../components/FilterBar";
import RoleGuard from "../components/RoleGuard";

export default function ClientManagement() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [gstin, setGstin] = useState("");
  const [legalName, setLegalName] = useState("");
  const clientsQuery = useQuery({ queryKey: ["clients", 1], queryFn: () => listClients(1, 100) });
  const createMutation = useMutation({
    mutationFn: () => createClient({ gstin, legal_name: legalName }),
    onSuccess: async () => {
      setGstin("");
      setLegalName("");
      await queryClient.invalidateQueries({ queryKey: ["clients"] });
    },
  });

  const filteredClients = useMemo(
    () => (clientsQuery.data ?? []).filter((client) => client.legal_name.toLowerCase().includes(search.toLowerCase()) || client.gstin.includes(search)),
    [clientsQuery.data, search],
  );

  return (
    <RoleGuard allow={["CA", "ADMIN"]} fallback={<ErrorState message="Only CA and Admin users can manage clients." />}>
      <div className="grid two">
        <section className="card">
          <h2>Registered Clients</h2>
          <FilterBar onReset={() => setSearch("")}>
            <label>
              Search
              <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Client name or GSTIN" />
            </label>
          </FilterBar>
          {filteredClients.length ? (
            <div className="table-shell">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>GSTIN</th>
                    <th>Legal Name</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredClients.map((client) => (
                    <tr key={client.id}>
                      <td className="code">{client.gstin}</td>
                      <td>{client.legal_name}</td>
                      <td>{new Date(client.created_at).toLocaleDateString("en-IN")}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : <EmptyState title="No clients found" description="Create a client or broaden the search filter." />}
        </section>
        <section className="card">
          <h2>Add Client</h2>
          <form className="grid" onSubmit={(event: FormEvent) => { event.preventDefault(); createMutation.mutate(); }}>
            <label>
              GSTIN
              <input value={gstin} onChange={(event) => setGstin(event.target.value.toUpperCase())} maxLength={15} />
            </label>
            <label>
              Legal Name
              <input value={legalName} onChange={(event) => setLegalName(event.target.value)} />
            </label>
            <button type="submit" disabled={createMutation.isPending}>Create Client</button>
          </form>
          {createMutation.error ? <ErrorState message={(createMutation.error as Error).message} /> : null}
        </section>
      </div>
    </RoleGuard>
  );
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
