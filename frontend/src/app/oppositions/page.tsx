"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { listTrademarks, listOppositions, type Trademark, type OppositionCase } from "@/lib/api";

const STAGE_COLORS: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  Filed: "secondary",
  Published: "secondary",
  OppositionWindow: "default",
  Opposed: "destructive",
  Resolved: "outline",
  Abandoned: "outline",
};

const TYPE_LABELS: Record<string, string> = {
  Opposition: "⚠ Opposition",
  Cancellation: "✂ Cancellation",
  CeaseAndDesist: "✉ C&D",
  Litigation: "⚖ Litigation",
};

interface CaseWithMark extends OppositionCase {
  trademark_name: string;
}

function daysUntil(dateStr: string | null): string {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  const diff = Math.round((d.getTime() - Date.now()) / 86400000);
  if (diff < 0) return `${Math.abs(diff)}d overdue`;
  if (diff === 0) return "Today";
  return `${diff}d`;
}

export default function OppositionsPage() {
  const [cases, setCases] = useState<CaseWithMark[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>("all");

  useEffect(() => {
    async function load() {
      try {
        const { items: trademarks } = await listTrademarks(100, 0);
        const all: CaseWithMark[] = [];
        await Promise.all(
          trademarks.map(async (tm: Trademark) => {
            try {
              const { items } = await listOppositions(tm.id);
              items.forEach((c) => all.push({ ...c, trademark_name: tm.name }));
            } catch {
              // skip this trademark if opposition fetch fails
            }
          })
        );
        all.sort(
          (a, b) =>
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        setCases(all);
      } catch {
        setError("Failed to load opposition cases.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const allStages = ["all", ...Array.from(new Set(cases.map((c) => c.stage)))];
  const displayed = filter === "all" ? cases : cases.filter((c) => c.stage === filter);

  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-1">
          Opposition &amp; Enforcement
        </h1>
        <p className="text-gray-600">
          Track oppositions, cancellations, cease &amp; desist letters, and litigation.
        </p>
      </div>

      {/* Stage filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {allStages.map((s) => (
          <Button
            key={s}
            variant={filter === s ? "default" : "outline"}
            onClick={() => setFilter(s)}
          >
            {s === "all" ? `All (${cases.length})` : `${s} (${cases.filter((c) => c.stage === s).length})`}
          </Button>
        ))}
      </div>

      {loading && (
        <div className="text-center py-16 text-gray-500">Loading cases…</div>
      )}

      {error && (
        <div className="rounded-md bg-red-50 border border-red-200 p-4 text-red-700">
          {error}
        </div>
      )}

      {!loading && !error && displayed.length === 0 && (
        <Card>
          <CardContent className="py-16 text-center text-gray-500">
            No opposition cases found
            {filter !== "all" ? ` with stage "${filter}"` : ""}. Add them via the Portfolio page.
          </CardContent>
        </Card>
      )}

      <div className="flex flex-col gap-4">
        {displayed.map((c) => (
          <Card key={c.id}>
            <CardHeader className="pb-2">
              <div className="flex items-start justify-between gap-2 flex-wrap">
                <div>
                  <CardTitle className="text-base">
                    {TYPE_LABELS[c.case_type] ?? c.case_type}
                    {c.case_number && (
                      <span className="ml-2 text-xs font-mono text-gray-500">
                        #{c.case_number}
                      </span>
                    )}
                  </CardTitle>
                  <p className="text-sm text-gray-500 mt-0.5">
                    Portfolio mark:{" "}
                    <span className="font-medium text-gray-700">
                      {c.trademark_name}
                    </span>
                  </p>
                </div>
                <Badge variant={STAGE_COLORS[c.stage] ?? "default"}>
                  {c.stage}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-3 text-sm">
                {c.opposing_party && (
                  <div>
                    <p className="text-gray-500">Opposing Party</p>
                    <p className="font-medium">{c.opposing_party}</p>
                  </div>
                )}
                {c.opposing_counsel && (
                  <div>
                    <p className="text-gray-500">Counsel</p>
                    <p className="font-medium">{c.opposing_counsel}</p>
                  </div>
                )}
                {c.response_deadline && (
                  <div>
                    <p className="text-gray-500">Response Deadline</p>
                    <p className={`font-medium ${daysUntil(c.response_deadline).includes("overdue") ? "text-red-600" : ""}`}>
                      {new Date(c.response_deadline).toLocaleDateString()} ({daysUntil(c.response_deadline)})
                    </p>
                  </div>
                )}
                {c.hearing_date && (
                  <div>
                    <p className="text-gray-500">Hearing Date</p>
                    <p className="font-medium">
                      {new Date(c.hearing_date).toLocaleDateString()} ({daysUntil(c.hearing_date)})
                    </p>
                  </div>
                )}
                {c.outcome && (
                  <div className="col-span-2">
                    <p className="text-gray-500">Outcome</p>
                    <p className="font-medium">{c.outcome}</p>
                  </div>
                )}
                {c.notes && (
                  <div className="col-span-2">
                    <p className="text-gray-500">Notes</p>
                    <p className="text-gray-700">{c.notes}</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
