const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const error = await response.text();
    throw new ApiError(`API error ${response.status}: ${error}`, response.status);
  }
  return response.json();
}

// ── Types ────────────────────────────────────────────────────────────────────

export interface TrademarkClass {
  id: string;
  trademark_id: string;
  nice_class_number: number;
  description: string | null;
  created_at: string;
}

export interface Trademark {
  id: string;
  name: string;
  owner: string;
  status: string;
  jurisdiction: string;
  application_number: string | null;
  registration_number: string | null;
  filing_date: string | null;
  registration_date: string | null;
  expiry_date: string | null;
  description: string | null;
  created_at: string;
  updated_at: string;
  classes: TrademarkClass[];
}

export interface TrademarkCreate {
  name: string;
  owner: string;
  status?: string;
  jurisdiction?: string;
  application_number?: string;
  registration_number?: string;
  filing_date?: string;
  registration_date?: string;
  expiry_date?: string;
  description?: string;
  classes?: { nice_class_number: number; description?: string }[];
}

export interface TrademarkUpdate {
  name?: string;
  owner?: string;
  status?: string;
  jurisdiction?: string;
  application_number?: string;
  registration_number?: string;
  filing_date?: string;
  registration_date?: string;
  expiry_date?: string;
  description?: string;
}

export interface TrademarkListResponse {
  items: Trademark[];
  total: number;
  limit: number;
  offset: number;
}

export interface WatchlistEntry {
  id: string;
  trademark_id: string;
  conflicting_mark_name: string;
  similarity_score: number | null;
  conflict_type: string;
  status: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface DeadlineAlert {
  id: string;
  trademark_id: string;
  deadline_type: string;
  due_date: string;
  status: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

// ── Trademark API ─────────────────────────────────────────────────────────────

export async function listTrademarks(
  limit = 20,
  offset = 0
): Promise<TrademarkListResponse> {
  return fetchJson(`/api/v1/trademarks/?limit=${limit}&offset=${offset}`);
}

export async function getTrademark(id: string): Promise<Trademark> {
  return fetchJson(`/api/v1/trademarks/${id}`);
}

export async function createTrademark(data: TrademarkCreate): Promise<Trademark> {
  return fetchJson("/api/v1/trademarks/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function updateTrademark(
  id: string,
  data: TrademarkUpdate
): Promise<Trademark> {
  return fetchJson(`/api/v1/trademarks/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export async function deleteTrademark(id: string): Promise<void> {
  const response = await fetch(`${API_BASE}/api/v1/trademarks/${id}`, {
    method: "DELETE",
  });
  if (!response.ok && response.status !== 204) {
    throw new ApiError(`Delete failed: ${response.status}`, response.status);
  }
}

// ── Watchlist API ─────────────────────────────────────────────────────────────

export async function listWatchlist(
  trademarkId: string
): Promise<{ items: WatchlistEntry[]; total: number }> {
  return fetchJson(`/api/v1/trademarks/${trademarkId}/watchlist`);
}

// ── Deadline API ──────────────────────────────────────────────────────────────

export async function listDeadlines(
  trademarkId: string
): Promise<{ items: DeadlineAlert[]; total: number }> {
  return fetchJson(`/api/v1/trademarks/${trademarkId}/deadlines`);
}

export async function upcomingDeadlines(
  days = 30
): Promise<{ items: DeadlineAlert[]; total: number }> {
  return fetchJson(`/api/v1/deadlines/upcoming?days=${days}`);
}

// ── Nice Classes API ──────────────────────────────────────────────────────────

export interface NiceClass {
  class_number: number;
  title: string;
  description: string;
  examples: string[];
}

export async function listNiceClasses(keyword = ""): Promise<NiceClass[]> {
  const qs = keyword ? `?keyword=${encodeURIComponent(keyword)}` : "";
  return fetchJson(`/api/v1/classes${qs}`);
}

export async function getNiceClass(classNumber: number): Promise<NiceClass> {
  return fetchJson(`/api/v1/classes/${classNumber}`);
}

// ── Search API ────────────────────────────────────────────────────────────────

export interface SearchResultItem {
  name: string;
  owner: string;
  jurisdiction: string;
  status: string;
  classes: number[];
  application_number: string;
  registration_date: string | null;
  phonetic_score: number;
  semantic_score: number;
  similarity_score: number;
  risk_level: "Low" | "Medium" | "High" | "Identical";
  conflict_type: string;
}

export interface SearchResponse {
  query: string;
  total: number;
  results: SearchResultItem[];
}

export async function runClearanceSearch(
  name: string,
  classes?: number[],
  jurisdiction?: string,
  minScore = 0.2
): Promise<SearchResponse> {
  return fetchJson("/api/v1/search", {
    method: "POST",
    body: JSON.stringify({ name, classes, jurisdiction, min_score: minScore }),
  });
}

// ── AI API ────────────────────────────────────────────────────────────────────

export interface ClassSuggestion {
  class_number: number;
  title: string;
  confidence: number;
  reasoning: string;
}

export async function suggestClasses(
  goodsServicesDescription: string
): Promise<{ description: string; suggestions: ClassSuggestion[] }> {
  return fetchJson("/api/v1/ai/suggest-classes", {
    method: "POST",
    body: JSON.stringify({ goods_services_description: goodsServicesDescription }),
  });
}

export interface CopilotAction {
  label: string;
  action: string;
}

export interface CopilotResponse {
  reply: string;
  suggested_actions: CopilotAction[];
}

export async function copilotChat(
  message: string,
  trademarkId?: string,
  trademarkContext?: string
): Promise<CopilotResponse> {
  return fetchJson("/api/v1/ai/copilot/chat", {
    method: "POST",
    body: JSON.stringify({
      message,
      trademark_id: trademarkId,
      trademark_context: trademarkContext,
    }),
  });
}

// ── Health ────────────────────────────────────────────────────────────────────

export async function getHealth() {
  return fetchJson<{ status: string }>("/health/");
}

export { ApiError };
