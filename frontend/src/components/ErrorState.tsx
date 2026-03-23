export default function ErrorState({ message }: { message: string }) {
  return <div className="error-panel">{message}</div>;
}
