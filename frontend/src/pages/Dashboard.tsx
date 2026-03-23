import { useAuth } from "../hooks/useAuth";

export default function Dashboard() {
  const { profile, token, role, tenantId } = useAuth();

  return (
    <div className="grid two">
      <section className="card">
        <h2>Workspace Overview</h2>
        <p>This dashboard is optimized for the production workflow defined in the GST compliance contexts: upload, validate, reconcile, review, and export.</p>
        <ul>
          <li>Auth token present: {token ? "Yes" : "No"}</li>
          <li>Tenant ID: <span className="code">{tenantId}</span></li>
          <li>Role: {profile?.role ?? role}</li>
        </ul>
      </section>
      <section className="card">
        <h2>Pipeline Stages</h2>
        <ol>
          <li>Upload</li>
          <li>Parse</li>
          <li>Normalize</li>
          <li>Entity Resolve</li>
          <li>Validate</li>
          <li>GSTN Verify</li>
          <li>Reconcile</li>
          <li>Prioritize</li>
          <li>Export</li>
        </ol>
      </section>
    </div>
  );
}
