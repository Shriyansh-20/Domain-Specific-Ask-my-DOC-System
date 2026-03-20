// src/api.js

const BASE_URL = "http://127.0.0.1:8000/api";

export const uploadPDFs = async (files) => {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("file", file); // backend should accept multiple
  });

  const res = await fetch(`${BASE_URL}/upload/`, {
    method: "POST",
    body: formData,
  });

  return res.json();
};

export const askQuestion = async (question, session_id) => {
  const res = await fetch(`${BASE_URL}/ask/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question, session_id }),
  });

  return res.json();
};