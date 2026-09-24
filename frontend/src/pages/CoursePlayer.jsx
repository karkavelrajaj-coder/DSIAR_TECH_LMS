import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";

export default function CoursePlayer() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [error, setError] = useState("");
  const [celebration, setCelebration] = useState("");

  async function load() {
    try {
      const res = await api.get(`/courses/${courseId}`);
      setCourse(res.data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, [courseId]);

  async function markComplete(lessonId) {
    const res = await api.post(`/lessons/${lessonId}/complete`);
    if (res.data.certificate_issued) {
      setCelebration(
        "🎓 Course complete and assignment approved — your certificate is ready! Check Certificates."
      );
    }
    load();
  }

  if (error) return <div className="text-sm text-red-600">{error}</div>;
  if (!course) return <div className="text-gray-500">Loading…</div>;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">▶ {course.title}</h1>

      {celebration && (
        <div className="mt-4 rounded-lg bg-green-50 px-4 py-3 text-sm text-green-700">
          {celebration}
        </div>
      )}

      <div className="mt-6 space-y-6">
        {course.modules.map((m) => (
          <div key={m.id} className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900">{m.title}</h2>
            <div className="mt-4 space-y-6">
              {m.lessons.map((l) => (
                <div key={l.id} className="border-t border-gray-100 pt-4 first:border-0 first:pt-0">
                  <h3 className="font-medium text-gray-900">
                    {l.title} {l.completed && <span className="text-green-600">✅</span>}
                  </h3>

                  {l.youtube_id && (
                    <div className="mt-2 aspect-video w-full max-w-2xl overflow-hidden rounded-lg bg-black">
                      <iframe
                        className="h-full w-full"
                        src={`https://www.youtube.com/embed/${l.youtube_id}`}
                        title={l.title}
                        allowFullScreen
                      />
                    </div>
                  )}

                  <div className="mt-3 flex flex-wrap gap-2">
                    {l.ppt_link && (
                      <a
                        href={l.ppt_link}
                        target="_blank"
                        rel="noreferrer"
                        className="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
                      >
                        📊 Open slides
                      </a>
                    )}
                    {l.colab_link && (
                      <a
                        href={l.colab_link}
                        target="_blank"
                        rel="noreferrer"
                        className="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
                      >
                        💻 Open Colab notebook
                      </a>
                    )}
                    {l.dataset_link && (
                      <a
                        href={l.dataset_link}
                        target="_blank"
                        rel="noreferrer"
                        className="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
                      >
                        📁 Download dataset
                      </a>
                    )}
                  </div>

                  {!l.completed && (
                    <button
                      onClick={() => markComplete(l.id)}
                      className="mt-3 rounded-lg bg-purple-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-purple-700"
                    >
                      Mark as complete
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
