// Auto-detects whether the page is running locally or live, so admin.html
// always talks to the right backend without any manual editing.
// Covers both "double-click to open" (file://) and "served via localhost".
const isLocal =
  window.location.protocol === "file:" ||
  ["localhost", "127.0.0.1"].includes(window.location.hostname);
const API_BASE = isLocal
  ? "http://localhost:8000/api/v1"
  : "https://cataloq-for-furniture.onrender.com/api/v1";
