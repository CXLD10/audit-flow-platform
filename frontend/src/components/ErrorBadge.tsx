<<<<<<< HEAD
export default function ErrorBadge() {
  return <span>Error badge scaffolded for later frontend phases.</span>;
=======
import { Severity } from "../types";

export default function ErrorBadge({ severity }: { severity: Severity | "CLEAN" }) {
  return <span className={`badge ${severity}`}>{severity}</span>;
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
