import { ReactNode } from "react";

export default function FilterBar({ children, onReset }: { children: ReactNode; onReset?: () => void }) {
  return (
    <div className="filter-bar">
      <div className="filter-controls">{children}</div>
      {onReset ? <button className="secondary" onClick={onReset}>Reset filters</button> : null}
    </div>
  );
}
