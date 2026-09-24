"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { 
  Sparkles, 
  ArrowRight, 
  ShieldCheck, 
  Terminal, 
  Code2, 
  Layers, 
  Cpu, 
  Play, 
  Bug, 
  Maximize2, 
  CheckCircle2, 
  Flame, 
  Activity,
  Zap,
  Server
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { fetchGlobalStats } from "@/lib/api";

const workflowNodes = [
  { step: "01", label: "Question", icon: Terminal, color: "text-blue-500", border: "border-blue-500/30", bg: "bg-blue-500/10" },
  { step: "02", label: "Think", icon: Zap, color: "text-amber-500", border: "border-amber-500/30", bg: "bg-amber-500/10" },
  { step: "03", label: "Code", icon: Code2, color: "text-emerald-500", border: "border-emerald-500/30", bg: "bg-emerald-500/10" },
  { step: "04", label: "Debug", icon: Bug, color: "text-rose-500", border: "border-rose-500/30", bg: "bg-rose-500/10" },
  { step: "05", label: "Design", icon: Layers, color: "text-purple-500", border: "border-purple-500/30", bg: "bg-purple-500/10" },
  { step: "06", label: "Scale", icon: Server, color: "text-teal-500", border: "border-teal-500/30", bg: "bg-teal-500/10" },
  { step: "07", label: "Crack", icon: CheckCircle2, color: "text-emerald-400", border: "border-emerald-400/40", bg: "bg-emerald-500/20" },
];

