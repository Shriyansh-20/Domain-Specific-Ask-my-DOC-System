import React, { useState } from "react";
import { uploadPDFs } from "../api";
import Loader from "./Loader";

const Upload = ({ sessionId, setSessionId, setFiles }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!selectedFiles.length) return;

    setLoading(true);

    const res = await uploadPDFs(selectedFiles);

    if (!sessionId) setSessionId(res.session_id);

    setFiles(prev => [...prev, ...selectedFiles.map(f => f.name)]);
    setSelectedFiles([]);
    setLoading(false);
  };

  return (
    <div className="card">
      <h3>Upload Documents</h3>

      <input
        type="file"
        multiple
        onChange={(e) => setSelectedFiles(Array.from(e.target.files))}
      />

      <div style={{ marginTop: "10px" }}>
        <button onClick={handleUpload} disabled={loading}>
          {loading ? <Loader /> : "Upload"}
        </button>
      </div>
    </div>
  );
};

export default Upload;