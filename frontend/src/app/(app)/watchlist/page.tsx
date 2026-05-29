"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { listTrademarks, listWatchlist, type Trademark, type WatchlistEntry } from "@/lib/api";

type ConflictStatus = "Active" | "Dismissed" | "Flagged";

const STATUS_VARIANTS: Record<ConflictStatus, "default" | "secondary" | "destructive" | "outline"> = {
  Active: "destructive",
  Flagged: "default",
  Dismissed: "outline",
};

function RiskBar({ score }: { score: number | null }) {
  if (score === null) return <span className="text-gray-400">—</span>;
  const pct = Math.round(score * 100);
  const color = pct >= 60 ? "bg-red-500" : pct >= 30 ? "bg-yellow-500" : "bg-green-500";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 bg-gray-200 rounded-full h-2 w-24">
        <div className={`${color} h-2 rounded-full`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-sm font-medium text-gray-700">{pct}%</span>
    </div>
  );
}

interface WatchEntryWithMark extends WatchlistEntry {
  trademark_name: string;
}

export default function WatchlistPage() {
  const [entries, setEntries] = useState<WatchEntryWithMark[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<"all" | ConflictStatus>("all");

  useEffect(() => {
    async function load() {
      try {
        const { items: trademarks } = await listTrademarks(100, 0);
        const all: WatchEntryWithMark[] = [];
        await Promise.all(
          trademarks.map(async (tm: Trademark) => {
            const { items } = await listWatchlist(tm.id);
            items.forEach((e) =>
              all.push({ ...e, trademark_name: tm.name })
            );
          })
        );
        all.sort((a, b) => (b.similarity_score ?? 0) - (a.similarity_score ?? 0));
        setEntries(all);
      } catch {
        setError("Failed to load watchlist. Is the backend running?");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const displayed =
    filter === "all" ? entries : entries.filter((e) => e.status === filter);

  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-1">Watch Service</h1>
          <p className="text-gray-600">Monitor conflicting marks across your portfolio.</p>
        </div>
      </div>

      {/* Filter bar */}
      <div className="flex gap-2 mb-6">
        {(["all", "Active", "Flagged", "Dismissed"] as const).map((f) => (
          <Button
            key={f}
            variant={filter === f ? "default" : "outline"}
            onClick={() => setFilter(f)}
          >
            {f === "all" ? "All" : f}
            {f === "all" && ` (${entries.length})`}
            {f !== "all" && ` (${entries.filter((e) => e.status === f).length})`}
          </Button>
        ))}
      </div>

      {loading && (
        <div className="text-center py-16 text-gray-500">Loading watchlist…</div>
      )}

      {error && (
        <div className="rounded-md bg-red-50 border border-red-200 p-4 text-red-700">
          {error}
        </div>
      )}

      {!loading && !error && displayed.length === 0 && (
        <Card>
          <CardContent className="py-16 text-center text-gray-500">
            No conflicts found
            {filter !== "all" ? ` with status "${filter}"` : ""}.
          </CardContent>
        </Card>
      )}

      <div className="flex flex-col gap-4">
        {displayed.map((entry) => (
          <Card key={entry.id}>
            <CardHeader className="pb-2">
              <div className="flex items-start justify-between gap-2">
                <CardTitle className="text-base">{entry.conflicting_mark_name}</CardTitle>
                <Badge variant={STATUS_VARIANTS[entry.status as ConflictStatus] ?? "default"}>
                  {entry.status}
                </Badge>
              </div>
              <p className="text-sm text-gray-500">
                Portfolio mark:{" "}
                <span className="font-medium text-gray-700">{entry.trademark_name}</span>
              </p>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-500 mb-1">Similarity Score</p>
                  <RiskBar score={entry.similarity_score} />
                </div>
                <div>
                  <p className="text-gray-500 mb-1">Conflict Type</p>
                  <p className="font-medium">{entry.conflict_type}</p>
                </div>
                {entry.notes && (
                  <div className="col-span-2">
                    <p className="text-gray-500 mb-1">Notes</p>
                    <p className="text-gray-700">{entry.notes}</p>
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
