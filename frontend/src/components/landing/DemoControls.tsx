"use client";

/**
 * Demo seed/clear controls for the landing page.
 *
 * To remove the demo feature entirely:
 *   1. Delete this file.
 *   2. Remove the <DemoControls /> block (inside the DEMO CONTROLS markers)
 *      and its import in src/app/page.tsx.
 *   3. Delete the backend demo router + service (see backend/app/api/v1/demo.py).
 *
 * Calls relative /api/v1/demo/* so it proxies through next.config.js rewrites.
 */
import { useEffect, useState } from "react";
import Link from "next/link";
import { Database, Play, RefreshCw, Terminal, Trash2 } from "lucide-react";

type DemoStatus = {
  enabled: boolean;
  seeded: boolean;
  counts: Record<string, number>;
};

type Phase = "loading" | "ready" | "unavailable";

export default function DemoControls() {
  const [status, setStatus] = useState<DemoStatus | null>(null);
  const [phase, setPhase] = useState<Phase>("loading");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    try {
      const res = await fetch("/api/v1/demo/status");
      if (!res.ok) throw new Error(await res.text());
      const s: DemoStatus = await res.json();
      setStatus(s);
      setPhase(s.enabled ? "ready" : "unavailable");
    } catch {
      setStatus(null);
      setPhase("unavailable");
    }
  }

  useEffect(() => {
    void refresh();
  }, []);

  async function call(method: "POST" | "DELETE") {
    setBusy(true);
    setError(null);
    try {
      const res = await fetch(
        method === "POST" ? "/api/v1/demo/seed" : "/api/v1/demo/reset",
        { method }
      );
      if (!res.ok) throw new Error(await res.text());
      setStatus(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="border-y border-indigo-100 bg-indigo-50/40">
      <div className="mx-auto max-w-5xl px-6 py-16">
        <div className="grid items-center gap-8 lg:grid-cols-[1fr_auto]">
          <div>
            <div className="inline-flex items-center gap-1 rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-indigo-700">
              <Database className="h-3 w-3" /> Try the demo
            </div>
            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              Load a sample trademark portfolio in one click.
            </h2>
            <p className="mt-3 max-w-2xl text-slate-600">
              The demo seeds a realistic portfolio — several marks across NICE
              classes and statuses, upcoming renewal and statement-of-use
              deadlines, a watchlist conflict, and an active opposition. Every
              mark name is prefixed{" "}
              <code className="rounded bg-white px-1.5 py-0.5 font-mono text-xs text-indigo-700">
                DEMO
              </code>{" "}
              so Clear removes only what was seeded.
            </p>

            {phase === "ready" && status?.seeded && (
              <p className="mt-3 text-sm text-slate-700">
                <strong>Seeded:</strong>{" "}
                {Object.entries(status.counts)
                  .map(([k, v]) => `${v} ${k}`)
                  .join(" · ")}
              </p>
            )}

            {phase === "unavailable" && (
              <div className="mt-5 rounded-xl border border-slate-200 bg-white p-4">
                <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-slate-800">
                  <Terminal className="h-4 w-4 text-indigo-600" />
                  Demo backend not connected
                </div>
                <p className="text-sm text-slate-600">
                  The demo endpoints are off (or the API isn&rsquo;t reachable).
                  Set{" "}
                  <code className="rounded bg-slate-100 px-1 py-0.5 font-mono">
                    ENABLE_DEMO_MODE=true
                  </code>{" "}
                  on the backend to activate this section.
                </p>
              </div>
            )}

            {error && (
              <div className="mt-3 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800">
                {error}
              </div>
            )}
          </div>

          <div className="flex flex-col gap-2 sm:flex-row lg:flex-col">
            {phase === "loading" && (
              <div className="text-xs text-slate-400">Checking demo backend…</div>
            )}

            {phase === "ready" && !status?.seeded && (
              <button
                type="button"
                onClick={() => call("POST")}
                disabled={busy}
                className="inline-flex items-center justify-center gap-2 rounded-lg bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow hover:bg-indigo-700 disabled:opacity-50"
              >
                <Play className="h-4 w-4" />
                {busy ? "Seeding…" : "Seed demo data"}
              </button>
            )}

            {phase === "ready" && status?.seeded && (
              <>
                <Link
                  href="/portfolio"
                  className="inline-flex items-center justify-center gap-2 rounded-lg bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow hover:bg-indigo-700"
                >
                  Open the portfolio →
                </Link>
                <button
                  type="button"
                  onClick={() => call("POST")}
                  disabled={busy}
                  className="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-50"
                >
                  <RefreshCw className="h-4 w-4" />
                  {busy ? "Re-seeding…" : "Re-seed"}
                </button>
                <button
                  type="button"
                  onClick={() => call("DELETE")}
                  disabled={busy}
                  className="inline-flex items-center justify-center gap-2 rounded-lg border border-red-200 bg-white px-5 py-3 text-sm font-semibold text-red-700 hover:bg-red-50 disabled:opacity-50"
                >
                  <Trash2 className="h-4 w-4" />
                  Clear demo data
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
