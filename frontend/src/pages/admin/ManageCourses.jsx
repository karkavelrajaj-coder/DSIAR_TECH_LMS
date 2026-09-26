import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { useAuth } from "../../context/AuthContext";
import {
  Badge,
  Button,
  Card,
  EmptyState,
  Field,
  IconButton,
  Input,
  Modal,
  PageHeader,
  Select,
  Textarea,
} from "../../components/ui";

const emptyCourse = { title: "", category: "", description: "", thumbnail_url: "", is_free: true, instructor_id: "" };
const emptyLesson = { title: "", youtube_id: "", ppt_link: "", colab_link: "", dataset_link: "" };

export default function ManageCourses() {
  const { user } = useAuth();
  const [courses, setCourses] = useState([]);
  const [instructors, setInstructors] = useState([]);
  const [expanded, setExpanded] = useState(null);
  const [modulesByCourse, setModulesByCourse] = useState({});
  const [courseModal, setCourseModal] = useState(null); // null | "new" | course object being edited

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
    // eslint-disable-next-line react-hooks/exhaustive-deps
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

  async function saveCourse(form) {
    if (form.id) {
      await api.patch(`/courses/${form.id}`, {
        title: form.title,
        category: form.category,
        description: form.description,
        thumbnail_url: form.thumbnail_url,
        is_free: form.is_free,
        instructor_id: form.instructor_id || null,
      });
    } else {
      await api.post("/courses", { ...form, instructor_id: form.instructor_id || null });
    }
    setCourseModal(null);
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

  async function renameModule(courseId, moduleId, title) {
    await api.patch(`/modules/${moduleId}`, { title });
    loadModules(courseId);
  }

  async function deleteModule(courseId, moduleId) {
    if (!confirm("Delete this module and all its lessons?")) return;
    await api.delete(`/modules/${moduleId}`);
    loadModules(courseId);
  }

  async function addLesson(courseId, moduleId, lesson) {
    if (!lesson.title) return;
    await api.post(`/modules/${moduleId}/lessons`, lesson);
    loadModules(courseId);
  }

  async function updateLesson(courseId, lessonId, lesson) {
    await api.patch(`/lessons/${lessonId}`, lesson);
    loadModules(courseId);
  }

  async function deleteLesson(courseId, lessonId) {
    if (!confirm("Delete this lesson?")) return;
    await api.delete(`/lessons/${lessonId}`);
    loadModules(courseId);
  }

  const instructorName = (id) => instructors.find((i) => i.id === id)?.name;

  return (
    <div>
      <PageHeader
        eyebrow="Content"
        title="Manage courses & content"
        description="Admins manage every course. Instructors only manage courses assigned to them."
        actions={<Button onClick={() => setCourseModal("new")}>+ New course</Button>}
      />

      {courses.length === 0 && (
        <div className="mt-8">
          <EmptyState icon="📘" title="No courses yet" description="Create your first course to get started." />
        </div>
      )}

      <div className="mt-6 space-y-4">
        {courses.map((c) => (
          <Card key={c.id} padded={false}>
            <div className="flex items-center justify-between gap-3 p-5">
              <button onClick={() => toggleExpand(c.id)} className="flex min-w-0 flex-1 items-center gap-3 text-left">
                <span className={`flex-shrink-0 text-xs text-ink-400 transition-transform ${expanded === c.id ? "rotate-90" : ""}`}>▶</span>
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="truncate font-display text-base font-bold text-ink-900">{c.title}</h2>
                    {c.category && <Badge variant="brand">{c.category}</Badge>}
                    {c.is_free && <Badge variant="success">Free</Badge>}
                  </div>
                  {c.instructor_id && (
                    <div className="mt-0.5 text-xs text-ink-500">Instructor: {instructorName(c.instructor_id) || "—"}</div>
                  )}
                </div>
              </button>
              <div className="flex flex-shrink-0 items-center gap-1.5">
                <IconButton onClick={() => setCourseModal(c)} aria-label="Edit course">
                  ✎
                </IconButton>
                <IconButton onClick={() => deleteCourse(c.id)} className="hover:bg-danger-50 hover:text-danger-600" aria-label="Delete course">
                  🗑
                </IconButton>
              </div>
            </div>

            {expanded === c.id && (
              <div className="border-t border-ink-100 bg-ink-50/50 p-5">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-ink-500">Modules & lessons</h3>
                <div className="mt-3">
                  <NewModuleForm onAdd={(title) => addModule(c.id, title)} />
                </div>
                <div className="mt-3 space-y-3">
                  {(modulesByCourse[c.id] || []).map((m) => (
                    <ModuleCard
                      key={m.id}
                      module={m}
                      onRename={(title) => renameModule(c.id, m.id, title)}
                      onDelete={() => deleteModule(c.id, m.id)}
                      onAddLesson={(lesson) => addLesson(c.id, m.id, lesson)}
                      onUpdateLesson={(lessonId, lesson) => updateLesson(c.id, lessonId, lesson)}
                      onDeleteLesson={(lessonId) => deleteLesson(c.id, lessonId)}
                    />
                  ))}
                  {(modulesByCourse[c.id] || []).length === 0 && (
                    <div className="rounded-lg border border-dashed border-ink-200 px-4 py-6 text-center text-sm text-ink-400">
                      No modules yet — add one above.
                    </div>
                  )}
                </div>
              </div>
            )}
          </Card>
        ))}
      </div>

      <CourseModal
        open={!!courseModal}
        course={courseModal === "new" ? null : courseModal}
        instructors={instructors}
        isAdmin={user.role === "admin"}
        onClose={() => setCourseModal(null)}
        onSave={saveCourse}
      />
    </div>
  );
}

function CourseModal({ open, course, instructors, isAdmin, onClose, onSave }) {
  const [form, setForm] = useState(emptyCourse);

  useEffect(() => {
    if (open) {
      setForm(
        course
          ? {
              id: course.id,
              title: course.title || "",
              category: course.category || "",
              description: course.description || "",
              thumbnail_url: course.thumbnail_url || "",
              is_free: !!course.is_free,
              instructor_id: course.instructor_id || "",
            }
          : emptyCourse
      );
    }
  }, [open, course]);

  return (
    <Modal open={open} onClose={onClose} title={course ? "Edit course" : "Add a new course"} wide>
      <form
        className="space-y-3"
        onSubmit={(e) => {
          e.preventDefault();
          if (!form.title) return;
          onSave(form);
        }}
      >
        <Field label="Title">
          <Input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
        </Field>
        <Field label="Category">
          <Input
            placeholder="e.g. Artificial Intelligence"
            value={form.category}
            onChange={(e) => setForm({ ...form, category: e.target.value })}
          />
        </Field>
        <Field label="Description">
          <Textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
        </Field>
        <Field label="Thumbnail" hint="Path (e.g. assets/AI Thumbnail.png) or a full URL">
          <Input value={form.thumbnail_url} onChange={(e) => setForm({ ...form, thumbnail_url: e.target.value })} />
        </Field>
        {isAdmin && (
          <Field label="Instructor">
            <Select value={form.instructor_id} onChange={(e) => setForm({ ...form, instructor_id: e.target.value })}>
              <option value="">— Unassigned (admin managed) —</option>
              {instructors.map((i) => (
                <option key={i.id} value={i.id}>
                  {i.name}
                </option>
              ))}
            </Select>
          </Field>
        )}
        <label className="flex items-center gap-2 text-sm text-ink-700">
          <input
            type="checkbox"
            checked={form.is_free}
            onChange={(e) => setForm({ ...form, is_free: e.target.checked })}
          />
          Free course
        </label>
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit">{course ? "Save changes" : "Create course"}</Button>
        </div>
      </form>
    </Modal>
  );
}

function NewModuleForm({ onAdd }) {
  const [title, setTitle] = useState("");
  return (
    <form
      className="flex gap-2"
      onSubmit={(e) => {
        e.preventDefault();
        onAdd(title);
        setTitle("");
      }}
    >
      <Input placeholder="New module title" value={title} onChange={(e) => setTitle(e.target.value)} />
      <Button type="submit" variant="secondary" className="flex-shrink-0">
        + Add module
      </Button>
    </form>
  );
}

function ModuleCard({ module: m, onRename, onDelete, onAddLesson, onUpdateLesson, onDeleteLesson }) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(m.title);
  const [addingLesson, setAddingLesson] = useState(false);

  return (
    <div className="rounded-xl border border-ink-200 bg-white">
      <div className="flex items-center justify-between gap-2 px-4 py-3">
        {editing ? (
          <form
            className="flex flex-1 gap-2"
            onSubmit={(e) => {
              e.preventDefault();
              onRename(title);
              setEditing(false);
            }}
          >
            <Input autoFocus value={title} onChange={(e) => setTitle(e.target.value)} />
            <Button size="sm" type="submit">Save</Button>
            <Button size="sm" type="button" variant="secondary" onClick={() => { setEditing(false); setTitle(m.title); }}>
              Cancel
            </Button>
          </form>
        ) : (
          <>
            <div className="font-semibold text-ink-800">{m.title}</div>
            <div className="flex flex-shrink-0 items-center gap-1">
              <Button size="sm" variant="secondary" onClick={() => setAddingLesson((v) => !v)}>
                + Lesson
              </Button>
              <IconButton onClick={() => setEditing(true)} aria-label="Rename module">
                ✎
              </IconButton>
              <IconButton onClick={onDelete} className="hover:bg-danger-50 hover:text-danger-600" aria-label="Delete module">
                🗑
              </IconButton>
            </div>
          </>
        )}
      </div>

      {m.lessons.length > 0 && (
        <ul className="divide-y divide-ink-100 border-t border-ink-100">
          {m.lessons.map((l) => (
            <LessonRow key={l.id} lesson={l} onUpdate={(data) => onUpdateLesson(l.id, data)} onDelete={() => onDeleteLesson(l.id)} />
          ))}
        </ul>
      )}

      {addingLesson && (
        <div className="border-t border-ink-100 p-3">
          <LessonForm
            onSubmit={(lesson) => {
              onAddLesson(lesson);
              setAddingLesson(false);
            }}
            onCancel={() => setAddingLesson(false)}
            submitLabel="Add lesson"
          />
        </div>
      )}
    </div>
  );
}

