"use client";

import React from "react";
import Link from "next/link";
import { 
  ArrowRight, 
  Sparkles, 
  Flame, 
  Activity, 
  ShieldCheck, 
  Terminal, 
  Layers, 
  Zap, 
  Award,
  ChevronRight
} from "lucide-react";

interface DifficultyTierCard {
  level: number;
  tier: string;
  milestone: string;
  title: string;
  description: string;
  questionsCount: string;
  colorBorder: string;
  colorHoverBorder: string;
  colorBadge: string;
  colorBg: string;
  accentColor: string;
  targetRole: string;
}

const tiersData: DifficultyTierCard[] = [
  {
    level: 1,
    tier: "BASIC",
    milestone: "FOUNDATION",
    title: "Basic",
    description: "Foundational definitions, underlying syntax, execution flow, and essential terminology.",
    questionsCount: "150+ Questions",
    colorBorder: "border-emerald-500/25",
    colorHoverBorder: "hover:border-emerald-500/60",
    colorBadge: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20",
    colorBg: "bg-emerald-500/5",
    accentColor: "text-emerald-500",
    targetRole: "Junior to Mid Engineer",
  },
  {
    level: 2,
    tier: "MEDIUM",
    milestone: "INTERMEDIATE",
    title: "Medium",
    description: "Standard engineering mechanics, component APIs, data flows, and state management patterns.",
    questionsCount: "150+ Questions",
    colorBorder: "border-sky-500/25",
    colorHoverBorder: "hover:border-sky-500/60",
    colorBadge: "bg-sky-500/10 text-sky-600 dark:text-sky-400 border-sky-500/20",
    colorBg: "bg-sky-500/5",
    accentColor: "text-sky-500",
    targetRole: "Mid-Level Software Engineer",
  },
  {
    level: 3,
    tier: "HARD",
    milestone: "ADVANCED",
    title: "Hard",
    description: "Nuanced edge cases, runtime bottlenecks, internal concurrency primitives, and memory behavior.",
    questionsCount: "150+ Questions",
    colorBorder: "border-indigo-500/25",
    colorHoverBorder: "hover:border-indigo-500/60",
    colorBadge: "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/20",
    colorBg: "bg-indigo-500/5",
    accentColor: "text-indigo-500",
    targetRole: "Senior Engineer",
  },
  {
    level: 4,
    tier: "TOUGH",
    milestone: "SENIOR",
    title: "Tough",
    description: "Multi-component cascades, non-trivial failure modes, memory leaks, and subtle algorithmic trade-offs.",
    questionsCount: "150+ Questions",
    colorBorder: "border-amber-500/25",
    colorHoverBorder: "hover:border-amber-500/60",
    colorBadge: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20",
    colorBg: "bg-amber-500/5",
    accentColor: "text-amber-500",
    targetRole: "Senior Engineer II",
  },
  {
    level: 5,
    tier: "VERY_TOUGH",
    milestone: "EXPERT",
    title: "Very Tough",
    description: "Designed for engineers who must reason beyond textbook answers: distributed race conditions and recovery.",
    questionsCount: "150+ Questions",
    colorBorder: "border-orange-600/25",
    colorHoverBorder: "hover:border-orange-600/60",
    colorBadge: "bg-orange-600/10 text-orange-600 dark:text-orange-400 border-orange-600/20",
    colorBg: "bg-orange-600/5",
    accentColor: "text-orange-600",
    targetRole: "Lead / Senior Specialist",
  },
  {
    level: 6,
    tier: "VERY_VERY_TOUGH",
    milestone: "PRINCIPAL",
    title: "Very Very Tough",
    description: "Extreme concurrency, speculative execution swarms, JVM / kernel lock contention, and high-frequency scale.",
    questionsCount: "150+ Questions",
    colorBorder: "border-rose-600/30",
    colorHoverBorder: "hover:border-rose-600/70",
    colorBadge: "bg-rose-600/15 text-rose-600 dark:text-rose-400 border-rose-600/30",
    colorBg: "bg-rose-600/5",
    accentColor: "text-rose-600",
    targetRole: "Principal Engineer",
  },
  {
    level: 7,
    tier: "PRODUCTION_SCENARIO",
    milestone: "PRODUCTION",
    title: "Production Scenario",
    description: "High-stakes production outages, cascading network partitions, telemetry forensics, and SLA defense.",
    questionsCount: "150+ Questions",
    colorBorder: "border-teal-500/35",
    colorHoverBorder: "hover:border-teal-500/70",
    colorBadge: "bg-teal-500/15 text-teal-600 dark:text-teal-300 border-teal-500/30",
    colorBg: "bg-teal-500/10",
    accentColor: "text-teal-500",
    targetRole: "Staff / Production Engineer",
  },
  {
    level: 8,
    tier: "EXPERT_DEEP_DIVE",
    milestone: "ARCHITECT",
    title: "Expert Deep Dive",
    description: "End-to-end distributed system design, multi-million QPS throughput budgets, and high-level architectural judgement.",
    questionsCount: "150+ Questions",
    colorBorder: "border-purple-600/35",
    colorHoverBorder: "hover:border-purple-600/70",
    colorBadge: "bg-purple-600/15 text-purple-600 dark:text-purple-300 border-purple-600/30",
    colorBg: "bg-purple-600/10",
    accentColor: "text-purple-500",
    targetRole: "Principal / Enterprise Architect",
  },
];

