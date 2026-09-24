import { useEffect, useState } from "react";
import { api } from "../api/client";

const statusBadge = {
  upcoming: "🔵 Upcoming",
  live: "🔴 Live now",
  ended: "⚪ Ended",
};

export default function LiveSessions() {
  const [sessions, setSessions] = useState([]);
  const [timezones, setTimezones] = useState([]);
  const [viewTz, setViewTz] = useState("Asia/Kolkata");
  const [joined, setJoined] = useState({}); // sessionId -> join_link
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    const [sessRes, tzRes, meRes] = await Promise.all([
      api.get("/my/live-sessions"),
      api.get("/timezones"),
      api.get("/auth/me"),
    ]);
    setSessions(sessRes.data);
    setTimezones(tzRes.data.options);
    setViewTz(meRes.data.timezone || "Asia/Kolkata");
    setLoading(false);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleTzChange(tz) {
    setViewTz(tz);
    await api.patch("/users/me/timezone", { timezone: tz });
  }

  async function handleJoin(sessionId) {
    const res = await api.post(`/live-sessions/${sessionId}/join`);
    setJoined({ ...joined, [sessionId]: res.data.join_link });
  }

  function formatInTz(iso, tz) {
    try {
      return new Date(iso).toLocaleString("en-US", {
        timeZone: tz,
        dateStyle: "medium",
        timeStyle: "short",
      });
    } catch {
      return iso;
    }
  }

  if (loading) return <div className="text-gray-500">Loading…</div>;

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">🎥 Live sessions</h1>
        <button
          onClick={load}
          className="rounded-lg border border-gray-200 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50"
        >
          🔄 Refresh
        </button>
      </div>

      <div className="mt-4">
        <label className="text-sm font-medium text-gray-700">🌐 View times in</label>
        <select
          value={viewTz}
          onChange={(e) => handleTzChange(e.target.value)}
          className="mt-1 block w-full max-w-md rounded-lg border border-gray-300 px-3 py-2 text-sm"
        >
          {timezones.map((tz) => (
            <option key={tz} value={tz}>
              {tz}
            </option>
          ))}
        </select>
      </div>

      {sessions.length === 0 && (
        <div className="mt-6 rounded-lg bg-blue-50 px-4 py-3 text-sm text-blue-700">
          No live sessions scheduled yet for your courses.
        </div>
      )}

      <div className="mt-6 space-y-4">
        {sessions.map((s) => (
          <div key={s.id} className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <div className="font-semibold text-gray-900">
              {s.title} · {statusBadge[s.status]}
            </div>
            <div className="mt-1 text-xs text-gray-500">
              Course: {s.course_title} · Host: {s.host_name} ·{" "}
              {formatInTz(s.scheduled_at, viewTz)} · {s.duration_minutes} min
            </div>
            {s.description && <p className="mt-2 text-sm text-gray-600">{s.description}</p>}

            {!joined[s.id] ? (
              s.can_join ? (
                <button
                  onClick={() => handleJoin(s.id)}
                  className="mt-3 rounded-lg bg-red-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-red-700"
                >
                  🔴 Join session
                </button>
              ) : (
                <div className="mt-2 text-xs text-gray-500">{s.join_blocked_reason}</div>
              )
            ) : (
              <div className="mt-3">
                <div className="aspect-video w-full max-w-3xl overflow-hidden rounded-lg bg-black">
                  <iframe
                    src={joined[s.id]}
                    title={s.title}
                    className="h-full w-full"
                    allow="camera; microphone; fullscreen; display-capture"
                  />
                </div>
                <button
                  onClick={() => {
                    const next = { ...joined };
                    delete next[s.id];
                    setJoined(next);
                  }}
                  className="mt-2 rounded-lg border border-gray-200 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50"
                >
                  Leave session
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
