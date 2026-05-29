"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Shield, Plus, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { listTrademarks, createTrademark, type Trademark } from "@/lib/api";

const STATUS_COLORS: Record<string, string> = {
  Pending: "secondary",
  Registered: "default",
  Refused: "destructive",
  Abandoned: "outline",
  Expired: "destructive",
  Cancelled: "outline",
};

export default function PortfolioPage() {
  const [trademarks, setTrademarks] = useState<Trademark[]>([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({ name: "", owner: "", jurisdiction: "US" });
  const [submitting, setSubmitting] = useState(false);

  async function load() {
    setLoading(true);
    try {
      const data = await listTrademarks(50, 0);
      setTrademarks(data.items);
      setTotal(data.total);
    } catch {
      // silently fail — backend may not be reachable in SSR context
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  const filtered = trademarks.filter((tm) =>
    tm.name.toLowerCase().includes(search.toLowerCase()) ||
    tm.owner.toLowerCase().includes(search.toLowerCase())
  );

  async function handleCreate() {
    if (!form.name || !form.owner) return;
    setSubmitting(true);
    try {
      await createTrademark(form);
      setShowCreate(false);
      setForm({ name: "", owner: "", jurisdiction: "US" });
      await load();
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Shield className="w-8 h-8" style={{ color: "#6366F1" }} />
          <div>
            <h1 className="text-2xl font-bold">Trademark Portfolio</h1>
            <p className="text-sm text-slate-500">{total} mark{total !== 1 ? "s" : ""} in portfolio</p>
          </div>
        </div>
        <Button onClick={() => setShowCreate(true)}>
          <Plus className="w-4 h-4 mr-2" /> Add Trademark
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {["Registered", "Pending", "Expired", "Refused"].map((status) => (
          <Card key={status}>
            <CardContent className="pt-4">
              <p className="text-2xl font-bold">
                {trademarks.filter((t) => t.status === status).length}
              </p>
              <p className="text-sm text-slate-500">{status}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Search + Table */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-3">
            <Search className="w-4 h-4 text-slate-400" />
            <Input
              placeholder="Search by name or owner..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="max-w-sm"
            />
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <p className="text-sm text-slate-500 py-8 text-center">Loading portfolio...</p>
          ) : filtered.length === 0 ? (
            <p className="text-sm text-slate-500 py-8 text-center">
              No trademarks found. Add your first mark above.
            </p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Mark Name</TableHead>
                  <TableHead>Owner</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Jurisdiction</TableHead>
                  <TableHead>Classes</TableHead>
                  <TableHead>Filed</TableHead>
                  <TableHead></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filtered.map((tm) => (
                  <TableRow key={tm.id}>
                    <TableCell className="font-medium">{tm.name}</TableCell>
                    <TableCell>{tm.owner}</TableCell>
                    <TableCell>
                      <Badge variant={STATUS_COLORS[tm.status] as "default" | "secondary" | "destructive" | "outline" ?? "secondary"}>
                        {tm.status}
                      </Badge>
                    </TableCell>
                    <TableCell>{tm.jurisdiction}</TableCell>
                    <TableCell>
                      {tm.classes.map((c) => (
                        <Badge key={c.id} variant="outline" className="mr-1 text-xs">
                          Cl.{c.nice_class_number}
                        </Badge>
                      ))}
                    </TableCell>
                    <TableCell className="text-sm text-slate-500">
                      {tm.filing_date ? new Date(tm.filing_date).toLocaleDateString() : "—"}
                    </TableCell>
                    <TableCell>
                      <Link href={`/portfolio/${tm.id}`}>
                        <Button variant="ghost" size="sm">View</Button>
                      </Link>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Create Dialog */}
      <Dialog open={showCreate} onOpenChange={setShowCreate}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Trademark</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 mt-2">
            <div className="space-y-1">
              <label className="text-sm font-medium">Mark Name</label>
              <Input
                placeholder="e.g. NovaMark"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium">Owner</label>
              <Input
                placeholder="e.g. Acme Corp"
                value={form.owner}
                onChange={(e) => setForm({ ...form, owner: e.target.value })}
              />
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium">Jurisdiction</label>
              <select
                value={form.jurisdiction}
                onChange={(e) => setForm({ ...form, jurisdiction: e.target.value })}
                className="flex h-9 w-full rounded-md border border-slate-200 bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1"
              >
                {["US", "EU", "WO", "UK", "CA", "AU"].map((j) => (
                  <option key={j} value={j}>{j}</option>
                ))}
              </select>
            </div>
            <Button
              className="w-full"
              onClick={handleCreate}
              disabled={submitting || !form.name || !form.owner}
            >
              {submitting ? "Adding..." : "Add to Portfolio"}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
