"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import {
  ShieldCheck,
  Plus,
  CheckCircle2,
  Clock,
  Filter,
  Eye,
  AlertCircle,
  Layers,
  Search,
  Edit2,
  Trash2,
  X,
  ChevronDown,
  Sparkles,
  RefreshCw,
  ExternalLink,
  FileText,
  Code,
  Check,
  Tag,
  ArrowRight,
  BookOpen,
  Info,
  Archive,
  Send,
  SlidersHorizontal,
  ChevronRight,
  UserCheck
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import {
  fetchAdminQuestions,
  fetchAdminQuestionDetail,
  updateAdminQuestion,
  updateAdminQuestionStatus,
  deleteAdminQuestion,
  createAdminQuestion,
  fetchTechnologies,
  TechnologyData,
  AdminQuestionsResponse
} from "@/lib/api";
import { DifficultyBadge, InterviewDepthBadge, Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const STATUS_CONFIG: Record<
  string,
  { label: string; badgeClass: string; dotClass: string }
> = {
  PUBLISHED: {
    label: "Published",
    badgeClass: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    dotClass: "bg-emerald-400",
  },
  DRAFT: {
    label: "Draft",
    badgeClass: "bg-zinc-500/10 text-zinc-400 border-zinc-500/30",
    dotClass: "bg-zinc-400",
  },
  AI_REVIEW: {
    label: "AI Review",
    badgeClass: "bg-purple-500/15 text-purple-400 border-purple-500/30",
    dotClass: "bg-purple-400",
  },
  TECHNICAL_REVIEW: {
    label: "Technical Review",
    badgeClass: "bg-amber-500/15 text-amber-400 border-amber-500/30",
    dotClass: "bg-amber-400",
  },
  APPROVED: {
    label: "Approved",
    badgeClass: "bg-sky-500/15 text-sky-400 border-sky-500/30",
    dotClass: "bg-sky-400",
  },
  ARCHIVED: {
    label: "Archived",
    badgeClass: "bg-rose-500/10 text-rose-400 border-rose-500/30",
    dotClass: "bg-rose-400",
  },
};

const DIFFICULTY_OPTIONS = [
  "ALL",
  "BASIC",
  "MEDIUM",
  "HARD",
  "TOUGH",
  "VERY_TOUGH",
  "VERY_VERY_TOUGH",
  "PRODUCTION_SCENARIO",
  "EXPERT_DEEP_DIVE",
];

const DEPTH_OPTIONS = ["L1", "L2", "L3", "L4", "L5"];
const QUESTION_TYPES = ["CONCEPTUAL", "ARCHITECTURE", "SCENARIO", "ALGORITHM", "SYSTEM_DESIGN"];
const STATUS_OPTIONS = ["ALL", "PUBLISHED", "DRAFT", "AI_REVIEW", "TECHNICAL_REVIEW", "APPROVED", "ARCHIVED"];

export default function AdminQuestionsPage() {
  const { user: currentUser, token, isLoading: authLoading, loginAsDemo } = useAuth();

  // Data states
  const [questions, setQuestions] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [counts, setCounts] = useState({
    total: 0,
    published: 0,
    draft: 0,
    in_review: 0,
    approved: 0,
    archived: 0,
    filtered: 0,
  });
  const [technologies, setTechnologies] = useState<TechnologyData[]>([]);
  const [loading, setLoading] = useState(true);

  // Filter states
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [techFilter, setTechFilter] = useState("ALL");
  const [diffFilter, setDiffFilter] = useState("ALL");

  // Notifications
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);

  // Modals state
  const [viewQuestion, setViewQuestion] = useState<any | null>(null);
  const [viewLoading, setViewLoading] = useState(false);

  const [editQuestion, setEditQuestion] = useState<any | null>(null);
  const [editTab, setEditTab] = useState<"core" | "answers" | "architecture" | "hints">("core");
  const [isSaving, setIsSaving] = useState(false);

  const [deleteQuestionTarget, setDeleteQuestionTarget] = useState<any | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  // Status dropdown toggle for rows
  const [statusDropdownOpenId, setStatusDropdownOpenId] = useState<string | null>(null);

  // Form state for Edit / Create Modal
  const [formData, setFormData] = useState({
    id: "",
    title: "",
    slug: "",
    technology_id: "",
    topic_id: "",
    difficulty: "MEDIUM",
    interview_depth: "L2",
    question_type: "CONCEPTUAL",
    role_target: "Software Engineer",
    experience_level: "Mid",
    estimated_time_minutes: 5,
    status: "PUBLISHED",
    short_answer: "",
    interview_ready_answer: "",
    deep_explanation: "",
    architecture_notes: "",
    code_example: "",
    why_interviewer_asks: "",
    interviewer_intent: "",
    common_mistakes: "",
    hint1: "",
    hint2: "",
    hint3: "",
    source_name: "Official Framework Documentation",
    source_url: "https://breakthecode.dev",
  });

  const showToast = (message: string, type: "success" | "error" = "success") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  // Load technologies
  useEffect(() => {
    fetchTechnologies().then((techs) => {
      setTechnologies(techs);
    });
  }, []);

  // Fetch Questions
  const loadQuestions = async () => {
    setLoading(true);
    try {
      const data: AdminQuestionsResponse = await fetchAdminQuestions(
        {
          status: statusFilter !== "ALL" ? statusFilter : undefined,
          technology: techFilter !== "ALL" ? techFilter : undefined,
          difficulty: diffFilter !== "ALL" ? diffFilter : undefined,
          q: searchQuery.trim() || undefined,
          limit: 100,
        },
        token || undefined
      );
      setQuestions(data.questions || []);
      setTotal(data.total || 0);
      if (data.counts) {
        setCounts(data.counts);
      }
    } catch (err: any) {
      console.error(err);
      showToast(err.message || "Failed to load questions", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadQuestions();
  }, [statusFilter, techFilter, diffFilter, token]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadQuestions();
  };

  // Single-click status transition
  const handleStatusTransition = async (questionId: string, newStatus: string, title: string) => {
    try {
      setStatusDropdownOpenId(null);
      await updateAdminQuestionStatus(questionId, newStatus, undefined, token || undefined);
      showToast(`Status updated: '${title}' is now ${newStatus}`);
      loadQuestions();
      if (viewQuestion && viewQuestion.id === questionId) {
        setViewQuestion({ ...viewQuestion, status: newStatus });
      }
    } catch (err: any) {
      showToast(err.message || "Failed to update status", "error");
    }
  };

  // Open Full Detail Modal
  const handleOpenView = async (q: any) => {
    setViewLoading(true);
    setViewQuestion(q);
    try {
      const detail = await fetchAdminQuestionDetail(q.id, token || undefined);
      setViewQuestion(detail);
    } catch (err) {
      console.error("Failed to load deep question details, using row data", err);
    } finally {
      setViewLoading(false);
    }
  };

  // Open Edit Modal
  const handleOpenEdit = async (q: any) => {
    let fullQ = q;
    try {
      fullQ = await fetchAdminQuestionDetail(q.id, token || undefined);
    } catch (e) {
      console.warn("Could not fetch full details, fallback to list item", e);
    }

    setFormData({
      id: fullQ.id,
      title: fullQ.title || "",
      slug: fullQ.slug || "",
      technology_id: fullQ.technology_id || (technologies[0]?.id ?? ""),
      topic_id: fullQ.topic_id || "",
      difficulty: fullQ.difficulty || "MEDIUM",
      interview_depth: fullQ.interview_depth || "L2",
      question_type: fullQ.question_type || "CONCEPTUAL",
      role_target: fullQ.role_target || "Software Engineer",
      experience_level: fullQ.experience_level || "Mid",
      estimated_time_minutes: fullQ.estimated_time_minutes || 5,
      status: fullQ.status || "PUBLISHED",
      short_answer: fullQ.short_answer || "",
      interview_ready_answer: fullQ.interview_ready_answer || "",
      deep_explanation: fullQ.deep_explanation || "",
      architecture_notes: fullQ.architecture_notes || "",
      code_example: fullQ.code_example || "",
      why_interviewer_asks: fullQ.why_interviewer_asks || "",
      interviewer_intent: fullQ.interviewer_intent || "",
      common_mistakes: Array.isArray(fullQ.common_mistakes)
        ? fullQ.common_mistakes.join("\n")
        : typeof fullQ.common_mistakes === "string"
        ? fullQ.common_mistakes
        : "",
      hint1: fullQ.hints?.[0]?.content || "",
      hint2: fullQ.hints?.[1]?.content || "",
      hint3: fullQ.hints?.[2]?.content || "",
      source_name: fullQ.sources?.[0]?.source_name || "Official Framework Documentation",
      source_url: fullQ.sources?.[0]?.source_url || "https://breakthecode.dev",
    });

    setEditTab("core");
    setEditQuestion(fullQ);
  };

  // Save Edit Form
  const handleSaveEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editQuestion) return;
    setIsSaving(true);

    const payload = {
      title: formData.title,
      slug: formData.slug || undefined,
      technology_id: formData.technology_id,
      topic_id: formData.topic_id || null,
      difficulty: formData.difficulty,
      interview_depth: formData.interview_depth,
      question_type: formData.question_type,
      role_target: formData.role_target,
      experience_level: formData.experience_level,
      estimated_time_minutes: Number(formData.estimated_time_minutes),
      status: formData.status,
      short_answer: formData.short_answer || null,
      interview_ready_answer: formData.interview_ready_answer,
      deep_explanation: formData.deep_explanation || null,
      architecture_notes: formData.architecture_notes || null,
      code_example: formData.code_example || null,
      why_interviewer_asks: formData.why_interviewer_asks || null,
      interviewer_intent: formData.interviewer_intent || null,
      common_mistakes: formData.common_mistakes
        .split("\n")
        .map((s) => s.trim())
        .filter(Boolean),
      hints: [
        { hint_level: 1, hint_type: "CONCEPTUAL", content: formData.hint1 || "Focus on the foundational mechanic." },
        { hint_level: 2, hint_type: "IMPLEMENTATION", content: formData.hint2 || "Consider runtime execution and constraints." },
        { hint_level: 3, hint_type: "ARCHITECTURE", content: formData.hint3 || "Analyze tradeoffs and distributed scenarios." },
      ],
      sources: [
        {
          source_name: formData.source_name || "Official Documentation",
          source_url: formData.source_url || "https://breakthecode.dev",
          license: "Attribution",
          attribution_required: 1,
        },
      ],
    };

    try {
      await updateAdminQuestion(editQuestion.id, payload, token || undefined);
      showToast(`Question '${formData.title}' updated successfully`);
      setEditQuestion(null);
      loadQuestions();
    } catch (err: any) {
      showToast(err.message || "Failed to update question", "error");
    } finally {
      setIsSaving(false);
    }
  };

  // Delete Question
  const handleDeleteConfirm = async () => {
    if (!deleteQuestionTarget) return;
    setIsDeleting(true);
    try {
      await deleteAdminQuestion(deleteQuestionTarget.id, token || undefined);
      showToast(`Question '${deleteQuestionTarget.title}' deleted successfully`);
      setDeleteQuestionTarget(null);
      if (viewQuestion && viewQuestion.id === deleteQuestionTarget.id) {
        setViewQuestion(null);
      }
      loadQuestions();
    } catch (err: any) {
      showToast(err.message || "Failed to delete question", "error");
    } finally {
      setIsDeleting(false);
    }
  };

  // Find topics for currently selected technology in edit form
  const selectedTechTopics = useMemo(() => {
    const tech = technologies.find((t) => t.id === formData.technology_id);
    return tech?.topics || [];
  }, [technologies, formData.technology_id]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8 animate-fade-in">
      {/* Toast Notification */}
      {toast && (
        <div
          className={`fixed bottom-6 right-6 z-50 p-4 rounded-xl shadow-2xl border flex items-center gap-3 backdrop-blur-md animate-slide-up ${
            toast.type === "success"
              ? "bg-emerald-950/90 text-emerald-200 border-emerald-500/40"
              : "bg-rose-950/90 text-rose-200 border-rose-500/40"
          }`}
        >
          {toast.type === "success" ? (
            <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0" />
          ) : (
            <AlertCircle className="h-5 w-5 text-rose-400 shrink-0" />
          )}
          <span className="text-sm font-medium">{toast.message}</span>
          <button
            onClick={() => setToast(null)}
            className="ml-2 text-muted-foreground hover:text-foreground"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      )}

      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-border/70">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-primary">
            <ShieldCheck className="h-4 w-4" />
            <span>Admin Governance CMS</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-foreground">
            Content Review & Question Lifecycle
          </h1>
          <p className="text-xs text-muted-foreground">
            Complete question CRUD operations, 15-part answer DNA curation, and gated publishing workflow.
          </p>
        </div>

        <div className="flex items-center gap-2.5 flex-wrap">
          <Button
            variant="outline"
            size="md"
            onClick={loadQuestions}
            disabled={loading}
            title="Refresh questions"
          >
            <RefreshCw className={`h-4 w-4 mr-1.5 ${loading ? "animate-spin" : ""}`} />
            <span>Sync</span>
          </Button>
          <Link href="/admin/coverage">
            <Button variant="outline" size="md">
              <Layers className="h-4 w-4 mr-1.5 text-primary" />
              <span>Coverage Matrix</span>
            </Button>
          </Link>
          <Link href="/admin/questions/new">
            <Button variant="primary" size="md">
              <Plus className="h-4 w-4 mr-1.5" />
              <span>New Question</span>
            </Button>
          </Link>
        </div>
      </div>

      {/* Summary Metrics Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-6 gap-3.5">
        <div
          onClick={() => setStatusFilter("ALL")}
          className={`p-4 rounded-xl bg-card border cursor-pointer transition-all hover:border-primary/50 ${
            statusFilter === "ALL" ? "border-primary ring-1 ring-primary/30" : "border-border/70"
          }`}
        >
          <span className="text-[11px] font-semibold text-muted-foreground uppercase block">Total Library</span>
          <p className="text-2xl font-bold text-foreground mt-1">{counts.total}</p>
        </div>

        <div
          onClick={() => setStatusFilter("PUBLISHED")}
          className={`p-4 rounded-xl bg-card border cursor-pointer transition-all hover:border-emerald-500/50 ${
            statusFilter === "PUBLISHED"
              ? "border-emerald-500 ring-1 ring-emerald-500/30"
              : "border-border/70"
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-emerald-500 uppercase">Live Published</span>
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
          </div>
          <p className="text-2xl font-bold text-emerald-500 mt-1">{counts.published}</p>
        </div>

        <div
          onClick={() => setStatusFilter("TECHNICAL_REVIEW")}
          className={`p-4 rounded-xl bg-card border cursor-pointer transition-all hover:border-amber-500/50 ${
            statusFilter === "TECHNICAL_REVIEW"
              ? "border-amber-500 ring-1 ring-amber-500/30"
              : "border-border/70"
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-amber-500 uppercase">In Review</span>
            <span className="h-2 w-2 rounded-full bg-amber-500" />
          </div>
          <p className="text-2xl font-bold text-amber-500 mt-1">{counts.in_review}</p>
        </div>

        <div
          onClick={() => setStatusFilter("DRAFT")}
          className={`p-4 rounded-xl bg-card border cursor-pointer transition-all hover:border-zinc-500/50 ${
            statusFilter === "DRAFT" ? "border-zinc-500 ring-1 ring-zinc-500/30" : "border-border/70"
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-zinc-400 uppercase">Drafts</span>
            <span className="h-2 w-2 rounded-full bg-zinc-400" />
          </div>
          <p className="text-2xl font-bold text-zinc-300 mt-1">{counts.draft}</p>
        </div>

        <div
          onClick={() => setStatusFilter("APPROVED")}
          className={`p-4 rounded-xl bg-card border cursor-pointer transition-all hover:border-sky-500/50 ${
            statusFilter === "APPROVED" ? "border-sky-500 ring-1 ring-sky-500/30" : "border-border/70"
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-sky-400 uppercase">Approved</span>
            <span className="h-2 w-2 rounded-full bg-sky-400" />
          </div>
          <p className="text-2xl font-bold text-sky-400 mt-1">{counts.approved}</p>
        </div>

        <div
          onClick={() => setStatusFilter("ARCHIVED")}
          className={`p-4 rounded-xl bg-card border cursor-pointer transition-all hover:border-rose-500/50 ${
            statusFilter === "ARCHIVED" ? "border-rose-500 ring-1 ring-rose-500/30" : "border-border/70"
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-rose-400 uppercase">Archived</span>
            <span className="h-2 w-2 rounded-full bg-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400 mt-1">{counts.archived}</p>
        </div>
      </div>

      {/* Control Filters Bar */}
      <div className="p-4 rounded-2xl border border-border/80 bg-card space-y-4 shadow-sm">
        <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by title, answer excerpt, or slug... (Press Enter)"
              className="w-full h-10 pl-10 pr-10 rounded-xl bg-muted/40 border border-border/70 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => {
                  setSearchQuery("");
                  setTimeout(loadQuestions, 50);
                }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>

          <Button type="submit" variant="primary" size="md">
            <span>Filter</span>
          </Button>
        </form>

        <div className="flex flex-wrap items-center gap-3 pt-2 border-t border-border/50 text-xs">
          <div className="flex items-center gap-1.5 text-muted-foreground font-medium">
            <SlidersHorizontal className="h-3.5 w-3.5" />
            <span>Filters:</span>
          </div>

          {/* Status Selector */}
          <div className="flex items-center gap-1">
            <span className="text-muted-foreground">Status:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="h-8 px-2.5 rounded-lg bg-muted/60 border border-border/70 text-xs font-semibold text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            >
              <option value="ALL">All Statuses ({counts.total})</option>
              <option value="PUBLISHED">Published ({counts.published})</option>
              <option value="TECHNICAL_REVIEW">Technical Review</option>
              <option value="AI_REVIEW">AI Review</option>
              <option value="APPROVED">Approved ({counts.approved})</option>
              <option value="DRAFT">Drafts ({counts.draft})</option>
              <option value="ARCHIVED">Archived ({counts.archived})</option>
            </select>
          </div>

          {/* Technology Selector */}
          <div className="flex items-center gap-1">
            <span className="text-muted-foreground">Technology:</span>
            <select
              value={techFilter}
              onChange={(e) => setTechFilter(e.target.value)}
              className="h-8 px-2.5 rounded-lg bg-muted/60 border border-border/70 text-xs font-semibold text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            >
              <option value="ALL">All Technologies</option>
              {technologies.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </select>
          </div>

          {/* Difficulty Selector */}
          <div className="flex items-center gap-1">
            <span className="text-muted-foreground">Difficulty:</span>
            <select
              value={diffFilter}
              onChange={(e) => setDiffFilter(e.target.value)}
              className="h-8 px-2.5 rounded-lg bg-muted/60 border border-border/70 text-xs font-semibold text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            >
              {DIFFICULTY_OPTIONS.map((diff) => (
                <option key={diff} value={diff}>
                  {diff === "ALL" ? "All Difficulties" : diff.replace(/_/g, " ")}
                </option>
              ))}
            </select>
          </div>

          {(statusFilter !== "ALL" || techFilter !== "ALL" || diffFilter !== "ALL" || searchQuery) && (
            <button
              onClick={() => {
                setStatusFilter("ALL");
                setTechFilter("ALL");
                setDiffFilter("ALL");
                setSearchQuery("");
              }}
              className="text-primary hover:underline font-semibold ml-auto"
            >
              Reset Filters
            </button>
          )}
        </div>
      </div>

      {/* Questions Data Table */}
      <div className="rounded-2xl border border-border/80 bg-card overflow-hidden shadow-sm">
        <div className="p-4 bg-muted/40 border-b border-border/70 flex items-center justify-between text-xs font-semibold text-muted-foreground uppercase tracking-wider">
          <span>Question Title & Taxonomy ({questions.length} displayed)</span>
          <span className="hidden md:inline">Tier & Depth</span>
          <span>Status & CRUD Actions</span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-muted-foreground space-y-3">
            <RefreshCw className="h-6 w-6 animate-spin mx-auto text-primary" />
            <p className="text-sm font-medium">Loading interview questions database...</p>
          </div>
        ) : questions.length === 0 ? (
          <div className="p-12 text-center text-muted-foreground space-y-3">
            <BookOpen className="h-8 w-8 mx-auto text-muted-foreground/60" />
            <p className="text-sm font-semibold text-foreground">No questions match the current filters</p>
            <p className="text-xs">Try adjusting your search criteria or create a new question.</p>
            <Link href="/admin/questions/new">
              <Button variant="primary" size="sm" className="mt-2">
                <Plus className="h-3.5 w-3.5 mr-1" />
                <span>Author Question</span>
              </Button>
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-border/60">
            {questions.map((q) => {
              const statusCfg = STATUS_CONFIG[q.status] || {
                label: q.status,
                badgeClass: "bg-muted text-foreground border-border",
                dotClass: "bg-foreground",
              };

              return (
                <div
                  key={q.id}
                  className="p-4 sm:p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-4 hover:bg-muted/20 transition-colors group"
                >
                  {/* Left Column: Title & Metadata */}
                  <div className="space-y-1.5 flex-1 min-w-0">
                    <div className="flex items-center gap-2 text-xs flex-wrap">
                      <span className="font-semibold text-primary">{q.technology_name}</span>
                      {q.topic_name && (
                        <>
                          <span className="text-muted-foreground">•</span>
                          <span className="text-muted-foreground">{q.topic_name}</span>
                        </>
                      )}
                      <span className="text-muted-foreground">•</span>
                      <span className="text-[11px] text-muted-foreground">
                        {q.question_type || "CONCEPTUAL"}
                      </span>
                      {q.estimated_time_minutes && (
                        <span className="text-[11px] text-muted-foreground flex items-center gap-1">
                          <Clock className="h-3 w-3 inline" /> {q.estimated_time_minutes}m
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleOpenView(q)}
                        className="font-bold text-sm sm:text-base text-foreground hover:text-primary transition-colors text-left block truncate"
                        title="Click to view question DNA"
                      >
                        {q.title}
                      </button>
                    </div>

                    <div className="text-[11px] text-muted-foreground flex items-center gap-3 flex-wrap">
                      <span className="font-mono text-[10px] text-muted-foreground/80">/{q.slug}</span>
                      <span>Views: {q.view_count || 0}</span>
                      {q.created_at && (
                        <span>Added: {new Date(q.created_at).toLocaleDateString()}</span>
                      )}
                    </div>
                  </div>

                  {/* Middle Column: Difficulty & Depth */}
                  <div className="flex items-center gap-2 shrink-0">
                    <DifficultyBadge difficulty={q.difficulty} />
                    <InterviewDepthBadge depth={q.interview_depth} />
                  </div>

                  {/* Right Column: Status & Action Buttons */}
                  <div className="flex items-center gap-2 shrink-0 flex-wrap justify-between lg:justify-end">
                    {/* Status Badge + Dropdown Trigger */}
                    <div className="relative">
                      <button
                        onClick={() =>
                          setStatusDropdownOpenId(statusDropdownOpenId === q.id ? null : q.id)
                        }
                        className={`text-xs px-2.5 py-1 rounded-full font-semibold border flex items-center gap-1.5 transition-all hover:scale-105 ${statusCfg.badgeClass}`}
                        title="Click to transition lifecycle status"
                      >
                        <span className={`h-1.5 w-1.5 rounded-full ${statusCfg.dotClass}`} />
                        <span>{statusCfg.label}</span>
                        <ChevronDown className="h-3 w-3 opacity-70" />
                      </button>

                      {/* Dropdown Menu */}
                      {statusDropdownOpenId === q.id && (
                        <div className="absolute right-0 mt-2 w-48 rounded-xl bg-card border border-border/80 shadow-xl py-1 z-30 animate-fade-in divide-y divide-border/40">
                          <div className="px-3 py-1.5 text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">
                            Transition Status
                          </div>
                          <div className="py-1">
                            {["PUBLISHED", "APPROVED", "TECHNICAL_REVIEW", "AI_REVIEW", "DRAFT", "ARCHIVED"].map(
                              (st) => (
                                <button
                                  key={st}
                                  onClick={() => handleStatusTransition(q.id, st, q.title)}
                                  className={`w-full text-left px-3 py-1.5 text-xs flex items-center justify-between hover:bg-muted transition-colors ${
                                    q.status === st ? "font-bold text-primary" : "text-foreground"
                                  }`}
                                >
                                  <span>{STATUS_CONFIG[st]?.label || st}</span>
                                  {q.status === st && <Check className="h-3.5 w-3.5 text-primary" />}
                                </button>
                              )
                            )}
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Action: Inspect / View */}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleOpenView(q)}
                      title="View Question DNA"
                    >
                      <Eye className="h-4 w-4 text-sky-400" />
                    </Button>

                    {/* Action: Edit */}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleOpenEdit(q)}
                      title="Edit Question Content"
                    >
                      <Edit2 className="h-4 w-4 text-amber-400" />
                    </Button>

                    {/* Action: Public Link */}
                    <Link href={`/questions/${q.slug}`} target="_blank">
                      <Button variant="ghost" size="sm" title="Preview Public Page">
                        <ExternalLink className="h-4 w-4 text-muted-foreground hover:text-foreground" />
                      </Button>
                    </Link>

                    {/* Action: Delete */}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setDeleteQuestionTarget(q)}
                      title="Delete Question"
                    >
                      <Trash2 className="h-4 w-4 text-rose-400 hover:text-rose-500" />
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* ========================================================================= */}
      {/* 1. VIEW / PREVIEW QUESTION MODAL */}
      {/* ========================================================================= */}
      {viewQuestion && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto animate-fade-in">
          <div className="bg-card border border-border/80 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            {/* Modal Header */}
            <div className="p-6 border-b border-border/70 flex items-start justify-between gap-4 bg-muted/20">
              <div className="space-y-2 flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-xs font-bold text-primary uppercase tracking-wider">
                    {viewQuestion.technology_name}
                  </span>
                  {viewQuestion.topic_name && (
                    <>
                      <span className="text-muted-foreground">•</span>
                      <span className="text-xs text-muted-foreground">{viewQuestion.topic_name}</span>
                    </>
                  )}
                  <DifficultyBadge difficulty={viewQuestion.difficulty} />
                  <InterviewDepthBadge depth={viewQuestion.interview_depth} />
                  <span
                    className={`text-xs px-2.5 py-0.5 rounded-full font-semibold border ${
                      STATUS_CONFIG[viewQuestion.status]?.badgeClass || "bg-muted"
                    }`}
                  >
                    {STATUS_CONFIG[viewQuestion.status]?.label || viewQuestion.status}
                  </span>
                </div>
                <h2 className="text-xl font-extrabold text-foreground">{viewQuestion.title}</h2>
                <div className="flex items-center gap-4 text-xs text-muted-foreground font-mono">
                  <span>Slug: /{viewQuestion.slug}</span>
                  <span>Est: {viewQuestion.estimated_time_minutes || 5} min</span>
                  <span>Type: {viewQuestion.question_type}</span>
                </div>
              </div>
              <button
                onClick={() => setViewQuestion(null)}
                className="text-muted-foreground hover:text-foreground p-1 rounded-lg hover:bg-muted"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto space-y-6 text-sm flex-1">
              {viewLoading ? (
                <div className="p-12 text-center text-muted-foreground">
                  <RefreshCw className="h-6 w-6 animate-spin mx-auto text-primary mb-2" />
                  <span>Loading deep question attributes...</span>
                </div>
              ) : (
                <>
                  {/* Short Answer */}
                  {viewQuestion.short_answer && (
                    <div className="p-4 rounded-xl bg-primary/5 border border-primary/20 space-y-1">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-primary">
                        1. Direct Short Answer
                      </span>
                      <p className="text-foreground leading-relaxed font-medium">
                        {viewQuestion.short_answer}
                      </p>
                    </div>
                  )}

                  {/* Interview-Ready Answer */}
                  <div className="space-y-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                      <Sparkles className="h-3.5 w-3.5 text-primary" />
                      2. Interview-Ready Answer (Full Verbal Blueprint)
                    </span>
                    <div className="p-4 rounded-xl bg-muted/30 border border-border/70 text-foreground whitespace-pre-wrap leading-relaxed font-sans">
                      {viewQuestion.interview_ready_answer}
                    </div>
                  </div>

                  {/* Code Example */}
                  {viewQuestion.code_example && (
                    <div className="space-y-2">
                      <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                        <Code className="h-3.5 w-3.5 text-teal-400" />
                        Practical Code Implementation
                      </span>
                      <pre className="p-4 rounded-xl bg-black/60 border border-border/70 text-xs font-mono text-emerald-400 overflow-x-auto leading-relaxed">
                        <code>{viewQuestion.code_example}</code>
                      </pre>
                    </div>
                  )}

                  {/* Deep Explanation */}
                  {viewQuestion.deep_explanation && (
                    <div className="space-y-2">
                      <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                        <BookOpen className="h-3.5 w-3.5 text-sky-400" />
                        Deep Technical Explanation & Mechanics
                      </span>
                      <div className="p-4 rounded-xl bg-muted/20 border border-border/60 text-muted-foreground whitespace-pre-wrap leading-relaxed">
                        {viewQuestion.deep_explanation}
                      </div>
                    </div>
                  )}

                  {/* Architecture & Intent */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {viewQuestion.architecture_notes && (
                      <div className="p-4 rounded-xl bg-card border border-border/70 space-y-1">
                        <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-400">
                          Architecture Notes
                        </span>
                        <p className="text-xs text-muted-foreground leading-relaxed whitespace-pre-wrap">
                          {viewQuestion.architecture_notes}
                        </p>
                      </div>
                    )}

                    {viewQuestion.interviewer_intent && (
                      <div className="p-4 rounded-xl bg-card border border-border/70 space-y-1">
                        <span className="text-[11px] font-bold uppercase tracking-wider text-amber-400">
                          Interviewer Intent & Reasoning
                        </span>
                        <p className="text-xs text-muted-foreground leading-relaxed whitespace-pre-wrap">
                          {viewQuestion.interviewer_intent}
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Hints */}
                  {viewQuestion.hints && viewQuestion.hints.length > 0 && (
                    <div className="space-y-2">
                      <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                        Socratic Hints ({viewQuestion.hints.length})
                      </span>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        {viewQuestion.hints.map((h: any, idx: number) => (
                          <div
                            key={idx}
                            className="p-3 rounded-xl bg-card border border-border/70 space-y-1"
                          >
                            <span className="text-[10px] font-bold text-primary uppercase">
                              Level {h.hint_level} • {h.hint_type}
                            </span>
                            <p className="text-xs text-foreground">{h.content}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>

            {/* Modal Footer */}
            <div className="p-4 bg-muted/20 border-t border-border/70 flex items-center justify-between gap-4">
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    const qToEdit = viewQuestion;
                    setViewQuestion(null);
                    handleOpenEdit(qToEdit);
                  }}
                >
                  <Edit2 className="h-3.5 w-3.5 mr-1 text-amber-400" />
                  <span>Edit Question</span>
                </Button>

                {viewQuestion.status !== "PUBLISHED" && (
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() =>
                      handleStatusTransition(viewQuestion.id, "PUBLISHED", viewQuestion.title)
                    }
                  >
                    <CheckCircle2 className="h-3.5 w-3.5 mr-1" />
                    <span>Publish Live</span>
                  </Button>
                )}
              </div>

              <Button variant="ghost" size="sm" onClick={() => setViewQuestion(null)}>
                <span>Close</span>
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 2. EDIT QUESTION MODAL */}
      {/* ========================================================================= */}
      {editQuestion && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto animate-fade-in">
          <div className="bg-card border border-border/80 rounded-2xl w-full max-w-4xl max-h-[92vh] flex flex-col shadow-2xl overflow-hidden">
            {/* Header */}
            <div className="p-6 border-b border-border/70 flex items-center justify-between gap-4 bg-muted/20">
              <div className="space-y-0.5">
                <h2 className="text-xl font-extrabold text-foreground flex items-center gap-2">
                  <Edit2 className="h-5 w-5 text-amber-400" />
                  <span>Edit Interview Question</span>
                </h2>
                <p className="text-xs text-muted-foreground truncate max-w-xl">
                  {editQuestion.title}
                </p>
              </div>
              <button
                onClick={() => setEditQuestion(null)}
                className="text-muted-foreground hover:text-foreground p-1 rounded-lg hover:bg-muted"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Tab Navigation */}
            <div className="px-6 py-2 border-b border-border/60 bg-muted/10 flex items-center gap-2 text-xs font-semibold overflow-x-auto">
              <button
                type="button"
                onClick={() => setEditTab("core")}
                className={`px-3 py-1.5 rounded-lg transition-colors ${
                  editTab === "core" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
                }`}
              >
                1. Core & Taxonomy
              </button>
              <button
                type="button"
                onClick={() => setEditTab("answers")}
                className={`px-3 py-1.5 rounded-lg transition-colors ${
                  editTab === "answers" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
                }`}
              >
                2. Answers & Deep Content
              </button>
              <button
                type="button"
                onClick={() => setEditTab("architecture")}
                className={`px-3 py-1.5 rounded-lg transition-colors ${
                  editTab === "architecture" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
                }`}
              >
                3. Architecture & Code
              </button>
              <button
                type="button"
                onClick={() => setEditTab("hints")}
                className={`px-3 py-1.5 rounded-lg transition-colors ${
                  editTab === "hints" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
                }`}
              >
                4. Hints & Sources
              </button>
            </div>

            {/* Form Body */}
            <form onSubmit={handleSaveEdit} className="flex-1 overflow-y-auto p-6 space-y-5">
              {/* TAB 1: CORE */}
              {editTab === "core" && (
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                      Question Title *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.title}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                      className="w-full h-10 px-3.5 rounded-xl bg-muted/40 border border-border/70 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        URL Slug
                      </label>
                      <input
                        type="text"
                        value={formData.slug}
                        onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                        className="w-full h-10 px-3.5 rounded-xl bg-muted/40 border border-border/70 text-xs font-mono text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Publishing Status *
                      </label>
                      <select
                        value={formData.status}
                        onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                        className="w-full h-10 px-3 rounded-xl bg-muted/40 border border-border/70 text-xs font-semibold text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      >
                        <option value="DRAFT">DRAFT (Draft Authoring)</option>
                        <option value="AI_REVIEW">AI_REVIEW (Automated AI Verification)</option>
                        <option value="TECHNICAL_REVIEW">TECHNICAL_REVIEW (Staff Peer Review)</option>
                        <option value="APPROVED">APPROVED (Ready to Publish)</option>
                        <option value="PUBLISHED">PUBLISHED (Live on Public Portal)</option>
                        <option value="ARCHIVED">ARCHIVED (De-listed)</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Technology Track *
                      </label>
                      <select
                        value={formData.technology_id}
                        onChange={(e) =>
                          setFormData({ ...formData, technology_id: e.target.value, topic_id: "" })
                        }
                        className="w-full h-10 px-3 rounded-xl bg-muted/40 border border-border/70 text-xs font-semibold text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      >
                        {technologies.map((t) => (
                          <option key={t.id} value={t.id}>
                            {t.name}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Topic Section
                      </label>
                      <select
                        value={formData.topic_id}
                        onChange={(e) => setFormData({ ...formData, topic_id: e.target.value })}
                        className="w-full h-10 px-3 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      >
                        <option value="">General Track (No Topic)</option>
                        {selectedTechTopics.map((top) => (
                          <option key={top.id} value={top.id}>
                            {top.name}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Estimated Time (Minutes)
                      </label>
                      <input
                        type="number"
                        min="1"
                        max="60"
                        value={formData.estimated_time_minutes}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            estimated_time_minutes: parseInt(e.target.value) || 5,
                          })
                        }
                        className="w-full h-10 px-3 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Difficulty Level *
                      </label>
                      <select
                        value={formData.difficulty}
                        onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
                        className="w-full h-10 px-3 rounded-xl bg-muted/40 border border-border/70 text-xs font-semibold text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      >
                        {DIFFICULTY_OPTIONS.filter((d) => d !== "ALL").map((diff) => (
                          <option key={diff} value={diff}>
                            {diff.replace(/_/g, " ")}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Interview Depth *
                      </label>
                      <select
                        value={formData.interview_depth}
                        onChange={(e) => setFormData({ ...formData, interview_depth: e.target.value })}
                        className="w-full h-10 px-3 rounded-xl bg-muted/40 border border-border/70 text-xs font-semibold text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      >
                        {DEPTH_OPTIONS.map((depth) => (
                          <option key={depth} value={depth}>
                            Level {depth}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Question Type
                      </label>
                      <select
                        value={formData.question_type}
                        onChange={(e) => setFormData({ ...formData, question_type: e.target.value })}
                        className="w-full h-10 px-3 rounded-xl bg-muted/40 border border-border/70 text-xs font-semibold text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      >
                        {QUESTION_TYPES.map((t) => (
                          <option key={t} value={t}>
                            {t}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Target Role
                      </label>
                      <input
                        type="text"
                        value={formData.role_target}
                        onChange={(e) => setFormData({ ...formData, role_target: e.target.value })}
                        placeholder="e.g. Senior Software Engineer"
                        className="w-full h-10 px-3 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Experience Level
                      </label>
                      <input
                        type="text"
                        value={formData.experience_level}
                        onChange={(e) => setFormData({ ...formData, experience_level: e.target.value })}
                        placeholder="e.g. 3-7 years"
                        className="w-full h-10 px-3 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 2: ANSWERS */}
              {editTab === "answers" && (
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                      1. Direct Short Answer (1–2 sentences)
                    </label>
                    <textarea
                      rows={2}
                      value={formData.short_answer}
                      onChange={(e) => setFormData({ ...formData, short_answer: e.target.value })}
                      placeholder="Concise direct statement summarizing the mechanism..."
                      className="w-full p-3 rounded-xl bg-muted/40 border border-border/70 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary leading-relaxed"
                    />
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                      2. Interview-Ready Answer (Full Verbal Blueprint) *
                    </label>
                    <textarea
                      rows={8}
                      required
                      value={formData.interview_ready_answer}
                      onChange={(e) => setFormData({ ...formData, interview_ready_answer: e.target.value })}
                      placeholder="Comprehensive, production-tested answer the candidate should deliver verbally..."
                      className="w-full p-3 rounded-xl bg-muted/40 border border-border/70 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary leading-relaxed font-sans"
                    />
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                      3. Deep Concept & Technical Explanation
                    </label>
                    <textarea
                      rows={6}
                      value={formData.deep_explanation}
                      onChange={(e) => setFormData({ ...formData, deep_explanation: e.target.value })}
                      placeholder="Deep internal mechanics, state graphs, execution models, and runtime internals..."
                      className="w-full p-3 rounded-xl bg-muted/40 border border-border/70 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary leading-relaxed font-sans"
                    />
                  </div>
                </div>
              )}

              {/* TAB 3: ARCHITECTURE & CODE */}
              {editTab === "architecture" && (
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                      Practical Code Implementation
                    </label>
                    <textarea
                      rows={7}
                      value={formData.code_example}
                      onChange={(e) => setFormData({ ...formData, code_example: e.target.value })}
                      placeholder="Python/TypeScript executable snippet demonstrating implementation..."
                      className="w-full p-3 rounded-xl bg-black/60 border border-border/70 text-xs font-mono text-emerald-400 focus:outline-none focus:ring-2 focus:ring-primary leading-relaxed"
                    />
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                      Architecture / Flow Notes
                    </label>
                    <textarea
                      rows={4}
                      value={formData.architecture_notes}
                      onChange={(e) => setFormData({ ...formData, architecture_notes: e.target.value })}
                      placeholder="Distributed boundaries, checkpoints, lock structures, failovers..."
                      className="w-full p-3 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary leading-relaxed"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Interviewer Intent & Reasoning
                      </label>
                      <textarea
                        rows={3}
                        value={formData.interviewer_intent}
                        onChange={(e) => setFormData({ ...formData, interviewer_intent: e.target.value })}
                        placeholder="Why do interviewers ask this? What signals are they evaluating?"
                        className="w-full p-3 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary leading-relaxed"
                      />
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Common Mistakes (one per line)
                      </label>
                      <textarea
                        rows={3}
                        value={formData.common_mistakes}
                        onChange={(e) => setFormData({ ...formData, common_mistakes: e.target.value })}
                        placeholder="Assuming single-threaded execution&#10;Forgetting to release lock on error"
                        className="w-full p-3 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary leading-relaxed"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 4: HINTS & SOURCES */}
              {editTab === "hints" && (
                <div className="space-y-4">
                  <div className="space-y-3">
                    <span className="text-xs font-bold uppercase tracking-wider text-primary">
                      Socratic Incremental Hints (L1 to L3)
                    </span>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold text-muted-foreground">
                        Hint 1 (Conceptual Foundation)
                      </label>
                      <input
                        type="text"
                        value={formData.hint1}
                        onChange={(e) => setFormData({ ...formData, hint1: e.target.value })}
                        placeholder="Gentle nudge toward the high-level concept..."
                        className="w-full h-10 px-3.5 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold text-muted-foreground">
                        Hint 2 (Implementation Mechanics)
                      </label>
                      <input
                        type="text"
                        value={formData.hint2}
                        onChange={(e) => setFormData({ ...formData, hint2: e.target.value })}
                        placeholder="Nudge on specific API or state management pattern..."
                        className="w-full h-10 px-3.5 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold text-muted-foreground">
                        Hint 3 (Edge Case & Architecture)
                      </label>
                      <input
                        type="text"
                        value={formData.hint3}
                        onChange={(e) => setFormData({ ...formData, hint3: e.target.value })}
                        placeholder="Direct pointer toward failure modes or distributed constraints..."
                        className="w-full h-10 px-3.5 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>
                  </div>

                  <div className="pt-3 border-t border-border/60 space-y-3">
                    <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                      Source Attribution & Provenance
                    </span>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div className="space-y-1.5">
                        <label className="text-xs font-semibold text-muted-foreground">
                          Source Publisher / Name
                        </label>
                        <input
                          type="text"
                          value={formData.source_name}
                          onChange={(e) => setFormData({ ...formData, source_name: e.target.value })}
                          className="w-full h-10 px-3.5 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                        />
                      </div>

                      <div className="space-y-1.5">
                        <label className="text-xs font-semibold text-muted-foreground">
                          Source Documentation URL
                        </label>
                        <input
                          type="url"
                          value={formData.source_url}
                          onChange={(e) => setFormData({ ...formData, source_url: e.target.value })}
                          className="w-full h-10 px-3.5 rounded-xl bg-muted/40 border border-border/70 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Modal Action Buttons */}
              <div className="pt-4 border-t border-border/70 flex items-center justify-between">
                <Button
                  type="button"
                  variant="ghost"
                  size="md"
                  onClick={() => setEditQuestion(null)}
                >
                  Cancel
                </Button>

                <div className="flex items-center gap-2">
                  {editTab !== "hints" ? (
                    <Button
                      type="button"
                      variant="outline"
                      size="md"
                      onClick={() => {
                        if (editTab === "core") setEditTab("answers");
                        else if (editTab === "answers") setEditTab("architecture");
                        else if (editTab === "architecture") setEditTab("hints");
                      }}
                    >
                      <span>Next Tab</span>
                      <ChevronRight className="h-4 w-4 ml-1" />
                    </Button>
                  ) : null}

                  <Button type="submit" variant="primary" size="md" disabled={isSaving}>
                    <CheckCircle2 className="h-4 w-4 mr-1.5" />
                    <span>{isSaving ? "Saving Changes..." : "Save Question"}</span>
                  </Button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 3. DELETE CONFIRMATION MODAL */}
      {/* ========================================================================= */}
      {deleteQuestionTarget && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-card border border-rose-500/30 rounded-2xl w-full max-w-md p-6 space-y-5 shadow-2xl">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
                <Trash2 className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-foreground">Confirm Permanent Deletion</h3>
                <p className="text-xs text-muted-foreground">This action cannot be undone.</p>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-muted/30 border border-border/70 space-y-1">
              <p className="text-xs text-muted-foreground font-semibold">Question to be deleted:</p>
              <p className="text-sm font-bold text-foreground">{deleteQuestionTarget.title}</p>
              <p className="text-[11px] text-muted-foreground font-mono">/{deleteQuestionTarget.slug}</p>
            </div>

            <p className="text-xs text-muted-foreground leading-relaxed">
              Deleting this question will cascade and remove all associated hints, sources, candidate attempts,
              bookmarks, and version snapshots from the database.
            </p>

            <div className="flex items-center justify-end gap-3 pt-2">
              <Button
                variant="ghost"
                size="md"
                onClick={() => setDeleteQuestionTarget(null)}
                disabled={isDeleting}
              >
                Cancel
              </Button>
              <Button
                variant="destructive"
                size="md"
                onClick={handleDeleteConfirm}
                disabled={isDeleting}
              >
                <Trash2 className="h-4 w-4 mr-1.5" />
                <span>{isDeleting ? "Deleting..." : "Permanently Delete"}</span>
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
