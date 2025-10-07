"use client";
import { useState } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

export default function UploadCSV() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) return alert("Please select a CSV file.");

    const { data, error } = await supabase.storage
      .from("uploads")
      .upload(`csvs/${file.name}`, file);

    if (error) return alert(error.message);

    const fileUrl = `${process.env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/public/uploads/csvs/${file.name}`;

    // Insert into eval_jobs
    const { error: insertError } = await supabase
      .from("eval_jobs")
      .insert([{ status: "pending", file_url: fileUrl }]);

    if (insertError) return alert(insertError.message);

    setMessage("File uploaded & job created successfully ✅");
  };

  return (
    <div className="p-6 border rounded-lg shadow-md">
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Upload CSV
      </button>
      {message && <p className="mt-4 text-green-600">{message}</p>}
    </div>
  );
}
