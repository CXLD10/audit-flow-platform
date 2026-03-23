import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useAuthStore } from "../state/authStore";

export default function Login() {
  const navigate = useNavigate();
  const { login, isLoggingIn } = useAuth();
  const setAuth = useAuthStore((state) => state.setAuth);
  const [email, setEmail] = useState("ca@example.com");
  const [password, setPassword] = useState("password123");
  const [tenantId, setTenantId] = useState("00000000-0000-0000-0000-000000000001");
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");
    setAuth({ tenantId });
    try {
      await login({ email, password });
      setAuth({ email, role: "CA" });
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  };

  return (
    <div className="card">
      <h2>Login</h2>
      <p>Use the tenant header and JWT login flow required by the backend auth route.</p>
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
        {error ? <div className="badge CRITICAL">{error}</div> : null}
      </form>
    </div>
  );
}
