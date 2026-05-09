"use client";
import { useEffect, useState } from "react";
import { getPreferences, updatePreferences } from "@/lib/api";
import { CheckCircle2, AlertCircle } from "lucide-react";

const LOCATIONS = ["All Australia", "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra", "Remote"];
const SENIORITY = ["JUNIOR", "MID", "SENIOR", "LEAD"];

export default function PreferencesPage() {
  const [form, setForm] = useState({
    preferred_location: "All Australia",
    min_salary_aud: "",
    max_salary_aud: "",
    tech_stack: "",
    seniority_level: "MID",
    max_applications_per_run: 5,
    match_score_threshold: 70,
  });
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    getPreferences()
      .then((p: any) => setForm({
        preferred_location: p.preferred_location || "All Australia",
        min_salary_aud: p.min_salary_aud ?? "",
        max_salary_aud: p.max_salary_aud ?? "",
        tech_stack: p.tech_stack || "",
        seniority_level: p.seniority_level || "MID",
        max_applications_per_run: p.max_applications_per_run ?? 5,
        match_score_threshold: p.match_score_threshold ?? 70,
      }))
      .catch(() => {});
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setMsg(null);
    try {
      await updatePreferences({
        ...form,
        min_salary_aud: form.min_salary_aud ? Number(form.min_salary_aud) : null,
        max_salary_aud: form.max_salary_aud ? Number(form.max_salary_aud) : null,
      });
      setMsg({ type: "success", text: "Preferences saved." });
    } catch (e: any) {
      setMsg({ type: "error", text: e.message });
    } finally {
      setSaving(false);
    }
  };

  const set = (key: string) => (val: any) => setForm((f) => ({ ...f, [key]: val }));

  return (
    <div className="max-w-xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Job Preferences</h1>
        <p className="text-gray-500 mt-1">Configure where and what the auto-apply targets.</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-5">
        {/* Location */}
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Preferred Location</label>
          <select
            value={form.preferred_location}
            onChange={(e) => set("preferred_location")(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {LOCATIONS.map((l) => <option key={l}>{l}</option>)}
          </select>
        </div>

        {/* Salary */}
        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Min Salary (AUD)</label>
            <input
              type="number"
              value={form.min_salary_aud}
              onChange={(e) => set("min_salary_aud")(e.target.value)}
              placeholder="e.g. 100000"
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Max Salary (AUD)</label>
            <input
              type="number"
              value={form.max_salary_aud}
              onChange={(e) => set("max_salary_aud")(e.target.value)}
              placeholder="e.g. 160000"
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Tech stack */}
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Tech Stack Keywords</label>
          <input
            value={form.tech_stack}
            onChange={(e) => set("tech_stack")(e.target.value)}
            placeholder="Python, React, AWS, Kubernetes…"
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Seniority */}
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Seniority Level</label>
          <div className="flex gap-2">
            {SENIORITY.map((s) => (
              <button
                key={s}
                onClick={() => set("seniority_level")(s)}
                className={`flex-1 py-2 text-sm font-medium rounded-lg border transition-colors ${
                  form.seniority_level === s
                    ? "bg-blue-600 text-white border-blue-600"
                    : "border-gray-300 text-gray-700 hover:border-blue-400"
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </div>

        {/* Match threshold */}
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-center">
            <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Min Match Score</label>
            <span className="text-sm font-bold text-blue-600">{form.match_score_threshold}%</span>
          </div>
          <input
            type="range"
            min={0}
            max={100}
            value={form.match_score_threshold}
            onChange={(e) => set("match_score_threshold")(Number(e.target.value))}
            className="w-full accent-blue-600"
          />
          <p className="text-xs text-gray-400">Only apply to jobs where AI scores the match ≥ this value.</p>
        </div>

        {/* Max apps */}
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Max Applications per Run</label>
          <input
            type="number"
            min={1}
            max={20}
            value={form.max_applications_per_run}
            onChange={(e) => set("max_applications_per_run")(Number(e.target.value))}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-24"
          />
        </div>

        {msg && (
          <div className={`flex items-center gap-2 text-sm rounded-lg px-4 py-3 ${msg.type === "success" ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>
            {msg.type === "success" ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
            {msg.text}
          </div>
        )}

        <button
          onClick={handleSave}
          disabled={saving}
          className="w-full bg-blue-600 text-white font-semibold py-2.5 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {saving ? "Saving…" : "Save Preferences"}
        </button>
      </div>
    </div>
  );
}
