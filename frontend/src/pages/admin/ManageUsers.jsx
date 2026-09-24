import { useEffect, useState } from "react";
import { api } from "../../api/client";

export default function ManageUsers() {
  const [users, setUsers] = useState([]);
  const [courses, setCourses] = useState([]);
  const [enrollments, setEnrollments] = useState([]);
  const [newAccount, setNewAccount] = useState({ name: "", email: "", password: "", role: "student" });
  const [enrollForm, setEnrollForm] = useState({ user_id: "", course_id: "" });
  const [error, setError] = useState("");

  async function load() {
    const [uRes, cRes, eRes] = await Promise.all([
      api.get("/users"),
      api.get("/courses/manage"),
      api.get("/enrollments"),
    ]);
    setUsers(uRes.data);
    setCourses(cRes.data);
    setEnrollments(eRes.data);
  }

  useEffect(() => {
    load();
  }, []);

  async function createAccount(e) {
    e.preventDefault();
    setError("");
    if (newAccount.password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    try {
      await api.post("/users", newAccount);
      setNewAccount({ name: "", email: "", password: "", role: "student" });
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function enrollStudent(e) {
    e.preventDefault();
    setError("");
    if (!enrollForm.user_id || !enrollForm.course_id) return;
    try {
      await api.post("/enrollments", enrollForm);
      setEnrollForm({ user_id: "", course_id: "" });
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function removeEnrollment(id) {
    await api.delete(`/enrollments/${id}`);
    load();
  }

  async function updateRole(userId, role) {
    await api.patch(`/users/${userId}/role`, { role });
    load();
  }

  const students = users.filter((u) => u.role === "student");

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">👥 Manage users</h1>
      <p className="text-sm text-gray-500">
        Only admins create accounts and enroll students. There's no public sign-up — this
        keeps course access tied to confirmed payment.
      </p>

      {error && <div className="mt-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>}

      <form onSubmit={createAccount} className="mt-6 space-y-3 rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="font-semibold text-gray-900">➕ Create a new account</h2>
        <input
          placeholder="Full name"
          value={newAccount.name}
          onChange={(e) => setNewAccount({ ...newAccount, name: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <input
          placeholder="Email"
          value={newAccount.email}
          onChange={(e) => setNewAccount({ ...newAccount, email: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <input
          type="password"
          placeholder="Temporary password"
          value={newAccount.password}
          onChange={(e) => setNewAccount({ ...newAccount, password: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <select
          value={newAccount.role}
          onChange={(e) => setNewAccount({ ...newAccount, role: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        >
          <option value="student">student</option>
          <option value="instructor">instructor</option>
          <option value="admin">admin</option>
        </select>
        <button type="submit" className="rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white hover:bg-purple-700">
          Create account
        </button>
      </form>

      <form onSubmit={enrollStudent} className="mt-6 space-y-3 rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="font-semibold text-gray-900">🎓 Enroll a student in a course</h2>
        <select
          value={enrollForm.user_id}
          onChange={(e) => setEnrollForm({ ...enrollForm, user_id: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        >
          <option value="">Select student</option>
          {students.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name} ({s.email})
            </option>
          ))}
        </select>
        <select
          value={enrollForm.course_id}
          onChange={(e) => setEnrollForm({ ...enrollForm, course_id: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        >
          <option value="">Select course (they've paid for this)</option>
          {courses.map((c) => (
            <option key={c.id} value={c.id}>
              {c.title}
            </option>
          ))}
        </select>
        <button type="submit" className="rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white hover:bg-purple-700">
          Enroll student
        </button>

        <h3 className="pt-2 text-sm font-semibold text-gray-700">Current enrollments</h3>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500">
              <th className="py-1">Student</th>
              <th>Course</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {enrollments.map((e) => (
              <tr key={e.id} className="border-t border-gray-100">
                <td className="py-1">
                  {e.student_name} <span className="text-gray-400">({e.student_email})</span>
                </td>
                <td>{e.course_title}</td>
                <td className="text-right">
                  <button onClick={() => removeEnrollment(e.id)} className="text-xs text-red-600 hover:underline">
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </form>

      <div className="mt-6 rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="font-semibold text-gray-900">All users</h2>
        <table className="mt-3 w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500">
              <th className="py-1">Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Change role</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-t border-gray-100">
                <td className="py-1">{u.name}</td>
                <td>{u.email}</td>
                <td>{u.role}</td>
                <td>
                  <select
                    defaultValue={u.role}
                    onChange={(e) => updateRole(u.id, e.target.value)}
                    className="rounded-lg border border-gray-300 px-2 py-1 text-xs"
                  >
                    <option value="student">student</option>
                    <option value="instructor">instructor</option>
                    <option value="admin">admin</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
