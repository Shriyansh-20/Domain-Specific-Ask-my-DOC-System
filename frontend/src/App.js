import React, { useState, useEffect } from "react";
import Upload from "./components/Upload";
import Chat from "./components/Chat";
import FileList from "./components/FileList";
import "./styles.css";

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [files, setFiles] = useState([]);
  const [dark, setDark] = useState(false);

  useEffect(() => {
    document.body.className = dark ? "dark" : "";
  }, [dark]);

  return (
    <div className="container">
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h2>Document QA System</h2>

        <button onClick={() => setDark(!dark)}>
          {dark ? "Light" : "Dark"}
        </button>
      </div>

      <Upload
        sessionId={sessionId}
        setSessionId={setSessionId}
        setFiles={setFiles}
      />

      <FileList files={files} />

      {sessionId && <Chat sessionId={sessionId} />}
    </div>
  );
}

export default App;