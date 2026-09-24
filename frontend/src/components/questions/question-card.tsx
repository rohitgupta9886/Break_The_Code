"use client";

import React, { useState, memo } from "react";
import Link from "next/link";
import { 
  Clock, 
  Eye, 
  Bookmark, 
  ArrowRight, 
  Zap, 
  Check, 
  Activity, 
  User, 
  BookOpen,
  Building2,
  Briefcase
} from "lucide-react";
import { QuestionCardData, prefetchQuestion } from "@/lib/api";
import { DifficultyBadge, TechnologyBadge, InterviewDepthBadge } from "@/components/ui/badge";

interface QuestionCardProps {
  question: QuestionCardData;
  colorIndex?: number;
}

const QuestionCardComponent: React.FC<QuestionCardProps> = ({ question }) => {
  const [isSaved, setIsSaved] = useState(false);

  const isProduction = question.difficulty === "PRODUCTION_SCENARIO" || question.scenario_type === "PRODUCTION_OUTAGE";

  return (
    <div
      onMouseEnter={() => prefetchQuestion(question.slug)}
      className="group rounded-2xl border border-border/70 hover:border-border-hover bg-surface hover:bg-surface-elevated/70 p-5 sm:p-6 shadow-2xs hover:shadow-elevation-1 transition-all duration-200 flex flex-col justify-between gap-5 relative"
    >
      {/* Top Meta Header */}
      <div className="space-y-3.5">
        <div className="flex items-center justify-between gap-2.5 flex-wrap text-xs sm:text-sm">
          <div className="flex items-center gap-2">
            <TechnologyBadge technology={question.technology_name} size="sm" />
            {question.topic_name && (
              <span className="text-xs font-mono font-medium text-muted-foreground hidden sm:inline">
                {question.topic_name}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <DifficultyBadge difficulty={question.difficulty} size="sm" />
            <InterviewDepthBadge depth={question.interview_depth} />
          </div>
        </div>

        {/* Question Title - Proportional Font & Style */}
        <Link href={`/questions/${question.slug}`} className="block">
          <h3 className="text-base sm:text-lg font-bold text-foreground group-hover:text-primary transition-colors leading-snug tracking-tight">
            {question.title}
          </h3>
        </Link>

        {/* Real Interview Company Provenance */}
        {question.tags && question.tags.length > 0 && (
          <div className="flex items-center gap-1.5 flex-wrap pt-0.5">
            <span className="text-xs font-semibold text-muted-foreground flex items-center gap-1 uppercase tracking-wider">
              <Building2 className="h-3 w-3 text-indigo-400" />
              <span>Real Interview:</span>
            </span>
            {question.tags.map((tag) => {
              const companyClass = {
                google: "bg-blue-500/10 text-blue-700 dark:text-blue-300 border-blue-500/30",
                meta: "bg-sky-500/10 text-sky-700 dark:text-sky-300 border-sky-500/30",
                amazon: "bg-amber-500/10 text-amber-800 dark:text-amber-300 border-amber-500/30",
                netflix: "bg-rose-500/10 text-rose-700 dark:text-rose-300 border-rose-500/30",
                openai: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border-emerald-500/30",
                stripe: "bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 border-indigo-500/30",
                databricks: "bg-orange-500/10 text-orange-700 dark:text-orange-300 border-orange-500/30",
                uber: "bg-neutral-800/10 dark:bg-white/10 text-foreground border-foreground/20",
                apple: "bg-slate-500/10 text-slate-800 dark:text-slate-200 border-slate-500/30",
                microsoft: "bg-cyan-500/10 text-cyan-700 dark:text-cyan-300 border-cyan-500/30",
              }[tag.slug] || "bg-white/90 dark:bg-black/40 text-foreground border-border/80";

              return (
                <span
                  key={tag.slug}
                  className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-bold border shadow-2xs transition-all ${companyClass}`}
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-current opacity-80" />
                  {tag.name}
                </span>
              );
            })}
          </div>
        )}

        {/* Scenario and Target Role Indicators */}
        <div className="flex flex-wrap items-center gap-3 text-xs sm:text-sm text-muted-foreground pt-1">
          {question.interview_round ? (
            <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-2 py-0.5 rounded-md bg-primary/10 text-primary border border-primary/20">
              <Briefcase className="h-3 w-3" />
              <span className="line-clamp-1">{question.interview_round}</span>
            </span>
          ) : isProduction ? (
            <span className="inline-flex items-center gap-1.5 text-teal-700 dark:text-teal-300 font-semibold font-mono text-xs">
              <Activity className="h-3.5 w-3.5 animate-pulse" />
              Production Scenario
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 text-muted-foreground font-mono text-xs">
              <Zap className="h-3.5 w-3.5 text-amber-500" />
              Standard Challenge
            </span>
          )}

          <span className="text-border">•</span>

          <span className="inline-flex items-center gap-1.5 text-xs font-medium">
            <User className="h-3.5 w-3.5 text-muted-foreground" />
            {question.role_target || (
              question.difficulty === "EXPERT_DEEP_DIVE" 
                ? "Staff / Architect" 
                : question.difficulty === "VERY_TOUGH" || question.difficulty === "VERY_VERY_TOUGH" 
                  ? "Senior Specialist" 
                  : "Senior Engineer"
            )}
          </span>

          <span className="text-border">•</span>

          <span className="inline-flex items-center gap-1.5 text-xs font-mono">
            <Clock className="h-3.5 w-3.5 text-muted-foreground" />
            {question.estimated_time_minutes || 10} min
          </span>
        </div>
      </div>

      {/* Bottom Action Buttons: [Think] [View Answer] [Save] */}
      <div className="pt-4 border-t border-border/60 flex items-center justify-between text-xs sm:text-sm">
        <div className="flex items-center gap-2.5">
          {/* Think Mode Action */}
          <Link
            href={`/questions/${question.slug}?mode=think`}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold bg-amber-500/15 text-amber-800 dark:text-amber-200 hover:bg-amber-500/25 transition-colors border border-amber-500/30"
          >
            <Zap className="h-3.5 w-3.5" />
            <span>Think</span>
          </Link>

          {/* View Answer Action */}
          <Link
            href={`/questions/${question.slug}`}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold bg-primary/10 text-primary hover:bg-primary/20 transition-colors border border-primary/25"
          >
            <BookOpen className="h-3.5 w-3.5" />
            <span>View Answer</span>
          </Link>
        </div>

        {/* Save Bookmark Action */}
        <button
          onClick={() => setIsSaved(!isSaved)}
          title={isSaved ? "Saved to bookmarks" : "Save question"}
          className={`flex items-center gap-1 p-2 rounded-xl border transition-all ${
            isSaved 
              ? "bg-amber-500/20 text-amber-600 border-amber-500/40" 
              : "text-muted-foreground hover:text-foreground hover:bg-black/5 dark:hover:bg-white/10 border-transparent"
          }`}
        >
          <Bookmark className={`h-4.5 w-4.5 ${isSaved ? "fill-amber-500 text-amber-500" : ""}`} />
        </button>
      </div>

    </div>
  );
};

export const QuestionCard = memo(QuestionCardComponent);
