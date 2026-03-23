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

  return (
    <div className="shell">
      <aside className="sidebar">
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
    </div>
  );
}
