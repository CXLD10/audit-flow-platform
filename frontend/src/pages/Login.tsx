<<<<<<< HEAD
export default function Login() {
  return <div>Login page scaffolded for later frontend phases.</div>;
=======
import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import ErrorState from "../components/ErrorState";
import { useAuth } from "../hooks/useAuth";
import { useAuthStore } from "../state/authStore";

export default function Login() {
  const navigate = useNavigate();
  const { login, isLoggingIn } = useAuth();
  const setSession = useAuthStore((state) => state.setSession);
  const [email, setEmail] = useState("ca@example.com");
  const [password, setPassword] = useState("password123");
  const [tenantId, setTenantId] = useState("00000000-0000-0000-0000-000000000001");
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");
    setSession({ tenantId });
    try {
      await login({ email, password });
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  };

  return (
    <div className="card login-card">
      <h2>Sign in</h2>
      <p>Authenticate with the tenant-aware backend before using upload, results, reconciliation, review, or export flows.</p>
      <form className="grid" onSubmit={handleSubmit}>
        <label>
          Tenant ID
          <input value={tenantId} onChange={(event) => setTenantId(event.target.value)} />
        </label>
        <label>
          Email
          <input value={email} onChange={(event) => setEmail(event.target.value)} />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
        </label>
        <button disabled={isLoggingIn} type="submit">{isLoggingIn ? "Signing in..." : "Sign in"}</button>
      </form>
      {error ? <ErrorState message={error} /> : null}
    </div>
  );
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
