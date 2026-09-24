"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { 
  Terminal, 
  BookOpen, 
  Layers, 
  Cpu, 
  Flame, 
  Sparkles, 
  CheckCircle2, 
  LayoutDashboard, 
  Bookmark, 
  RotateCcw, 
  History, 
  ChevronDown, 
  ChevronRight,
  Filter,
  Play
} from "lucide-react";
import { cn } from "@/lib/utils";

export const AppSidebar: React.FC = () => {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const currentDiff = searchParams.get("difficulty");
  const currentTech = searchParams.get("technology");

  const [questionsOpen, setQuestionsOpen] = useState(true);
  const [techOpen, setTechOpen] = useState(true);
  const [interviewOpen, setInterviewOpen] = useState(true);
  const [learningOpen, setLearningOpen] = useState(true);

  const difficulties = [
    { label: "All Questions", value: "", count: "1,200" },
    { label: "Level 1 · Basic", value: "BASIC", count: "150" },
    { label: "Level 2 · Medium", value: "MEDIUM", count: "150" },
    { label: "Level 3 · Hard", value: "HARD", count: "150" },
    { label: "Level 4 · Tough", value: "TOUGH", count: "150" },
    { label: "Level 5 · Very Tough", value: "VERY_TOUGH", count: "150" },
    { label: "Level 6 · Very Very Tough", value: "VERY_VERY_TOUGH", count: "150" },
    { label: "Level 7 · Production", value: "PRODUCTION_SCENARIO", count: "150" },
    { label: "Level 8 · Expert", value: "EXPERT_DEEP_DIVE", count: "150" },
  ];

  const technologies = [
    { label: "AI & GenAI", value: "langgraph", icon: Cpu, color: "text-purple-500" },
    { label: "RAG & Vector DBs", value: "rag-vector-db", icon: Layers, color: "text-cyan-500" },
    { label: "Java & JVM", value: "java-backend", icon: Terminal, color: "text-orange-500" },
    { label: "DSA & Algorithms", value: "dsa", icon: Terminal, color: "text-pink-500" },
    { label: "System Design", value: "system-design", icon: Layers, color: "text-teal-500" },
  ];

  return (
    <aside className="w-64 shrink-0 hidden lg:block sticky top-20 self-start max-h-[calc(100vh-6rem)] overflow-y-auto pr-3 space-y-6 select-none font-sans text-xs">
      
      {/* Quick Dashboard Link */}
      <Link
        href="/dashboard"
        className={cn(
          "flex items-center justify-between px-3 py-2 rounded-xl font-semibold transition-all",
          pathname === "/dashboard"
            ? "bg-primary text-primary-foreground shadow-sm"
            : "text-muted-foreground hover:text-foreground hover:bg-muted/60"
        )}
      >
        <span className="flex items-center gap-2">
          <LayoutDashboard className="h-4 w-4" />
          <span>Dashboard</span>
        </span>
        <span className="text-[10px] font-mono opacity-80">Overview</span>
      </Link>

      {/* 1. Questions Section */}
      <div className="space-y-1">
        <button
          onClick={() => setQuestionsOpen(!questionsOpen)}
          className="w-full flex items-center justify-between px-2.5 py-1.5 text-muted-foreground hover:text-foreground font-bold uppercase tracking-wider text-[10px]"
        >
          <span className="flex items-center gap-1.5">
            <BookOpen className="h-3.5 w-3.5 text-primary" />
            Questions
          </span>
          {questionsOpen ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
        </button>

        {questionsOpen && (
          <div className="space-y-0.5 pl-2 border-l border-border/60 ml-2.5 pt-1">
            {difficulties.map((diff) => {
              const isActive = pathname === "/questions" && (
                (!diff.value && !currentDiff) || currentDiff === diff.value
              );

              return (
                <Link
                  key={diff.label}
                  href={diff.value ? `/questions?difficulty=${diff.value}` : "/questions"}
                  className={cn(
                    "flex items-center justify-between px-2.5 py-1.5 rounded-lg font-medium transition-colors",
                    isActive
                      ? "bg-primary/10 text-primary font-bold"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted/40"
                  )}
                >
                  <span className="truncate">{diff.label}</span>
                  <span className="text-[10px] font-mono text-muted-foreground/60">{diff.count}</span>
                </Link>
              );
            })}
          </div>
        )}
      </div>

      {/* 2. Technologies Section */}
      <div className="space-y-1">
        <button
          onClick={() => setTechOpen(!techOpen)}
          className="w-full flex items-center justify-between px-2.5 py-1.5 text-muted-foreground hover:text-foreground font-bold uppercase tracking-wider text-[10px]"
        >
          <span className="flex items-center gap-1.5">
            <Layers className="h-3.5 w-3.5 text-teal-500" />
            Technologies
          </span>
          {techOpen ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
        </button>

        {techOpen && (
          <div className="space-y-0.5 pl-2 border-l border-border/60 ml-2.5 pt-1">
            {technologies.map((t) => {
              const Icon = t.icon;
              const isActive = pathname === "/questions" && currentTech === t.value;

              return (
                <Link
                  key={t.value}
                  href={`/questions?technology=${t.value}`}
                  className={cn(
                    "flex items-center justify-between px-2.5 py-1.5 rounded-lg font-medium transition-colors",
                    isActive
                      ? "bg-primary/10 text-primary font-bold"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted/40"
                  )}
                >
                  <span className="flex items-center gap-2 truncate">
                    <Icon className={cn("h-3 w-3", t.color)} />
                    <span>{t.label}</span>
                  </span>
                  <span className="text-[10px] font-mono text-muted-foreground/60">240</span>
                </Link>
              );
            })}
          </div>
        )}
      </div>

      {/* 3. Interview Modes */}
      <div className="space-y-1">
        <button
          onClick={() => setInterviewOpen(!interviewOpen)}
          className="w-full flex items-center justify-between px-2.5 py-1.5 text-muted-foreground hover:text-foreground font-bold uppercase tracking-wider text-[10px]"
        >
          <span className="flex items-center gap-1.5">
            <Play className="h-3.5 w-3.5 text-amber-500" />
            Interview Modes
          </span>
          {interviewOpen ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
        </button>

        {interviewOpen && (
          <div className="space-y-0.5 pl-2 border-l border-border/60 ml-2.5 pt-1">
            <Link
              href="/questions?difficulty=PRODUCTION_SCENARIO"
              className="flex items-center justify-between px-2.5 py-1.5 rounded-lg font-medium text-muted-foreground hover:text-foreground hover:bg-muted/40 transition-colors"
            >
              <span className="flex items-center gap-2">
                <Flame className="h-3 w-3 text-amber-500" />
                <span>Incident Drill</span>
              </span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-amber-500/10 text-amber-600 font-bold">HOT</span>
            </Link>
            <Link
              href="/difficulty"
              className="flex items-center justify-between px-2.5 py-1.5 rounded-lg font-medium text-muted-foreground hover:text-foreground hover:bg-muted/40 transition-colors"
            >
              <span className="flex items-center gap-2">
                <Sparkles className="h-3 w-3 text-purple-500" />
                <span>Difficulty Progression</span>
              </span>
              <span className="text-[10px] font-mono text-muted-foreground/60">8 Tiers</span>
            </Link>
          </div>
        )}
      </div>

      {/* 4. My Learning */}
      <div className="space-y-1">
        <button
          onClick={() => setLearningOpen(!learningOpen)}
          className="w-full flex items-center justify-between px-2.5 py-1.5 text-muted-foreground hover:text-foreground font-bold uppercase tracking-wider text-[10px]"
        >
          <span className="flex items-center gap-1.5">
            <Bookmark className="h-3.5 w-3.5 text-emerald-500" />
            My Learning
          </span>
          {learningOpen ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
        </button>

        {learningOpen && (
          <div className="space-y-0.5 pl-2 border-l border-border/60 ml-2.5 pt-1">
            <Link
              href="/dashboard/bookmarks"
              className="flex items-center justify-between px-2.5 py-1.5 rounded-lg font-medium text-muted-foreground hover:text-foreground hover:bg-muted/40 transition-colors"
            >
              <span className="flex items-center gap-2">
                <Bookmark className="h-3 w-3 text-amber-500" />
                <span>Saved Questions</span>
              </span>
            </Link>
            <Link
              href="/dashboard/revision"
              className="flex items-center justify-between px-2.5 py-1.5 rounded-lg font-medium text-muted-foreground hover:text-foreground hover:bg-muted/40 transition-colors"
            >
              <span className="flex items-center gap-2">
                <RotateCcw className="h-3 w-3 text-blue-500" />
                <span>Spaced Repetition</span>
              </span>
            </Link>
            <Link
              href="/dashboard/history"
              className="flex items-center justify-between px-2.5 py-1.5 rounded-lg font-medium text-muted-foreground hover:text-foreground hover:bg-muted/40 transition-colors"
            >
              <span className="flex items-center gap-2">
                <History className="h-3 w-3 text-purple-500" />
                <span>Attempt History</span>
              </span>
            </Link>
          </div>
        )}
      </div>

    </aside>
  );
};
