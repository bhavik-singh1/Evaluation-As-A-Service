import UploadCSV from "../components/UploadCSV";

export default function Home() {
  return (
    <main className="p-10">
      <h1 className="text-2xl font-bold mb-4">Upload CSV for Evaluation</h1>
      <UploadCSV />
    </main>
  );
}
