const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

export type DifficultyLevel = 
  | "BASIC" 
  | "MEDIUM" 
  | "HARD" 
  | "TOUGH" 
  | "VERY_TOUGH" 
  | "VERY_VERY_TOUGH" 
  | "PRODUCTION_SCENARIO" 
  | "EXPERT_DEEP_DIVE";

export interface QuestionCardData {
  id: string;
  slug: string;
  title: string;
  difficulty: DifficultyLevel | string;
  difficulty_score?: number;
  interview_depth: string;
  question_type: string;
  scenario_type?: string;
  estimated_time_minutes: number;
  role_target?: string;
  interview_round?: string;
  technology_name: string;
  technology_slug: string;
  topic_name?: string;
  tags?: Array<{ name: string; slug: string }>;
  view_count: number;
  upvote_count: number;
  status: string;
  created_at: string;
}

export interface TechnologyData {
  id: string;
  name: string;
  slug: string;
  short_description: string;
  icon: string;
  question_count: number;
  topics: Array<{ id: string; name: string; slug: string }>;
}

export interface QuestionDetailData {
  id: string;
  slug: string;
  title: string;
  difficulty: DifficultyLevel | string;
  difficulty_score?: number;
  interview_depth: string;
  question_type: string;
  scenario_type?: string;
  role_target: string;
  experience_level: string;
  interview_round?: string;
  estimated_time_minutes: number;
  short_answer: string;
  interview_ready_answer: string;
  deep_explanation: string;
  architecture_notes: string;
  code_example: string;
  why_interviewer_asks?: string;
  interviewer_intent: string;
  production_considerations?: string;
  failure_modes?: string;
  tradeoffs?: string;
  common_mistakes: string[];
  status: string;
  content_origin: string;
  technology_version?: string;
  technical_accuracy_score?: number;
  overall_quality_score?: number;
  view_count: number;
  upvote_count: number;
  technology_name: string;
  technology_slug: string;
  topic_name: string;
  is_bookmarked?: boolean;
  hints: Array<{
    id: string;
    hint_level: number;
    hint_type: string;
    content: string;
  }>;
  sources: Array<{
    source_name: string;
    source_url: string;
    publisher?: string;
    category?: string;
    license: string;
    attribution_required: number;
  }>;
  followups: Array<{
    id: string;
    followup_question: string;
    answer_guidance?: string;
  }>;
  tags: Array<{ name: string; slug: string }>;
}

export interface ReadingModeQuestion {
  id: string;
  slug: string;
  title: string;
  difficulty: string;
  difficulty_score?: number;
  interview_depth: string;
  question_type: string;
  scenario_type?: string;
  role_target?: string;
  experience_level?: string;
  interview_round?: string;
  estimated_time_minutes: number;
  short_answer?: string;
  interview_ready_answer: string;
  deep_explanation?: string;
  architecture_notes?: string;
  code_example?: string;
  why_interviewer_asks?: string;
  interviewer_intent?: string;
  production_considerations?: string;
  failure_modes?: string;
  tradeoffs?: string;
  common_mistakes?: string[];
  status: string;
  view_count: number;
  upvote_count: number;
  created_at: string;
  topic_name?: string;
  topic_slug?: string;
  hints?: Array<{
    id: string;
    hint_level: number;
    hint_type: string;
    content: string;
  }>;
  sources?: Array<{
    source_name: string;
    source_url: string;
    license?: string;
  }>;
  followups?: Array<{
    id: string;
    followup_question: string;
    answer_guidance?: string;
  }>;
  tags?: Array<{ name: string; slug: string }>;
}

export interface ReadingModeTier {
  tier: string;
  level_code: string;
  label: string;
  sub: string;
  experience_range: string;
  description: string;
  badge_color: string;
  count: number;
  questions: ReadingModeQuestion[];
}

export interface ReadingModeData {
  success?: boolean;
  technology: {
    id: string;
    name: string;
    slug: string;
    short_description: string;
    icon: string;
    question_count: number;
    topics: Array<{ id: string; name: string; slug: string }>;
    technology_version: string;
    last_reviewed_at: string;
  };
  summary: {
    total_questions: number;
    total_tiers: number;
    counts_by_tier: Record<string, number>;
  };
  tiers: ReadingModeTier[];
}

export interface AnswerEvaluationData {
  overall_score: number;
  correctness: { score: number; feedback: string };
  completeness: { score: number; feedback: string };
  technical_depth: { score: number; feedback: string };
  clarity: { score: number; feedback: string };
  covered_points: string[];
  missed_points: string[];
  improved_answer: string;
  actionable_advice: string;
}

export interface SocraticHintData {
  hint_level: number;
  hint_type: string;
  socratic_question: string;
  guiding_clue: string;
}

