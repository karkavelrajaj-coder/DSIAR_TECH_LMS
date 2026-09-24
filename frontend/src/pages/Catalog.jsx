import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function Catalog() {
  const { user } = useAuth();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    const res = await api.get("/courses");
    setCourses(res.data);
    setLoading(false);
  }

  useEffect(() => {
    load();
  }, []);

  async function handlePreviewEnroll(courseId) {
    await api.post(`/enrollments/preview/${courseId}`);
    load();
  }

  if (loading) return <div className="text-gray-500">Loading courses…</div>;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">📚 Course catalog</h1>
      <p className="mt-1 text-sm text-gray-500">
        Practical, hands-on courses in AI, ML, cybersecurity, and emerging technologies.
      </p>

      {courses.length === 0 && (
        <div className="mt-6 rounded-lg bg-blue-50 px-4 py-3 text-sm text-blue-700">
          No courses published yet — check back soon.
        </div>
      )}

      <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {courses.map((c) => (
          <div key={c.id} className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
            {c.thumbnail_url && (
              <div className="mb-3 aspect-video overflow-hidden rounded-lg bg-gray-100">
                {/* thumbnail_url may be a relative asset path served by the
                    backend at /assets/... , or a full URL */}
                <img
                  src={
                    c.thumbnail_url.startsWith("http")
                      ? c.thumbnail_url
                      : `/api/static/${c.thumbnail_url.replace(/^assets\//, "")}`
                  }
                  alt={c.title}
                  className="h-full w-full object-cover"
                  onError={(e) => (e.currentTarget.style.display = "none")}
                />
              </div>
            )}
            <h2 className="text-lg font-semibold text-gray-900">{c.title}</h2>
            <div className="text-xs text-gray-500">{c.category}</div>
            <p className="mt-2 line-clamp-3 text-sm text-gray-600">{c.description}</p>

            <div className="mt-4">
              {c.is_enrolled ? (
                <span className="inline-block rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">
                  ✅ Enrolled
                </span>
              ) : user.role === "student" ? (
                <span className="text-xs text-gray-500">
                  🔒 Not enrolled — contact D'siar Tech to purchase access.
                </span>
              ) : (
                <button
                  onClick={() => handlePreviewEnroll(c.id)}
                  className="w-full rounded-lg border border-purple-200 bg-purple-50 px-3 py-1.5 text-sm font-medium text-purple-700 hover:bg-purple-100"
                >
                  Enroll (preview)
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
