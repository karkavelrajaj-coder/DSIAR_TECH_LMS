import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { useAuth } from "../../context/AuthContext";

export default function ManageCourses() {
  const { user } = useAuth();
  const [courses, setCourses] = useState([]);
  const [instructors, setInstructors] = useState([]);
  const [expanded, setExpanded] = useState(null);
  const [modulesByCourse, setModulesByCourse] = useState({});
  const [newCourse, setNewCourse] = useState({
    title: "",
    category: "",
    description: "",
    thumbnail_url: "",
    is_free: true,
    instructor_id: "",
  });

  async function load() {
    const res = await api.get("/courses/manage");
    setCourses(res.data);
    if (user.role === "admin") {
      const ires = await api.get("/users/instructors");
      setInstructors(ires.data);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function loadModules(courseId) {
    const res = await api.get(`/courses/${courseId}`);
    setModulesByCourse((prev) => ({ ...prev, [courseId]: res.data.modules }));
  }

  async function toggleExpand(courseId) {
    if (expanded === courseId) {
      setExpanded(null);
      return;
    }
    setExpanded(courseId);
    if (!modulesByCourse[courseId]) await loadModules(courseId);
  }

  async function createCourse(e) {
    e.preventDefault();
    if (!newCourse.title) return;
    await api.post("/courses", {
      ...newCourse,
      instructor_id: newCourse.instructor_id || null,
    });
    setNewCourse({ title: "", category: "", description: "", thumbnail_url: "", is_free: true, instructor_id: "" });
    load();
  }

  async function deleteCourse(id) {
    if (!confirm("Delete this course and all its modules/lessons?")) return;
    await api.delete(`/courses/${id}`);
    load();
  }

  async function addModule(courseId, title) {
    if (!title) return;
    await api.post(`/courses/${courseId}/modules`, { title });
    loadModules(courseId);
  }

  async function deleteModule(courseId, moduleId) {
    await api.delete(`/modules/${moduleId}`);
    loadModules(courseId);
  }

  async function addLesson(courseId, moduleId, lesson) {
    if (!lesson.title) return;
    await api.post(`/modules/${moduleId}/lessons`, lesson);
    loadModules(courseId);
  }

  async function deleteLesson(courseId, lessonId) {
    await api.delete(`/lessons/${lessonId}`);
    loadModules(courseId);
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">🛠️ Manage courses & content</h1>
      <p className="text-sm text-gray-500">
        Admins manage every course. Instructors only manage courses assigned to them.
      </p>

      <form onSubmit={createCourse} className="mt-6 space-y-3 rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="font-semibold text-gray-900">➕ Add a new course</h2>
        <input
          placeholder="Title"
          value={newCourse.title}
          onChange={(e) => setNewCourse({ ...newCourse, title: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <input
          placeholder="Category (e.g. Artificial Intelligence)"
          value={newCourse.category}
          onChange={(e) => setNewCourse({ ...newCourse, category: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <textarea
          placeholder="Description"
          value={newCourse.description}
          onChange={(e) => setNewCourse({ ...newCourse, description: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        <input
          placeholder="Thumbnail path (e.g. assets/AI Thumbnail.png) or URL"
          value={newCourse.thumbnail_url}
          onChange={(e) => setNewCourse({ ...newCourse, thumbnail_url: e.target.value })}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
        />
        {user.role === "admin" && (
          <select
            value={newCourse.instructor_id}
            onChange={(e) => setNewCourse({ ...newCourse, instructor_id: e.target.value })}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
          >
            <option value="">— Unassigned (admin managed) —</option>
            {instructors.map((i) => (
              <option key={i.id} value={i.id}>
                {i.name}
              </option>
            ))}
          </select>
        )}
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input
            type="checkbox"
            checked={newCourse.is_free}
            onChange={(e) => setNewCourse({ ...newCourse, is_free: e.target.checked })}
          />
          Free course
        </label>
        <button type="submit" className="rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white hover:bg-purple-700">
          Create course
        </button>
      </form>

      <div className="mt-6 space-y-4">
        {courses.map((c) => (
          <div key={c.id} className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <button onClick={() => toggleExpand(c.id)} className="text-left font-semibold text-gray-900">
                📘 {c.title}
              </button>
              <button onClick={() => deleteCourse(c.id)} className="text-sm text-red-600 hover:underline">
                🗑 Delete course
              </button>
            </div>

            {expanded === c.id && (
              <div className="mt-4 space-y-4 border-t border-gray-100 pt-4">
                <h3 className="text-sm font-semibold text-gray-700">Modules & lessons</h3>
                <NewModuleForm onAdd={(title) => addModule(c.id, title)} />
                {(modulesByCourse[c.id] || []).map((m) => (
                  <div key={m.id} className="rounded-lg border border-gray-100 bg-gray-50 p-3">
                    <div className="flex items-center justify-between">
                      <div className="font-medium text-gray-800">{m.title}</div>
                      <button onClick={() => deleteModule(c.id, m.id)} className="text-xs text-red-600 hover:underline">
                        🗑 Delete
                      </button>
                    </div>
                    <ul className="mt-2 space-y-1">
                      {m.lessons.map((l) => (
                        <li key={l.id} className="flex items-center justify-between text-sm text-gray-600">
                          <span>
                            • {l.title} — youtube: {l.youtube_id || "—"}
                          </span>
                          <button onClick={() => deleteLesson(c.id, l.id)} className="text-xs text-red-600 hover:underline">
                            🗑
                          </button>
                        </li>
                      ))}
                    </ul>
                    <NewLessonForm onAdd={(lesson) => addLesson(c.id, m.id, lesson)} />
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function NewModuleForm({ onAdd }) {
  const [title, setTitle] = useState("");
  return (
    <div className="flex gap-2">
      <input
        placeholder="New module title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="flex-1 rounded-lg border border-gray-300 px-3 py-1.5 text-sm"
      />
      <button
        onClick={() => {
          onAdd(title);
          setTitle("");
        }}
        className="rounded-lg bg-gray-800 px-3 py-1.5 text-xs font-medium text-white hover:bg-gray-900"
      >
        Add module
      </button>
    </div>
  );
}

function NewLessonForm({ onAdd }) {
  const [lesson, setLesson] = useState({ title: "", youtube_id: "", ppt_link: "", colab_link: "", dataset_link: "" });
  return (
    <div className="mt-2 grid grid-cols-2 gap-2">
      <input
        placeholder="Lesson title"
        value={lesson.title}
        onChange={(e) => setLesson({ ...lesson, title: e.target.value })}
        className="col-span-2 rounded-lg border border-gray-300 px-3 py-1.5 text-sm"
      />
      <input
        placeholder="YouTube video ID"
        value={lesson.youtube_id}
        onChange={(e) => setLesson({ ...lesson, youtube_id: e.target.value })}
        className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm"
      />
      <input
        placeholder="Slides link"
        value={lesson.ppt_link}
        onChange={(e) => setLesson({ ...lesson, ppt_link: e.target.value })}
        className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm"
      />
      <input
        placeholder="Colab link"
        value={lesson.colab_link}
        onChange={(e) => setLesson({ ...lesson, colab_link: e.target.value })}
        className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm"
      />
      <input
        placeholder="Dataset link"
        value={lesson.dataset_link}
        onChange={(e) => setLesson({ ...lesson, dataset_link: e.target.value })}
        className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm"
      />
      <button
        onClick={() => {
          onAdd(lesson);
          setLesson({ title: "", youtube_id: "", ppt_link: "", colab_link: "", dataset_link: "" });
        }}
        className="col-span-2 rounded-lg bg-purple-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-purple-700"
      >
        Add lesson
      </button>
    </div>
  );
}
