"use client";

import React, { useState } from "react";
import Link from "next/link";
import { 
  Flame, 
  Clock, 
  CheckCircle2, 
  ArrowRight, 
  Play, 
  Sparkles, 
  ShieldCheck,
  Cpu
} from "lucide-react";
import { Button } from "@/components/ui/button";

export const DailyChallenge: React.FC = () => {
  const [isCompleted, setIsCompleted] = useState(false);

  return (
    <section className="w-full py-12 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="rounded-3xl border border-amber-500/30 bg-gradient-to-r from-amber-500/10 via-card to-purple-500/10 p-6 sm:p-10 shadow-lg relative overflow-hidden">
          
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
            <div className="space-y-4 max-w-3xl">
              <div className="flex flex-wrap items-center gap-2.5">
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-500/15 text-amber-600 dark:text-amber-400 border border-amber-500/30">
                  <Flame className="h-3.5 w-3.5 fill-current" />
                  <span>Today&apos;s Interview Challenge</span>
                </span>
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-500/15 text-purple-600 dark:text-purple-300 border border-purple-500/25">
                  <Cpu className="h-3 w-3" />
                  LangGraph
                </span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-orange-600/15 text-orange-600 dark:text-orange-400 border border-orange-600/25">
                  Level 5 · Very Tough
                </span>
              </div>

              <h3 className="text-2xl sm:text-3xl font-extrabold text-foreground tracking-tight">
                How would you recover a failed LangGraph workflow without repeating external side effects?
              </h3>

              <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                Analyze checkpoint state serialization, idempotency tokens across tools, and human-in-the-loop replay mechanics during third-party API timeout crashes.
              </p>

              <div className="flex items-center gap-4 text-xs font-mono text-muted-foreground">
                <span className="flex items-center gap-1">
                  <Clock className="h-3.5 w-3.5 text-amber-500" />
                  <span>10 min target response</span>
                </span>
                <span>•</span>
                <span>Production Scenario</span>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row lg:flex-col gap-3 shrink-0">
              <Link href="/questions/langgraph-basic-zero-downtime-9">
                <Button size="lg" className="w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold shadow-md shadow-amber-500/20">
                  <Play className="h-4 w-4 mr-1.5 fill-current" />
                  <span>Start Challenge</span>
                </Button>
              </Link>
              <button
                onClick={() => setIsCompleted(!isCompleted)}
                className={`w-full inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl text-xs font-semibold border transition-all ${
                  isCompleted 
                    ? "bg-emerald-500/15 text-emerald-600 border-emerald-500/30" 
                    : "bg-muted/40 text-muted-foreground border-border/80 hover:text-foreground"
                }`}
              >
                <CheckCircle2 className="h-4 w-4" />
                <span>{isCompleted ? "Marked Complete ✓" : "Mark as Solved"}</span>
              </button>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};
