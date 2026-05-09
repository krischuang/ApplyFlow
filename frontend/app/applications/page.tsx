"use client";
import { useEffect, useState } from "react";
import { getApplications, updateApplicationStatus } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import { ExternalLink, Bot, ChevronDown, ChevronUp } from "lucide-react";

const STATUSES = ["ALL", "SAVED", "APPLIED", "INTERVIEWING", "OFFER", "REJECTED", "WITHDRAWN", "FAILED"];

export default function ApplicationsPage() {
  const [apps, setApps] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("ALL");
  const [expanded, setExpanded] = useState<number | null>(null);

  useEffect(() => {
    const status = filter === "ALL" ? undefined : filter;
    setLoading(true);
    getApplications(status)
      .then((data: any) => setApps(data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [filter]);

  const handleStatusChange = async (id: number, status: string) => {
    try {
      const updated: any = await updateApplicationStatus(id, status);
      setApps((prev) => prev.map((a) => (a.id === id ? updated : a)));
    } catch {}
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Applications</h1>
        <p className="text-gray-500 mt-1">{apps.length} total</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        {STATUSES.map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`px-3 py-1.5 text-sm font-medium rounded-lg transition-colors ${
              filter === s ? "bg-blue-600 text-white" : "bg-white border border-gray-300 text-gray-700 hover:border-blue-400"
            }`}
          >
            {s}
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-gray-400">Loading…</div>
        ) : apps.length === 0 ? (
          <div className="p-8 text-center text-gray-400">No applications found.</div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-xs text-gray-500 uppercase tracking-wide border-b border-gray-100">
                <th className="px-6 py-3 text-left font-medium">Job</th>
                <th className="px-4 py-3 text-left font-medium">Location</th>
                <th className="px-4 py-3 text-left font-medium">Salary</th>
                <th className="px-4 py-3 text-center font-medium">Score</th>
                <th className="px-4 py-3 text-center font-medium">Status</th>
                <th className="px-4 py-3 text-center font-medium">Applied</th>
                <th className="px-4 py-3 text-center font-medium">Source</th>
                <th className="px-4 py-3 text-center font-medium" />
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {apps.map((app) => (
                <>
                  <tr key={app.id} className="hover:bg-gray-50/50">
                    <td className="px-6 py-4">
                      <div className="flex items-start gap-2">
                        <div>
                          <p className="font-medium text-gray-900">{app.job_title}</p>
                          <p className="text-gray-500 text-xs mt-0.5">{app.company_name}</p>
                        </div>
                        {app.job_url && (
                          <a href={app.job_url} target="_blank" rel="noreferrer" className="text-blue-500 hover:text-blue-700 mt-0.5">
                            <ExternalLink size={14} />
                          </a>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-4 text-gray-600">{app.location || "—"}</td>
                    <td className="px-4 py-4 text-gray-600">{app.salary_range || "—"}</td>
                    <td className="px-4 py-4 text-center">
                      {app.match_score ? (
                        <span className="font-bold text-purple-600">{app.match_score}%</span>
                      ) : "—"}
                    </td>
                    <td className="px-4 py-4 text-center">
                      <select
                        value={app.status}
                        onChange={(e) => handleStatusChange(app.id, e.target.value)}
                        className="text-xs border border-gray-200 rounded-md px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      >
                        {["SAVED","APPLIED","INTERVIEWING","OFFER","REJECTED","WITHDRAWN"].map((s) => (
                          <option key={s}>{s}</option>
                        ))}
                      </select>
                    </td>
                    <td className="px-4 py-4 text-center text-gray-500">{app.applied_date || "—"}</td>
                    <td className="px-4 py-4 text-center">
                      {app.auto_applied && (
                        <span title="Auto-applied by AI" className="inline-flex items-center gap-1 text-xs bg-indigo-50 text-indigo-600 rounded-full px-2 py-0.5 font-medium">
                          <Bot size={12} /> AI
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-4 text-center">
                      {app.cover_letter_used && (
                        <button
                          onClick={() => setExpanded(expanded === app.id ? null : app.id)}
                          className="text-gray-400 hover:text-gray-700"
                        >
                          {expanded === app.id ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                        </button>
                      )}
                    </td>
                  </tr>
                  {expanded === app.id && app.cover_letter_used && (
                    <tr key={`${app.id}-cl`}>
                      <td colSpan={8} className="px-6 py-4 bg-gray-50 border-t border-gray-100">
                        <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Cover Letter Used</p>
                        <p className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">{app.cover_letter_used}</p>
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
