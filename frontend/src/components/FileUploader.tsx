import { ChangeEvent } from "react";

export default function FileUploader({ onChange }: { onChange: (file: File | null) => void }) {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.files?.[0] ?? null);
  };

  return <input type="file" accept=".csv,.xlsx,.xls" onChange={handleChange} />;
}
