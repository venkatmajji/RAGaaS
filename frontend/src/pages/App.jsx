import React, { useState } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const upload = async () => {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch("/upload", { method: "POST", body: form });
    const data = await res.json();
    alert("Uploaded: " + JSON.stringify(data));
  };

  const ask = async () => {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    setAnswer(data.answer);
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">CloudDocs Chat</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={upload} className="ml-2 p-2 bg-blue-500 text-white">Upload</button>
      <div className="mt-6">
        <input value={question} onChange={e => setQuestion(e.target.value)} className="border p-2 w-96" />
        <button onClick={ask} className="ml-2 p-2 bg-green-500 text-white">Ask</button>
      </div>
      {answer && <p className="mt-4 p-4 bg-gray-100 rounded">Answer: {answer}</p>}
    </div>
  );
}
