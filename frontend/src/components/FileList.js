import React from "react";

const FileList = ({ files }) => {
  return (
    <div className="card">
      <h4>Documents</h4>

      {files.length === 0 ? (
        <p>No documents uploaded</p>
      ) : (
        <div>
          {files.map((file, i) => (
            <div key={i}>{file}</div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FileList;