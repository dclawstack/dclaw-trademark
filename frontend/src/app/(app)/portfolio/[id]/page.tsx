"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, Shield, AlertCircle, Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  getTrademark,
  listWatchlist,
  listDeadlines,
  type Trademark,
  type WatchlistEntry,
  type DeadlineAlert,
} from "@/lib/api";

const STATUS_COLORS: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  Pending: "secondary",
  Registered: "default",
  Refused: "destructive",
  Abandoned: "outline",
  Expired: "destructive",
  Cancelled: "outline",
};

const DEADLINE_STATUS_COLORS: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  Pending: "secondary",
  Completed: "default",
  Dismissed: "outline",
  Overdue: "destructive",
};

function SimilarityBar({ score }: { score: number | null }) {
  if (score === null) return <span className="text-slate-400 text-xs">N/A</span>;
  const pct = Math.round(score * 100);
  const color = score > 0.6 ? "#EF4444" : score > 0.3 ? "#F59E0B" : "#22C55E";
  return (
    <div className="flex items-center gap-2">
      <div className="w-24 bg-slate-100 rounded-full h-2">
        <div className="h-2 rounded-full" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
      <span className="text-xs font-mono">{pct}%</span>
    </div>
  );
}

export default function TrademarkDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [trademark, setTrademark] = useState<Trademark | null>(null);
  const [watchlist, setWatchlist] = useState<WatchlistEntry[]>([]);
  const [deadlines, setDeadlines] = useState<DeadlineAlert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [tm, wl, dl] = await Promise.all([
          getTrademark(id),
          listWatchlist(id),
          listDeadlines(id),
        ]);
        setTrademark(tm);
        setWatchlist(wl.items);
        setDeadlines(dl.items);
      } catch {
        router.push("/portfolio");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id, router]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <p className="text-slate-500">Loading trademark...</p>
      </div>
    );
  }

  if (!trademark) return null;

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Back + Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => router.push("/portfolio")}>
          <ArrowLeft className="w-4 h-4 mr-1" /> Portfolio
        </Button>
      </div>

      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <Shield className="w-9 h-9" style={{ color: "#6366F1" }} />
          <div>
            <h1 className="text-2xl font-bold">{trademark.name}</h1>
            <p className="text-sm text-slate-500">{trademark.owner} · {trademark.jurisdiction}</p>
          </div>
        </div>
        <Badge variant={STATUS_COLORS[trademark.status] ?? "secondary"}>
          {trademark.status}
        </Badge>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-4">
            <p className="text-xs text-slate-500">Application #</p>
            <p className="font-mono text-sm mt-1">{trademark.application_number ?? "—"}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4">
            <p className="text-xs text-slate-500">Registration #</p>
            <p className="font-mono text-sm mt-1">{trademark.registration_number ?? "—"}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4">
            <p className="text-xs text-slate-500">Filed</p>
            <p className="text-sm mt-1">
              {trademark.filing_date ? new Date(trademark.filing_date).toLocaleDateString() : "—"}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4">
            <p className="text-xs text-slate-500">Expires</p>
            <p className="text-sm mt-1">
              {trademark.expiry_date ? new Date(trademark.expiry_date).toLocaleDateString() : "—"}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="watchlist">
            Watchlist {watchlist.length > 0 && `(${watchlist.length})`}
          </TabsTrigger>
          <TabsTrigger value="deadlines">
            Deadlines {deadlines.filter((d) => d.status === "Pending").length > 0 &&
              `(${deadlines.filter((d) => d.status === "Pending").length})`}
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4 mt-4">
          <Card>
            <CardHeader><CardTitle>Nice Classes</CardTitle></CardHeader>
            <CardContent>
              {trademark.classes.length === 0 ? (
                <p className="text-sm text-slate-500">No classes assigned.</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {trademark.classes.map((cls) => (
                    <div key={cls.id} className="flex items-center gap-1.5 bg-slate-50 border rounded-md px-3 py-1.5">
                      <Badge variant="outline" className="text-xs">Class {cls.nice_class_number}</Badge>
                      {cls.description && (
                        <span className="text-sm text-slate-600">{cls.description}</span>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
          {trademark.description && (
            <Card>
              <CardHeader><CardTitle>Description</CardTitle></CardHeader>
              <CardContent>
                <p className="text-sm text-slate-700">{trademark.description}</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Watchlist Tab */}
        <TabsContent value="watchlist" className="mt-4">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Eye className="w-4 h-4" />
                <CardTitle>Conflicting Marks</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              {watchlist.length === 0 ? (
                <p className="text-sm text-slate-500 py-4 text-center">No conflicts detected.</p>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Mark</TableHead>
                      <TableHead>Conflict Type</TableHead>
                      <TableHead>Similarity</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {watchlist.map((entry) => (
                      <TableRow key={entry.id}>
                        <TableCell className="font-medium">{entry.conflicting_mark_name}</TableCell>
                        <TableCell>
                          <Badge variant="outline">{entry.conflict_type}</Badge>
                        </TableCell>
                        <TableCell>
                          <SimilarityBar score={entry.similarity_score} />
                        </TableCell>
                        <TableCell>
                          <Badge variant={entry.status === "Active" ? "secondary" : "outline"}>
                            {entry.status}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Deadlines Tab */}
        <TabsContent value="deadlines" className="mt-4">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <AlertCircle className="w-4 h-4" />
                <CardTitle>Upcoming Deadlines</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              {deadlines.length === 0 ? (
                <p className="text-sm text-slate-500 py-4 text-center">No deadlines tracked.</p>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Type</TableHead>
                      <TableHead>Due Date</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Notes</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {deadlines
                      .sort(
                        (a, b) =>
                          new Date(a.due_date).getTime() - new Date(b.due_date).getTime()
                      )
                      .map((dl) => (
                        <TableRow key={dl.id}>
                          <TableCell>
                            <Badge variant="outline">{dl.deadline_type}</Badge>
                          </TableCell>
                          <TableCell>
                            {new Date(dl.due_date).toLocaleDateString()}
                          </TableCell>
                          <TableCell>
                            <Badge variant={DEADLINE_STATUS_COLORS[dl.status] ?? "secondary"}>
                              {dl.status}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-sm text-slate-500">
                            {dl.notes ?? "—"}
                          </TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
