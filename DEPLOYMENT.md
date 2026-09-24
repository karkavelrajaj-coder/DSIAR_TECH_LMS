# Deploying to GitHub + Render (free tier)

This app is two independently-deployed services from one repo:

- **`dsiar-lms-backend`** — FastAPI, deployed as a Render **Web Service**
  built from the root `Dockerfile`.
- **`dsiar-lms-frontend`** — the React/Vite app, deployed as a Render
  **Static Site** (no Docker needed — Render just runs `npm run build` and
  serves the `dist/` folder over its CDN, which is free with no sleep).

Both are defined in `render.yaml` so Render can create them together as a
**Blueprint**.

## 0. Push this repo to a new GitHub repo

```bash
cd dsiar-lms-v2
git add .
git commit -m "Enterprise LMS: FastAPI backend + React frontend (Phase 1)"
git branch -M main
git remote add origin https://github.com/<you>/<new-repo-name>.git
git push -u origin main
```

This is a **brand-new repo**, separate from your existing `dsiar-lms`
Streamlit repo — that one keeps running untouched on Streamlit Cloud.

## 1. Deploy the Blueprint on Render

1. Go to the Render dashboard → **New** → **Blueprint**.
2. Pick the new GitHub repo. Render reads `render.yaml` and shows both
   services (`dsiar-lms-backend`, `dsiar-lms-frontend`).
3. Click **Apply**. Render will ask you to fill in the env vars marked
   `sync: false` in `render.yaml` — for the first deploy you can leave
   `CORS_ORIGINS` and `VITE_API_BASE_URL` blank; you'll set them in step 4.
4. Fill in at minimum:
   - `MONGO_URI` — same connection string as your Streamlit app's, but see
     **Database** below — this new app uses a different database name so
     it never touches your existing course data.
   - `SEED_ADMIN_EMAIL`, `SEED_ADMIN_PASSWORD` — creates the first admin on
     boot (same as the Streamlit app's secrets).
   - `DIGITALSAMBA_TEAM_ID`, `DIGITALSAMBA_DEVELOPER_KEY` — same values as
     your Streamlit app's secrets; Digital Samba doesn't care which app
     calls it.

## 2. Database — brand new, nothing shared with Streamlit

`render.yaml` sets `DB_NAME=dsiar_lms_v2`. This is a **new, separate
database** inside the same free Atlas cluster (`Cluster0`) your Streamlit
app already uses — same cluster, different database name, so:

- The Streamlit app keeps reading/writing its own `dsiar_lms` database,
  completely unaffected.
- This new app starts with zero data: no courses, no users except the
  seed admin. You'll re-create courses/modules/lessons (or write a seed
  script like your old `scripts/seed_ai_course.py` / `seed_ml_course.py`,
  pointed at this backend's `/api/courses`, `/api/courses/{id}/modules`,
  `/api/modules/{id}/lessons` endpoints instead of Mongo directly).
- Atlas Network Access must allow Render's IPs — easiest is to keep (or
  add) `0.0.0.0/0` in Atlas → Network Access, the same setting you already
  needed for Streamlit Cloud.

If you'd rather start this new app with a **copy** of your existing course
catalog, say so and I'll write a one-off script that copies `courses`,
`modules`, `lessons`, and `assignments` from `dsiar_lms` into
`dsiar_lms_v2` (read-only against the old data, so the Streamlit app is
still never touched).

## 3. Wait for both builds to finish

- Backend build: installs `backend/requirements.txt` inside the Docker
  image, then starts `uvicorn app:app`. Watch the Render logs for
  `Application startup complete.`
- Frontend build: `npm install && npm run build` inside `frontend/`.

## 4. Wire the two services together

Once both have URLs (e.g. `https://dsiar-lms-backend.onrender.com` and
`https://dsiar-lms-frontend.onrender.com`):

1. Backend service → Environment → set `CORS_ORIGINS` to the frontend's
   URL (exactly, no trailing slash) → save (triggers a redeploy).
2. Frontend service → Environment → set `VITE_API_BASE_URL` to the
   backend's URL **plus `/api`** (e.g.
   `https://dsiar-lms-backend.onrender.com/api`) → save (triggers a
   rebuild, since Vite bakes env vars in at build time).

## 5. Verify

1. Open the frontend URL → you should see the login page.
2. Log in with `SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD`.
3. Admin → Manage Users → create an instructor and a student.
4. Admin → Manage Courses → create a course, a module, a lesson.
5. Admin → Manage Users → enroll the student.
6. Log in as the student, complete the lesson, submit the assignment (if
   you posted one), grade it as the instructor, confirm the certificate
   PNG renders for the student.
7. Try a live session: schedule it, start it as host, join it as the
   student (needs real `DIGITALSAMBA_*` keys set on the backend).

## Notes on Render's free tier

- Free **Web Services** (the backend) spin down after ~15 minutes of no
  traffic and take ~30–60s to wake back up on the next request — the
  same cold-start tradeoff Streamlit Cloud has.
- Free **Static Sites** (the frontend) don't sleep and are served from
  Render's CDN.
- No credit card required for either, same as your Atlas M0 cluster and
  Digital Samba's free plan.
