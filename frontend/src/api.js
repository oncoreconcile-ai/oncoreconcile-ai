/**
 * Shared API fetch helper for OncoReconcile AI frontend.
 * Tries multiple base URLs to find the backend automatically.
 */
const configuredApi = import.meta.env.VITE_API_BASE_URL;
const currentHostApi = `${window.location.protocol}//${window.location.hostname || "127.0.0.1"}:8000`;
const API_CANDIDATES = Array.from(new Set([
  configuredApi,
  currentHostApi,
  "http://127.0.0.1:8000",
  "http://localhost:8000",
].filter(Boolean)));

export async function apiFetch(path, options = {}) {
  let lastError;
  for (const baseUrl of API_CANDIDATES) {
    try {
      const response = await fetch(`${baseUrl}${path}`, options);
      window.__ONCORECONCILE_API_BASE__ = baseUrl;
      return response;
    } catch (error) {
      lastError = error;
    }
  }
  throw lastError || new Error("Backend API is not reachable.");
}
