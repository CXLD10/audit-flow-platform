export default function ErrorBadge({ severity }: { severity: string }) {
  return <span className={`badge ${severity}`}>{severity}</span>;
}
