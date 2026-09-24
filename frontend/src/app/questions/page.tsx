"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useSearchParams, useRouter } from "next/navigation";
import { Search, BookOpen, Target, ArrowRight, ChevronRight } from "lucide-react";
import { fetchQuestions, fetchTechnologies, getCachedData, prefetchReadingModeTrack, QuestionCardData, TechnologyData } from "@/lib/api";
import { QuestionCard } from "@/components/questions/question-card";
import { FilterSidebar } from "@/components/questions/filter-sidebar";
import { DifficultyTierBar } from "@/components/questions/difficulty-tier-bar";
import { TechnologyTrackBar } from "@/components/questions/technology-track-bar";

function QuestionsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [questions, setQuestions] = useState<QuestionCardData[]>([]);
  const [total, setTotal] = useState(0);
  const [technologies, setTechnologies] = useState<TechnologyData[]>([]);
  const [loading, setLoading] = useState(true);
  const [isNavigatingToReading, setIsNavigatingToReading] = useState(false);

  const initialSearch = searchParams.get("search") || "";
  const initialTech = searchParams.get("technology") || "";
  const initialDifficulty = searchParams.get("difficulty") || "";
  const initialDepth = searchParams.get("interview_depth") || "";

  const [search, setSearch] = useState(initialSearch);
  const [debouncedSearch, setDebouncedSearch] = useState(initialSearch);
  const [selectedTech, setSelectedTech] = useState(initialTech);
  const [selectedDifficulty, setSelectedDifficulty] = useState(initialDifficulty);
  const [selectedDepth, setSelectedDepth] = useState(initialDepth);

  // Debounce search input by 250ms
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
    }, 250);
    return () => clearTimeout(timer);
  }, [search]);

  // Pre-warm the alternate Reading Mode route & data so clicking is instantaneous
  useEffect(() => {
    const targetTech = selectedTech || "langgraph";
    router.prefetch(`/questions-and-answers/${targetTech}`);
    prefetchReadingModeTrack(targetTech);
  }, [router, selectedTech]);

  // Load technologies taxonomy
  useEffect(() => {
    fetchTechnologies().then((techs) => setTechnologies(techs));
  }, []);

  // Fetch questions on filter update with instant cache response
  useEffect(() => {
    let isMounted = true;
    const query = new URLSearchParams();
    if (selectedTech) query.set("technology", selectedTech);
    if (selectedDifficulty) query.set("difficulty", selectedDifficulty);
    if (selectedDepth) query.set("interview_depth", selectedDepth);
    if (debouncedSearch) query.set("search", debouncedSearch);
    query.set("limit", "30");

    const cacheKey = `questions:${query.toString()}`;
    const cached = getCachedData<{ items: QuestionCardData[]; total: number; pages: number }>(cacheKey);

    if (cached) {
      setQuestions(cached.items);
      setTotal(cached.total);
      setLoading(false);
      return;
    }

    setLoading(true);

    fetchQuestions({
      technology: selectedTech,
      difficulty: selectedDifficulty,
      interview_depth: selectedDepth,
      search: debouncedSearch,
      limit: 30,
    }).then((data) => {
      if (isMounted) {
        setQuestions(data.items);
        setTotal(data.total);
        setLoading(false);
      }
    });

    return () => {
      isMounted = false;
    };
  }, [selectedTech, selectedDifficulty, selectedDepth, debouncedSearch]);

  const handleDifficultySelect = (difficulty: string) => {
    setSelectedDifficulty(difficulty);
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      if (difficulty) {
        params.set("difficulty", difficulty);
      } else {
        params.delete("difficulty");
      }
      const newUrl = `${window.location.pathname}${params.toString() ? `?${params.toString()}` : ""}`;
      window.history.replaceState(null, "", newUrl);
    }
  };

  const handleTechSelect = (techSlug: string) => {
    setSelectedTech(techSlug);
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      if (techSlug) {
        params.set("technology", techSlug);
      } else {
        params.delete("technology");
      }
      const newUrl = `${window.location.pathname}${params.toString() ? `?${params.toString()}` : ""}`;
      window.history.replaceState(null, "", newUrl);
    }
  };

  const handleFilterChange = (filters: { tech?: string; difficulty?: string; depth?: string }) => {
    if (filters.tech !== undefined) setSelectedTech(filters.tech);
    if (filters.difficulty !== undefined) setSelectedDifficulty(filters.difficulty);
    if (filters.depth !== undefined) setSelectedDepth(filters.depth);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 sm:pt-8 pb-12 w-full space-y-8">
      {/* Top Bar: Breadcrumbs on Left, Mode Switcher on Right (Under Navbar - Exact Same Position as Reading Mode) */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 sm:gap-2 text-xs sm:text-sm text-muted-foreground flex-wrap font-medium">
          <Link href="/" className="hover:text-foreground p-1 -m-1">Home</Link>
          <ChevronRight className="h-3.5 w-3.5" />
          <Link href="/learn" className="hover:text-foreground p-1 -m-1">Curriculum Tracks</Link>
          <ChevronRight className="h-3.5 w-3.5" />
          <span className="font-bold text-primary">{selectedTech ? selectedTech.toUpperCase() : "PRACTICE TRACKS"}</span>
          <ChevronRight className="h-3.5 w-3.5" />
          <span className="font-mono text-xs px-2.5 py-0.5 rounded-md bg-amber-100/90 dark:bg-amber-950/60 text-amber-800 dark:text-amber-200 font-semibold border border-amber-200/90 dark:border-amber-900/60">
            Interactive Practice Studio
          </span>
        </nav>

        {/* Dual Mode Switcher - Positioned on EXACT SAME Right Side under Navbar */}
        <div className="inline-flex items-center p-1.5 rounded-2xl bg-gradient-to-r from-amber-500/20 via-pink-500/15 to-rose-500/20 border-2 border-amber-400/80 dark:border-amber-500/70 shadow-lg shadow-amber-500/10 flex-wrap gap-2 self-start md:self-auto shrink-0">
          <span className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-black bg-gradient-to-r from-amber-500 via-amber-600 to-orange-600 text-white shadow-md shadow-amber-500/30">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-80"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400"></span>
            </span>
            <Target className="h-4 w-4" />
            <span>Practice Mode (Active)</span>
          </span>

          <Link
            href={`/questions-and-answers/${selectedTech || "langgraph"}`}
            prefetch={true}
            onClick={() => setIsNavigatingToReading(true)}
            onMouseEnter={() => {
              router.prefetch(`/questions-and-answers/${selectedTech || "langgraph"}`);
              prefetchReadingModeTrack(selectedTech || "langgraph");
            }}
            onTouchStart={() => {
              router.prefetch(`/questions-and-answers/${selectedTech || "langgraph"}`);
              prefetchReadingModeTrack(selectedTech || "langgraph");
            }}
            className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-extrabold bg-rose-500/20 hover:bg-rose-500 text-rose-900 dark:text-rose-100 hover:text-white border border-rose-500/50 hover:border-rose-500 transition-all duration-200 group shadow-xs cursor-pointer active:scale-95"
            title="Switch to Single-Page Reading Mode with Complete Answers"
          >
            {isNavigatingToReading ? (
              <>
                <span className="inline-block h-4 w-4 border-2 border-rose-500 border-t-transparent rounded-full animate-spin" />
                <span>Opening Reading Mode...</span>
              </>
            ) : (
              <>
                <BookOpen className="h-4 w-4 text-rose-600 dark:text-rose-400 group-hover:text-white group-hover:scale-110 transition-transform" />
                <span>Switch to Reading Mode</span>
                <ArrowRight className="h-4 w-4 text-rose-600 dark:text-rose-400 group-hover:text-white group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </Link>
        </div>
      </div>

      {/* Title & Description Row */}
      <div className="space-y-3 max-w-4xl pb-4 border-b border-border/60">
        <h1 className="text-2xl sm:text-4xl lg:text-5xl font-black tracking-tight text-foreground leading-tight">
          Practice Interview Questions
        </h1>
        <p className="text-xs sm:text-base text-muted-foreground leading-relaxed">
          Curated, production-grade technical interview questions across AI/GenAI, Java/Backend, and System Design. Practice with live Think Mode stopwatch, comprehensive AI evaluation, and progressive hint unlocking.
        </p>
      </div>

      {/* 1. Technology Track Selection Bar - Positioned Just Above Level Buttons */}
      <TechnologyTrackBar
        selectedTech={selectedTech}
        onSelectTech={handleTechSelect}
        technologies={technologies}
      />

      {/* 2. 8 Difficulty Tiers (Level buttons) on Upper Side of Screen */}
      <DifficultyTierBar
        selectedDifficulty={selectedDifficulty}
        onSelectDifficulty={handleDifficultySelect}
        totalFiltered={total}
      />

      {/* Main Layout: Filters Sidebar + Grid */}
      <div className="flex flex-col lg:flex-row gap-8 items-start">
        {/* Faceted Filters */}
        <FilterSidebar
          selectedTech={selectedTech}
          selectedDifficulty={selectedDifficulty}
          selectedDepth={selectedDepth}
          onFilterChange={handleFilterChange}
          technologies={technologies}
        />

        {/* Content Column */}
        <div className="flex-1 w-full space-y-6">
          {/* Search bar & Count badge */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="relative w-full sm:max-w-md">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search questions by keyword or concept..."
                className="w-full h-11 pl-10 pr-4 rounded-xl bg-card border border-border/80 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all shadow-sm"
              />
            </div>
            <div className="text-xs font-mono text-muted-foreground shrink-0">
              Showing <span className="font-bold text-foreground">{questions.length}</span> of {total} questions
            </div>
          </div>

          {/* Loading Skeleton */}
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div
                  key={i}
                  className="h-44 rounded-xl border border-border/60 bg-card p-5 animate-pulse space-y-4"
                >
                  <div className="h-4 w-28 bg-muted rounded" />
                  <div className="h-6 w-full bg-muted rounded" />
                  <div className="h-4 w-3/4 bg-muted rounded" />
                </div>
              ))}
            </div>
          ) : questions.length === 0 ? (
            <div className="rounded-2xl border border-border/80 bg-card p-12 text-center space-y-3">
              <div className="h-12 w-12 rounded-full bg-muted/60 text-muted-foreground flex items-center justify-center mx-auto">
                <BookOpen className="h-6 w-6" />
              </div>
              <h3 className="font-bold text-base text-foreground">No questions found</h3>
              <p className="text-xs text-muted-foreground max-w-sm mx-auto">
                No interview questions matched your current filter criteria. Try resetting filters or searching another keyword.
              </p>
              <button
                onClick={() => {
                  setSelectedTech("");
                  setSelectedDifficulty("");
                  setSelectedDepth("");
                  setSearch("");
                }}
                className="text-xs font-semibold text-primary hover:underline pt-2"
              >
                Clear all filters
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {questions.map((q, idx) => (
                <QuestionCard key={q.id} question={q} colorIndex={idx} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function QuestionsPage() {
  return (
    <Suspense
      fallback={
        <div className="max-w-7xl mx-auto px-4 py-16 text-center text-sm text-muted-foreground">
          Loading Question Directory...
        </div>
      }
    >
      <QuestionsContent />
    </Suspense>
  );
}
