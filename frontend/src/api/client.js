import axios from "axios";

// In dev, Vite proxies /api -> http://localhost:8000 (see vite.config.js).
// In production, set VITE_API_BASE_URL to the deployed Render backend URL.
const baseURL = import.meta.env.VITE_API_BASE_URL || "/api";

export const api = axios.create({
  baseURL,
  withCredentials: true, // sends/receives the httpOnly JWT cookie
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.detail || err.message || "Something went wrong.";
    return Promise.reject(new Error(message));
  }
);
