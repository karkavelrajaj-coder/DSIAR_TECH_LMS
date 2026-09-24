import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const studentLinks = [
  { to: "/catalog", label: "Course Catalog", icon: "📚" },
  { to: "/my-learning", label: "My Learning", icon: "🎓" },
  { to: "/assignments", label: "Assignments", icon: "📝" },
  { to: "/certificates", label: "Certificates", icon: "🏆" },
  { to: "/live-sessions", label: "Live Sessions", icon: "🎥" },
];

const instructorLinks = [
  { to: "/admin/courses", label: "Manage Courses", icon: "🛠️" },
  { to: "/admin/grading", label: "Assignments & Grading", icon: "📥" },
  { to: "/admin/live-sessions", label: "Manage Live Sessions", icon: "🗓️" },
];

const adminOnlyLinks = [{ to: "/admin/users", label: "Manage Users", icon: "👥" }];

export function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  let links = studentLinks;
  if (user.role === "instructor") links = [...instructorLinks, ...studentLinks];
  if (user.role === "admin") links = [...adminOnlyLinks, ...instructorLinks, ...studentLinks];

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <aside className="flex w-64 flex-shrink-0 flex-col border-r border-gray-200 bg-white">
        <div className="border-b border-gray-100 px-5 py-5">
          <div className="text-lg font-semibold text-gray-900">🎓 D'siar Tech</div>
          <div className="text-xs text-gray-500">LMS</div>
        </div>
        <nav className="flex-1 space-y-1 px-3 py-4">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                `flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition ${
                  isActive
                    ? "bg-purple-50 text-purple-700"
                    : "text-gray-600 hover:bg-gray-100"
                }`
              }
            >
              <span>{l.icon}</span>
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-gray-100 px-5 py-4">
          <div className="truncate text-sm font-medium text-gray-900">{user.name}</div>
          <div className="truncate text-xs text-gray-500">
            {user.email} · {user.role}
          </div>
          <button
            onClick={handleLogout}
            className="mt-3 w-full rounded-lg border border-gray-200 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100"
          >
            Log out
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
}
