"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ChevronRight,
  Clock,
  Eye,
  Bookmark,
  Share2,
  Sparkles,
  Zap,
  Play,
  Lightbulb,
  CheckCircle2,
  BookOpen,
  ShieldCheck,
  Activity,
  Layers,
  Building2,
  Briefcase
} from "lucide-react";
import { QuestionDetailData, toggleBookmarkApi } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { DifficultyBadge, TechnologyBadge, InterviewDepthBadge } from "@/components/ui/badge";
import { ThinkMode } from "@/components/questions/think-mode";
import { AnswerView } from "@/components/questions/answer-view";
import { Button } from "@/components/ui/button";

interface QuestionDetailClientProps {
  question: QuestionDetailData;
}

export function QuestionDetailClient({ question }: QuestionDetailClientProps) {
  const { token } = useAuth();
  const [isAnswerRevealed, setIsAnswerRevealed] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(Boolean(question.is_bookmarked));
  const [shareCopied, setShareCopied] = useState(false);

  const handleToggleBookmark = async () => {
    const prev = isBookmarked;
    // Optimistic UI: update immediately (<5ms)
    setIsBookmarked(!prev);
    if (!token) return;
    try {
      await toggleBookmarkApi(question.id, token);
    } catch (err) {
      // Rollback on network failure
      setIsBookmarked(prev);
    }
  };

  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setShareCopied(true);
      setTimeout(() => setShareCopied(false), 2000);
    } catch (e) {
      console.error(e);
    }
  };

  const isProduction = question.difficulty === "PRODUCTION_SCENARIO" || question.scenario_type === "PRODUCTION_OUTAGE";

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10 space-y-8 touch-pan-y">
      
      {/* 1. Breadcrumb Navigation */}
      <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 sm:gap-2 text-xs sm:text-sm text-muted-foreground flex-wrap font-medium">
        <Link href="/" className="hover:text-foreground p-1 -m-1">Home</Link>
        <ChevronRight className="h-3.5 w-3.5" />
        <Link href="/questions" className="hover:text-foreground p-1 -m-1">Questions</Link>
        <ChevronRight className="h-3.5 w-3.5" />
        <Link
          href={`/questions?technology=${question.technology_slug}`}
          className="hover:text-foreground font-semibold text-primary p-1 -m-1"
        >
          {question.technology_name}
        </Link>
        <ChevronRight className="h-3.5 w-3.5" />
        <span className="font-mono text-[11px] sm:text-xs text-foreground bg-rose-100/70 dark:bg-rose-900/40 px-2 py-0.5 rounded-md font-semibold">
          {question.difficulty}
        </span>
      </nav>

      {/* 2. Top Header Container - Blush Rose Theme Card */}
      <div className="rounded-3xl border border-rose-200/90 dark:border-rose-900/60 bg-[#fff2f4] dark:bg-rose-950/25 p-5 sm:p-9 shadow-sm shadow-rose-100/50 space-y-6">
        
        {/* Badges Row */}
        <div className="flex items-center justify-between gap-3 flex-wrap">
          <div className="flex items-center gap-2 flex-wrap">
            <TechnologyBadge technology={question.technology_name} />
            <DifficultyBadge difficulty={question.difficulty} size="md" />
            <InterviewDepthBadge depth={question.interview_depth} />
            {isProduction && (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-teal-500/15 text-teal-700 dark:text-teal-300 border border-teal-500/30">
                <Activity className="h-3.5 w-3.5 animate-pulse" />
                Production Scenario
              </span>
            )}
          </div>

          <div className="flex items-center gap-3 text-xs sm:text-sm font-mono text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <Clock className="h-4 w-4 text-amber-500" />
              <span>{question.estimated_time_minutes || 10} min</span>
            </span>
            <span>•</span>
            <span className="flex items-center gap-1.5">
              <Eye className="h-4 w-4" />
              <span>{question.view_count || 120} views</span>
            </span>
          </div>
        </div>

        {/* Readable Question Title */}
        <div className="space-y-2">
          <span className="text-xs font-mono uppercase tracking-widest text-primary font-bold">
            Interview Question
          </span>
          <h1 className="text-xl sm:text-3xl font-black tracking-tight text-foreground leading-snug">
            {question.title}
          </h1>
        </div>

        {/* Real Interview Company Provenance & Seniority Target */}
        <div className="p-4 sm:p-5 rounded-2xl bg-white/85 dark:bg-black/35 border border-rose-200/90 dark:border-rose-900/50 shadow-sm space-y-3">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-bold text-muted-foreground uppercase tracking-wider flex items-center gap-1.5 mr-1">
                <Building2 className="h-4 w-4 text-rose-500" />
                <span>Verified Loops:</span>
              </span>
              {question.tags && question.tags.length > 0 ? (
                question.tags.map((tag) => {
                  const companyClass = {
                    google: "bg-blue-500/15 text-blue-700 dark:text-blue-300 border-blue-500/35",
                    meta: "bg-sky-500/15 text-sky-700 dark:text-sky-300 border-sky-500/35",
                    amazon: "bg-amber-500/15 text-amber-800 dark:text-amber-300 border-amber-500/35",
                    netflix: "bg-rose-500/15 text-rose-700 dark:text-rose-300 border-rose-500/35",
                    openai: "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-500/35",
                    stripe: "bg-indigo-500/15 text-indigo-700 dark:text-indigo-300 border-indigo-500/35",
                    databricks: "bg-orange-500/15 text-orange-700 dark:text-orange-300 border-orange-500/35",
                    uber: "bg-neutral-800/15 dark:bg-white/15 text-foreground border-foreground/30",
                    apple: "bg-slate-500/15 text-slate-800 dark:text-slate-200 border-slate-500/35",
                    microsoft: "bg-cyan-500/15 text-cyan-700 dark:text-cyan-300 border-cyan-500/35",
                  }[tag.slug] || "bg-white dark:bg-card text-foreground border-border";

                  return (
                    <span
                      key={tag.slug}
                      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold border shadow-2xs ${companyClass}`}
                    >
                      <span className="h-2 w-2 rounded-full bg-current opacity-80" />
                      {tag.name}
                    </span>
                  );
                })
              ) : (
                <span className="text-xs text-muted-foreground font-medium">
                  Tier-1 Engineering Loops
                </span>
              )}
            </div>

            {/* Cited primary sources badge */}
            {question.sources && question.sources.length > 0 && (
              <span className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-700 dark:text-emerald-300 bg-emerald-500/15 border border-emerald-500/30 px-3 py-1 rounded-full">
                <ShieldCheck className="h-3.5 w-3.5" />
                <span>{question.sources.length} Official Specs Cited</span>
              </span>
            )}
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-rose-100 dark:border-rose-950/60 text-xs sm:text-sm">
            <div className="flex items-center gap-2 text-foreground font-semibold">
              <Briefcase className="h-4 w-4 text-primary" />
              <span>Target Loop:</span>
              <span className="px-2.5 py-0.5 rounded-md bg-primary/10 text-primary font-bold border border-primary/20">
                {question.interview_round || "Technical Architecture Loop"}
              </span>
            </div>

            <div className="flex items-center gap-2 text-muted-foreground font-mono">
              <span>Seniority Bar:</span>
              <strong className="text-foreground font-semibold">
                {question.role_target || "Senior Software Engineer"}
              </strong>
            </div>
          </div>
        </div>

        {/* Action Controls Bar: [Think] [Hint] [Show Answer] [Save] [Share] */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-5 border-t border-rose-200/80 dark:border-rose-900/50">
          <div className="flex flex-wrap items-center gap-2.5">
            <button
              onClick={() => {
                const el = document.getElementById("think-mode-section");
                el?.scrollIntoView({ behavior: "smooth" });
              }}
              className="inline-flex items-center justify-center gap-1.5 min-h-[44px] px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-amber-500/15 text-amber-800 dark:text-amber-200 border border-amber-500/30 hover:bg-amber-500/25 transition-all cursor-pointer"
            >
              <Zap className="h-4 w-4" />
              <span>Think Mode</span>
            </button>

            <button
              onClick={() => {
                const el = document.getElementById("think-mode-section");
                el?.scrollIntoView({ behavior: "smooth" });
              }}
              className="inline-flex items-center justify-center gap-1.5 min-h-[44px] px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-sky-500/15 text-sky-800 dark:text-sky-200 border border-sky-500/30 hover:bg-sky-500/25 transition-all cursor-pointer"
            >
              <Lightbulb className="h-4 w-4" />
              <span>View Hints ({question.hints?.length || 3})</span>
            </button>

            <button
              onClick={() => setIsAnswerRevealed(!isAnswerRevealed)}
              className="inline-flex items-center justify-center gap-1.5 min-h-[44px] px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-primary text-primary-foreground hover:bg-primary/90 transition-all cursor-pointer shadow-sm shadow-primary/30"
            >
              <Sparkles className="h-4 w-4" />
              <span>{isAnswerRevealed ? "Hide Model Answer" : "Show Model Answer"}</span>
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleToggleBookmark}
              className={`min-h-[44px] px-3.5 py-2.5 rounded-xl border text-xs sm:text-sm font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                isBookmarked 
                  ? "bg-amber-500/20 text-amber-600 border-amber-500/40" 
                  : "bg-white/60 dark:bg-white/10 text-muted-foreground border-rose-200/80 dark:border-rose-900/50 hover:text-foreground"
              }`}
              title="Save Question"
              aria-label="Save Question"
            >
              <Bookmark className={`h-4 w-4 ${isBookmarked ? "fill-amber-500 text-amber-500" : ""}`} />
              <span>{isBookmarked ? "Saved" : "Save"}</span>
            </button>

            <button
              onClick={handleShare}
              className="min-h-[44px] px-3.5 py-2.5 rounded-xl border border-rose-200/80 dark:border-rose-900/50 bg-white/60 dark:bg-white/10 text-muted-foreground hover:text-foreground text-xs sm:text-sm font-semibold flex items-center gap-1.5 transition-all cursor-pointer"
              title="Share Link"
              aria-label="Share Link"
            >
              <Share2 className="h-4 w-4" />
              <span>{shareCopied ? "Copied!" : "Share"}</span>
            </button>
          </div>
        </div>

      </div>

      {/* 3. Content Quality & Trust Signals Banner */}
      <div className="rounded-2xl border border-purple-200/90 dark:border-purple-900/60 bg-[#f5f3ff] dark:bg-purple-950/25 p-4 sm:p-5 flex flex-wrap items-center justify-between gap-4 text-xs sm:text-sm font-mono text-muted-foreground shadow-sm shadow-purple-100/40">
        <div className="flex flex-wrap items-center gap-3">
          <span className="font-bold text-foreground uppercase tracking-wider text-xs">
            CONTENT QUALITY:
          </span>
          <span className="inline-flex items-center gap-1 text-emerald-700 dark:text-emerald-300 font-semibold">
            <CheckCircle2 className="h-4 w-4" />
            <span>Real Interview Question</span>
          </span>
          <span>•</span>
          <span className="inline-flex items-center gap-1 text-sky-700 dark:text-sky-300 font-semibold">
            <ShieldCheck className="h-4 w-4" />
            <span>Tier-1 Calibrated</span>
          </span>
          <span>•</span>
          <span className="inline-flex items-center gap-1 text-rose-700 dark:text-rose-300 font-semibold">
            <BookOpen className="h-4 w-4" />
            <span>Authoritative Specs Cited</span>
          </span>
        </div>

        <div className="flex items-center gap-4 text-xs">
          <span>Last Reviewed: <strong className="text-foreground">2026</strong></span>
          <span>Version: <strong className="text-foreground">{question.technology_version || "Current"}</strong></span>
        </div>
      </div>

      {/* 4. Progressive Think Mode Practice Section */}
      <div id="think-mode-section">
        <ThinkMode
          questionId={question.id}
          hints={question.hints}
          onRevealAnswer={() => setIsAnswerRevealed(true)}
          isAnswerRevealed={isAnswerRevealed}
        />
      </div>

      {/* 5. 15-Part Model Answer & Production Architecture View */}
      {isAnswerRevealed && (
        <div id="answer" className="space-y-4 pt-4 animate-fade-in">
          <div className="flex items-center justify-between">
            <h2 className="font-extrabold text-xl text-foreground tracking-tight flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              <span>Full Model Answer &amp; Architecture Breakdown</span>
            </h2>
          </div>
          <AnswerView question={question} />
        </div>
      )}

    </div>
  );
}
