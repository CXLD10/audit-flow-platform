<<<<<<< HEAD
export default function FileUploader() {
  return <div>File uploader component scaffolded for later frontend phases.</div>;
=======
import { ChangeEvent } from "react";

export default function FileUploader({ onChange }: { onChange: (file: File | null) => void }) {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.files?.[0] ?? null);
  };

  return <input type="file" accept=".csv,.xlsx,.xls" onChange={handleChange} />;
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
}
