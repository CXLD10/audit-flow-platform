import { useQuery } from "@tanstack/react-query";
import { apiClient } from "../api/client";
import RoleGuard from "../components/RoleGuard";

async function listAuditLogs() {
  const response = await apiClient.get("/admin/audit-logs");
  return response.data as Array<{ id: string; action_type: string; entity_type: string; created_at: string }>;
}

export default function AuditLog() {
  const query = useQuery({ queryKey: ["audit-logs"], queryFn: listAuditLogs });

  return (
    <RoleGuard allow={["ADMIN"]}>
      <div className="card">
        <h2>Audit Log</h2>
        <table>
          <thead>
            <tr>
              <th>Action</th>
              <th>Entity</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {(query.data ?? []).map((log) => (
              <tr key={log.id}>
                <td>{log.action_type}</td>
                <td>{log.entity_type}</td>
                <td>{log.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </RoleGuard>
  );
}