const DEFAULT_TECHNOLOGIES: TechnologyData[] = [
  {
    id: "tech-1",
    name: "LangGraph & Agentic AI",
    slug: "langgraph",
    short_description: "Stateful multi-agent systems, human-in-the-loop, and cyclic computational graphs.",
    icon: "Bot",
    question_count: 10,
    topics: [
      { id: "top-1", name: "State & Checkpointing", slug: "checkpointing" },
      { id: "top-2", name: "Multi-Agent Workflows", slug: "multi-agent" },
    ],
  },
  {
    id: "tech-2",
    name: "RAG & Vector Databases",
    slug: "rag-vector-db",
    short_description: "Hybrid search, embeddings, reranking, and semantic retrieval architectures.",
    icon: "Database",
    question_count: 8,
    topics: [{ id: "top-3", name: "Hybrid Retrieval & Reranking", slug: "hybrid-retrieval" }],
  },
  {
    id: "tech-3",
    name: "Java & JVM Concurrency",
    slug: "java-backend",
    short_description: "Core Java, Virtual Threads, memory model, GC algorithms, and Spring Boot microservices.",
    icon: "Coffee",
    question_count: 10,
    topics: [
      { id: "top-4", name: "Concurrency & Virtual Threads", slug: "concurrency" },
      { id: "top-5", name: "Spring Boot Transactions", slug: "spring-transactions" },
    ],
  },
  {
    id: "tech-4",
    name: "DSA & Algorithms",
    slug: "dsa",
    short_description: "Dynamic programming, graph algorithms, monotonic data structures, and algorithmic trade-offs.",
    icon: "Binary",
    question_count: 10,
    topics: [
      { id: "top-6", name: "Dynamic Programming", slug: "dynamic-programming" },
      { id: "top-7", name: "Graph Algorithms", slug: "graphs" },
    ],
  },
  {
    id: "tech-5",
    name: "System Design",
    slug: "system-design",
    short_description: "Distributed caching, message queues, rate limiting, and high-availability architecture.",
    icon: "Layers",
    question_count: 8,
    topics: [{ id: "top-8", name: "Distributed Caching", slug: "distributed-caching" }],
  },
];

// High-performance client/server memory cache with TTL to eliminate UI lag & network drag
const memoryCache = new Map<string, { timestamp: number; data: any }>();
const inFlightRequests = new Map<string, Promise<any>>();
const DEFAULT_CACHE_TTL_MS = 120 * 1000; // 120 seconds

export function getCachedData<T>(key: string, ttlMs: number = DEFAULT_CACHE_TTL_MS): T | null {
  const entry = memoryCache.get(key);
  if (!entry) return null;
  if (Date.now() - entry.timestamp > ttlMs) {
    memoryCache.delete(key);
    return null;
  }
  return entry.data as T;
}

export function setCachedData<T>(key: string, data: T): void {
  if (memoryCache.size > 200) {
    const oldest = memoryCache.keys().next().value;
    if (oldest) memoryCache.delete(oldest);
  }
  memoryCache.set(key, { timestamp: Date.now(), data });
}

/**
 * Deduplicates in-flight network requests so simultaneous callers share one promise.
 */
function dedupe<T>(key: string, fn: () => Promise<T>): Promise<T> {
  const existing = inFlightRequests.get(key);
  if (existing) return existing as Promise<T>;

  const promise = fn().finally(() => {
    inFlightRequests.delete(key);
  });
  inFlightRequests.set(key, promise);
  return promise;
}

export async function fetchTechnologies(): Promise<TechnologyData[]> {
  const cached = getCachedData<TechnologyData[]>("technologies", 180 * 1000);
  if (cached) return cached;

  return dedupe("technologies", async () => {
    try {
      const res = await fetch(`${API_BASE}/technologies`, { next: { revalidate: 120 } });
      if (!res.ok) throw new Error("Failed to load technologies");
      const json = await res.json();
      setCachedData("technologies", json);
      return json;
    } catch (error) {
      return DEFAULT_TECHNOLOGIES;
    }
  });
}

export async function fetchQuestions(params: {
  technology?: string;
  difficulty?: string;
  interview_depth?: string;
  question_type?: string;
  search?: string;
  page?: number;
  limit?: number;
} = {}): Promise<{ items: QuestionCardData[]; total: number; pages: number }> {
  const query = new URLSearchParams();
  if (params.technology) query.set("technology", params.technology);
  if (params.difficulty) query.set("difficulty", params.difficulty);
  if (params.interview_depth) query.set("interview_depth", params.interview_depth);
  if (params.question_type) query.set("question_type", params.question_type);
  if (params.search) query.set("search", params.search);
  if (params.page) query.set("page", params.page.toString());
  if (params.limit) query.set("limit", params.limit.toString());

  const cacheKey = `questions:${query.toString()}`;
  const cached = getCachedData<{ items: QuestionCardData[]; total: number; pages: number }>(cacheKey, 90 * 1000);
  if (cached) return cached;

  return dedupe(cacheKey, async () => {
    try {
      const res = await fetch(`${API_BASE}/questions?${query.toString()}`);
      if (!res.ok) throw new Error("Failed to load questions");
      const json = await res.json();
      const result = {
        items: json.items || [],
        total: json.total || 0,
        pages: json.pages || 1,
      };
      setCachedData(cacheKey, result);
      return result;
    } catch (error) {
      console.error("fetchQuestions error:", error);
      return { items: [], total: 0, pages: 1 };
    }
  });
}

