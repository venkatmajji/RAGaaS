import React, { useEffect, useState } from "react";
import { supabase } from "../../../supabaseClient";
import LoginModal from "../../../components/LoginModal";

export default function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(false);

  const API_BASE = "https://ragaas.onrender.com";

  // Supabase auth listener
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user || null);
    });
    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user || null);
    });
    return () => listener.subscription.unsubscribe();
  }, []);

  const upload = async () => {
    if (!file) return alert("Please select a file to upload.");
    if (!user) return setShowLogin(true);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: form,
        headers: {
          Authorization: `Bearer ${(await supabase.auth.getSession()).data.session.access_token}`
        }
      });

      if (!res.ok) {
        const errText = await res.text();
        console.error(`❌ Server responded with ${res.status}: ${errText}`);
        alert(`Upload failed with ${res.status}: ${errText}`);
        return;
      }

      const data = await res.json();
      alert("✅ Uploaded: " + JSON.stringify(data));
    } catch (err) {
      alert("❌ Upload request failed.");
      console.error("Upload error:", err);
    }
  };

  const ask = async () => {
    if (!question.trim()) return alert("Please enter a question.");
    setLoading(true);
    setAnswer("");

    try {
      const res = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${(await supabase.auth.getSession()).data.session.access_token}`
        },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setAnswer(data.answer || "No answer returned.");
    } catch (err) {
      setAnswer("❌ Failed to get an answer.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto font-sans">
      <h1 className="text-2xl font-bold text-blue-700 mb-4">RAGaaS AI</h1>

      {!user ? (
        <>
          <button
            onClick={() => setShowLogin(true)}
            className="mb-4 px-4 py-2 bg-blue-700 text-white rounded"
          >
            Sign in to Upload or Ask
          </button>
          <LoginModal open={showLogin} onClose={() => setShowLogin(false)} />
        </>
      ) : (
        <>
          {/* Upload */}
          <div className="mb-6">
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            <button
              onClick={upload}
              className="ml-2 px-4 py-2 bg-blue-600 text-white rounded"
            >
              Upload
            </button>
          </div>

          {/* Ask */}
          <div className="mb-4">
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question..."
              className="border px-4 py-2 w-full rounded"
            />
            <button
              onClick={ask}
              disabled={loading}
              className="mt-2 px-4 py-2 bg-green-600 text-white rounded"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>

          {/* Answer */}
          {answer && (
            <div className="mt-4 bg-gray-100 p-4 rounded shadow">
              <h2 className="font-semibold text-gray-700 mb-2">Answer:</h2>
              <p>{answer}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
