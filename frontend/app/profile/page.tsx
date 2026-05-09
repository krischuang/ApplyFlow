"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { getProfile, updateProfile, uploadResume } from "@/lib/api";
import { Upload, CheckCircle2, AlertCircle } from "lucide-react";

export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [msg, setMsg] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [form, setForm] = useState({ full_name: "", email: "", phone: "", current_location: "", experience_summary: "", education_summary: "", skills: "" });
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    getProfile()
      .then((p: any) => {
        setProfile(p);
        setForm({
          full_name: p.full_name || "",
          email: p.email || "",
          phone: p.phone || "",
          current_location: p.current_location || "",
          experience_summary: p.experience_summary || "",
          education_summary: p.education_summary || "",
          skills: (p.skills || []).join(", "),
        });
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleUpload = useCallback(async (file: File) => {
    setUploading(true);
    setMsg(null);
    try {
      const p = await uploadResume(file);
      setProfile(p);
      setForm({
        full_name: p.full_name || "",
        email: p.email || "",
        phone: p.phone || "",
        current_location: p.current_location || "",
        experience_summary: p.experience_summary || "",
        education_summary: p.education_summary || "",
        skills: (p.skills || []).join(", "),
      });
      setMsg({ type: "success", text: "Resume uploaded and profile updated by AI." });
    } catch (e: any) {
      setMsg({ type: "error", text: e.message });
    } finally {
      setUploading(false);
    }
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setMsg(null);
    try {
      const skills = form.skills.split(",").map((s) => s.trim()).filter(Boolean);
      const p = await updateProfile({ ...form, skills });
      setProfile(p);
      setMsg({ type: "success", text: "Profile saved." });
    } catch (e: any) {
      setMsg({ type: "error", text: e.message });
    } finally {
      setSaving(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file?.type === "application/pdf") handleUpload(file);
  };

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Profile</h1>
        <p className="text-gray-500 mt-1">Upload your resume — AI will parse it and fill your profile automatically.</p>
      </div>

      {/* Resume upload */}
      <div
        className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:border-blue-400 hover:bg-blue-50/30 transition-colors"
        onClick={() => fileRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
      >
        <Upload className="mx-auto text-gray-400 mb-3" size={32} />
        <p className="text-sm font-medium text-gray-700">
          {uploading ? "Parsing resume with AI…" : "Drop your PDF resume here, or click to browse"}
        </p>
        <p className="text-xs text-gray-400 mt-1">PDF only · Max 10 MB</p>
        {profile?.has_resume && (
          <p className="text-xs text-green-600 mt-2 font-medium">✓ Resume on file</p>
        )}
        <input ref={fileRef} type="file" accept=".pdf" className="hidden" onChange={(e) => {
          const f = e.target.files?.[0];
          if (f) handleUpload(f);
        }} />
      </div>

      {msg && (
        <div className={`flex items-center gap-2 text-sm rounded-lg px-4 py-3 ${msg.type === "success" ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>
          {msg.type === "success" ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
          {msg.text}
        </div>
      )}

      {/* Profile form */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        <h2 className="font-semibold text-gray-900">Profile Details</h2>

        <div className="grid grid-cols-2 gap-4">
          <Field label="Full Name" value={form.full_name} onChange={(v) => setForm({ ...form, full_name: v })} />
          <Field label="Email" value={form.email} onChange={(v) => setForm({ ...form, email: v })} type="email" />
          <Field label="Phone" value={form.phone} onChange={(v) => setForm({ ...form, phone: v })} />
          <Field label="Location (AU city)" value={form.current_location} onChange={(v) => setForm({ ...form, current_location: v })} placeholder="e.g. Sydney, NSW" />
        </div>

        <Field label="Skills (comma-separated)" value={form.skills} onChange={(v) => setForm({ ...form, skills: v })} placeholder="Java, Python, React, AWS…" />
        <TextArea label="Experience Summary" value={form.experience_summary} onChange={(v) => setForm({ ...form, experience_summary: v })} rows={4} />
        <TextArea label="Education Summary" value={form.education_summary} onChange={(v) => setForm({ ...form, education_summary: v })} rows={2} />

        <button
          onClick={handleSave}
          disabled={saving}
          className="w-full bg-blue-600 text-white font-semibold py-2.5 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {saving ? "Saving…" : "Save Profile"}
        </button>
      </div>
    </div>
  );
}

function Field({ label, value, onChange, type = "text", placeholder }: { label: string; value: string; onChange: (v: string) => void; type?: string; placeholder?: string }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
  );
}

function TextArea({ label, value, onChange, rows = 3 }: { label: string; value: string; onChange: (v: string) => void; rows?: number }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">{label}</label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={rows}
        className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
      />
    </div>
  );
}