export async function fetchQuestionBySlug(slug: string): Promise<QuestionDetailData | null> {
  const cacheKey = `question:${slug}`;
  const cached = getCachedData<QuestionDetailData>(cacheKey, 120 * 1000);
  if (cached) return cached;

  return dedupe(cacheKey, async () => {
    try {
      const res = await fetch(`${API_BASE}/questions/${slug}`);
      if (!res.ok) return null;
      const json = await res.json();
      if (json.data) {
        setCachedData(cacheKey, json.data);
      }
      return json.data;
    } catch (error) {
      console.error("fetchQuestionBySlug error:", error);
      return null;
    }
  });
}

export async function fetchReadingMode(technologySlug: string): Promise<ReadingModeData | null> {
  const cacheKey = `reading-mode:${technologySlug}`;
  const cached = getCachedData<ReadingModeData>(cacheKey, 180 * 1000);
  if (cached) return cached;

  return dedupe(cacheKey, async () => {
    try {
      const res = await fetch(`${API_BASE}/questions/reading-mode/${technologySlug}`);
      if (!res.ok) return null;
      const json = await res.json();
      setCachedData(cacheKey, json);
      return json;
    } catch (error) {
      console.error("fetchReadingMode error:", error);
      return null;
    }
  });
}

/** Pre-warms cache in memory without blocking UI */
export function prefetchQuestion(slug: string): void {
  fetchQuestionBySlug(slug).catch(() => {});
}

export function prefetchReadingModeTrack(techSlug: string): void {
  fetchReadingMode(techSlug).catch(() => {});
}

export async function toggleBookmarkApi(questionId: string, token: string): Promise<boolean> {
  const res = await fetch(`${API_BASE}/questions/${questionId}/bookmark`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });
  if (!res.ok) throw new Error("Bookmark request failed");
  const data = await res.json();
  return Boolean(data.bookmarked);
}

export async function evaluateAnswer(
  questionId: string,
  candidateAnswer: string,
  timeSpentSeconds: number = 0,
  token?: string | null
): Promise<AnswerEvaluationData & { xp_earned?: number; streak_days?: number; new_badges?: string[]; srs_interval_days?: number } | null> {
  try {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const res = await fetch(`${API_BASE}/ai/evaluate-answer`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        question_id: questionId,
        candidate_answer: candidateAnswer,
        time_spent_seconds: timeSpentSeconds,
      }),
    });
    if (!res.ok) throw new Error("Evaluation request failed");
    return await res.json();
  } catch (error) {
    console.error("evaluateAnswer error:", error);
    return null;
  }
}

export async function fetchSocraticHint(
  questionId: string,
  candidateThought?: string,
  hintLevel: number = 1
): Promise<SocraticHintData | null> {
  try {
    const res = await fetch(`${API_BASE}/ai/socratic-hint`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question_id: questionId,
        candidate_thought: candidateThought || null,
        hint_level: hintLevel,
      }),
    });
    if (!res.ok) throw new Error("Hint request failed");
    return await res.json();
  } catch (error) {
    console.error("fetchSocraticHint error:", error);
    return null;
  }
}

export async function fetchUserDashboard(token?: string): Promise<any> {
  if (!token) return null;
  try {
    const res = await fetch(`${API_BASE}/users/dashboard`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to load user dashboard");
    return await res.json();
  } catch (error) {
    console.error("fetchUserDashboard error:", error);
    return null;
  }
}

export async function fetchUserBookmarks(token: string): Promise<any[]> {
  try {
    const res = await fetch(`${API_BASE}/users/bookmarks`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) return [];
    const data = await res.json();
    return data.items || [];
  } catch (error) {
    console.error("fetchUserBookmarks error:", error);
    return [];
  }
}

export async function toggleBookmark(token: string, questionId: string): Promise<boolean | null> {
  try {
    const res = await fetch(`${API_BASE}/questions/${questionId}/bookmark`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) return null;
    const data = await res.json();
    return data.bookmarked;
  } catch (error) {
    console.error("toggleBookmark error:", error);
    return null;
  }
}

export async function fetchUserHistory(token: string, page: number = 1, limit: number = 20): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/users/history?page=${page}&limit=${limit}`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) return { items: [], total: 0 };
    return await res.json();
  } catch (error) {
    console.error("fetchUserHistory error:", error);
    return { items: [], total: 0 };
  }
}

export async function fetchRevisionQueue(token: string): Promise<{ items: any[]; total: number; due_count: number }> {
  try {
    const res = await fetch(`${API_BASE}/users/revision`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) return { items: [], total: 0, due_count: 0 };
    return await res.json();
  } catch (error) {
    console.error("fetchRevisionQueue error:", error);
    return { items: [], total: 0, due_count: 0 };
  }
}

export async function submitRevisionReview(token: string, questionId: string, grade: number): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/users/revision/${questionId}/review`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ grade }),
    });
    if (!res.ok) throw new Error("Failed to record review");
    return await res.json();
  } catch (error) {
    console.error("submitRevisionReview error:", error);
    return null;
  }
}

