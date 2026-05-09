const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

// ── Profile ──────────────────────────────────────────────────────────────────
export async function uploadResume(file: File) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}/api/v1/profile/resume`, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export const getProfile = () => req("/api/v1/profile");
export const updateProfile = (data: object) =>
  req("/api/v1/profile", { method: "PUT", body: JSON.stringify(data) });

// ── Preferences ───────────────────────────────────────────────────────────────
export const getPreferences = () => req("/api/v1/profile/preferences");
export const updatePreferences = (data: object) =>
  req("/api/v1/profile/preferences", { method: "PUT", body: JSON.stringify(data) });

// ── Applications ──────────────────────────────────────────────────────────────
export const getApplications = (status?: string) =>
  req(`/api/v1/applications${status ? `?status=${status}` : ""}`);
export const updateApplicationStatus = (id: number, status: string) =>
  req(`/api/v1/applications/${id}/status?status=${status}`, { method: "PATCH" });

// ── Auto Apply ────────────────────────────────────────────────────────────────
export const startAutoApplyRun = () =>
  req("/api/v1/auto-apply/run", { method: "POST", body: "{}" });
export const getRunStatus = (runId: string) =>
  req(`/api/v1/auto-apply/runs/${runId}`);
export const getAllRuns = () => req("/api/v1/auto-apply/runs");
