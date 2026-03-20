import React from "react";

const Loader = () => {
  return (
    <div style={{ display: "flex", gap: "6px" }}>
      <div className="dot" />
      <div className="dot" />
      <div className="dot" />
    </div>
  );
};

export default Loader;