export async function fetchUserBadges(token: string): Promise<{ badges: any[]; unlocked_count: number; total_badges: number }> {
  try {
    const res = await fetch(`${API_BASE}/users/badges`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) return { badges: [], unlocked_count: 0, total_badges: 0 };
    return await res.json();
  } catch (error) {
    console.error("fetchUserBadges error:", error);
    return { badges: [], unlocked_count: 0, total_badges: 0 };
  }
}

export async function fetchDailyChallenge(token: string): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/users/daily-challenge`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) return null;
    const data = await res.json();
    return data.challenge;
  } catch (error) {
    console.error("fetchDailyChallenge error:", error);
    return null;
  }
}

export async function fetchAdminAnalytics(token: string): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/admin/analytics`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error("Admin request failed");
    return await res.json();
  } catch (error) {
    console.error("fetchAdminAnalytics error:", error);
    return null;
  }
}

export async function fetchQuestionStats(): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/questions/stats`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to load question stats");
    return await res.json();
  } catch (error) {
    console.error("fetchQuestionStats error:", error);
    return null;
  }
}

export const fetchGlobalStats = fetchQuestionStats;

export async function fetchCoverageMatrix(): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/admin/content/matrix`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to load coverage matrix");
    return await res.json();
  } catch (error) {
    console.error("fetchCoverageMatrix error:", error);
    return null;
  }
}

export async function fetchContentSources(): Promise<any[]> {
  try {
    const res = await fetch(`${API_BASE}/admin/content/sources`, { cache: "no-store" });
    if (!res.ok) return [];
    const data = await res.json();
    return data.items || [];
  } catch (error) {
    console.error("fetchContentSources error:", error);
    return [];
  }
}

export interface AdminQuestionsResponse {
  success: boolean;
  total: number;
  counts: {
    total: number;
    published: number;
    draft: number;
    in_review: number;
    approved: number;
    archived: number;
    filtered: number;
  };
  page: number;
  limit: number;
  questions: any[];
}

export async function fetchAdminQuestions(
  params: {
    status?: string;
    technology?: string;
    difficulty?: string;
    q?: string;
    page?: number;
    limit?: number;
  },
  token?: string
): Promise<AdminQuestionsResponse> {
  const query = new URLSearchParams();
  if (params.status && params.status !== "ALL") query.append("status", params.status);
  if (params.technology && params.technology !== "ALL") query.append("technology", params.technology);
  if (params.difficulty && params.difficulty !== "ALL") query.append("difficulty", params.difficulty);
  if (params.q) query.append("q", params.q);
  if (params.page) query.append("page", params.page.toString());
  if (params.limit) query.append("limit", params.limit.toString());

  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}/admin/questions?${query.toString()}`, {
    headers,
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to load admin questions: ${res.statusText}`);
  }
  return await res.json();
}

export async function fetchAdminQuestionDetail(id: string, token?: string): Promise<any> {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}/admin/questions/${id}`, {
    headers,
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Failed to load question details: ${res.statusText}`);
  }
  const data = await res.json();
  return data.question;
}

export async function createAdminQuestion(payload: any, token?: string): Promise<any> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}/admin/questions`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to create question: ${res.statusText}`);
  }
  return await res.json();
}

export async function updateAdminQuestion(id: string, payload: any, token?: string): Promise<any> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}/admin/questions/${id}`, {
    method: "PUT",
    headers,
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to update question: ${res.statusText}`);
  }
  return await res.json();
}

export async function updateAdminQuestionStatus(
  id: string,
  status: string,
  note?: string,
  token?: string
): Promise<any> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}/admin/questions/${id}/status`, {
    method: "PATCH",
    headers,
    body: JSON.stringify({ status, note }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to update question status: ${res.statusText}`);
  }
  return await res.json();
}

export async function deleteAdminQuestion(id: string, token?: string): Promise<any> {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}/admin/questions/${id}`, {
    method: "DELETE",
    headers,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to delete question: ${res.statusText}`);
  }
  return await res.json();
}