export const DifficultyExplorer: React.FC = () => {
  return (
    <section className="w-full py-20 bg-background relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Heading */}
        <div className="text-center max-w-3xl mx-auto mb-14 space-y-3">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-primary/10 text-primary border border-primary/20">
            <Layers className="h-3.5 w-3.5" />
            <span>Progressive Interview Depth</span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-foreground">
            How Far Can You Go?
          </h2>
          <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
            Move step-by-step from core syntax to production war-room diagnosis and high-throughput architectural defense.
          </p>

          {/* Horizontal Progression Ribbon */}
          <div className="hidden lg:flex items-center justify-center gap-2 pt-6 overflow-x-auto select-none">
            {tiersData.map((tier, idx) => (
              <React.Fragment key={tier.level}>
                <span className={`px-2.5 py-1 rounded-lg text-[10px] font-mono font-bold tracking-wider border ${tier.colorBadge}`}>
                  {tier.milestone}
                </span>
                {idx < tiersData.length - 1 && (
                  <ChevronRight className="h-3.5 w-3.5 text-muted-foreground/40 shrink-0" />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* 8 Difficulty Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {tiersData.map((item) => (
            <div
              key={item.level}
              className={`rounded-2xl border ${item.colorBorder} ${item.colorHoverBorder} bg-card p-5 shadow-sm hover:shadow-xl transition-all duration-200 flex flex-col justify-between group hover:-translate-y-1`}
            >
              <div className="space-y-3.5">
                {/* Level Tag & Badge */}
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-muted-foreground">
                    LEVEL {item.level}
                  </span>
                  <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${item.colorBadge}`}>
                    {item.milestone}
                  </span>
                </div>

                <div className="space-y-1.5">
                  <h3 className="text-lg font-extrabold text-foreground group-hover:text-primary transition-colors">
                    {item.title}
                  </h3>
                  <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">
                    {item.description}
                  </p>
                </div>
              </div>

              <div className="mt-5 pt-3.5 border-t border-border/60 space-y-3">
                <div className="flex items-center justify-between text-[11px] font-mono text-muted-foreground">
                  <span>{item.targetRole}</span>
                  <span className="font-bold text-foreground">{item.questionsCount}</span>
                </div>

                <Link
                  href={`/questions?difficulty=${item.tier}`}
                  className="w-full inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold bg-muted/50 hover:bg-primary hover:text-primary-foreground transition-all duration-150 group-hover:shadow-sm"
                >
                  <span>Explore Questions</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};
