"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { runClearanceSearch, type SearchResultItem } from "@/lib/api";

const RISK_COLORS: Record<string, string> = {
  Identical: "destructive",
  High: "destructive",
  Medium: "secondary",
  Low: "outline",
};

const JURISDICTIONS = ["", "US", "EU", "WO", "UK", "AU", "CA"];

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [jurisdiction, setJurisdiction] = useState("");
  const [results, setResults] = useState<SearchResultItem[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState(false);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const resp = await runClearanceSearch(
        query,
        undefined,
        jurisdiction || undefined
      );
      setResults(resp.results);
      setSearched(true);
    } catch {
      setError("Search failed. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Trademark Clearance Search
        </h1>
        <p className="text-gray-600">
          Check if your proposed mark conflicts with existing registrations.
        </p>
      </div>

      <Card className="mb-8">
        <CardContent className="pt-6">
          <form onSubmit={handleSearch} className="flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <Label htmlFor="query">Mark Name</Label>
              <Input
                id="query"
                placeholder="e.g. NovaMark"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                required
              />
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="jurisdiction">Jurisdiction (optional)</Label>
              <Select
                id="jurisdiction"
                value={jurisdiction}
                onChange={(e) => setJurisdiction(e.target.value)}
              >
                {JURISDICTIONS.map((j) => (
                  <option key={j} value={j}>
                    {j || "All jurisdictions"}
                  </option>
                ))}
              </Select>
            </div>
            <Button type="submit" disabled={loading || !query.trim()}>
              {loading ? "Searching…" : "Search"}
            </Button>
          </form>
        </CardContent>
      </Card>

      {error && (
        <div className="rounded-md bg-red-50 border border-red-200 p-4 text-red-700 mb-6">
          {error}
        </div>
      )}

      {searched && results !== null && (
        <div>
          <h2 className="text-xl font-semibold mb-4">
            {results.length === 0
              ? "No conflicts found"
              : `${results.length} potential conflict${results.length !== 1 ? "s" : ""} found`}
          </h2>
          <div className="flex flex-col gap-4">
            {results.map((item, i) => (
              <Card key={i}>
                <CardHeader className="pb-2">
                  <div className="flex items-start justify-between gap-2">
                    <CardTitle className="text-lg">{item.name}</CardTitle>
                    <Badge variant={RISK_COLORS[item.risk_level] as "destructive" | "secondary" | "outline" | "default"}>
                      {item.risk_level} Risk
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-500">
                    {item.owner} · {item.jurisdiction} · {item.status}
                  </p>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-500">Similarity Score</p>
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-indigo-500 h-2 rounded-full"
                            style={{ width: `${Math.round(item.similarity_score * 100)}%` }}
                          />
                        </div>
                        <span className="font-medium text-gray-700">
                          {Math.round(item.similarity_score * 100)}%
                        </span>
                      </div>
                    </div>
                    <div>
                      <p className="text-gray-500">Conflict Type</p>
                      <p className="font-medium mt-1">{item.conflict_type}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Application No.</p>
                      <p className="font-mono text-xs mt-1">{item.application_number}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Nice Classes</p>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {item.classes.map((c) => (
                          <span
                            key={c}
                            className="inline-flex items-center rounded bg-indigo-100 text-indigo-800 text-xs px-1.5 py-0.5"
                          >
                            Class {c}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                  <div className="mt-3 flex gap-4 text-xs text-gray-500">
                    <span>Phonetic: {Math.round(item.phonetic_score * 100)}%</span>
                    <span>Semantic: {Math.round(item.semantic_score * 100)}%</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
