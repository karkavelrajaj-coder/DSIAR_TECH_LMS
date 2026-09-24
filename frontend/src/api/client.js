import axios from "axios";

// In dev, Vite proxies /api -> http://localhost:8000 (see vite.config.js).
// In production, set VITE_API_BASE_URL to the deployed Render backend URL.
const baseURL = import.meta.env.VITE_API_BASE_URL || "/api";

const TOKEN_KEY = "dsiar_access_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

export const api = axios.create({
  baseURL,
  withCredentials: true, // also sends the cookie, useful in local dev (same-origin via the Vite proxy)
});

// The deployed frontend and backend live on different onrender.com
// subdomains, and browsers (Incognito especially) block third-party
// cookies between them — so the cookie alone isn't reliable in
// production. Sending the JWT explicitly as a Bearer header works
// regardless of cookie policy, and is what the backend checks first.
api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.detail || err.message || "Something went wrong.";
    return Promise.reject(new Error(message));
  }
);