function LessonRow({ lesson, onUpdate, onDelete }) {
  const [editing, setEditing] = useState(false);

  if (editing) {
    return (
      <li className="p-3">
        <LessonForm
          initial={lesson}
          onSubmit={(data) => {
            onUpdate(data);
            setEditing(false);
          }}
          onCancel={() => setEditing(false)}
          submitLabel="Save lesson"
        />
      </li>
    );
  }

  return (
    <li className="flex items-center justify-between gap-2 px-4 py-2.5 text-sm">
      <div className="min-w-0 flex-1">
        <div className="truncate text-ink-800">{lesson.title}</div>
        <div className="mt-0.5 flex flex-wrap gap-1.5 text-[11px] text-ink-400">
          {lesson.youtube_id ? <Badge variant="brand">▶ video</Badge> : <span>no video</span>}
          {lesson.ppt_link && <Badge variant="neutral">slides</Badge>}
          {lesson.colab_link && <Badge variant="neutral">colab</Badge>}
          {lesson.dataset_link && <Badge variant="neutral">dataset</Badge>}
        </div>
      </div>
      <div className="flex flex-shrink-0 items-center gap-1">
        <IconButton onClick={() => setEditing(true)} aria-label="Edit lesson">
          ✎
        </IconButton>
        <IconButton onClick={onDelete} className="hover:bg-danger-50 hover:text-danger-600" aria-label="Delete lesson">
          🗑
        </IconButton>
      </div>
    </li>
  );
}

