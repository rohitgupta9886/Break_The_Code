import React from "react";
import Link from "next/link";
import { Layers, ArrowRight, Cpu, Database, Terminal, Binary, Sparkles, BookOpen, Target, Zap } from "lucide-react";
import { fetchTechnologies } from "@/lib/api";

const techStyles: Record<string, {
  color: string;
  badgeBg: string;
  badgeText: string;
  borderColor: string;
  hoverBorder: string;
  iconBg: string;
  icon: any;
}> = {
  langgraph: {
    color: "#7c3aed",
    badgeBg: "bg-purple-500/10",
    badgeText: "text-purple-600 dark:text-purple-300",
    borderColor: "border-purple-500/25",
    hoverBorder: "hover:border-purple-500/60",
    iconBg: "bg-purple-500/10 text-purple-600 dark:text-purple-400",
    icon: Cpu,
  },
  "rag-vector-db": {
    color: "#06b6d4",
    badgeBg: "bg-cyan-500/10",
    badgeText: "text-cyan-600 dark:text-cyan-300",
    borderColor: "border-cyan-500/25",
    hoverBorder: "hover:border-cyan-500/60",
    iconBg: "bg-cyan-500/10 text-cyan-600 dark:text-cyan-400",
    icon: Database,
  },
  "java-backend": {
    color: "#ea580c",
    badgeBg: "bg-orange-500/10",
    badgeText: "text-orange-600 dark:text-orange-300",
    borderColor: "border-orange-500/25",
    hoverBorder: "hover:border-orange-500/60",
    iconBg: "bg-orange-500/10 text-orange-600 dark:text-orange-400",
    icon: Terminal,
  },
  dsa: {
    color: "#a855f7",
    badgeBg: "bg-pink-500/10",
    badgeText: "text-pink-600 dark:text-pink-300",
    borderColor: "border-pink-500/25",
    hoverBorder: "hover:border-pink-500/60",
    iconBg: "bg-pink-500/10 text-pink-600 dark:text-pink-400",
    icon: Binary,
  },
  "system-design": {
    color: "#0d9488",
    badgeBg: "bg-teal-500/10",
    badgeText: "text-teal-600 dark:text-teal-300",
    borderColor: "border-teal-500/25",
    hoverBorder: "hover:border-teal-500/60",
    iconBg: "bg-teal-500/10 text-teal-600 dark:text-teal-400",
    icon: Layers,
  },
};

export const revalidate = 60;

export default async function LearnPage() {
  const technologies = await fetchTechnologies();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Header */}
      <div className="space-y-3">
        <div className="inline-flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-primary">
          <Sparkles className="h-4 w-4" />
          <span>Curriculum & Learning Tracks</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-foreground">
          Engineering Preparation Tracks
        </h1>
        <p className="text-sm sm:text-base text-muted-foreground max-w-2xl leading-relaxed">
          Select a technical track to practice conceptual foundations, deep implementation patterns, and production scenario trade-offs across 8 calibrated difficulty tiers.
        </p>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {technologies.map((tech) => {
          const style = techStyles[tech.slug] || {
            color: "#3b82f6",
            badgeBg: "bg-primary/10",
            badgeText: "text-primary",
            borderColor: "border-border/80",
            hoverBorder: "hover:border-primary/60",
            iconBg: "bg-primary/10 text-primary",
            icon: Layers,
          };
          const Icon = style.icon;

          return (
            <div
              key={tech.id}
              className={`rounded-3xl border ${style.borderColor} ${style.hoverBorder} bg-card p-6 shadow-sm hover:shadow-xl transition-all duration-200 flex flex-col justify-between hover:-translate-y-1`}
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className={`h-11 w-11 rounded-xl ${style.iconBg} border border-border/40 flex items-center justify-center`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <span className={`text-xs font-mono font-bold px-3 py-1 rounded-full ${style.badgeBg} ${style.badgeText} border border-border/40`}>
                    {tech.question_count || 240} Questions
                  </span>
                </div>

                <div className="space-y-2">
                  <h3 className="text-xl font-bold text-foreground">{tech.name}</h3>
                  <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                    {tech.short_description || "Comprehensive interview preparation calibrated across 8 difficulty tiers with production trade-offs."}
                  </p>
                </div>

                {/* 8 Difficulty Tiers Bar */}
                <div className="pt-2">
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

                {/* Topics list */}
                {tech.topics && tech.topics.length > 0 && (
                  <div className="pt-3 flex flex-wrap gap-1.5">
                    {tech.topics.map((t) => (
                      <span
                        key={t.id}
                        className="text-[11px] font-mono px-2 py-0.5 rounded-md bg-muted/60 text-muted-foreground border border-border/40"
                      >
                        {t.name}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div className="mt-6 pt-4 border-t border-border/60 space-y-2.5">
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
                  <span className="text-[11px] text-rose-100/90 leading-tight mt-1">
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
                  <span className="text-[11px] text-muted-foreground leading-tight mt-1">
                    Practice Mode: Test your knowledge with interactive question-by-question practice.
                  </span>
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
