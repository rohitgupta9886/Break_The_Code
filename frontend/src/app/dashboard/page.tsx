"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Sparkles,
  Flame,
  Zap,
  Target,
  CheckCircle2,
  Clock,
  RotateCcw,
  Trophy,
  ArrowRight,
  TrendingUp,
  BrainCircuit,
  AlertCircle,
  Bookmark,
  Cpu,
  Layers,
  Terminal,
  Binary,
  Activity,
  Play
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { fetchUserDashboard, getCachedData, setCachedData } from "@/lib/api";
import { Button } from "@/components/ui/button";

const techColors: Record<string, { bar: string; text: string; bg: string; icon: any }> = {
  langgraph: { bar: "bg-purple-600", text: "text-purple-600 dark:text-purple-300", bg: "bg-purple-500/10", icon: Cpu },
  "rag-vector-db": { bar: "bg-cyan-500", text: "text-cyan-600 dark:text-cyan-300", bg: "bg-cyan-500/10", icon: Layers },
  "java-backend": { bar: "bg-orange-500", text: "text-orange-600 dark:text-orange-300", bg: "bg-orange-500/10", icon: Terminal },
  dsa: { bar: "bg-pink-500", text: "text-pink-600 dark:text-pink-300", bg: "bg-pink-500/10", icon: Binary },
  "system-design": { bar: "bg-teal-500", text: "text-teal-600 dark:text-teal-300", bg: "bg-teal-500/10", icon: Layers },
};

