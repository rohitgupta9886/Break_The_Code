"use client";

import React from "react";
import Link from "next/link";
import { 
  Bot, 
  Database, 
  Coffee, 
  Binary, 
  Layers, 
  ArrowRight, 
  Sparkles, 
  Cpu, 
  Server, 
  Terminal, 
  Activity, 
  Zap,
  Network,
  BookOpen,
  Target
} from "lucide-react";
import { TechnologyData } from "@/lib/api";

const techStyles: Record<string, {
  color: string;
  cardBg: string;
  badgeBg: string;
  badgeText: string;
  borderColor: string;
  hoverBorder: string;
  iconBg: string;
  iconColor: string;
  icon: any;
}> = {
  langgraph: {
    color: "#7c3aed",
    cardBg: "bg-[#f5f3ff] dark:bg-purple-950/25",
    badgeBg: "bg-purple-100/90 dark:bg-purple-900/50",
    badgeText: "text-purple-800 dark:text-purple-200",
    borderColor: "border-purple-200/90 dark:border-purple-900/60",
    hoverBorder: "hover:border-purple-400 dark:hover:border-purple-600",
    iconBg: "bg-purple-100 text-purple-700 dark:bg-purple-900/60 dark:text-purple-300",
    iconColor: "text-purple-600",
    icon: Cpu,
  },
  "rag-vector-db": {
    color: "#06b6d4",
    cardBg: "bg-[#f0f9ff] dark:bg-sky-950/25",
    badgeBg: "bg-sky-100/90 dark:bg-sky-900/50",
    badgeText: "text-sky-800 dark:text-sky-200",
    borderColor: "border-sky-200/90 dark:border-sky-900/60",
    hoverBorder: "hover:border-sky-400 dark:hover:border-sky-600",
    iconBg: "bg-sky-100 text-sky-700 dark:bg-sky-900/60 dark:text-sky-300",
    iconColor: "text-sky-600",
    icon: Database,
  },
  "java-backend": {
    color: "#ea580c",
    cardBg: "bg-[#fff7ed] dark:bg-orange-950/25",
    badgeBg: "bg-orange-100/90 dark:bg-orange-900/50",
    badgeText: "text-orange-800 dark:text-orange-200",
    borderColor: "border-orange-200/90 dark:border-orange-900/60",
    hoverBorder: "hover:border-orange-400 dark:hover:border-orange-600",
    iconBg: "bg-orange-100 text-orange-700 dark:bg-orange-900/60 dark:text-orange-300",
    iconColor: "text-orange-600",
    icon: Terminal,
  },
  dsa: {
    color: "#e11d48",
    cardBg: "bg-[#fff1f4] dark:bg-rose-950/25",
    badgeBg: "bg-rose-100/90 dark:bg-rose-900/50",
    badgeText: "text-rose-800 dark:text-rose-200",
    borderColor: "border-rose-200/90 dark:border-rose-900/60",
    hoverBorder: "hover:border-rose-400 dark:hover:border-rose-600",
    iconBg: "bg-rose-100 text-rose-700 dark:bg-rose-900/60 dark:text-rose-300",
    iconColor: "text-rose-600",
    icon: Binary,
  },
  "system-design": {
    color: "#0d9488",
    cardBg: "bg-[#f0fdfa] dark:bg-teal-950/25",
    badgeBg: "bg-teal-100/90 dark:bg-teal-900/50",
    badgeText: "text-teal-800 dark:text-teal-200",
    borderColor: "border-teal-200/90 dark:border-teal-900/60",
    hoverBorder: "hover:border-teal-400 dark:hover:border-teal-600",
    iconBg: "bg-teal-100 text-teal-700 dark:bg-teal-900/60 dark:text-teal-300",
    iconColor: "text-teal-600",
    icon: Layers,
  },
};

interface TrackGridProps {
  technologies: TechnologyData[];
}

