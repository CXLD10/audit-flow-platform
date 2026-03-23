import { Severity } from "../types";

export default function ErrorBadge({ severity }: { severity: Severity | "CLEAN" }) {
  return <span className={`badge ${severity}`}>{severity}</span>;
}
