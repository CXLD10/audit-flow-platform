export default function ProgressBar({ pct }: { pct: number }) {
  return (
    <div className="progress-shell" aria-label="Batch progress">
      <div className="progress-bar" style={{ width: `${pct}%` }} />
    </div>
  );
}