export const TrackGrid: React.FC<TrackGridProps> = ({ technologies }) => {
  return (
    <section className="w-full py-20 bg-muted/20 border-y border-border/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-4">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-primary/10 text-primary border border-primary/20">
              <Sparkles className="h-3.5 w-3.5" />
              <span>Technology Specializations</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight text-foreground">
              Explore By Technology
            </h2>
            <p className="text-sm sm:text-base text-muted-foreground max-w-2xl leading-relaxed">
              Calibrated interview question collections with unique architectural failure modes, 
              concurrency traps, and production trade-offs across modern engineering stacks.
            </p>
          </div>
          <Link
            href="/questions"
            className="text-xs sm:text-sm font-bold text-primary hover:text-primary-hover flex items-center gap-1.5 group shrink-0"
          >
            <span>Explore All 1,200+ Questions</span>
            <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        {/* Technology Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {technologies.map((tech) => {
            const style = techStyles[tech.slug] || {
              color: "#e11d48",
              cardBg: "bg-[#fff1f4] dark:bg-rose-950/25",
              badgeBg: "bg-rose-100/90 dark:bg-rose-900/50",
              badgeText: "text-rose-800 dark:text-rose-200",
              borderColor: "border-rose-200/90 dark:border-rose-900/60",
              hoverBorder: "hover:border-rose-400 dark:hover:border-rose-600",
              iconBg: "bg-rose-100 text-rose-700 dark:bg-rose-900/60",
              iconColor: "text-rose-600",
              icon: Layers,
            };
            const Icon = style.icon;

            return (
              <div
                key={tech.id}
                className={`group relative rounded-3xl border ${style.borderColor} ${style.hoverBorder} ${style.cardBg} p-6 sm:p-7 shadow-sm hover:shadow-xl transition-all duration-200 flex flex-col justify-between hover:-translate-y-1.5`}
              >
                {/* Top Header */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className={`h-11 w-11 rounded-xl ${style.iconBg} border border-border/40 flex items-center justify-center transition-transform duration-200 group-hover:scale-105 shadow-sm`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    <span className={`text-xs font-mono font-bold px-3 py-1 rounded-full ${style.badgeBg} ${style.badgeText} border border-border/40 shadow-xs`}>
                      {tech.question_count || 240} Questions
                    </span>
                  </div>

                  <div className="space-y-2">
                    <h3 className="text-xl font-extrabold text-foreground group-hover:text-primary transition-colors flex items-center justify-between">
                      <span>{tech.name}</span>
                    </h3>
                    <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed line-clamp-2">
                      {tech.short_description || "Comprehensive interview questions calibrated across 8 difficulty tiers with production trade-offs."}
                    </p>
                  </div>
                </div>

                {/* Difficulty Distribution Mini Bar & Topic Chips */}
                <div className="mt-5 pt-3.5 border-t border-border/60 space-y-3">
                  <div>
                    <div className="flex items-center justify-between text-[11px] font-mono text-muted-foreground mb-1.5">
                      <span>8 Difficulty Tiers</span>
                      <span className="font-semibold text-foreground">30 / tier</span>
                    </div>
                    <div className="grid grid-cols-8 gap-1 h-1.5 w-full rounded-full overflow-hidden bg-muted">
                      <div className="bg-emerald-500 rounded-sm" title="Basic (30)" />
                      <div className="bg-sky-500 rounded-sm" title="Medium (30)" />
                      <div className="bg-indigo-500 rounded-sm" title="Hard (30)" />
                      <div className="bg-amber-500 rounded-sm" title="Tough (30)" />
                      <div className="bg-orange-600 rounded-sm" title="Very Tough (30)" />
                      <div className="bg-rose-600 rounded-sm" title="Very Very Tough (30)" />
                      <div className="bg-teal-500 rounded-sm" title="Production Scenario (30)" />
                      <div className="bg-purple-600 rounded-sm" title="Expert Deep Dive (30)" />
                    </div>
                  </div>
                  
                  {/* Topic Chips */}
                  {tech.topics && tech.topics.length > 0 && (
                    <div className="flex flex-wrap gap-1.5">
                      {tech.topics.slice(0, 3).map((topic) => (
                        <span
                          key={topic.id}
                          className="text-[10px] px-2 py-0.5 rounded-md bg-muted/60 text-muted-foreground font-mono"
                        >
                          {topic.name}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Dual Mode Actions */}
                  <div className="space-y-2.5 pt-3 border-t border-border/40">
                    <Link
                      href={`/questions-and-answers/${tech.slug}`}
                      className="flex flex-col p-3 rounded-2xl bg-rose-600 hover:bg-rose-500 text-white shadow-sm hover:shadow-md transition-all duration-150 group"
                    >
                      <div className="flex items-center justify-between font-extrabold text-xs">
                        <span className="flex items-center gap-1.5">
                          <BookOpen className="h-4 w-4 shrink-0" />
                          <span>Read Questions &amp; Answers</span>
                        </span>
                        <ArrowRight className="h-3.5 w-3.5 opacity-90 group-hover:translate-x-1 transition-transform" />
                      </div>
                      <span className="text-[11px] text-rose-100/90 leading-tight mt-1 text-left">
                        Read Mode: Read, revise and understand all interview questions on one page.
                      </span>
                    </Link>

                    <Link
                      href={`/questions?technology=${tech.slug}`}
                      className="flex flex-col p-3 rounded-2xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-800 dark:text-amber-200 transition-all duration-150 group shadow-2xs"
                    >
                      <div className="flex items-center justify-between font-extrabold text-xs">
                        <span className="flex items-center gap-1.5">
                          <Zap className="h-4 w-4 text-amber-500 shrink-0" />
                          <span>Practice Mode</span>
                        </span>
                        <ArrowRight className="h-3.5 w-3.5 text-amber-500 opacity-80 group-hover:translate-x-1 transition-transform" />
                      </div>
                      <span className="text-[11px] text-muted-foreground leading-tight mt-1 text-left">
                        Practice Mode: Test your knowledge with interactive question-by-question practice.
                      </span>
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