export const Hero: React.FC = () => {
  const [activeNode, setActiveNode] = useState(0);
  const [stats, setStats] = useState({
    totalQuestions: 1200,
    technologies: 5,
    difficulties: 8,
    productionQuestions: 300,
  });

  useEffect(() => {
    fetchGlobalStats().then((res) => {
      if (res && res.total_questions) {
        setStats({
          totalQuestions: res.total_questions,
          technologies: res.total_technologies || 5,
          difficulties: 8,
          productionQuestions: res.questions_by_difficulty?.PRODUCTION_SCENARIO || 150,
        });
      }
    });

    const interval = setInterval(() => {
      setActiveNode((prev) => (prev + 1) % workflowNodes.length);
    }, 2200);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="relative w-full pt-12 pb-20 overflow-hidden tech-grid">
      {/* Subtle radial ambient gradients */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[350px] bg-gradient-to-tr from-primary/15 via-purple-500/10 to-teal-500/10 blur-3xl pointer-events-none -z-10 rounded-full" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Column: Headlines & Call to Actions */}
          <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
            {/* Trust Pill */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-primary/10 text-primary border border-primary/25 backdrop-blur-md">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>Production-Grade Technical Interview Knowledge Platform</span>
            </div>

            {/* Brand Title */}
            <div className="space-y-1.5">
              <span className="text-xs sm:text-sm font-mono uppercase tracking-[0.25em] text-muted-foreground font-semibold block">
                Enterprise Engineering Preparation
              </span>
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight text-foreground leading-[1.1]">
                BREAK THE CODE
              </h1>
              <h2 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold bg-gradient-to-r from-primary via-indigo-400 to-cyan-400 bg-clip-text text-transparent">
                Break The Code. Crack The Interview.
              </h2>
            </div>

            {/* Subheading */}
            <p className="text-base sm:text-lg text-muted-foreground max-w-2xl mx-auto lg:mx-0 leading-relaxed font-normal">
              Master technical interviews through progressively harder questions, real-world scenarios, system design challenges and production engineering problems.
            </p>

            {/* 3 Call to Action Buttons */}
            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-3.5 pt-2">
              <Link href="/questions">
                <Button size="lg" variant="primary" className="font-semibold shadow-md shadow-primary/20">
                  <span>Explore Questions</span>
                  <ArrowRight className="h-4 w-4 ml-1.5" />
                </Button>
              </Link>
              <Link href="/questions?difficulty=PRODUCTION_SCENARIO">
                <Button size="lg" variant="outline" className="font-semibold border-teal-500/40 text-teal-600 dark:text-teal-400 hover:bg-teal-500/10">
                  <Play className="h-4 w-4 mr-1.5 fill-current" />
                  <span>Start Interview</span>
                </Button>
              </Link>
              <Link href="/difficulty">
                <Button size="lg" variant="ghost" className="font-medium text-muted-foreground hover:text-foreground">
                  <Sparkles className="h-4 w-4 mr-1.5 text-amber-500" />
                  <span>Browse by Difficulty</span>
                </Button>
              </Link>
            </div>

            {/* Real Statistics from DB */}
            <div className="pt-6 grid grid-cols-2 sm:grid-cols-4 gap-4 border-t border-border/80 max-w-xl mx-auto lg:mx-0 text-left">
              <div>
                <p className="text-2xl sm:text-3xl font-extrabold text-foreground tracking-tight">
                  {stats.totalQuestions.toLocaleString()}+
                </p>
                <p className="text-xs text-muted-foreground font-medium">Interview Questions</p>
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-extrabold text-purple-600 dark:text-purple-400 tracking-tight">
                  {stats.difficulties}
                </p>
                <p className="text-xs text-muted-foreground font-medium">Difficulty Levels</p>
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-extrabold text-teal-600 dark:text-teal-400 tracking-tight">
                  50+
                </p>
                <p className="text-xs text-muted-foreground font-medium">Technology Topics</p>
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-extrabold text-amber-600 dark:text-amber-400 tracking-tight">
                  {stats.productionQuestions}+
                </p>
                <p className="text-xs text-muted-foreground font-medium">Production Scenarios</p>
              </div>
            </div>
          </div>

          {/* Right Column: Interactive Progression & Technical Node Visual */}
          <div className="lg:col-span-5 flex justify-center">
            <div className="w-full max-w-md rounded-2xl glass-panel p-6 border border-border/80 shadow-2xl relative overflow-hidden">
              {/* Top Bar */}
              <div className="flex items-center justify-between pb-4 mb-5 border-b border-border/60">
                <div className="flex items-center gap-2">
                  <div className="flex gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
                    <span className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
                  </div>
                  <span className="text-xs font-mono text-muted-foreground ml-2 font-semibold">
                    ENGINEERING_PIPELINE
                  </span>
                </div>
                <span className="px-2 py-0.5 rounded text-[11px] font-mono font-semibold bg-primary/10 text-primary border border-primary/20">
                  STEP {activeNode + 1}/7
                </span>
              </div>

              {/* Connected Progression Pipeline */}
              <div className="space-y-2 relative">
                {workflowNodes.map((node, idx) => {
                  const Icon = node.icon;
                  const isCurrent = activeNode === idx;
                  const isPassed = activeNode > idx;

                  return (
                    <div
                      key={node.step}
                      className={`flex items-center justify-between p-2.5 rounded-xl border transition-all duration-300 ${
                        isCurrent 
                          ? `${node.bg} ${node.border} shadow-sm translate-x-1` 
                          : isPassed 
                            ? "bg-card/40 border-border/40 opacity-70"
                            : "bg-transparent border-transparent opacity-40"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span className="font-mono text-xs text-muted-foreground select-none w-5">
                          {node.step}
                        </span>
                        <div className={`p-1.5 rounded-lg ${isCurrent ? node.bg : "bg-muted/40"} ${node.color}`}>
                          <Icon className="h-4 w-4" />
                        </div>
                        <span className={`text-sm font-semibold ${isCurrent ? "text-foreground font-bold" : "text-muted-foreground"}`}>
                          {node.label}
                        </span>
                      </div>

                      <div className="flex items-center gap-2">
                        {isCurrent && (
                          <span className="text-[10px] font-mono uppercase tracking-wider text-primary font-bold animate-pulse">
                            ACTIVE
                          </span>
                        )}
                        {isPassed && (
                          <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" />
                        )}
                        <span className="text-xs text-muted-foreground/40 font-mono">
                          {idx === 0 && "Raw Problem"}
                          {idx === 1 && "Trade-offs"}
                          {idx === 2 && "Implementation"}
                          {idx === 3 && "Edge-cases"}
                          {idx === 4 && "Architecture"}
                          {idx === 5 && "High Throughput"}
                          {idx === 6 && "Interview Success"}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Bottom Quick Action */}
              <div className="mt-5 pt-4 border-t border-border/60 flex items-center justify-between text-xs">
                <span className="text-muted-foreground font-medium">Progressive 8-Tier Path</span>
                <Link
                  href="/difficulty"
                  className="font-semibold text-primary hover:underline flex items-center gap-1"
                >
                  View Tier Architecture &rarr;
                </Link>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};
