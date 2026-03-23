import { NavLink, Route, Routes } from "react-router-dom";
import AuditLog from "./pages/AuditLog";
import BatchProgress from "./pages/BatchProgress";
import BatchUpload from "./pages/BatchUpload";
import ClientManagement from "./pages/ClientManagement";
import Dashboard from "./pages/Dashboard";
import ExportPage from "./pages/ExportPage";
import Login from "./pages/Login";
import ReconciliationResults from "./pages/ReconciliationResults";
import ValidationResults from "./pages/ValidationResults";
import { useAuth } from "./hooks/useAuth";
<<<<<<< HEAD

const navigation = [
  ["/", "Dashboard"],
  ["/upload", "Upload"],
  ["/progress", "Progress"],
  ["/validation", "Validation"],
  ["/reconciliation", "Reconciliation"],
  ["/clients", "Clients"],
  ["/audit", "Audit"],
  ["/export", "Export"],
];

export default function App() {
  const { token } = useAuth();
=======
import RoleGuard from "./components/RoleGuard";

const navigation = [
  { path: "/", label: "Dashboard", roles: ["CA", "CLIENT", "ADMIN"] as const },
  { path: "/upload", label: "Upload", roles: ["CA", "CLIENT", "ADMIN"] as const },
  { path: "/progress", label: "Progress", roles: ["CA", "CLIENT", "ADMIN"] as const },
  { path: "/validation", label: "Validation", roles: ["CA", "CLIENT", "ADMIN"] as const },
  { path: "/reconciliation", label: "Reconciliation", roles: ["CA", "CLIENT", "ADMIN"] as const },
  { path: "/clients", label: "Clients", roles: ["CA", "ADMIN"] as const },
  { path: "/audit", label: "Audit", roles: ["ADMIN"] as const },
  { path: "/export", label: "Export", roles: ["CA", "ADMIN"] as const },
];

export default function App() {
  const { token, role, email, tenantId, logout } = useAuth();
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c

  return (
    <div className="shell">
      <aside className="sidebar">
<<<<<<< HEAD
        <h1>Tax Compliance</h1>
        <p>GST validation and reconciliation workspace.</p>
        <nav>
          {navigation.map(([path, label]) => (
            <NavLink key={path} to={path} className={({ isActive }) => (isActive ? "active-link" : "") }>
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="token-state">{token ? "Authenticated" : "Anonymous"}</div>
      </aside>
      <main className="content">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<BatchUpload />} />
          <Route path="/progress" element={<BatchProgress />} />
          <Route path="/validation" element={<ValidationResults />} />
          <Route path="/reconciliation" element={<ReconciliationResults />} />
          <Route path="/clients" element={<ClientManagement />} />
          <Route path="/audit" element={<AuditLog />} />
          <Route path="/export" element={<ExportPage />} />
        </Routes>
      </main>
=======
        <div>
          <div className="eyebrow">GST Compliance</div>
          <h1>Audit Flow Platform</h1>
          <p>Upload, validate, reconcile, review, and export client GST data with a deterministic workflow.</p>
        </div>
        <nav>
          {navigation.map((item) => (
            <RoleGuard key={item.path} allow={[...item.roles]}>
              <NavLink key={item.path} to={item.path} className={({ isActive }) => (isActive ? "active-link" : "") }>
                {item.label}
              </NavLink>
            </RoleGuard>
          ))}
        </nav>
      </aside>
      <div className="main-column">
        <header className="topbar">
          <div>
            <div className="topbar-title">Production Workspace</div>
            <div className="topbar-subtitle">Tenant <span className="code">{tenantId}</span></div>
          </div>
          <div className="topbar-user">
            <div>{email || "Not signed in"}</div>
            <div className="inline-actions">
              <span className="badge CLEAN">{role}</span>
              {token ? <button className="secondary" onClick={logout}>Sign out</button> : <NavLink to="/login">Sign in</NavLink>}
            </div>
          </div>
        </header>
        <main className="content">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<BatchUpload />} />
            <Route path="/progress" element={<BatchProgress />} />
            <Route path="/validation" element={<ValidationResults />} />
            <Route path="/reconciliation" element={<ReconciliationResults />} />
            <Route path="/clients" element={<ClientManagement />} />
            <Route path="/audit" element={<AuditLog />} />
            <Route path="/export" element={<ExportPage />} />
          </Routes>
        </main>
      </div>
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
    </div>
  );
}
