// public toggle UI component in React
import { useState } from "react";

export default function PublicToggle({ doc_id, isPublic }) {
  const [isPublicState, setIsPublicState] = useState(isPublic);

  const toggle = async () => {
    const newStatus = !isPublicState;
    await fetch("/api/documents/toggle-public", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ doc_id, is_public: newStatus }),
    });
    setIsPublicState(newStatus);
  };

  return (
    <label style={{ display: "flex", alignItems: "center", gap: "8px" }}>
      <input type="checkbox" checked={isPublicState} onChange={toggle} />
      Public
    </label>
  );
}