function LessonForm({ initial, onSubmit, onCancel, submitLabel }) {
  const [lesson, setLesson] = useState(initial ? { ...emptyLesson, ...initial } : emptyLesson);

  return (
    <form
      className="grid grid-cols-1 gap-2 sm:grid-cols-2"
      onSubmit={(e) => {
        e.preventDefault();
        if (!lesson.title) return;
        onSubmit(lesson);
      }}
    >
      <Input
        className="sm:col-span-2"
        placeholder="Lesson title"
        value={lesson.title}
        onChange={(e) => setLesson({ ...lesson, title: e.target.value })}
      />
      <Input
        placeholder="YouTube video ID"
        value={lesson.youtube_id}
        onChange={(e) => setLesson({ ...lesson, youtube_id: e.target.value })}
      />
      <Input
        placeholder="Slides link"
        value={lesson.ppt_link}
        onChange={(e) => setLesson({ ...lesson, ppt_link: e.target.value })}
      />
      <Input
        placeholder="Colab link"
        value={lesson.colab_link}
        onChange={(e) => setLesson({ ...lesson, colab_link: e.target.value })}
      />
      <Input
        placeholder="Dataset link"
        value={lesson.dataset_link}
        onChange={(e) => setLesson({ ...lesson, dataset_link: e.target.value })}
      />
      <div className="flex gap-2 sm:col-span-2">
        <Button type="submit" size="sm">{submitLabel}</Button>
        <Button type="button" size="sm" variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
      </div>
    </form>
  );
}
