"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { 
  Sparkles, 
  Layers, 
  ArrowRight, 
  ShieldCheck, 
  BrainCircuit, 
  Terminal, 
  Flame, 
  AlertTriangle, 
  Crown,
  Clock,
  Compass
} from "lucide-react";
import { fetchQuestionStats } from "@/lib/api";

interface TierCardInfo {
  tier: string;
  label: string;
  tagline: string;
  description: string;
  level: number;
  timeEstimate: string;
  accentColor: string;
  badgeBg: string;
  icon: any;
}

const TIERS: TierCardInfo[] = [
  {
    tier: "BASIC",
    label: "Basic",
    tagline: "Master the Fundamentals",
    description: "Foundational definitions, underlying mechanisms, and core syntax expected of every candidate.",
    level: 1,
    timeEstimate: "3-5 mins",
    accentColor: "from-emerald-500/20 to-teal-500/10 border-emerald-500/30 text-emerald-400",
    badgeBg: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20",
    icon: Compass,
  },
  {
    tier: "MEDIUM",
    label: "Medium",
    tagline: "Build Strong Foundations",
    description: "Standard engineering mechanics, common configurations, state flows, and API contracts.",
    level: 2,
    timeEstimate: "5-7 mins",
    accentColor: "from-sky-500/20 to-blue-500/10 border-sky-500/30 text-sky-400",
    badgeBg: "bg-sky-500/10 text-sky-500 border-sky-500/20",
    icon: Terminal,
  },
  {
    tier: "HARD",
    label: "Hard",
    tagline: "Test Your Technical Depth",
    description: "Nuanced edge cases, internal concurrency primitives, memory management, and runtime bottlenecks.",
    level: 3,
    timeEstimate: "7-10 mins",
    accentColor: "from-amber-500/20 to-yellow-500/10 border-amber-500/30 text-amber-400",
    badgeBg: "bg-amber-500/10 text-amber-500 border-amber-500/20",
    icon: BrainCircuit,
  },
  {
    tier: "TOUGH",
    label: "Tough",
    tagline: "Think Like a Senior Engineer",
    description: "Complex multi-component interactions, non-trivial failure cascades, and algorithm trade-offs.",
    level: 4,
    timeEstimate: "10-12 mins",
    accentColor: "from-purple-500/20 to-violet-500/10 border-purple-500/30 text-purple-400",
    badgeBg: "bg-purple-500/10 text-purple-500 border-purple-500/20",
    icon: Layers,
  },
  {
    tier: "VERY_TOUGH",
    label: "Very Tough",
    tagline: "Senior-Level Challenges",
    description: "Distributed race conditions, zero-downtime migrations, memory-leak diagnostics, and crash recovery.",
    level: 5,
    timeEstimate: "12-15 mins",
    accentColor: "from-rose-500/20 to-pink-500/10 border-rose-500/30 text-rose-400",
    badgeBg: "bg-rose-500/10 text-rose-500 border-rose-500/20",
    icon: Flame,
  },
  {
    tier: "VERY_VERY_TOUGH",
    label: "Very Very Tough",
    tagline: "Expert-Level Problems",
    description: "Extreme scale concurrency, speculative execution swarms, kernel/JVM lock contention, and deep optimizations.",
    level: 6,
    timeEstimate: "15-18 mins",
    accentColor: "from-red-600/20 to-rose-700/10 border-red-500/40 text-red-400",
    badgeBg: "bg-red-500/15 text-red-400 border-red-500/30",
    icon: AlertTriangle,
  },
  {
    tier: "PRODUCTION_SCENARIO",
    label: "Production Scenario",
    tagline: "Real-World Engineering Incidents",
    description: "High-stakes production outages, cascading network partitions, data corruption mitigation, and SLA defenses.",
    level: 7,
    timeEstimate: "15-20 mins",
    accentColor: "from-indigo-500/25 to-purple-600/15 border-indigo-500/40 text-indigo-400",
    badgeBg: "bg-indigo-500/15 text-indigo-400 border-indigo-500/30",
    icon: ShieldCheck,
  },
  {
    tier: "EXPERT_DEEP_DIVE",
    label: "Expert Deep Dive",
    tagline: "Staff & Principal Architect Level",
    description: "End-to-end distributed system design, multi-million QPS throughput budgets, and architectural judgement.",
    level: 8,
    timeEstimate: "20+ mins",
    accentColor: "from-amber-400/25 to-yellow-600/15 border-amber-400/40 text-amber-300",
    badgeBg: "bg-amber-400/15 text-amber-300 border-amber-400/30",
    icon: Crown,
  },
];

export default function DifficultyBrowsePage() {
  const [stats, setStats] = useState<Record<string, number>>({});
  const [totalQuestions, setTotalQuestions] = useState<number>(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuestionStats().then((data) => {
      if (data && data.success) {
        setStats(data.by_difficulty || {});
        setTotalQuestions(data.total_questions || 0);
      }
      setLoading(false);
    });
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 w-full space-y-12">
      {/* Page Header */}
      <div className="space-y-4 max-w-3xl">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-primary/10 text-primary border border-primary/20">
          <Sparkles className="h-3.5 w-3.5" />
          <span>Difficulty-Based Learning Engine</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-foreground">
          Browse by Difficulty
        </h1>
        <p className="text-base text-muted-foreground leading-relaxed">
          Technical interviews test how you reason under escalating complexity. Progressively level up your architectural, 
          debugging, and systems design skills across 8 calibrated difficulty tiers.
        </p>
        <div className="flex items-center gap-4 text-xs font-mono text-muted-foreground pt-2">
          <span>Total Database Questions: <strong className="text-foreground">{totalQuestions || 1200}</strong></span>
          <span>•</span>
          <span>Minimum 30 Questions per Category & Tier</span>
        </div>
      </div>

      {/* 8 Difficulty Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {TIERS.map((tier) => {
          const Icon = tier.icon;
          const count = stats[tier.tier] ?? 150;

          return (
            <Link 
              key={tier.tier}
              href={`/questions?difficulty=${tier.tier}`}
              className="group relative rounded-2xl border bg-card/60 p-6 flex flex-col justify-between transition-all duration-300 hover:shadow-xl hover:-translate-y-1 backdrop-blur-sm"
              style={{
                borderColor: "rgba(255, 255, 255, 0.08)",
              }}
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className={`p-2.5 rounded-xl border ${tier.badgeBg}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-muted/60 text-muted-foreground">
                    LEVEL {tier.level}
                  </span>
                </div>

                <div className="space-y-1.5">
                  <h3 className="text-xl font-bold tracking-tight text-foreground group-hover:text-primary transition-colors">
                    {tier.label}
                  </h3>
                  <p className="text-xs font-semibold text-primary/90">
                    {tier.tagline}
                  </p>
                </div>

                <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">
                  {tier.description}
                </p>
              </div>

              <div className="pt-6 border-t border-border/50 mt-6 flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5 text-muted-foreground font-mono">
                  <Clock className="h-3.5 w-3.5" />
                  <span>{tier.timeEstimate}</span>
                </div>

                <div className="flex items-center gap-1 font-bold text-foreground group-hover:text-primary transition-colors">
                  <span>{loading ? "..." : `${count}+ Questions`}</span>
                  <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
