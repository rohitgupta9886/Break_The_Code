"use client";

import React from "react";
import Link from "next/link";
import { 
  AlertTriangle, 
  Activity, 
  Flame, 
  ShieldCheck, 
  Sparkles, 
  ArrowRight, 
  Server, 
  Cpu, 
  CheckCircle2, 
  Bug, 
  Terminal,
  BookOpen
} from "lucide-react";
import { Button } from "@/components/ui/button";

export const ProductionHighlights: React.FC = () => {
  return (
    <section className="w-full py-20 bg-muted/20 border-t border-border/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
        
        {/* Section 1: Production Incident Drill & Staff Engineer Corner */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
          
          {/* Left Column: Real-World Production Incident Card */}
          <div className="lg:col-span-6 rounded-2xl border border-teal-500/30 bg-[#0a1118] text-slate-100 p-6 sm:p-8 flex flex-col justify-between shadow-xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-teal-500/10 rounded-full blur-3xl pointer-events-none -z-0" />

            <div className="space-y-5 relative z-10">
              <div className="flex items-center justify-between">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono font-bold bg-teal-500/20 text-teal-300 border border-teal-500/30">
                  <Activity className="h-3.5 w-3.5 animate-pulse text-teal-400" />
                  <span>PRODUCTION INCIDENT SIMULATION</span>
                </div>
                <span className="px-2.5 py-0.5 rounded text-[11px] font-mono font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30">
                  SEV-1 OUTAGE
                </span>
              </div>

              <div className="space-y-2">
                <h3 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
                  Kafka Consumer Lag Spiked 20x Under Heavy Rebalancing
                </h3>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                  During peak traffic, partition rebalances caused stop-the-world pauses, tripping heartbeat timeouts 
                  and triggering cascading group re-joins across 12 consumer replicas.
                </p>
              </div>

              {/* Telemetry Snapshot Box */}
              <div className="rounded-xl bg-slate-900/90 border border-slate-800 p-4 font-mono text-xs text-slate-300 space-y-2">
                <div className="flex justify-between text-slate-400 text-[11px] pb-1 border-b border-slate-800">
                  <span>METRIC</span>
                  <span>RECORDED VALUE</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">max.poll.interval.ms:</span>
                  <span className="text-rose-400 font-bold">300,000ms EXCEEDED</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">GC Pause (G1GC):</span>
                  <span className="text-amber-400">8.2s Humongous Alloc</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Uncommitted Offsets:</span>
                  <span className="text-teal-400">4,820,110 messages</span>
                </div>
              </div>

              <div className="space-y-2">
                <h4 className="text-xs font-mono uppercase tracking-wider text-teal-400 font-bold">
                  What Interviewers Look For:
                </h4>
                <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                  <li>Decoupling message fetch loops from slow asynchronous processing pipelines</li>
                  <li>Tuning cooperative sticky assignors vs. eager stop-the-world assignors</li>
                  <li>Preventing zombie writes with transactional idempotency tokens</li>
                </ul>
              </div>
            </div>

            <div className="pt-6 mt-6 border-t border-slate-800/80 flex items-center justify-between relative z-10">
              <span className="text-xs text-slate-400 font-mono">Category: Distributed Systems</span>
              <Link href="/questions?difficulty=PRODUCTION_SCENARIO">
                <Button size="sm" className="bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold">
                  <span>Drill Incident Scenarios</span>
                  <ArrowRight className="h-3.5 w-3.5 ml-1" />
                </Button>
              </Link>
            </div>
          </div>

          {/* Right Column: Staff Engineer Corner & Interviewer Trap */}
          <div className="lg:col-span-6 flex flex-col justify-between gap-6">
            
            {/* Staff Engineer Corner */}
            <div className="rounded-2xl border border-purple-500/30 bg-[#0e0e1a] text-slate-100 p-6 sm:p-7 shadow-xl space-y-4">
              <div className="flex items-center justify-between">
                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">
                  <Sparkles className="h-3.5 w-3.5 text-purple-400" />
                  <span>STAFF ENGINEER CORNER</span>
                </div>
                <span className="text-xs font-mono text-purple-400 font-semibold">LEVEL 8 ARCHITECT</span>
              </div>

              <h3 className="text-xl sm:text-2xl font-black text-white">
                Designing for Reliability, Blast Radii & Cost Budgets
              </h3>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                Staff interviews do not judge whether code compiles. They test architectural tradeoffs: 
                blast-radius isolation, active-active multi-region replication costs, and graceful degradation during vector database latency spikes.
              </p>

              <div className="pt-2 flex flex-wrap gap-2">
                <span className="px-2.5 py-1 rounded-md text-[11px] font-mono bg-purple-900/40 text-purple-200 border border-purple-800/60">
                  CAP vs. PACELC
                </span>
                <span className="px-2.5 py-1 rounded-md text-[11px] font-mono bg-purple-900/40 text-purple-200 border border-purple-800/60">
                  Cell-Based Architecture
                </span>
                <span className="px-2.5 py-1 rounded-md text-[11px] font-mono bg-purple-900/40 text-purple-200 border border-purple-800/60">
                  Cost per 1M Vector Searches
                </span>
              </div>
            </div>

            {/* Interviewer Trap Card */}
            <div className="rounded-2xl border border-amber-500/35 bg-card p-6 shadow-md space-y-3.5">
              <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400 font-bold text-xs uppercase tracking-wider font-mono">
                <AlertTriangle className="h-4 w-4" />
                <span>Interviewer Trap: &ldquo;Exactly-Once Processing&rdquo;</span>
              </div>

              <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                <strong className="text-foreground">Candidate Claim:</strong> &ldquo;We configured Kafka and Flink for exactly-once processing so duplicate orders are mathematically impossible.&rdquo;
              </p>

              <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-900 dark:text-amber-200 space-y-1">
                <p className="font-bold">Interviewer Counter-Punch:</p>
                <p>
                  &ldquo;What happens when your consumer executes an HTTP call to an external payment gateway before committing offsets? 
                  Does Kafka&apos;s EOS guarantee that the external payment gateway won&apos;t charge twice?&rdquo;
                </p>
              </div>

              <div className="flex items-center justify-between text-xs pt-1">
                <span className="text-muted-foreground font-mono">15-Part Answer Breakdown</span>
                <Link href="/questions?difficulty=TOUGH" className="font-semibold text-primary hover:underline flex items-center gap-1">
                  Master Interview Traps &rarr;
                </Link>
              </div>
            </div>

          </div>

        </div>

        {/* Section 2: Trust Signals Banner */}
        <div className="rounded-2xl border border-border/80 bg-card p-6 sm:p-8 shadow-sm">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6 text-center sm:text-left">
            
            <div className="space-y-1.5">
              <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 font-bold text-xs uppercase tracking-wider">
                <CheckCircle2 className="h-4 w-4" />
                <span>Technically Reviewed</span>
              </div>
              <p className="text-xs text-muted-foreground">
                All 1,200 questions vetted for production accuracy, code validity, and real trade-offs.
              </p>
            </div>

            <div className="space-y-1.5">
              <div className="flex items-center gap-2 text-sky-600 dark:text-sky-400 font-bold text-xs uppercase tracking-wider">
                <BookOpen className="h-4 w-4" />
                <span>Source Referenced</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Citations link to official documentation (LangGraph, Kafka, JVM, PostgreSQL, Redis).
              </p>
            </div>

            <div className="space-y-1.5">
              <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400 font-bold text-xs uppercase tracking-wider">
                <ShieldCheck className="h-4 w-4" />
                <span>Version Aware</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Modern specifications: Python 3.12, Java 21+ Virtual Threads, LangGraph 0.2+, and Kafka 3.7.
              </p>
            </div>

            <div className="space-y-1.5">
              <div className="flex items-center gap-2 text-teal-600 dark:text-teal-400 font-bold text-xs uppercase tracking-wider">
                <Activity className="h-4 w-4" />
                <span>Production Focused</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Zero superficial trivia. Emphasizes failure cascades, tail latencies, and outage forensics.
              </p>
            </div>

            <div className="space-y-1.5">
              <div className="flex items-center gap-2 text-purple-600 dark:text-purple-400 font-bold text-xs uppercase tracking-wider">
                <Sparkles className="h-4 w-4" />
                <span>Original Content</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Curated technical problem statements with 15-part model answer DNA and ASCII topologies.
              </p>
            </div>

          </div>
        </div>

      </div>
    </section>
  );
};
