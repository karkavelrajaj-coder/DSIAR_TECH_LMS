import { useEffect, useState } from "react";
import { api } from "../../api/client";

const statusBadge = { upcoming: "🔵 Upcoming", live: "🔴 Live now", ended: "⚪ Ended" };

export default function ManageLiveSessions() {
  const [courses, setCourses] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [timezones, setTimezones] = useState([]);
  const [hostView, setHostView] = useState({}); // sessionId -> join_link
  const [form, setForm] = useState({
    course_id: "",
    title: "",
    description: "",
    date: "",
    time: "18:00",
    timezone: "Asia/Kolkata",
    duration_minutes: 60,
  });

  async function load() {
    const [cRes, sRes, tzRes] = await Promise.all([
      api.get("/courses/manage"),
      api.get("/live-sessions/manage"),
      api.get("/timezones"),
    ]);
    setCourses(cRes.data);
    setSessions(sRes.data);
    setTimezones(tzRes.data.options);
  }

  useEffect(() => {
    load();
  }, []);

  const courseTitle = (id) => courses.find((c) => c.id === id)?.title || "Unknown";

  async function schedule(e) {
    e.preventDefault();
    if (!form.course_id || !form.title || !form.date) return;
    await api.post("/live-sessions", { ...form, time: `${form.time}:00` });
    setForm({ ...form, title: "", description: "" });
    load();
  }

  async function deleteSession(id) {
    if (!confirm("Delete this session?")) return;
    await api.delete(`/live-sessions/${id}`);
    load();
  }

  async function startSession(id) {
    try {
      const res = await api.post(`/live-sessions/${id}/start`);
      setHostView({ ...hostView, [id]: res.data.join_link });
      load();
    } catch (err) {
      alert(err.message);
    }
  }

  async function endSession(id) {
    await api.post(`/live-sessions/${id}/end`);
    const next = { ...hostView };
    delete next[id];
    setHostView(next);
    load();
  }

  function formatUtc(iso) {
    return new Date(iso).toLocaleString();
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">🎥 Manage live sessions</h1>
      <p className="text-sm text-gray-500">
        Admins schedule for every course. Instructors only schedule for courses assigned to them.
      </p>

      <form onSubmit={schedule} className="mt-6 space-y-3 rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="font-semibold text-gray-900">➕ Schedule a new live session</h2>
        <select
          value={form.course_id}
          onChange={(e) => setForm({ ...form, course_id: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        >
          <option value="">Select course</option>
          {courses.map((c) => (
            <option key={c.id} value={c.id}>
              {c.title}
            </option>
          ))}
        </select>
        <input
          placeholder="Session title, e.g. Live Q&A: Neural Networks"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <textarea
          placeholder="What will this session cover? (optional)"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <select
          value={form.timezone}
          onChange={(e) => setForm({ ...form, timezone: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        >
          {timezones.map((tz) => (
            <option key={tz} value={tz}>
              {tz}
            </option>
          ))}
        </select>
        <div className="grid grid-cols-3 gap-2">
          <input
            type="date"
            value={form.date}
            onChange={(e) => setForm({ ...form, date: e.target.value })}
            className="rounded-lg border border-gray-300 px-3 py-2 text-sm"
          />
          <input
            type="time"
            value={form.time}
            onChange={(e) => setForm({ ...form, time: e.target.value })}
            className="rounded-lg border border-gray-300 px-3 py-2 text-sm"
          />
          <input
            type="number"
            min={15}
            max={300}
            step={15}
            value={form.duration_minutes}
            onChange={(e) => setForm({ ...form, duration_minutes: Number(e.target.value) })}
            className="rounded-lg border border-gray-300 px-3 py-2 text-sm"
          />
        </div>
        <button type="submit" className="rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white hover:bg-purple-700">
          Schedule session
        </button>
      </form>

      <div className="mt-6 space-y-4">
        {sessions.map((s) => (
          <div key={s.id} className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-semibold text-gray-900">
                  {s.title} · {statusBadge[s.status]}
                </div>
                <div className="text-xs text-gray-500">
                  Course: {courseTitle(s.course_id)} · Host: {s.host_name} · {formatUtc(s.scheduled_at)} (
                  {s.scheduled_tz}) · {s.duration_minutes} min
                </div>
              </div>
              <button onClick={() => deleteSession(s.id)} className="text-sm text-red-600 hover:underline">
                🗑 Delete
              </button>
            </div>
            {s.description && <p className="mt-2 text-sm text-gray-600">{s.description}</p>}

            <div className="mt-2 text-xs text-gray-500">
              {s.ended_at && `✅ Ended at ${formatUtc(s.ended_at)}.`}
              {!s.ended_at && s.started_at && `🟢 Started at ${formatUtc(s.started_at)} — students can now join.`}
              {!s.ended_at && !s.started_at && "⏳ Not started yet — students won't see an active Join button until you start it."}
            </div>

            {!hostView[s.id] ? (
              <button
                onClick={() => startSession(s.id)}
                className="mt-3 rounded-lg bg-green-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-green-700"
              >
                {s.ended_at ? "🔁 Start a new session" : "▶️ Start / rejoin session"}
              </button>
            ) : (
              <div className="mt-3">
                <div className="aspect-video w-full max-w-3xl overflow-hidden rounded-lg bg-black">
                  <iframe
                    src={hostView[s.id]}
                    title={s.title}
                    className="h-full w-full"
                    allow="camera; microphone; fullscreen; display-capture"
                  />
                </div>
                <div className="mt-2 flex gap-2">
                  <button
                    onClick={() => {
                      const next = { ...hostView };
                      delete next[s.id];
                      setHostView(next);
                    }}
                    className="rounded-lg border border-gray-200 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50"
                  >
                    Leave (keep session open)
                  </button>
                  <button
                    onClick={() => endSession(s.id)}
                    className="rounded-lg bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700"
                  >
                    🔴 End session for everyone
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
