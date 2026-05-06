"use client";

import { useState } from "react";
import { Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface TrademarkCheck {
  id: string;
  trademark_name: string;
  trademark_class: string;
  availability_status: string;
  similar_marks: string[];
  registration_likelihood: string;
  created_at: string
}

export default function Dashboard() {
  const [trademarkName, setTrademarkName] = useState("");
const [trademarkClass, setTrademarkClass] = useState("Class 9");
  const [trademarkCheck, setTrademarkCheck] = useState<TrademarkCheck | null>(null);
  const [extraData, setExtraData] = useState<any>(null);
const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    if (!trademarkName || !trademarkClass) return;
    setLoading(true);
    try {
      const res = await fetch("/checks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        trademarkName: trademarkName,
        trademark_class: trademarkClass,
        }),
      });
      const data = await res.json();
      setTrademarkCheck(data);
      const extraRes = await fetch(`/checks/${check_id}/watchlist`);
      const extraData = await extraRes.json();
      setExtraData(extraData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <div className="flex items-center gap-3">
        <Eye className="w-8 h-8" style={{ color: "#C026D3" }} />
        <div>
          <h1 className="text-2xl font-bold">DClaw Trademark</h1>
          <p className="text-sm text-slate-500">Trademark monitoring</p>
        </div>
        <Badge className="ml-auto" style={{ backgroundColor: "#C026D3" }}>Legal</Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Check Trademark</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Trademark name</label>
              <Input value={trademarkName} onChange={(e) => setTrademarkName(e.target.value)} placeholder="e.g. NovaSync" />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Class</label>
              <select value={trademarkClass} onChange={(e) => setTrademarkClass(e.target.value)} className="flex h-9 w-full rounded-md border border-slate-200 bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-brand">
                <option value="Class 9">Class 9</option><option value="Class 25">Class 25</option><option value="Class 35">Class 35</option><option value="Class 42">Class 42</option>
              </select>
            </div>
          </div>
          <Button onClick={handleSubmit} disabled={loading || !trademarkName || !trademarkClass}>
            {loading ? "Processing..." : "Check Trademark"}
          </Button>
        </CardContent>
      </Card>

      {trademarkCheck && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          <Card>
            <CardHeader>
              <CardTitle>Check Results</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p><strong>ID:</strong> {check.id}</p>
              <p><strong>Trademark:</strong> {check.trademark_name}</p>
              <p><strong>Class:</strong> {check.trademark_class}</p>
              <p><strong>Availability:</strong> {check.availability_status}</p>
              <p><strong>Registration Likelihood:</strong> {check.registration_likelihood}</p>
              <p><strong>Created:</strong> {new Date(check.created_at).toLocaleString()}</p>
            </CardContent>
          </Card>
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Similar Marks</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {check.similar_marks.map((item: string, i: number) => (
                  <Badge key={i} variant="secondary">{item}</Badge>
                ))}
              </div>
            </CardContent>
          </Card>
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Watchlist</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {extraData?.map((rec: any, i: number) => (
                  <div key={i} className="flex items-center justify-between p-2 bg-slate-50 rounded">
                    <span className="text-sm">{rec.mark}</span>
                    <Badge variant={rec.status === "Registered" ? "default" : "secondary"}>{rec.status}</Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