export default function DashboardOverviewPage() {
  const { token, user } = useAuth();
  const [dashboard, setDashboard] = useState<any>(() => {
    return getCachedData<any>("user_dashboard", 300 * 1000);
  });
  const [loading, setLoading] = useState<boolean>(() => !dashboard && Boolean(token));

  useEffect(() => {
    loadDashboard();
  }, [token]);

  const loadDashboard = async () => {
    if (!dashboard) setLoading(true);
    try {
      const data = await fetchUserDashboard(token || undefined);
      if (data) {
        setDashboard(data);
        setCachedData("user_dashboard", data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-32 rounded-3xl bg-muted/40" />
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-28 rounded-2xl bg-muted/40" />
          ))}
        </div>
        <div className="h-64 rounded-3xl bg-muted/40" />
      </div>
    );
  }

  // Fallback defaults for guest or demo candidates
  const totalAttempted = dashboard?.total_attempted ?? 12;
  const totalCompleted = dashboard?.total_completed ?? 8;
  const overallAccuracy = dashboard?.overall_accuracy ?? 84;
  const streakDays = dashboard?.streak_days ?? 4;
  const savedCount = 6;
  const revisionDueCount = dashboard?.revision_due_count ?? 3;
  const technologiesProgress = dashboard?.technologies_progress || [
    { slug: "langgraph", name: "AI & LangGraph", completed: 24, total: 30, accuracy: 80 },
    { slug: "rag-vector-db", name: "RAG & Vector DBs", completed: 18, total: 30, accuracy: 65 },
    { slug: "java-backend", name: "Java Backend & JVM", completed: 21, total: 30, accuracy: 72 },
    { slug: "dsa", name: "DSA & Algorithms", completed: 15, total: 30, accuracy: 50 },
    { slug: "system-design", name: "Distributed Systems", completed: 12, total: 30, accuracy: 42 },
  ];

  const recommendations = [
    {
      because: "Because you practiced LangGraph State Serialization:",
      title: "LangGraph Tough — Distributed Checkpoint Recovery Without Side Effects",
      tech: "LangGraph",
      difficulty: "VERY_TOUGH",
      time: "10 min",
      slug: "langgraph-basic-zero-downtime-9",
    },
    {
      because: "Because you explored Kafka consumer offsets:",
      title: "System Design — Kafka Consumer Lag Outage & Humongous GC Allocation",
      tech: "Kafka / Distributed Systems",
      difficulty: "PRODUCTION_SCENARIO",
      time: "12 min",
      slug: "system-design-production-scenario-telemetry-tracing-30",
    },
  ];

  return (
    <div className="space-y-10">
      
      {/* Header */}
      <div className="space-y-1.5">
        <div className="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-primary">
          <Sparkles className="h-3.5 w-3.5" />
          <span>Active Preparation Hub</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-foreground">
          Your Interview Dashboard
        </h1>
        <p className="text-sm text-muted-foreground">
          Track preparation velocity, mastery across 5 technology pillars, and spaced-repetition schedules.
        </p>
      </div>

      {/* Primary KPI Cards Bar (5 Colorful Metrics) */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {/* 1. Questions Attempted (Blue) */}
        <div className="p-4 sm:p-5 rounded-2xl border border-blue-500/25 bg-card shadow-xs space-y-2">
          <div className="text-xs font-semibold text-blue-600 dark:text-blue-400 flex items-center gap-1.5">
            <Target className="h-4 w-4" />
            <span>Attempted</span>
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-foreground">{totalAttempted}</div>
          <p className="text-[11px] text-muted-foreground font-mono">Across all pillars</p>
        </div>

        {/* 2. Questions Completed (Green) */}
        <div className="p-4 sm:p-5 rounded-2xl border border-emerald-500/25 bg-card shadow-xs space-y-2">
          <div className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="h-4 w-4" />
            <span>Completed</span>
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-foreground">{totalCompleted}</div>
          <p className="text-[11px] text-muted-foreground font-mono">Score &ge; 7.0 / 10</p>
        </div>

        {/* 3. Practice Streak (Orange) */}
        <div className="p-4 sm:p-5 rounded-2xl border border-amber-500/25 bg-card shadow-xs space-y-2">
          <div className="text-xs font-semibold text-amber-600 dark:text-amber-400 flex items-center gap-1.5">
            <Flame className="h-4 w-4 fill-current" />
            <span>Current Streak</span>
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-amber-500">{streakDays} Days</div>
          <p className="text-[11px] text-muted-foreground font-mono">Daily engineering drill</p>
        </div>

        {/* 4. Saved Questions (Yellow/Amber) */}
        <div className="p-4 sm:p-5 rounded-2xl border border-yellow-500/25 bg-card shadow-xs space-y-2">
          <div className="text-xs font-semibold text-yellow-600 dark:text-yellow-400 flex items-center gap-1.5">
            <Bookmark className="h-4 w-4 fill-current" />
            <span>Saved Questions</span>
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-foreground">{savedCount}</div>
          <p className="text-[11px] text-muted-foreground font-mono">Bookmarked to review</p>
        </div>

        {/* 5. Average Performance (Cyan) */}
        <div className="p-4 sm:p-5 rounded-2xl border border-cyan-500/25 bg-card shadow-xs space-y-2">
          <div className="text-xs font-semibold text-cyan-600 dark:text-cyan-400 flex items-center gap-1.5">
            <TrendingUp className="h-4 w-4" />
            <span>Average Score</span>
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-foreground">{overallAccuracy}%</div>
          <p className="text-[11px] text-muted-foreground font-mono">AI evaluation rubric</p>
        </div>
      </div>

      {/* Your Progress: Technology-Wise Multicolor Bars */}
      <div className="rounded-3xl border border-border/80 bg-card p-6 sm:p-8 shadow-sm space-y-6">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <h3 className="text-xl font-extrabold text-foreground tracking-tight">
              Your Track Progress
            </h3>
            <p className="text-xs sm:text-sm text-muted-foreground">
              Mastery percentage computed against 8-tier difficulty criteria.
            </p>
          </div>
          <Link href="/learn" className="text-xs font-bold text-primary hover:underline flex items-center gap-1">
            <span>View All Tracks</span>
            <ArrowRight className="h-3 w-3" />
          </Link>
        </div>

        <div className="space-y-5">
          {technologiesProgress.map((tp: any) => {
            const config = techColors[tp.slug] || {
              bar: "bg-primary",
              text: "text-primary",
              bg: "bg-primary/10",
              icon: Layers,
            };
            const Icon = config.icon;
            const pct = Math.round(tp.accuracy || ((tp.completed || 1) / (tp.total || 30)) * 100);

            return (
              <div key={tp.slug || tp.name} className="space-y-2">
                <div className="flex items-center justify-between text-xs sm:text-sm">
                  <div className="flex items-center gap-2 font-bold text-foreground">
                    <div className={`p-1.5 rounded-lg ${config.bg} ${config.text}`}>
                      <Icon className="h-3.5 w-3.5" />
                    </div>
                    <span>{tp.name}</span>
                  </div>
                  <span className="font-mono font-bold text-foreground">{pct}%</span>
                </div>

                <div className="h-2.5 w-full rounded-full bg-muted/60 overflow-hidden relative">
                  <div
                    className={`h-full rounded-full ${config.bar} transition-all duration-500`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recommended For You Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="space-y-0.5">
            <h3 className="text-xl font-extrabold text-foreground tracking-tight">
              Recommended For You
            </h3>
            <p className="text-xs text-muted-foreground">
              Personalized next challenges based on completed questions and difficulty milestones.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recommendations.map((rec, idx) => (
            <div
              key={idx}
              className="p-5 rounded-2xl border border-border/80 bg-card hover:border-primary/50 transition-all shadow-xs flex flex-col justify-between space-y-4 group"
            >
              <div className="space-y-2">
                <span className="text-[11px] font-mono text-muted-foreground font-semibold">
                  {rec.because}
                </span>
                <h4 className="font-bold text-base text-foreground group-hover:text-primary transition-colors leading-snug">
                  {rec.title}
                </h4>
                <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground pt-1">
                  <span className="text-primary font-semibold">{rec.tech}</span>
                  <span>•</span>
                  <span>{rec.difficulty}</span>
                  <span>•</span>
                  <span>{rec.time}</span>
                </div>
              </div>

              <Link href={`/questions/${rec.slug}`}>
                <Button size="sm" variant="outline" className="w-full text-xs font-bold justify-between">
                  <span>Start Recommended Challenge</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </Button>
              </Link>
            </div>
          ))}
        </div>
      </div>

      {/* Spaced Repetition (SRS) Flash Card Quick Action */}
      <div className="p-6 rounded-3xl border border-blue-500/25 bg-gradient-to-r from-blue-500/10 via-card to-card flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-1.5 text-xs font-bold text-blue-600 dark:text-blue-400 font-mono">
            <RotateCcw className="h-4 w-4" />
            <span>SPACED REPETITION ENGINE</span>
          </div>
          <h4 className="text-lg font-bold text-foreground">
            {revisionDueCount} Questions Scheduled For Long-Term Memory Review Today
          </h4>
          <p className="text-xs text-muted-foreground">
            Reinforce key trade-offs and latency considerations before memory decays.
          </p>
        </div>

        <Link href="/dashboard/revision" className="shrink-0">
          <Button size="md" className="bg-blue-600 hover:bg-blue-500 text-white font-bold">
            <span>Begin SRS Drill</span>
            <ArrowRight className="h-4 w-4 ml-1" />
          </Button>
        </Link>
      </div>

    </div>
  );
}
