import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { FormEvent, useState } from "react";
import { createClient, listClients } from "../api/clients";
import RoleGuard from "../components/RoleGuard";

export default function ClientManagement() {
  const queryClient = useQueryClient();
  const clientsQuery = useQuery({ queryKey: ["clients"], queryFn: listClients });
  const [gstin, setGstin] = useState("");
  const [legalName, setLegalName] = useState("");
  const createMutation = useMutation({
    mutationFn: () => createClient({ gstin, legal_name: legalName }),
    onSuccess: async () => {
      setGstin("");
      setLegalName("");
      await queryClient.invalidateQueries({ queryKey: ["clients"] });
    },
  });

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    createMutation.mutate();
  };

  return (
    <RoleGuard allow={["CA", "ADMIN"]}>
      <div className="grid two">
        <section className="card">
          <h2>Registered Clients</h2>
          <table>
            <thead>
              <tr>
                <th>GSTIN</th>
                <th>Legal Name</th>
              </tr>
            </thead>
            <tbody>
              {(clientsQuery.data ?? []).map((client) => (
                <tr key={client.id}>
                  <td className="code">{client.gstin}</td>
                  <td>{client.legal_name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
        <section className="card">
          <h2>Add Client</h2>
          <form className="grid" onSubmit={handleSubmit}>
            <label>
              GSTIN
              <input value={gstin} onChange={(event) => setGstin(event.target.value)} maxLength={15} />
            </label>
            <label>
              Legal Name
              <input value={legalName} onChange={(event) => setLegalName(event.target.value)} />
            </label>
            <button type="submit" disabled={createMutation.isPending}>Create Client</button>
          </form>
        </section>
      </div>
    </RoleGuard>
  );
}
