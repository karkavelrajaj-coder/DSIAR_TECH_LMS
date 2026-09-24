import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

export default function MyLearning() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/my/learning").then((res) => {
      setCourses(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="text-gray-500">Loading…</div>;

  if (courses.length === 0) {
    return (
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">🎓 My learning</h1>
        <div className="mt-6 rounded-lg bg-blue-50 px-4 py-3 text-sm text-blue-700">
          You haven't enrolled in any courses yet. Head to the Course Catalog
          to get started.
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">🎓 My learning</h1>
      <div className="mt-6 space-y-4">
        {courses.map((c) => (
          <div
            key={c.id}
            className="flex items-center justify-between rounded-xl border border-gray-200 bg-white p-5 shadow-sm"
          >
            <div className="flex-1">
              <h2 className="text-lg font-semibold text-gray-900">{c.title}</h2>
              <div className="mt-2 h-2 w-full max-w-md rounded-full bg-gray-100">
                <div
                  className="h-2 rounded-full bg-purple-600"
                  style={{ width: `${Math.round(c.progress_pct * 100)}%` }}
                />
              </div>
              <div className="mt-1 text-xs text-gray-500">
                {c.lessons_completed}/{c.lessons_total} lessons completed
              </div>
            </div>
            <button
              onClick={() => navigate(`/course/${c.id}`)}
              className="ml-6 rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white hover:bg-purple-700"
            >
              Open course ▶
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
