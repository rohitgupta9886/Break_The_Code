"use client";

import React, { useState, useEffect, useMemo, useRef } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  BookOpen,
  Target,
  Search,
  ChevronRight,
  ChevronDown,
  ChevronUp,
  Sparkles,
  Layers,
  Code,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Eye,
  Bookmark,
  Share2,
  Check,
  Building2,
  Flame,
  Zap,
  ArrowRight,
  RotateCcw,
  AlertTriangle,
  Lightbulb,
  ExternalLink,
  Filter,
  ListOrdered,
  X,
  Menu
} from "lucide-react";
import { ReadingModeData, ReadingModeQuestion, ReadingModeTier, fetchReadingMode, getCachedData, prefetchReadingModeTrack } from "@/lib/api";
import { CodeBlock } from "@/components/ui/code-block";
import { DifficultyBadge, InterviewDepthBadge } from "@/components/ui/badge";
import { FormattedAnswer } from "@/components/ui/formatted-answer";
import { KNOWN_TRACKS } from "@/components/questions/technology-track-bar";

interface ReadingModeClientProps {
  initialData?: ReadingModeData | null;
  techSlug: string;
}

const BATCH_SIZE = 25;

export function ReadingModeClient({ initialData, techSlug }: ReadingModeClientProps) {
  const router = useRouter();
  const [data, setData] = useState<ReadingModeData | null>(() => {
    if (initialData) return initialData;
    return getCachedData<ReadingModeData>(`reading-mode:${techSlug}`, 180 * 1000);
  });
  const [loading, setLoading] = useState(!data);

  // Pre-warm interactive Practice Mode route so clicking is instantaneous
  useEffect(() => {
    router.prefetch(`/questions?technology=${techSlug}`);
  }, [router, techSlug]);

  // Client-side fetch & caching for instant loading
  useEffect(() => {
    let isMounted = true;
    if (!data) {
      setLoading(true);
      fetchReadingMode(techSlug).then((res) => {
        if (isMounted && res) {
          setData(res);
          if (res.tiers && res.tiers.length > 0 && res.tiers[0].questions.length > 0) {
            setExpandedIds((prev) => {
              const next = new Set(prev);
              next.add(res.tiers[0].questions[0].id);
              if (res.tiers[0].questions.length > 1) {
                next.add(res.tiers[0].questions[1].id);
              }
              return next;
            });
          }
        }
        if (isMounted) setLoading(false);
      });
    }
    return () => {
      isMounted = false;
    };
  }, [techSlug, data]);

  // Filter & Search State
  const [searchQuery, setSearchQuery] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchQuery);
    }, 200);
    return () => clearTimeout(timer);
  }, [searchQuery]);

  const [selectedTier, setSelectedTier] = useState<string>("ALL");
  const [selectedType, setSelectedType] = useState<string>("ALL");
  const [interviewReadyOnly, setInterviewReadyOnly] = useState(false);

  // Mobile Drawer State
  const [isMobileTocOpen, setIsMobileTocOpen] = useState(false);

  // Progressive Mounting Count
  const [renderedCount, setRenderedCount] = useState<number>(BATCH_SIZE);

  // Accordion Expand / Collapse State (Default expand first 2)
  const [expandedIds, setExpandedIds] = useState<Set<string>>(() => {
    const initial = new Set<string>();
    if (initialData?.tiers && initialData.tiers.length > 0 && initialData.tiers[0].questions.length > 0) {
      initial.add(initialData.tiers[0].questions[0].id);
      if (initialData.tiers[0].questions.length > 1) {
        initial.add(initialData.tiers[0].questions[1].id);
      }
    }
    return initial;
  });

  // Reading Progress State (Local Storage)
  const [readIds, setReadIds] = useState<Set<string>>(new Set());
  const [bookmarkedIds, setBookmarkedIds] = useState<Set<string>>(new Set());
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    try {
      const storedRead = localStorage.getItem(`btc_read_${techSlug}`);
      if (storedRead) {
        setReadIds(new Set(JSON.parse(storedRead)));
      }
      const storedBookmarks = localStorage.getItem("btc_bookmarks");
      if (storedBookmarks) {
        setBookmarkedIds(new Set(JSON.parse(storedBookmarks)));
      }
    } catch {
      // Ignore localStorage errors
    }
  }, [techSlug]);

  const toggleRead = (questionId: string) => {
    setReadIds((prev) => {
      const next = new Set(prev);
      if (next.has(questionId)) {
        next.delete(questionId);
      } else {
        next.add(questionId);
      }
      try {
        localStorage.setItem(`btc_read_${techSlug}`, JSON.stringify(Array.from(next)));
      } catch {}
      return next;
    });
  };

  const toggleBookmark = (questionId: string) => {
    setBookmarkedIds((prev) => {
      const next = new Set(prev);
      if (next.has(questionId)) {
        next.delete(questionId);
      } else {
        next.add(questionId);
      }
      try {
        localStorage.setItem("btc_bookmarks", JSON.stringify(Array.from(next)));
      } catch {}
      return next;
    });
  };

  const toggleExpand = (questionId: string) => {
    setExpandedIds((prev) => {
      const next = new Set(prev);
      if (next.has(questionId)) {
        next.delete(questionId);
      } else {
        next.add(questionId);
      }
      return next;
    });
  };

  const expandAll = () => {
    if (!data) return;
    const all = new Set<string>();
    data.tiers.forEach((tier) => tier.questions.forEach((q) => all.add(q.id)));
    setExpandedIds(all);
    setRenderedCount(9999);
  };

  const collapseAll = () => {
    setExpandedIds(new Set());
  };

  const copyShareLink = (slug: string, id: string) => {
    if (typeof window === "undefined") return;
    const url = `${window.location.origin}/questions-and-answers/${techSlug}#q-${slug}`;
    navigator.clipboard.writeText(url);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Filtered Questions & Tiers
  const filteredTiers = useMemo(() => {
    if (!data) return [];
    const query = debouncedSearch.trim().toLowerCase();

    return data.tiers
      .map((tier) => {
        if (selectedTier !== "ALL" && tier.tier !== selectedTier) {
          return null;
        }

        const matchingQuestions = tier.questions.filter((q) => {
          if (selectedType !== "ALL" && q.question_type !== selectedType) {
            return false;
          }

          if (!query) return true;

          const titleMatch = q.title.toLowerCase().includes(query);
          const topicMatch = q.topic_name?.toLowerCase().includes(query);
          const tagMatch = q.tags?.some((t) => t.name.toLowerCase().includes(query));
          const answerMatch =
            q.interview_ready_answer?.toLowerCase().includes(query) ||
            q.short_answer?.toLowerCase().includes(query) ||
            q.deep_explanation?.toLowerCase().includes(query);

          return titleMatch || topicMatch || tagMatch || answerMatch;
        });

        if (matchingQuestions.length === 0) return null;

        return {
          ...tier,
          matchingCount: matchingQuestions.length,
          questions: matchingQuestions,
        };
      })
      .filter(Boolean) as (ReadingModeTier & { matchingCount: number })[];
  }, [data, debouncedSearch, selectedTier, selectedType]);

  const totalFilteredQuestions = useMemo(() => {
    return filteredTiers.reduce((acc, t) => acc + t.questions.length, 0);
  }, [filteredTiers]);

  const totalQuestions = data?.summary?.total_questions || 0;
  const progressPercent = totalQuestions > 0 ? Math.round((readIds.size / totalQuestions) * 100) : 0;

  // Progressive batching count reset when search / tier filter changes
  useEffect(() => {
    setRenderedCount(BATCH_SIZE);
  }, [searchQuery, selectedTier, selectedType]);

  const techNames: Record<string, string> = {
    "langgraph": "LangGraph & Agentic AI",
    "rag-vector-db": "RAG & Vector Databases",
    "java-backend": "Java & JVM Concurrency",
    "dsa": "DSA & Algorithms",
    "system-design": "System Design",
  };
  const fallbackTechName = techNames[techSlug] || techSlug.toUpperCase();

  if (loading || !data) {
    return (
      <div className="min-h-screen bg-background text-foreground pb-24 touch-pan-y">
        <header className="border-b border-rose-200/80 dark:border-rose-900/60 bg-gradient-to-b from-rose-50/50 via-background to-background dark:from-rose-950/20 dark:via-background dark:to-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 sm:pt-8 pb-8 sm:pb-10 space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 sm:gap-2 text-xs sm:text-sm text-muted-foreground flex-wrap font-medium">
                <Link href="/" className="hover:text-foreground p-1 -m-1">Home</Link>
                <ChevronRight className="h-3.5 w-3.5" />
                <Link href="/learn" className="hover:text-foreground p-1 -m-1">Curriculum Tracks</Link>
                <ChevronRight className="h-3.5 w-3.5" />
                <span className="font-bold text-primary">{fallbackTechName}</span>
                <ChevronRight className="h-3.5 w-3.5" />
                <span className="font-mono text-[11px] sm:text-xs px-2 py-0.5 rounded-md bg-rose-100/90 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 font-semibold border border-rose-200/90 dark:border-rose-900/60">
                  Q&A Reading Mode
                </span>
              </nav>

              <div className="inline-flex items-center p-1.5 rounded-2xl bg-gradient-to-r from-rose-500/20 via-pink-500/15 to-amber-500/20 border-2 border-rose-400/80 dark:border-rose-500/70 shadow-lg shadow-rose-500/10 flex-wrap gap-2 self-start md:self-auto shrink-0">
                <span className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-black bg-gradient-to-r from-rose-600 via-pink-600 to-rose-700 text-white shadow-md shadow-rose-600/30">
                  <span className="relative flex h-2.5 w-2.5">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-80"></span>
                    <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400"></span>
                  </span>
                  <BookOpen className="h-4 w-4" />
                  <span>Reading Mode (Active)</span>
                </span>

                <Link
                  href={`/questions?technology=${techSlug}`}
                  prefetch={true}
                  onClick={(e) => {
                    e.preventDefault();
                    router.push(`/questions?technology=${techSlug}`);
                  }}
                  className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-extrabold bg-amber-500/20 hover:bg-amber-500 text-amber-900 dark:text-amber-100 hover:text-white border border-amber-500/50 hover:border-amber-500 transition-all duration-200 group shadow-xs cursor-pointer"
                >
                  <Target className="h-4 w-4 text-amber-600 dark:text-amber-400 group-hover:text-white group-hover:scale-110 transition-transform" />
                  <span>Switch to Practice Mode</span>
                  <ArrowRight className="h-4 w-4 text-amber-600 dark:text-amber-400 group-hover:text-white group-hover:translate-x-1 transition-transform" />
                </Link>
              </div>
            </div>

            <div className="space-y-3 max-w-4xl">
              <div className="h-10 sm:h-12 w-3/4 bg-rose-200/40 dark:bg-rose-950/40 rounded-2xl animate-pulse" />
              <div className="h-5 w-1/2 bg-muted/60 rounded-xl animate-pulse" />
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-6">
          <div className="h-24 rounded-2xl bg-card border border-border/60 animate-pulse" />
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="h-28 rounded-2xl bg-card border border-border/60 animate-pulse" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  const { technology, summary } = data;

  // Running total calculation for progressive rendering
  let cumulativeRendered = 0;

  return (
    <div className="min-h-screen bg-background text-foreground pb-24 touch-pan-y">
      {/* 1. Header Banner */}
      <header className="border-b border-rose-200/80 dark:border-rose-900/60 bg-gradient-to-b from-rose-50/50 via-background to-background dark:from-rose-950/20 dark:via-background dark:to-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 sm:pt-8 pb-8 sm:pb-10 space-y-6">
          
          {/* Top Bar: Breadcrumbs on Left, Mode Switcher on Right (Under Navbar) */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 sm:gap-2 text-xs sm:text-sm text-muted-foreground flex-wrap font-medium">
              <Link href="/" className="hover:text-foreground p-1 -m-1">Home</Link>
              <ChevronRight className="h-3.5 w-3.5" />
              <Link href="/learn" className="hover:text-foreground p-1 -m-1">Curriculum Tracks</Link>
              <ChevronRight className="h-3.5 w-3.5" />
              <span className="font-bold text-primary">{technology.name}</span>
              <ChevronRight className="h-3.5 w-3.5" />
              <span className="font-mono text-[11px] sm:text-xs px-2 py-0.5 rounded-md bg-rose-100/90 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 font-semibold border border-rose-200/90 dark:border-rose-900/60">
                Q&A Reading Mode
              </span>
            </nav>

            {/* Dual Mode Switcher - Positioned on Right Side under Navbar */}
            <div className="inline-flex items-center p-1.5 rounded-2xl bg-gradient-to-r from-rose-500/20 via-pink-500/15 to-amber-500/20 border-2 border-rose-400/80 dark:border-rose-500/70 shadow-lg shadow-rose-500/10 flex-wrap gap-2 self-start md:self-auto shrink-0">
              <span className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-black bg-gradient-to-r from-rose-600 via-pink-600 to-rose-700 text-white shadow-md shadow-rose-600/30">
                <span className="relative flex h-2.5 w-2.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-80"></span>
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400"></span>
                </span>
                <BookOpen className="h-4 w-4" />
                <span>Reading Mode (Active)</span>
              </span>

              <Link
                href={`/questions?technology=${technology.slug}`}
                prefetch={true}
                onClick={(e) => {
                  e.preventDefault();
                  router.push(`/questions?technology=${technology.slug || techSlug}`);
                }}
                onMouseEnter={() => router.prefetch(`/questions?technology=${technology.slug}`)}
                onTouchStart={() => router.prefetch(`/questions?technology=${technology.slug}`)}
                className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-extrabold bg-amber-500/20 hover:bg-amber-500 text-amber-900 dark:text-amber-100 hover:text-white border border-amber-500/50 hover:border-amber-500 transition-all duration-200 group shadow-xs cursor-pointer"
                title="Switch to Interactive Practice Mode with Think Mode & AI Evaluation"
              >
                <Target className="h-4 w-4 text-amber-600 dark:text-amber-400 group-hover:text-white group-hover:scale-110 transition-transform" />
                <span>Switch to Practice Mode</span>
                <ArrowRight className="h-4 w-4 text-amber-600 dark:text-amber-400 group-hover:text-white group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>

          {/* Title & Description */}
          <div className="space-y-3 max-w-4xl">
            <h1 className="text-2xl sm:text-4xl lg:text-5xl font-black tracking-tight text-foreground leading-tight">
              {technology.name} Interview Questions &amp; Answers
            </h1>
            <p className="text-xs sm:text-base text-muted-foreground leading-relaxed">
              {technology.short_description || "Comprehensive interview preparation calibrated across validated difficulty levels. Read, understand, and master foundational mechanics, practical code, and production trade-offs on one continuous page."}
            </p>
          </div>

          {/* Track Summary Badges & Reading Progress */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 pt-4 border-t border-rose-200/60 dark:border-rose-900/40">
            <div className="p-3 sm:p-3.5 rounded-2xl bg-card border border-border/80 space-y-0.5 sm:space-y-1 shadow-2xs">
              <span className="text-xs font-mono text-muted-foreground uppercase tracking-wider font-bold">Total Questions</span>
              <p className="text-xl sm:text-2xl font-black text-foreground">{totalQuestions}</p>
            </div>
            
            <div className="p-3 sm:p-3.5 rounded-2xl bg-card border border-border/80 space-y-0.5 sm:space-y-1 shadow-2xs">
              <span className="text-xs font-mono text-muted-foreground uppercase tracking-wider font-bold">Calibrated Tiers</span>
              <p className="text-xl sm:text-2xl font-black text-rose-600 dark:text-rose-400">{summary.total_tiers} Tiers</p>
            </div>

            <div className="p-3 sm:p-3.5 rounded-2xl bg-card border border-border/80 space-y-1 shadow-2xs col-span-2">
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className="text-muted-foreground">Reading Progress</span>
                <span className="font-mono text-foreground font-bold">{readIds.size} / {totalQuestions} Read ({progressPercent}%)</span>
              </div>
              <div className="h-2.5 w-full bg-muted rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-rose-500 via-pink-500 to-emerald-500 transition-all duration-300 rounded-full"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>
          </div>

        </div>
      </header>

      {/* 2. Sticky Control Bar - Fixed at top-20 to avoid Navbar overlap */}
      <div className="sticky top-20 z-30 w-full bg-white/95 dark:bg-[#0c050d]/95 backdrop-blur-xl border-b border-rose-200/80 dark:border-rose-900/60 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 space-y-2.5">
          
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
            {/* Search Input */}
            <div className="relative flex-1 w-full max-w-md">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-rose-500 pointer-events-none" />
              <input
                type="text"
                aria-label="Search questions, answers, and concepts"
                placeholder="Search questions, code, gotchas..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full h-11 pl-10 pr-10 rounded-xl text-xs sm:text-sm bg-rose-50/50 dark:bg-black/30 border border-rose-200/80 dark:border-rose-900/60 focus:outline-none focus:ring-2 focus:ring-rose-500/50 text-foreground placeholder:text-muted-foreground"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery("")}
                  className="absolute right-2 top-1/2 -translate-y-1/2 min-h-[36px] min-w-[36px] flex items-center justify-center text-xs text-muted-foreground hover:text-foreground font-semibold"
                  aria-label="Clear search"
                >
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>

            {/* Global Actions */}
            <div className="flex items-center gap-2 flex-wrap">
              {/* Interview-Ready Toggle */}
              <button
                onClick={() => setInterviewReadyOnly(!interviewReadyOnly)}
                className={`inline-flex items-center justify-center gap-1.5 min-h-[44px] px-3.5 py-2 rounded-xl text-xs font-bold border transition-all cursor-pointer ${
                  interviewReadyOnly
                    ? "bg-rose-500 text-white border-rose-500 shadow-xs"
                    : "bg-card text-muted-foreground hover:text-foreground border-border/80"
                }`}
                title="Highlight concise elevator-pitch answers for rapid revision"
              >
                <Sparkles className="h-3.5 w-3.5" />
                <span>60s Answer Mode</span>
              </button>

              {/* Expand / Collapse All */}
              <button
                onClick={expandAll}
                className="inline-flex items-center justify-center gap-1 min-h-[44px] px-3 py-2 rounded-xl text-xs font-bold bg-card border border-border/80 hover:bg-muted text-foreground transition-all cursor-pointer"
              >
                <ChevronDown className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Expand All</span>
                <span className="sm:hidden">Expand</span>
              </button>

              <button
                onClick={collapseAll}
                className="inline-flex items-center justify-center gap-1 min-h-[44px] px-3 py-2 rounded-xl text-xs font-bold bg-card border border-border/80 hover:bg-muted text-foreground transition-all cursor-pointer"
              >
                <ChevronUp className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Collapse</span>
              </button>

              {/* Mobile TOC Quick Jump Button */}
              <button
                onClick={() => setIsMobileTocOpen(true)}
                className="lg:hidden inline-flex items-center justify-center gap-1.5 min-h-[44px] px-3.5 py-2 rounded-xl text-xs font-bold bg-primary/10 text-primary border border-primary/30 hover:bg-primary/20 transition-all cursor-pointer"
                aria-label="Open Table of Contents"
              >
                <ListOrdered className="h-3.5 w-3.5" />
                <span>Jump TOC</span>
              </button>
            </div>
          </div>

          {/* Technology Tracks Selection - Positioned Just Above Level Buttons */}
          <div className="flex items-center gap-1.5 overflow-x-auto scrollbar-none pt-2 pb-2.5 border-b border-border/40 touch-pan-x">
            <span className="text-[11px] font-mono uppercase font-bold text-muted-foreground mr-1 shrink-0">
              Track:
            </span>
            {KNOWN_TRACKS.map((t) => {
              const isSelected = techSlug === t.slug;
              const Icon = t.icon;
              return (
                <button
                  key={t.slug}
                  onClick={() => router.push(`/questions-and-answers/${t.slug}`)}
                  onMouseEnter={() => prefetchReadingModeTrack(t.slug)}
                  className={`min-h-[36px] px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer flex items-center gap-1.5 shrink-0 ${
                    isSelected
                      ? `${t.activeBg} shadow-2xs`
                      : "bg-muted/60 text-muted-foreground hover:text-foreground hover:bg-muted"
                  }`}
                >
                  <Icon className={`h-3.5 w-3.5 ${isSelected ? "text-white" : t.color}`} />
                  <span>{t.name}</span>
                </button>
              );
            })}
          </div>

          {/* Tier Filter Pills & Count (Mobile Horizontal Scrollable) */}
          <div className="flex items-center justify-between gap-3 overflow-x-auto scrollbar-none pt-1 touch-pan-y">
            <div className="flex items-center gap-1.5 flex-nowrap sm:flex-wrap">
              <span className="text-[11px] font-mono uppercase font-bold text-muted-foreground mr-1 shrink-0">Level:</span>
              <button
                onClick={() => setSelectedTier("ALL")}
                className={`min-h-[38px] px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer shrink-0 ${
                  selectedTier === "ALL"
                    ? "bg-primary text-primary-foreground shadow-2xs"
                    : "bg-muted/60 text-muted-foreground hover:text-foreground"
                }`}
              >
                All ({totalQuestions})
              </button>
              {data.tiers.map((t) => (
                <button
                  key={t.tier}
                  onClick={() => setSelectedTier(selectedTier === t.tier ? "ALL" : t.tier)}
                  className={`min-h-[38px] px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer flex items-center gap-1 shrink-0 ${
                    selectedTier === t.tier
                      ? "bg-primary text-primary-foreground shadow-2xs"
                      : "bg-muted/60 text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <span>{t.level_code}</span>
                  <span className="hidden md:inline">{t.label}</span>
                  <span className="text-[10px] opacity-80">({t.count})</span>
                </button>
              ))}
            </div>

            <div className="text-xs font-mono font-semibold text-muted-foreground shrink-0 hidden sm:block">
              Showing <strong className="text-foreground">{totalFilteredQuestions}</strong> of {totalQuestions}
            </div>
          </div>

          {/* Question Type Filter Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto scrollbar-none pt-1 border-t border-border/40 touch-pan-y">
            <span className="text-[11px] font-mono uppercase font-bold text-muted-foreground mr-1 shrink-0">Type:</span>
            {["ALL", "CONCEPTUAL", "IMPLEMENTATION", "ARCHITECTURE", "DEBUGGING", "SCENARIO"].map((typeKey) => {
              const label = typeKey === "ALL" 
                ? "All Types" 
                : typeKey.charAt(0) + typeKey.slice(1).toLowerCase();
              const isSelected = selectedType === typeKey;
              return (
                <button
                  key={typeKey}
                  onClick={() => setSelectedType(isSelected && typeKey !== "ALL" ? "ALL" : typeKey)}
                  className={`min-h-[34px] px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer shrink-0 ${
                    isSelected
                      ? "bg-rose-500 text-white shadow-2xs"
                      : "bg-muted/60 text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {label}
                </button>
              );
            })}
          </div>

        </div>
      </div>

      {/* 3. Main Content: TOC Sidebar + Continuous Questions */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left: Sticky Table of Contents (Desktop) */}
          <aside className="hidden lg:block lg:col-span-3 sticky top-56 space-y-4 max-h-[calc(100vh-15rem)] overflow-y-auto pr-2 scrollbar-thin">
            <div className="p-4 rounded-2xl bg-card border border-border/80 shadow-2xs space-y-2">
              <div className="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-muted-foreground">
                <ListOrdered className="h-4 w-4 text-primary" />
                <span>Table of Contents</span>
              </div>
              <p className="text-[11px] text-muted-foreground leading-snug">
                Click any question to jump directly to its complete explanation.
              </p>
            </div>

            <div className="space-y-4">
              {filteredTiers.map((tier) => (
                <div key={tier.tier} className="space-y-1.5">
                  <a
                    href={`#tier-${tier.tier.toLowerCase()}`}
                    className="flex items-center justify-between text-xs font-bold text-foreground px-2 hover:text-primary transition-colors"
                  >
                    <span className="flex items-center gap-1.5">
                      <span className="h-2 w-2 rounded-full bg-rose-500" />
                      <span>{tier.level_code} {tier.label}</span>
                    </span>
                    <span className="font-mono text-[11px] text-muted-foreground">({tier.questions.length})</span>
                  </a>

                  <div className="space-y-0.5 pl-3 border-l-2 border-border/80">
                    {tier.questions.map((q, idx) => {
                      const isRead = readIds.has(q.id);
                      return (
                        <a
                          key={q.id}
                          href={`#q-${q.slug}`}
                          className="block text-xs text-muted-foreground hover:text-primary transition-colors py-1 truncate group"
                          title={q.title}
                        >
                          <span className="font-mono text-xs text-muted-foreground mr-1.5 font-bold">
                            {idx + 1 < 10 ? `0${idx + 1}` : idx + 1}.
                          </span>
                          <span className={`font-bold ${isRead ? "line-through opacity-70" : "text-foreground/90"}`}>{q.title}</span>
                          {isRead && <Check className="inline h-3 w-3 text-emerald-500 ml-1" />}
                        </a>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </aside>

          {/* Right: Continuous Question Cards Feed */}
          <main className="lg:col-span-9 space-y-12">
            {filteredTiers.length === 0 ? (
              <div className="p-12 text-center rounded-3xl bg-card border border-border/80 space-y-4">
                <Search className="h-10 w-10 mx-auto text-muted-foreground opacity-60" />
                <h3 className="text-lg font-bold text-foreground">No Matching Questions Found</h3>
                <p className="text-xs sm:text-sm text-muted-foreground max-w-sm mx-auto">
                  No interview questions match your current query &ldquo;{searchQuery}&rdquo;. Try another search term or reset filters.
                </p>
                <button
                  onClick={() => {
                    setSearchQuery("");
                    setSelectedTier("ALL");
                    setSelectedType("ALL");
                  }}
                  className="min-h-[44px] px-5 py-2.5 rounded-xl text-xs font-bold bg-primary text-primary-foreground hover:bg-primary/90 transition-all cursor-pointer"
                >
                  Reset All Filters
                </button>
              </div>
            ) : (() => {
              let cumulativeRendered = 0;
              return filteredTiers.map((tier) => {
                // Determine which questions in this tier to render based on progressive count
                const questionsToRender = tier.questions.filter(() => {
                  cumulativeRendered++;
                  return cumulativeRendered <= renderedCount;
                });

                if (questionsToRender.length === 0) return null;

                return (
                  <section key={tier.tier} id={`tier-${tier.tier.toLowerCase()}`} className="space-y-6 scroll-mt-36">
                    
                    {/* Tier Header Card */}
                    <div className="p-5 sm:p-6 rounded-3xl bg-gradient-to-r from-rose-100/60 via-background to-card dark:from-rose-950/30 dark:via-background dark:to-card border border-rose-200/90 dark:border-rose-900/60 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div className="space-y-1.5">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className={`text-xs font-mono font-extrabold px-3 py-1 rounded-full border shadow-2xs ${tier.badge_color}`}>
                            {tier.level_code} • {tier.label.toUpperCase()}
                          </span>
                          <span className="text-xs font-semibold text-muted-foreground">
                            {tier.experience_range}
                          </span>
                        </div>
                        <h2 className="text-xl sm:text-2xl font-black text-foreground tracking-tight">
                          {tier.label} Technical Interview Focus
                        </h2>
                        <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed max-w-2xl">
                          {tier.description}
                        </p>
                      </div>

                      <div className="text-left sm:text-right shrink-0">
                        <span className="text-2xl sm:text-3xl font-black text-rose-600 dark:text-rose-400">
                          {tier.questions.length}
                        </span>
                        <span className="block text-[11px] font-mono text-muted-foreground uppercase font-semibold">
                          Questions in Tier
                        </span>
                      </div>
                    </div>

                    {/* List of Questions in this Tier with content-visibility: auto */}
                    <div className="space-y-5">
                      {questionsToRender.map((q, idx) => {
                        const isExpanded = expandedIds.has(q.id);
                        const isRead = readIds.has(q.id);
                        const isBookmarked = bookmarkedIds.has(q.id);

                        return (
                          <article
                            key={q.id}
                            id={`q-${q.slug}`}
                            className={`cv-auto rounded-3xl border transition-all duration-200 bg-card overflow-hidden scroll-mt-48 shadow-xs ${
                              isRead
                                ? "border-emerald-500/30 bg-emerald-500/[0.02]"
                                : "border-border/80 hover:border-rose-300 dark:hover:border-rose-800"
                            }`}
                          >
                            {/* Question Card Header (Always Visible) */}
                            <div className="p-5 sm:p-6 space-y-3">
                              <div className="flex items-center justify-between gap-2 flex-wrap">
                                <div className="flex items-center gap-2 flex-wrap">
                                  <span className="font-mono text-xs font-black px-2.5 py-1 rounded-lg bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20">
                                    Q{idx + 1 < 10 ? `0${idx + 1}` : idx + 1}
                                  </span>
                                  <DifficultyBadge difficulty={q.difficulty} size="sm" />
                                  <InterviewDepthBadge depth={q.interview_depth} />
                                  {q.topic_name && (
                                    <span className="text-xs font-mono font-semibold text-muted-foreground hidden sm:inline">
                                      • {q.topic_name}
                                    </span>
                                  )}
                                </div>

                                <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
                                  <span className="flex items-center gap-1">
                                    <Clock className="h-3.5 w-3.5 text-amber-500" />
                                    <span>{q.estimated_time_minutes} min</span>
                                  </span>
                                  {isRead && (
                                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30">
                                      <Check className="h-3 w-3" /> Read
                                    </span>
                                  )}
                                </div>
                              </div>

                              {/* Question Title - Extra Bold */}
                              <div className="cursor-pointer" onClick={() => toggleExpand(q.id)}>
                                <h3 className="text-base sm:text-xl font-black text-foreground tracking-tight leading-snug hover:text-primary transition-colors">
                                  {q.title}
                                </h3>
                              </div>

                              {/* Company Provenance Tags */}
                              {q.tags && q.tags.length > 0 && (
                                <div className="flex items-center gap-1.5 flex-wrap pt-0.5">
                                  <span className="text-xs font-bold text-muted-foreground flex items-center gap-1 uppercase tracking-wider">
                                    <Building2 className="h-3 w-3 text-rose-500" />
                                    <span>Real Loop:</span>
                                  </span>
                                  {q.tags.map((tag) => (
                                    <span
                                      key={tag.slug}
                                      className="text-xs px-2.5 py-0.5 rounded-md bg-muted/70 text-foreground font-mono font-semibold border border-border/60"
                                    >
                                      {tag.name}
                                    </span>
                                  ))}
                                </div>
                              )}

                              {/* Actions Bar & Expand Button */}
                              <div className="flex items-center justify-between gap-3 pt-3 border-t border-border/60 flex-wrap">
                                <div className="flex items-center gap-2 flex-wrap">
                                  <button
                                    onClick={() => toggleExpand(q.id)}
                                    className="inline-flex items-center justify-center gap-1.5 min-h-[44px] px-4 py-2 rounded-xl text-xs font-bold bg-primary text-primary-foreground hover:bg-primary/90 transition-all cursor-pointer"
                                  >
                                    {isExpanded ? (
                                      <>
                                        <ChevronUp className="h-3.5 w-3.5" />
                                        <span>Hide Answer</span>
                                      </>
                                    ) : (
                                      <>
                                        <ChevronDown className="h-3.5 w-3.5" />
                                        <span>Show Complete Answer</span>
                                      </>
                                    )}
                                  </button>

                                  {/* Direct Practice Link */}
                                  <Link
                                    href={`/questions/${q.slug}`}
                                    className="inline-flex items-center justify-center gap-1.5 min-h-[44px] px-3.5 py-2 rounded-xl text-xs font-bold bg-amber-500/10 text-amber-800 dark:text-amber-200 border border-amber-500/30 hover:bg-amber-500/20 transition-all"
                                    title="Test yourself on this specific question with Think Mode timer and AI evaluation"
                                  >
                                    <Target className="h-3.5 w-3.5 text-amber-500" />
                                    <span>Practice</span>
                                  </Link>
                                </div>

                                <div className="flex items-center gap-1.5">
                                  {/* Mark as Read */}
                                  <button
                                    onClick={() => toggleRead(q.id)}
                                    className={`min-h-[44px] min-w-[44px] flex items-center justify-center rounded-xl text-xs font-semibold border transition-all cursor-pointer ${
                                      isRead
                                        ? "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-500/30"
                                        : "bg-muted/40 text-muted-foreground hover:text-foreground border-border/60"
                                    }`}
                                    title={isRead ? "Mark as unread" : "Mark as read"}
                                    aria-label="Toggle mark as read"
                                  >
                                    <Check className="h-4 w-4" />
                                  </button>

                                  {/* Bookmark */}
                                  <button
                                    onClick={() => toggleBookmark(q.id)}
                                    className={`min-h-[44px] min-w-[44px] flex items-center justify-center rounded-xl text-xs font-semibold border transition-all cursor-pointer ${
                                      isBookmarked
                                        ? "bg-amber-500/15 text-amber-600 border-amber-500/30"
                                        : "bg-muted/40 text-muted-foreground hover:text-foreground border-border/60"
                                    }`}
                                    title={isBookmarked ? "Remove bookmark" : "Save bookmark"}
                                    aria-label="Toggle bookmark"
                                  >
                                    <Bookmark className={`h-4 w-4 ${isBookmarked ? "fill-amber-500 text-amber-500" : ""}`} />
                                  </button>

                                  {/* Share Link */}
                                  <button
                                    onClick={() => copyShareLink(q.slug, q.id)}
                                    className="min-h-[44px] min-w-[44px] flex items-center justify-center rounded-xl text-xs font-semibold bg-muted/40 text-muted-foreground hover:text-foreground border border-border/60 transition-all cursor-pointer"
                                    title="Copy direct question link"
                                    aria-label="Share question link"
                                  >
                                    {copiedId === q.id ? (
                                      <Check className="h-4 w-4 text-emerald-500" />
                                    ) : (
                                      <Share2 className="h-4 w-4" />
                                    )}
                                  </button>
                                </div>
                              </div>
                            </div>

                            {/* Expandable Complete Answer Area */}
                            {isExpanded && (
                              <div className="border-t border-rose-200/80 dark:border-rose-900/60 bg-[#fffbfc] dark:bg-[#150912]/50 p-5 sm:p-7 space-y-6">
                                
                                {/* 1. Interview-Ready Direct Answer (Elevator Pitch) */}
                                {q.interview_ready_answer && (
                                  <div className="p-5 sm:p-6 rounded-2xl bg-gradient-to-r from-rose-500/10 via-pink-500/10 to-amber-500/5 border border-rose-400/40 dark:border-rose-800/60 space-y-3">
                                    <div className="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-rose-700 dark:text-rose-300">
                                      <Sparkles className="h-4 w-4 text-rose-500" />
                                      <span>Interview-Ready Model Answer (60-Second Verbal Response)</span>
                                    </div>
                                    <div className="answer-lead text-foreground/95 selection:bg-rose-500/20">
                                      <FormattedAnswer text={q.interview_ready_answer} variant="lead" />
                                    </div>
                                  </div>
                                )}

                                {/* 2. Direct Answer / Short Answer */}
                                {!interviewReadyOnly && q.short_answer && q.short_answer !== q.interview_ready_answer && (
                                  <div className="space-y-2 p-4 sm:p-5 rounded-2xl bg-muted/40 border border-border/60">
                                    <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-muted-foreground">
                                      Direct Answer Summary
                                    </h4>
                                    <div className="answer-body text-foreground">
                                      <FormattedAnswer text={q.short_answer} />
                                    </div>
                                  </div>
                                )}

                                {/* 3. Deep Technical Explanation */}
                                {!interviewReadyOnly && q.deep_explanation && (
                                  <div className="space-y-3 pt-3 border-t border-border/40">
                                    <div className="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-foreground">
                                      <BookOpen className="h-4 w-4 text-primary" />
                                      <span>Core Concept &amp; Deep Technical Explanation</span>
                                    </div>
                                    <div className="answer-body text-foreground/95 space-y-3">
                                      <FormattedAnswer text={q.deep_explanation} />
                                    </div>
                                  </div>
                                )}

                                {/* 4. Practical Implementation Code */}
                                {!interviewReadyOnly && q.code_example && (
                                  <div className="space-y-2.5 pt-3 border-t border-border/40">
                                    <div className="flex items-center justify-between">
                                      <div className="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-foreground">
                                        <Code className="h-4 w-4 text-emerald-500" />
                                        <span>Production Implementation Pattern</span>
                                      </div>
                                      <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-muted text-foreground/80 border border-border/60">
                                        {techSlug === "java-backend" ? "java" : "python"}
                                      </span>
                                    </div>
                                    <CodeBlock
                                      code={q.code_example}
                                      language={techSlug === "java-backend" ? "java" : "python"}
                                    />
                                  </div>
                                )}

                                {/* 5. Production Considerations & Trade-offs */}
                                {!interviewReadyOnly && (q.production_considerations || q.tradeoffs) && (
                                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-3 border-t border-border/40">
                                    {q.production_considerations && (
                                      <div className="p-4 sm:p-5 rounded-2xl bg-card border border-border/80 space-y-2">
                                        <div className="flex items-center gap-1.5 text-xs font-mono font-bold text-teal-600 dark:text-teal-400 uppercase">
                                          <Layers className="h-3.5 w-3.5" />
                                          <span>Production Considerations</span>
                                        </div>
                                        <div className="text-sm sm:text-base text-foreground/90">
                                          <FormattedAnswer text={q.production_considerations} />
                                        </div>
                                      </div>
                                    )}

                                    {q.tradeoffs && (
                                      <div className="p-4 sm:p-5 rounded-2xl bg-card border border-border/80 space-y-2">
                                        <div className="flex items-center gap-1.5 text-xs font-mono font-bold text-indigo-600 dark:text-indigo-400 uppercase">
                                          <RotateCcw className="h-3.5 w-3.5" />
                                          <span>Architectural Trade-offs</span>
                                        </div>
                                        <div className="text-sm sm:text-base text-foreground/90">
                                          <FormattedAnswer text={q.tradeoffs} />
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                )}

                                {/* 6. Common Mistakes / Interviewer Traps */}
                                {!interviewReadyOnly && q.common_mistakes && q.common_mistakes.length > 0 && (
                                  <div className="p-4 sm:p-5 rounded-2xl bg-amber-500/10 border border-amber-500/30 space-y-2.5">
                                    <div className="flex items-center gap-2 text-xs font-mono font-bold text-amber-800 dark:text-amber-300 uppercase">
                                      <AlertTriangle className="h-4 w-4 text-amber-500" />
                                      <span>Common Candidate Mistakes &amp; Interviewer Traps</span>
                                    </div>
                                    <ul className="space-y-2 text-sm sm:text-base text-foreground/90 list-disc list-inside leading-relaxed sm:leading-[1.75]">
                                      {q.common_mistakes.map((m, i) => (
                                        <li key={i} className="leading-relaxed">
                                          <span className="font-semibold text-foreground">{(typeof m === "string" ? m : JSON.stringify(m)).replace(/\*/g, "")}</span>
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                )}

                                {/* 7. Realistic Follow-Up Questions */}
                                {!interviewReadyOnly && q.followups && q.followups.length > 0 && (
                                  <div className="p-4 sm:p-5 rounded-2xl bg-purple-500/10 border border-purple-500/30 space-y-3">
                                    <div className="flex items-center gap-2 text-xs font-mono font-bold text-purple-700 dark:text-purple-300 uppercase">
                                      <Zap className="h-4 w-4 text-purple-500" />
                                      <span>Likely Interviewer Follow-Ups</span>
                                    </div>
                                    <div className="space-y-3">
                                      {q.followups.map((f, i) => (
                                        <div key={i} className="space-y-1.5">
                                          <p className="font-bold text-foreground text-sm sm:text-base leading-snug">
                                            &ldquo;{f.followup_question?.replace(/\*/g, "")}&rdquo;
                                          </p>
                                          {f.answer_guidance && (
                                            <p className="text-sm sm:text-base text-foreground/80 leading-relaxed pl-3 border-l-2 border-purple-400 font-normal">
                                              {f.answer_guidance.replace(/\*/g, "")}
                                            </p>
                                          )}
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                )}

                                {/* Bottom Practice Callout */}
                                <div className="flex items-center justify-between pt-2 border-t border-border/40 text-xs">
                                  <span className="text-muted-foreground">Ready to test yourself under timed interview pressure?</span>
                                  <Link
                                    href={`/questions/${q.slug}`}
                                    className="font-bold text-primary hover:underline inline-flex items-center gap-1 min-h-[44px]"
                                  >
                                    <span>Practice in Interactive Studio</span>
                                    <ArrowRight className="h-3.5 w-3.5" />
                                  </Link>
                                </div>

                              </div>
                            )}
                          </article>
                        );
                      })}
                    </div>

                  </section>
                );
              });
            })()}

            {/* Load More Button if progressive mounting has more items */}
            {renderedCount < totalFilteredQuestions && (
              <div className="text-center py-6">
                <button
                  onClick={() => setRenderedCount((prev) => prev + BATCH_SIZE)}
                  className="min-h-[48px] px-8 py-3 rounded-2xl font-bold text-sm bg-card border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground transition-all shadow-sm cursor-pointer"
                >
                  Load Next {Math.min(BATCH_SIZE, totalFilteredQuestions - renderedCount)} Questions ({renderedCount} / {totalFilteredQuestions})
                </button>
              </div>
            )}

            {/* Bottom Final Navigation */}
            <div className="p-6 sm:p-10 rounded-3xl bg-card border border-border/80 text-center space-y-5 shadow-sm">
              <div className="h-12 w-12 rounded-2xl bg-primary/10 text-primary mx-auto flex items-center justify-center">
                <CheckCircle2 className="h-6 w-6" />
              </div>
              <div className="space-y-1.5 max-w-md mx-auto">
                <h3 className="text-lg sm:text-xl font-bold text-foreground">
                  You&apos;ve reached the end of {technology.name} Questions
                </h3>
                <p className="text-xs sm:text-sm text-muted-foreground">
                  Solidify your knowledge by attempting questions in Practice Mode with Think Mode stopwatch and AI feedback.
                </p>
              </div>

              <div className="flex items-center justify-center gap-3 flex-wrap">
                <Link
                  href={`/questions?technology=${technology.slug}`}
                  className="min-h-[44px] px-5 py-2.5 rounded-xl font-bold text-xs bg-primary text-primary-foreground hover:bg-primary/90 transition-all inline-flex items-center gap-2"
                >
                  <Target className="h-4 w-4" />
                  <span>Practice This Track</span>
                </Link>

                <Link
                  href="/learn"
                  className="min-h-[44px] px-5 py-2.5 rounded-xl font-bold text-xs border border-border/80 hover:bg-muted text-foreground transition-all inline-flex items-center gap-2"
                >
                  <BookOpen className="h-4 w-4 text-muted-foreground" />
                  <span>Browse All Tracks</span>
                </Link>

                <button
                  onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
                  className="min-h-[44px] px-5 py-2.5 rounded-xl font-bold text-xs bg-muted/60 hover:bg-muted text-foreground transition-all cursor-pointer inline-flex items-center gap-1.5"
                >
                  <ChevronUp className="h-4 w-4" />
                  <span>Back to Top</span>
                </button>
              </div>
            </div>

          </main>
        </div>
      </div>

      {/* Floating Mobile TOC Quick Action Pill */}
      <div className="lg:hidden fixed bottom-6 right-4 z-40">
        <button
          onClick={() => setIsMobileTocOpen(true)}
          className="flex items-center gap-2 min-h-[48px] px-4 py-3 rounded-full bg-primary text-primary-foreground font-bold text-xs shadow-xl shadow-primary/30 border border-primary-foreground/20 cursor-pointer active:scale-95 transition-transform"
          aria-label="Open Table of Contents Drawer"
        >
          <ListOrdered className="h-4 w-4" />
          <span>Jump to Tier / Q&amp;A</span>
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
        </button>
      </div>

      {/* Mobile Slide-Over TOC Drawer */}
      {isMobileTocOpen && (
        <div className="fixed inset-0 z-50 flex flex-col justify-end lg:hidden">
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black/60 backdrop-blur-xs transition-opacity"
            onClick={() => setIsMobileTocOpen(false)}
          />

          {/* Drawer Content */}
          <div className="relative w-full max-h-[85vh] bg-card border-t border-border rounded-t-3xl shadow-2xl overflow-hidden flex flex-col z-10 animate-in slide-in-from-bottom duration-300">
            {/* Drawer Header */}
            <div className="p-4 border-b border-border flex items-center justify-between">
              <div className="flex items-center gap-2">
                <ListOrdered className="h-5 w-5 text-primary" />
                <h3 className="font-bold text-sm text-foreground">Table of Contents &amp; Quick Jump</h3>
              </div>
              <button
                onClick={() => setIsMobileTocOpen(false)}
                className="min-h-[40px] min-w-[40px] flex items-center justify-center rounded-xl bg-muted/60 text-foreground"
                aria-label="Close Drawer"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Reading Progress Indicator */}
            <div className="px-5 py-3 bg-muted/30 border-b border-border/60">
              <div className="flex items-center justify-between text-xs font-semibold pb-1.5">
                <span className="text-muted-foreground">Reading Progress</span>
                <span className="font-mono text-foreground font-bold">{readIds.size} / {totalQuestions} Read ({progressPercent}%)</span>
              </div>
              <div className="h-2 w-full bg-muted rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-rose-500 to-emerald-500 rounded-full"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>

            {/* Scrollable Jump Links */}
            <div className="p-4 overflow-y-auto space-y-4 max-h-[60vh]">
              {filteredTiers.map((tier) => (
                <div key={tier.tier} className="space-y-1.5">
                  <a
                    href={`#tier-${tier.tier.toLowerCase()}`}
                    onClick={() => setIsMobileTocOpen(false)}
                    className="flex items-center justify-between text-xs font-bold text-foreground px-2 py-1.5 rounded-lg bg-muted/40"
                  >
                    <span className="flex items-center gap-2">
                      <span className="h-2.5 w-2.5 rounded-full bg-rose-500" />
                      <span>{tier.level_code} • {tier.label}</span>
                    </span>
                    <span className="font-mono text-[11px] text-muted-foreground font-semibold">
                      {tier.questions.length} Qs
                    </span>
                  </a>

                  <div className="space-y-1 pl-3 border-l-2 border-border/80">
                    {tier.questions.map((q, idx) => {
                      const isRead = readIds.has(q.id);
                      return (
                        <a
                          key={q.id}
                          href={`#q-${q.slug}`}
                          onClick={() => {
                            setRenderedCount(9999);
                            setIsMobileTocOpen(false);
                          }}
                          className="flex items-center justify-between text-xs sm:text-sm text-muted-foreground hover:text-primary py-2 truncate group"
                        >
                          <span className="truncate pr-2">
                            <span className="font-mono text-xs text-muted-foreground mr-1.5 font-bold">
                              {idx + 1 < 10 ? `0${idx + 1}` : idx + 1}.
                            </span>
                            <span className={`font-bold ${isRead ? "line-through opacity-70" : "text-foreground"}`}>{q.title}</span>
                          </span>
                          {isRead && <Check className="h-3.5 w-3.5 text-emerald-500 shrink-0" />}
                        </a>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
