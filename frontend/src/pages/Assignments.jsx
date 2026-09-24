import { useEffect, useState } from "react";
import { api } from "../api/client";

const statusStyles = {
  approved: "bg-green-50 text-green-700",
  rejected: "bg-red-50 text-red-700",
  pending: "bg-yellow-50 text-yellow-700",
};

export default function Assignments() {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [drafts, setDrafts] = useState({});

  async function load() {
    setLoading(true);
    const res = await api.get("/my/assignments");
    setAssignments(res.data);
    setLoading(false);
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(assignmentId) {
    const text = (drafts[assignmentId] || "").trim();
    if (!text) return;
    await api.post(`/assignments/${assignmentId}/submit`, { link_or_text: text });
    load();
  }

  if (loading) return <div className="text-gray-500">Loading…</div>;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">📝 Assignments</h1>

      {assignments.length === 0 && (
        <div className="mt-6 rounded-lg bg-blue-50 px-4 py-3 text-sm text-blue-700">
          Enroll in a course to see its assignments here.
        </div>
      )}

      <div className="mt-6 space-y-4">
        {assignments.map((a) => (
          <div key={a.id} className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900">{a.title}</h2>
            <div className="text-xs text-gray-500">
              Course: {a.course_title} · Due: {a.due_date || "No deadline"}
            </div>

            {a.locked ? (
              <div className="mt-3 rounded-lg bg-yellow-50 px-3 py-2 text-sm text-yellow-700">
                🔒 Locked — finish all the lessons in <strong>{a.course_title}</strong> to
                unlock this assignment ({a.lessons_completed}/{a.lessons_total} lessons completed).
              </div>
            ) : (
              <>
                <p className="mt-2 text-sm text-gray-600">{a.description}</p>

                {a.submission ? (
                  <div className="mt-3">
                    <span
                      className={`inline-block rounded-full px-3 py-1 text-xs font-medium ${
                        statusStyles[a.submission.status] || statusStyles.pending
                      }`}
                    >
                      {a.submission.status === "approved" && "✅ Approved"}
                      {a.submission.status === "rejected" && "❌ Needs revision"}
                      {a.submission.status === "pending" && "⏳ Pending review"}
                    </span>
                    <div className="mt-2 text-sm text-gray-600">
                      Your submission: {a.submission.link_or_text}
                    </div>
                    {a.submission.status !== "pending" && (
                      <div className="mt-1 text-sm text-gray-600">
                        Grade: {a.submission.grade ?? "—"} · Feedback: {a.submission.feedback || "—"}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="mt-3">
                    <textarea
                      rows={3}
                      placeholder="Paste your project link (GitHub/Colab/Drive) or answer"
                      value={drafts[a.id] || ""}
                      onChange={(e) => setDrafts({ ...drafts, [a.id]: e.target.value })}
                      className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-purple-500 focus:outline-none"
                    />
                    <button
                      onClick={() => submit(a.id)}
                      className="mt-2 rounded-lg bg-purple-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-purple-700"
                    >
                      Submit assignment
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
