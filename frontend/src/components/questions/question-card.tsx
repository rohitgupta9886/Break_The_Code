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

const cardThemes = [
  {
    bg: "bg-[#fff1f4] dark:bg-rose-950/30",
    border: "border-rose-200/90 dark:border-rose-900/60 hover:border-rose-400 dark:hover:border-rose-600",
    hoverShadow: "hover:shadow-lg hover:shadow-rose-100/70 dark:hover:shadow-none",
    titleHover: "group-hover:text-rose-600 dark:group-hover:text-rose-400",
    accentBorder: "border-rose-200/70 dark:border-rose-900/50",
    pillBg: "bg-rose-100/80 text-rose-800 dark:bg-rose-900/40 dark:text-rose-200",
  },
  {
    bg: "bg-[#f5f3ff] dark:bg-purple-950/30",
    border: "border-purple-200/90 dark:border-purple-900/60 hover:border-purple-400 dark:hover:border-purple-600",
    hoverShadow: "hover:shadow-lg hover:shadow-purple-100/70 dark:hover:shadow-none",
    titleHover: "group-hover:text-purple-600 dark:group-hover:text-purple-400",
    accentBorder: "border-purple-200/70 dark:border-purple-900/50",
    pillBg: "bg-purple-100/80 text-purple-800 dark:bg-purple-900/40 dark:text-purple-200",
  },
  {
    bg: "bg-[#fffbeb] dark:bg-amber-950/30",
    border: "border-amber-200/90 dark:border-amber-900/60 hover:border-amber-400 dark:hover:border-amber-600",
    hoverShadow: "hover:shadow-lg hover:shadow-amber-100/70 dark:hover:shadow-none",
    titleHover: "group-hover:text-amber-600 dark:group-hover:text-amber-400",
    accentBorder: "border-amber-200/70 dark:border-amber-900/50",
    pillBg: "bg-amber-100/80 text-amber-800 dark:bg-amber-900/40 dark:text-amber-200",
  },
  {
    bg: "bg-[#ecfdf5] dark:bg-emerald-950/30",
    border: "border-emerald-200/90 dark:border-emerald-900/60 hover:border-emerald-400 dark:hover:border-emerald-600",
    hoverShadow: "hover:shadow-lg hover:shadow-emerald-100/70 dark:hover:shadow-none",
    titleHover: "group-hover:text-emerald-600 dark:group-hover:text-emerald-400",
    accentBorder: "border-emerald-200/70 dark:border-emerald-900/50",
    pillBg: "bg-emerald-100/80 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-200",
  },
  {
    bg: "bg-[#f0f9ff] dark:bg-sky-950/30",
    border: "border-sky-200/90 dark:border-sky-900/60 hover:border-sky-400 dark:hover:border-sky-600",
    hoverShadow: "hover:shadow-lg hover:shadow-sky-100/70 dark:hover:shadow-none",
    titleHover: "group-hover:text-sky-600 dark:group-hover:text-sky-400",
    accentBorder: "border-sky-200/70 dark:border-sky-900/50",
    pillBg: "bg-sky-100/80 text-sky-800 dark:bg-sky-900/40 dark:text-sky-200",
  },
  {
    bg: "bg-[#fff7ed] dark:bg-orange-950/30",
    border: "border-orange-200/90 dark:border-orange-900/60 hover:border-orange-400 dark:hover:border-orange-600",
    hoverShadow: "hover:shadow-lg hover:shadow-orange-100/70 dark:hover:shadow-none",
    titleHover: "group-hover:text-orange-600 dark:group-hover:text-orange-400",
    accentBorder: "border-orange-200/70 dark:border-orange-900/50",
    pillBg: "bg-orange-100/80 text-orange-800 dark:bg-orange-900/40 dark:text-orange-200",
  },
  {
    bg: "bg-[#fdf4ff] dark:bg-fuchsia-950/30",
    border: "border-fuchsia-200/90 dark:border-fuchsia-900/60 hover:border-fuchsia-400 dark:hover:border-fuchsia-600",
    hoverShadow: "hover:shadow-lg hover:shadow-fuchsia-100/70 dark:hover:shadow-none",
    titleHover: "group-hover:text-fuchsia-600 dark:group-hover:text-fuchsia-400",
    accentBorder: "border-fuchsia-200/70 dark:border-fuchsia-900/50",
    pillBg: "bg-fuchsia-100/80 text-fuchsia-800 dark:bg-fuchsia-900/40 dark:text-fuchsia-200",
  },
  {
    bg: "bg-[#f0fdfa] dark:bg-teal-950/30",
    border: "border-teal-200/90 dark:border-teal-900/60 hover:border-teal-400 dark:hover:border-teal-600",
    hoverShadow: "hover:shadow-lg hover:shadow-teal-100/70 dark:hover:shadow-none",
    titleHover: "group-hover:text-teal-600 dark:group-hover:text-teal-400",
    accentBorder: "border-teal-200/70 dark:border-teal-900/50",
    pillBg: "bg-teal-100/80 text-teal-800 dark:bg-teal-900/40 dark:text-teal-200",
  },
];

function getHash(str: string) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

const QuestionCardComponent: React.FC<QuestionCardProps> = ({ question, colorIndex }) => {
  const [isSaved, setIsSaved] = useState(false);

  const themeIdx = colorIndex !== undefined 
    ? Math.abs(colorIndex) % cardThemes.length 
    : getHash(question.id || question.slug) % cardThemes.length;
  const theme = cardThemes[themeIdx];

  const isProduction = question.difficulty === "PRODUCTION_SCENARIO" || question.scenario_type === "PRODUCTION_OUTAGE";

  return (
    <div
      onMouseEnter={() => prefetchQuestion(question.slug)}
      className={`group rounded-2xl border ${theme.border} ${theme.bg} p-6 ${theme.hoverShadow} transition-all duration-200 flex flex-col justify-between gap-5 relative`}
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
          <h3 className={`text-base sm:text-lg font-black text-foreground ${theme.titleHover} transition-colors leading-snug tracking-tight`}>
            {question.title}
          </h3>
        </Link>

        {/* Real Interview Company Provenance */}
        {question.tags && question.tags.length > 0 && (
          <div className="flex items-center gap-1.5 flex-wrap pt-0.5">
            <span className="text-xs font-bold text-muted-foreground flex items-center gap-1 uppercase tracking-wider">
              <Building2 className="h-3 w-3 text-rose-500" />
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
      <div className={`pt-4 border-t ${theme.accentBorder} flex items-center justify-between text-xs sm:text-sm`}>
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
