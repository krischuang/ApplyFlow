"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { getAllRuns, getRunStatus, startAutoApplyRun } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import { Play, RefreshCw, ExternalLink } from "lucide-react";

export default function AutoApplyPage() {
  const [runs, setRuns] = useState<any[]>([]);
  const [activeRunId, setActiveRunId] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Load past runs on mount
  useEffect(() => {
    getAllRuns().then((r: any) => setRuns(r)).catch(() => {});
  }, []);

  // Poll active run
  const pollRun = useCallback((runId: string) => {
    if (pollRef.current) clearInterval(pollRef.current);
    pollRef.current = setInterval(async () => {
      try {
        const state: any = await getRunStatus(runId);
        setRuns((prev) => {
          const idx = prev.findIndex((r) => r.run_id === runId);
          if (idx === -1) return [state, ...prev];
          return prev.map((r) => (r.run_id === runId ? state : r));
        });
        if (state.status === "COMPLETED" || state.status === "FAILED") {
          clearInterval(pollRef.current!);
          setActiveRunId(null);
        }
      } catch {
        clearInterval(pollRef.current!);
      }
    }, 2500);
  }, []);

  useEffect(() => () => { if (pollRef.current) clearInterval(pollRef.current); }, []);

  const handleStart = async () => {
    setStarting(true);
    setError(null);
    try {
      const res: any = await startAutoApplyRun();
      setActiveRunId(res.run_id);
      setRuns((prev) => [{ run_id: res.run_id, status: "RUNNING", jobs_found: 0, jobs_matched: 0, applications_submitted: 0, applications_failed: 0, results: [], started_at: new Date().toISOString() }, ...prev]);
      pollRun(res.run_id);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setStarting(false);
    }
  };

  const activeRun = runs.find((r) => r.run_id === activeRunId);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Auto Apply</h1>
        <p className="text-gray-500 mt-1">
          One click — AI scrapes Seek.com.au, scores jobs against your profile, and submits applications.
        </p>
      </div>

      {/* Start button */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 flex items-center justify-between gap-4">
        <div>
          <p className="font-semibold text-gray-900">Start a new run</p>
          <p className="text-sm text-gray-500 mt-0.5">Scrapes Seek, scores with Claude AI, applies to top matches.</p>
        </div>
        <button
          onClick={handleStart}
          disabled={starting || !!activeRunId}
          className="inline-flex items-center gap-2 bg-blue-600 text-white font-semibold px-5 py-2.5 rounded-xl hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {starting ? <RefreshCw size={16} className="animate-spin" /> : <Play size={16} />}
          {activeRunId ? "Running…" : "Start Run"}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">{error}</div>
      )}

      {/* Active run progress */}
      {activeRun && (
        <RunCard run={activeRun} isActive />
      )}

      {/* Past runs */}
      {runs.filter((r) => r.run_id !== activeRunId).length > 0 && (
        <div className="space-y-4">
          <h2 className="font-semibold text-gray-700">Past Runs</h2>
          {runs.filter((r) => r.run_id !== activeRunId).map((r) => (
            <RunCard key={r.run_id} run={r} />
          ))}
        </div>
      )}
    </div>
  );
}

function RunCard({ run, isActive = false }: { run: any; isActive?: boolean }) {
  const [expanded, setExpanded] = useState(isActive);

  return (
    <div className={`bg-white rounded-xl border ${isActive ? "border-blue-300 ring-1 ring-blue-200" : "border-gray-200"}`}>
      <div className="px-6 py-4 flex items-center justify-between cursor-pointer" onClick={() => setExpanded(!expanded)}>
        <div className="flex items-center gap-3">
          <StatusBadge status={run.status} />
          <span className="text-sm text-gray-500 font-mono">{run.run_id.slice(0, 8)}…</span>
          {isActive && run.status === "RUNNING" && (
            <RefreshCw size={14} className="text-blue-500 animate-spin" />
          )}
        </div>
        <div className="flex items-center gap-6 text-sm">
          <Stat label="Found" value={run.jobs_found} />
          <Stat label="Matched" value={run.jobs_matched} />
          <Stat label="Submitted" value={run.applications_submitted} color="text-green-600" />
          <Stat label="Failed" value={run.applications_failed} color="text-red-500" />
        </div>
      </div>

      {expanded && run.results?.length > 0 && (
        <div className="border-t border-gray-100">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-xs text-gray-500 uppercase tracking-wide">
                <th className="px-6 py-2 text-left font-medium">Job</th>
                <th className="px-4 py-2 text-left font-medium">Company</th>
                <th className="px-4 py-2 text-center font-medium">Score</th>
                <th className="px-4 py-2 text-center font-medium">Result</th>
                <th className="px-4 py-2 text-left font-medium">Reason</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {run.results.map((r: any, i: number) => (
                <tr key={i} className="hover:bg-gray-50/50">
                  <td className="px-6 py-3">
                    <a href={r.job_url} target="_blank" rel="noreferrer" className="font-medium text-blue-600 hover:underline flex items-center gap-1">
                      {r.job_title} <ExternalLink size={12} />
                    </a>
                  </td>
                  <td className="px-4 py-3 text-gray-600">{r.company}</td>
                  <td className="px-4 py-3 text-center font-semibold text-purple-600">{r.match_score}%</td>
                  <td className="px-4 py-3 text-center"><StatusBadge status={r.status} /></td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{r.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {run.error && (
        <div className="border-t border-red-100 bg-red-50 px-6 py-3 text-sm text-red-600">{run.error}</div>
      )}
    </div>
  );
}

function Stat({ label, value, color = "text-gray-900" }: { label: string; value: number; color?: string }) {
  return (
    <div className="text-center">
      <p className={`font-bold ${color}`}>{value}</p>
      <p className="text-xs text-gray-400">{label}</p>
    </div>
  );
}
