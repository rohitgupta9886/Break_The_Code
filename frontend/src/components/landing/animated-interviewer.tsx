"use client";

import React, { useState, useEffect } from "react";
import { Bot, User, Sparkles, CheckCircle2 } from "lucide-react";

interface DialogStep {
  speaker: "ai" | "candidate";
  text: string;
}

const dialogue: DialogStep[] = [
  {
    speaker: "ai",
    text: "How would you design a production-grade RAG system for 10 million documents?",
  },
  {
    speaker: "candidate",
    text: "I would start by separating ingestion, retrieval, and generation. Ingestion chunks documents and stores them in PostgreSQL with pgvector HNSW indexing, alongside BM25 sparse inverted indexes.",
  },
  {
    speaker: "ai",
    text: "Why would you choose hybrid retrieval over dense vectors alone?",
  },
  {
    speaker: "candidate",
    text: "Dense vectors capture semantic concepts, but fail on exact part numbers and acronyms. Hybrid search with Reciprocal Rank Fusion gives the best of both, followed by cross-encoder reranking.",
  },
  {
    speaker: "ai",
    text: "Excellent technical depth. How would you handle cache stampedes on hot query embeddings?",
  },
];

export const AnimatedInterviewer: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep((prev) => (prev + 1) % dialogue.length);
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="relative w-full max-w-xl mx-auto rounded-2xl glass-panel p-5 border border-border/80 shadow-2xl overflow-hidden glow-primary">
      {/* Terminal Title Bar */}
      <div className="flex items-center justify-between pb-3.5 mb-3.5 border-b border-border/40">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
            <div className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
          </div>
          <span className="text-xs font-mono font-medium text-muted-foreground ml-2 flex items-center gap-1.5">
            <Bot className="h-3.5 w-3.5 text-primary" />
            AI Interviewer · Live Session
          </span>
        </div>
        <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-ping" />
          L4 Architecture
        </span>
      </div>

      {/* Message Feed */}
      <div className="space-y-3.5 min-h-[260px] flex flex-col justify-end">
        {dialogue.slice(0, currentStep + 1).map((msg, idx) => {
          const isAi = msg.speaker === "ai";
          return (
            <div
              key={idx}
              className={`flex items-start gap-3 transition-all duration-300 animate-fade-in ${
                isAi ? "" : "flex-row-reverse"
              }`}
            >
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 text-xs font-bold ${
                  isAi
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "bg-secondary text-secondary-foreground border border-border"
                }`}
              >
                {isAi ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
              </div>
              <div
                className={`rounded-2xl px-4 py-2.5 text-xs sm:text-sm leading-relaxed max-w-[85%] ${
                  isAi
                    ? "bg-muted/80 text-foreground border border-border/50 rounded-tl-sm"
                    : "bg-primary text-primary-foreground font-medium rounded-tr-sm shadow"
                }`}
              >
                {msg.text}
              </div>
            </div>
          );
        })}
      </div>

      {/* Real-time Evaluation Card */}
      <div className="mt-4 pt-3.5 border-t border-border/40 flex items-center justify-between text-xs text-muted-foreground">
        <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 font-medium">
          <CheckCircle2 className="h-4 w-4" />
          <span>Active Rubric: Correctness 9.4 · Depth 9.2</span>
        </div>
        <div className="flex items-center gap-1 font-mono text-[11px]">
          <Sparkles className="h-3 w-3 text-primary animate-spin" />
          <span>LangGraph Evaluator</span>
        </div>
      </div>
    </div>
  );
};
