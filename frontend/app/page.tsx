"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { getApplications } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import { ArrowRight, BriefcaseBusiness, CheckCircle2, TrendingUp } from "lucide-react";

export default function Dashboard() {
  const [apps, setApps] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getApplications()
      .then((data: any) => setApps(data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const total = apps.length;
  const applied = apps.filter((a) => a.status === "APPLIED").length;
  const scores = apps.map((a) => a.match_score).filter(Boolean);
  const avgScore = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : null;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">AI auto-apply for Australian software engineering roles</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard icon={<BriefcaseBusiness className="text-blue-500" size={20} />} label="Total Applications" value={total} />
        <StatCard icon={<CheckCircle2 className="text-green-500" size={20} />} label="Successfully Applied" value={applied} />
        <StatCard icon={<TrendingUp className="text-purple-500" size={20} />} label="Avg Match Score" value={avgScore ? `${avgScore}%` : "—"} />
      </div>

      {/* CTA */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-8 text-white">
        <h2 className="text-xl font-bold">Ready to auto-apply?</h2>
        <p className="text-blue-100 mt-1 mb-5">
          AI finds matching software engineering jobs on Seek.com.au and applies on your behalf.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/auto-apply"
            className="inline-flex items-center gap-2 bg-white text-blue-700 font-semibold px-5 py-2.5 rounded-xl hover:bg-blue-50 transition-colors"
          >
            Start Auto-Apply <ArrowRight size={16} />
          </Link>
          <Link
            href="/profile"
            className="inline-flex items-center gap-2 border border-white/30 text-white font-medium px-5 py-2.5 rounded-xl hover:bg-white/10 transition-colors"
          >
            Set Up Profile
          </Link>
        </div>
      </div>

      {/* Recent applications */}
      <div className="bg-white rounded-xl border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h2 className="font-semibold text-gray-900">Recent Applications</h2>
          <Link href="/applications" className="text-sm text-blue-600 hover:underline">
            View all
          </Link>
        </div>
        {loading ? (
          <div className="p-8 text-center text-gray-400">Loading…</div>
        ) : apps.length === 0 ? (
          <div className="p-8 text-center text-gray-400">
            No applications yet — start an auto-apply run!
          </div>
        ) : (
          <div className="divide-y divide-gray-50">
            {apps.slice(0, 6).map((app: any) => (
              <div key={app.id} className="px-6 py-4 flex items-center justify-between gap-4">
                <div className="min-w-0">
                  <p className="font-medium text-gray-900 truncate">{app.job_title}</p>
                  <p className="text-sm text-gray-500 truncate">
                    {app.company_name} · {app.location || "AU"}
                  </p>
                </div>
                <div className="flex items-center gap-3 shrink-0">
                  {app.match_score && (
                    <span className="text-sm font-semibold text-purple-600">{app.match_score}%</span>
                  )}
                  <StatusBadge status={app.status} />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: string | number }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 flex items-start gap-4">
      <div className="bg-gray-50 rounded-lg p-2">{icon}</div>
      <div>
        <p className="text-sm text-gray-500">{label}</p>
        <p className="text-2xl font-bold text-gray-900 mt-0.5">{value}</p>
      </div>
    </div>
  );
}
