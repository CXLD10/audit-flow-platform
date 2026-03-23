<<<<<<< HEAD
export default function ProgressBar() {
  return <div>Progress bar component scaffolded for later frontend phases.</div>;
=======
export default function ProgressBar({ pct }: { pct: number }) {
  return (
    <div className="progress-shell" aria-label="Batch progress">
      <div className="progress-bar" style={{ width: `${Math.max(0, Math.min(pct, 100))}%` }} />
    </div>
  );
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
