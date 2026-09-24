import { useEffect, useState } from "react";
import { api } from "../../api/client";

export default function Grading() {
  const [courses, setCourses] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [submissionsByAssignment, setSubmissionsByAssignment] = useState({});
  const [newAssignment, setNewAssignment] = useState({ course_id: "", title: "", description: "", due_date: "" });
  const [drafts, setDrafts] = useState({});

  async function load() {
    const [cRes, aRes] = await Promise.all([api.get("/courses/manage"), api.get("/assignments/manage")]);
    setCourses(cRes.data);
    setAssignments(aRes.data);
    for (const a of aRes.data) loadSubmissions(a.id);
  }

  async function loadSubmissions(assignmentId) {
    const res = await api.get(`/assignments/${assignmentId}/submissions`);
    setSubmissionsByAssignment((prev) => ({ ...prev, [assignmentId]: res.data }));
  }

  useEffect(() => {
    load();
  }, []);

  const courseTitle = (id) => courses.find((c) => c.id === id)?.title || "Unknown";

  async function postAssignment(e) {
    e.preventDefault();
    if (!newAssignment.course_id || !newAssignment.title) return;
    await api.post("/assignments", newAssignment);
    setNewAssignment({ course_id: "", title: "", description: "", due_date: "" });
    load();
  }

  async function deleteAssignment(id) {
    if (!confirm("Delete this assignment and all its submissions?")) return;
    await api.delete(`/assignments/${id}`);
    load();
  }

  function updateDraft(subId, field, value) {
    setDrafts((prev) => ({ ...prev, [subId]: { ...prev[subId], [field]: value } }));
  }

  async function saveGrade(assignmentId, sub) {
    const draft = drafts[sub.id] || {};
    await api.patch(`/submissions/${sub.id}`, {
      grade: draft.grade ?? sub.grade ?? 0,
      status: draft.status ?? sub.status,
      feedback: draft.feedback ?? sub.feedback ?? "",
    });
    loadSubmissions(assignmentId);
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">📥 Assignments & grading</h1>

      <form onSubmit={postAssignment} className="mt-6 space-y-3 rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="font-semibold text-gray-900">➕ Post a new assignment</h2>
        <select
          value={newAssignment.course_id}
          onChange={(e) => setNewAssignment({ ...newAssignment, course_id: e.target.value })}
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
          placeholder="Assignment title"
          value={newAssignment.title}
          onChange={(e) => setNewAssignment({ ...newAssignment, title: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <textarea
          placeholder="Description / instructions"
          value={newAssignment.description}
          onChange={(e) => setNewAssignment({ ...newAssignment, description: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <input
          type="date"
          value={newAssignment.due_date}
          onChange={(e) => setNewAssignment({ ...newAssignment, due_date: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <button type="submit" className="rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white hover:bg-purple-700">
          Post assignment
        </button>
      </form>

      <div className="mt-6 space-y-4">
        {assignments.map((a) => (
          <div key={a.id} className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-semibold text-gray-900">{a.title}</h2>
                <div className="text-xs text-gray-500">
                  Course: {courseTitle(a.course_id)} · Due: {a.due_date || "No deadline"}
                </div>
              </div>
              <button onClick={() => deleteAssignment(a.id)} className="text-sm text-red-600 hover:underline">
                🗑 Delete
              </button>
            </div>
            <p className="mt-2 text-sm text-gray-600">{a.description}</p>

            <div className="mt-3 space-y-3">
              {(submissionsByAssignment[a.id] || []).length === 0 && (
                <div className="text-xs text-gray-400">No submissions yet.</div>
              )}
              {(submissionsByAssignment[a.id] || []).map((s) => (
                <div key={s.id} className="rounded-lg border border-gray-100 bg-gray-50 p-3">
                  <div className="text-sm text-gray-800">
                    {s.student_name} <span className="text-gray-400">({s.student_email})</span>
                  </div>
                  <div className="text-sm text-gray-600">Submission: {s.link_or_text}</div>
                  <div className="mt-2 grid grid-cols-3 gap-2">
                    <input
                      type="number"
                      min={0}
                      max={100}
                      placeholder="Grade"
                      defaultValue={s.grade ?? ""}
                      onChange={(e) => updateDraft(s.id, "grade", Number(e.target.value))}
                      className="rounded-lg border border-gray-300 px-2 py-1 text-sm"
                    />
                    <select
                      defaultValue={s.status}
                      onChange={(e) => updateDraft(s.id, "status", e.target.value)}
                      className="rounded-lg border border-gray-300 px-2 py-1 text-sm"
                    >
                      <option value="pending">pending</option>
                      <option value="approved">approved</option>
                      <option value="rejected">rejected</option>
                    </select>
                    <button
                      onClick={() => saveGrade(a.id, s)}
                      className="rounded-lg bg-purple-600 px-3 py-1 text-xs font-medium text-white hover:bg-purple-700"
                    >
                      Save grade
                    </button>
                  </div>
                  <input
                    placeholder="Feedback"
                    defaultValue={s.feedback}
                    onChange={(e) => updateDraft(s.id, "feedback", e.target.value)}
                    className="mt-2 w-full rounded-lg border border-gray-300 px-2 py-1 text-sm"
                  />
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
