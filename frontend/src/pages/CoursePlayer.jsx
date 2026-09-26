import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import { Badge, Button, LoadingScreen, ProgressBar } from "../components/ui";

/**
 * Real course-player layout: a curriculum sidebar (every lesson listed once,
 * with its completion state) and a main pane that shows exactly ONE lesson
 * at a time — video, then its resources, then a completion action. This
 * replaces the earlier "every lesson's video stacked on one long page"
 * layout, which was carried over from the Streamlit app's single-page
 * constraint and doesn't hold up as a real course player.
 */
export default function CoursePlayer() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [error, setError] = useState("");
  const [celebration, setCelebration] = useState("");
  const [activeLessonId, setActiveLessonId] = useState(null);
  const [collapsedModules, setCollapsedModules] = useState({});
  const [sidebarOpen, setSidebarOpen] = useState(false);

  async function load(preferredLessonId) {
    try {
      const res = await api.get(`/courses/${courseId}`);
      setCourse(res.data);
      setActiveLessonId((current) => {
        const flat = res.data.modules.flatMap((m) => m.lessons);
        if (preferredLessonId && flat.some((l) => l.id === preferredLessonId)) return preferredLessonId;
        if (current && flat.some((l) => l.id === current)) return current;
        const firstIncomplete = flat.find((l) => !l.completed);
        return (firstIncomplete || flat[0])?.id || null;
      });
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [courseId]);

  const flatLessons = useMemo(() => course?.modules.flatMap((m) => m.lessons) || [], [course]);
  const totalLessons = flatLessons.length;
  const completedCount = flatLessons.filter((l) => l.completed).length;
  const overallProgress = totalLessons ? completedCount / totalLessons : 0;

  const activeIndex = flatLessons.findIndex((l) => l.id === activeLessonId);
  const activeLesson = activeIndex >= 0 ? flatLessons[activeIndex] : null;
  const activeModule = course?.modules.find((m) => m.lessons.some((l) => l.id === activeLessonId));
  const nextLesson = activeIndex >= 0 ? flatLessons[activeIndex + 1] : null;
  const prevLesson = activeIndex > 0 ? flatLessons[activeIndex - 1] : null;

  async function markComplete(lessonId) {
    const res = await api.post(`/lessons/${lessonId}/complete`);
    if (res.data.certificate_issued) {
      setCelebration("🎓 Course complete and assignment approved — your certificate is ready! Check Certificates.");
    }
    const idx = flatLessons.findIndex((l) => l.id === lessonId);
    const next = flatLessons[idx + 1];
    await load(next ? next.id : lessonId);
  }

  function selectLesson(lessonId) {
    setActiveLessonId(lessonId);
    setSidebarOpen(false);
  }

  function toggleModule(moduleId) {
    setCollapsedModules((prev) => ({ ...prev, [moduleId]: !prev[moduleId] }));
  }

  if (error) return <div className="text-sm text-danger-600">{error}</div>;
  if (!course) return <LoadingScreen label="Loading course…" />;

  return (
    <div className="-mx-4 -my-6 flex h-[calc(100vh-3.5rem)] flex-col sm:-mx-8 sm:-my-8 lg:h-screen">
      {/* Top bar */}
      <div className="flex flex-shrink-0 items-center gap-3 border-b border-ink-200 bg-white px-4 py-3 sm:px-6">
        <Link
          to="/my-learning"
          className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg text-ink-500 hover:bg-ink-100"
        >
          ←
        </Link>
        <div className="min-w-0 flex-1">
          <div className="truncate font-display text-sm font-bold text-ink-900 sm:text-base">{course.title}</div>
          <div className="mt-1 flex items-center gap-2">
            <ProgressBar value={overallProgress} className="w-32 sm:w-56" />
            <span className="text-xs font-medium text-ink-500">
              {completedCount}/{totalLessons} lessons · {Math.round(overallProgress * 100)}%
            </span>
          </div>
        </div>
        <button
          onClick={() => setSidebarOpen(true)}
          className="flex h-8 items-center gap-1.5 rounded-lg border border-ink-200 px-3 text-xs font-medium text-ink-600 hover:bg-ink-50 lg:hidden"
        >
          📑 Curriculum
        </button>
      </div>

      {celebration && (
        <div className="flex-shrink-0 bg-success-50 px-4 py-2.5 text-sm text-success-700 sm:px-6">{celebration}</div>
      )}

      <div className="relative flex min-h-0 flex-1">
        {/* Curriculum sidebar */}
        <aside
          className={`absolute inset-y-0 left-0 z-30 w-80 flex-shrink-0 overflow-y-auto border-r border-ink-200 bg-white transition-transform lg:static lg:z-auto lg:translate-x-0 ${
            sidebarOpen ? "translate-x-0 shadow-card-lg" : "-translate-x-full"
          }`}
        >
          <div className="flex items-center justify-between border-b border-ink-100 px-4 py-3 lg:hidden">
            <span className="text-sm font-semibold text-ink-800">Curriculum</span>
            <button onClick={() => setSidebarOpen(false)} className="text-ink-400">✕</button>
          </div>
          <div className="p-3">
            {course.modules.map((m, mi) => {
              const moduleDone = m.lessons.filter((l) => l.completed).length;
              const collapsed = collapsedModules[m.id];
              return (
                <div key={m.id} className="mb-2 overflow-hidden rounded-xl border border-ink-100">
                  <button
                    onClick={() => toggleModule(m.id)}
                    className="flex w-full items-center justify-between gap-2 bg-ink-50 px-3 py-2.5 text-left"
                  >
                    <div className="min-w-0">
                      <div className="text-[11px] font-semibold uppercase tracking-wide text-ink-400">
                        Module {mi + 1}
                      </div>
                      <div className="truncate text-sm font-semibold text-ink-800">{m.title}</div>
                    </div>
                    <div className="flex flex-shrink-0 items-center gap-2">
                      <span className="text-[11px] font-medium text-ink-400">
                        {moduleDone}/{m.lessons.length}
                      </span>
                      <span className={`text-xs text-ink-400 transition-transform ${collapsed ? "-rotate-90" : ""}`}>▾</span>
                    </div>
                  </button>
                  {!collapsed && (
                    <ul>
                      {m.lessons.map((l) => {
                        const active = l.id === activeLessonId;
                        return (
                          <li key={l.id}>
                            <button
                              onClick={() => selectLesson(l.id)}
                              className={`flex w-full items-start gap-2.5 border-t border-ink-100 px-3 py-2.5 text-left text-sm transition ${
                                active ? "bg-brand-50 text-brand-700" : "text-ink-600 hover:bg-ink-50"
                              }`}
                            >
                              <span className="mt-0.5 flex-shrink-0">
                                {l.completed ? (
                                  <span className="flex h-4 w-4 items-center justify-center rounded-full bg-success-600 text-[9px] text-white">✓</span>
                                ) : active ? (
                                  <span className="flex h-4 w-4 items-center justify-center rounded-full border-2 border-brand-600" />
                                ) : (
                                  <span className="flex h-4 w-4 items-center justify-center rounded-full border-2 border-ink-200" />
                                )}
                              </span>
                              <span className={`min-w-0 flex-1 truncate ${active ? "font-semibold" : ""}`}>{l.title}</span>
                              {l.youtube_id && <span className="flex-shrink-0 text-xs text-ink-300">▶</span>}
                            </button>
                          </li>
                        );
                      })}
                    </ul>
                  )}
                </div>
              );
            })}
          </div>
        </aside>
        {sidebarOpen && (
          <div className="fixed inset-0 z-20 bg-ink-900/40 lg:hidden" onClick={() => setSidebarOpen(false)} />
        )}

        {/* Active lesson */}
        <div className="min-w-0 flex-1 overflow-y-auto">
          {!activeLesson ? (
            <div className="p-8 text-sm text-ink-500">This course doesn't have any lessons yet.</div>
          ) : (
            <div className="mx-auto max-w-3xl px-4 py-6 sm:px-8">
              <div className="text-xs font-semibold uppercase tracking-wide text-brand-600">{activeModule?.title}</div>
              <div className="mt-1 flex flex-wrap items-center gap-2">
                <h1 className="font-display text-xl font-bold text-ink-900 sm:text-2xl">{activeLesson.title}</h1>
                {activeLesson.completed && <Badge variant="success">✓ Completed</Badge>}
              </div>

              {activeLesson.youtube_id ? (
                <div className="mt-5 aspect-video w-full overflow-hidden rounded-2xl bg-black shadow-card-lg">
                  <iframe
                    key={activeLesson.id}
                    className="h-full w-full"
                    src={`https://www.youtube.com/embed/${activeLesson.youtube_id}`}
                    title={activeLesson.title}
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  />
                </div>
              ) : (
                <div className="mt-5 flex aspect-video w-full items-center justify-center rounded-2xl border border-dashed border-ink-200 bg-ink-50 text-sm text-ink-400">
                  No video attached to this lesson yet.
                </div>
              )}

              {(activeLesson.ppt_link || activeLesson.colab_link || activeLesson.dataset_link) && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {activeLesson.ppt_link && (
                    <ResourceLink href={activeLesson.ppt_link} icon="📊" label="Slides" />
                  )}
                  {activeLesson.colab_link && (
                    <ResourceLink href={activeLesson.colab_link} icon="💻" label="Colab notebook" />
                  )}
                  {activeLesson.dataset_link && (
                    <ResourceLink href={activeLesson.dataset_link} icon="📁" label="Dataset" />
                  )}
                </div>
              )}

              <div className="mt-8 flex flex-wrap items-center justify-between gap-3 border-t border-ink-100 pt-6">
                <Button variant="secondary" disabled={!prevLesson} onClick={() => prevLesson && selectLesson(prevLesson.id)}>
                  ← Previous
                </Button>
                <div className="flex-1" />
                {!activeLesson.completed ? (
                  <Button onClick={() => markComplete(activeLesson.id)}>Mark complete{nextLesson ? " & continue" : ""}</Button>
                ) : nextLesson ? (
                  <Button onClick={() => selectLesson(nextLesson.id)}>Next lesson →</Button>
                ) : (
                  <Badge variant="success">🎉 You've finished this course</Badge>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function ResourceLink({ href, icon, label }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      className="inline-flex items-center gap-1.5 rounded-lg border border-ink-200 bg-white px-3 py-1.5 text-xs font-medium text-ink-600 hover:bg-ink-50"
    >
      {icon} {label}
    </a>
  );
}
