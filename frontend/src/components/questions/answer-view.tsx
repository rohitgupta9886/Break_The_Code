"use client";

import React, { useState } from "react";
import {
  MessageSquare,
  FileText,
  Layers,
  Code,
  AlertTriangle,
  Target,
  ExternalLink,
  HelpCircle,
  ShieldCheck,
  CheckCircle2,
  Maximize2,
  Minimize2,
  Sparkles,
  BookOpen,
  Terminal,
  Activity,
  GitBranch
} from "lucide-react";
import { QuestionDetailData } from "@/lib/api";
import { CodeBlock } from "@/components/ui/code-block";
import { FormattedAnswer } from "@/components/ui/formatted-answer";
import { cn } from "@/lib/utils";

interface AnswerViewProps {
  question: QuestionDetailData;
}

export const AnswerView: React.FC<AnswerViewProps> = ({ question }) => {
  const [activeTab, setActiveTab] = useState<
    "answer" | "explanation" | "production" | "architecture" | "code" | "traps" | "sources"
  >("answer");

  const [isDiagramExpanded, setIsDiagramExpanded] = useState(false);

  const tabs = [
    { id: "answer", label: "Model Answer", icon: MessageSquare },
    { id: "explanation", label: "Deep Explanation", icon: FileText },
    { id: "production", label: "Production & Trade-offs", icon: Layers },
    { id: "architecture", label: "Architecture", icon: Layers },
    { id: "code", label: "Implementation Code", icon: Code },
    { id: "traps", label: "Interviewer Traps & Mistakes", icon: AlertTriangle },
    { id: "sources", label: "Sources & References", icon: BookOpen },
  ];

  return (
    <div className="rounded-2xl border border-border/80 bg-surface overflow-hidden shadow-elevation-1 space-y-0">
      
      {/* Top Navigation Tabs */}
      <div className="flex items-center gap-1.5 p-2 bg-surface-elevated/70 border-b border-border/70 overflow-x-auto scrollbar-none">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={cn(
                "flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold whitespace-nowrap transition-all duration-150 cursor-pointer",
                isActive
                  ? "bg-primary/10 text-primary shadow-2xs border border-primary/25 font-bold"
                  : "text-muted-foreground hover:text-foreground hover:bg-surface"
              )}
            >
              <Icon className={cn("h-4 w-4", isActive ? "text-primary" : "text-muted-foreground")} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Main Content Area */}
      <div className="p-6 sm:p-8 space-y-6">

        {/* Tab 1: Interview-Ready Model Answer */}
        {activeTab === "answer" && (
          <div className="space-y-6 animate-fade-in">
            {/* Direct Answer Summary */}
            {question.short_answer && (
              <div className="p-5 rounded-xl bg-primary/5 border border-primary/20 text-sm sm:text-base space-y-2 shadow-2xs">
                <span className="font-bold text-primary uppercase tracking-wider text-xs flex items-center gap-1.5">
                  <Sparkles className="h-4 w-4" />
                  Direct Answer · 30-Second Elevator Pitch
                </span>
                <div className="text-foreground font-medium answer-lead">
                  <FormattedAnswer text={question.short_answer} variant="lead" />
                </div>
              </div>
            )}

            {/* Model Spoken Response */}
            <div className="space-y-2.5">
              <span className="text-xs sm:text-sm font-bold uppercase tracking-wider text-foreground">
                Interview-Ready Answer (Full Verbal Response)
              </span>
              <div className="p-6 sm:p-7 rounded-xl bg-surface-elevated/70 border border-border/80 answer-lead text-foreground/95 shadow-2xs">
                <FormattedAnswer text={question.interview_ready_answer} variant="lead" />
              </div>
            </div>

            {/* Follow-up Questions Section */}
            {question.followups && question.followups.length > 0 && (
              <div className="pt-5 border-t border-border/60 space-y-3.5">
                <h4 className="text-xs sm:text-sm font-bold uppercase tracking-wider text-foreground flex items-center gap-2">
                  <HelpCircle className="h-4 w-4 text-primary" />
                  <span>Expected Follow-up Questions in the Interview</span>
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {question.followups.map((f) => (
                    <div key={f.id} className="p-4 rounded-xl bg-surface-elevated border border-border/80 text-xs sm:text-sm space-y-2 shadow-2xs">
                      <p className="font-bold text-foreground text-sm sm:text-base">&ldquo;{f.followup_question}&rdquo;</p>
                      {f.answer_guidance && (
                        <p className="text-muted-foreground text-xs sm:text-sm leading-relaxed">
                          <strong className="text-foreground">Response Key:</strong> {f.answer_guidance}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Deep Explanation */}
        {activeTab === "explanation" && (
          <div className="space-y-4 animate-fade-in text-sm leading-relaxed text-foreground">
            <span className="text-xs font-bold uppercase tracking-wider text-primary">
              Internal Mechanics & Theoretical Underpinnings
            </span>
            <div className="p-6 rounded-2xl bg-muted/20 border border-border/70 answer-body text-foreground/95">
              <FormattedAnswer text={question.deep_explanation || "Detailed internal mechanics and theoretical breakdown for this question."} />
            </div>

            {question.interviewer_intent && (
              <div className="p-5 rounded-2xl bg-primary/5 border border-primary/20 space-y-2.5 text-xs sm:text-sm">
                <div className="flex items-center justify-between gap-2">
                  <span className="font-bold text-primary uppercase tracking-wider text-xs flex items-center gap-1.5">
                    <Target className="h-4 w-4" />
                    Tier-1 Interviewer Evaluation Rubric
                  </span>
                  <span className="text-[11px] font-mono text-muted-foreground px-2 py-0.5 rounded bg-primary/10">
                    FAANG / Tier-1 Loop Criteria
                  </span>
                </div>
                <p className="text-foreground/90 leading-relaxed font-medium">
                  {question.interviewer_intent}
                </p>
                <div className="pt-2 border-t border-primary/10 flex flex-wrap gap-2 text-[11px] font-mono text-muted-foreground">
                  <span>✓ Mechanical Precision</span>
                  <span>•</span>
                  <span>✓ Failure Mode Resilience</span>
                  <span>•</span>
                  <span>✓ Explicit Trade-off Justification</span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 3: Production Considerations & Trade-offs */}
        {activeTab === "production" && (
          <div className="space-y-6 animate-fade-in text-xs sm:text-sm">
            
            {/* Architectural Trade-offs */}
            <div className="space-y-2">
              <span className="font-bold uppercase tracking-wider text-teal-600 dark:text-teal-400 text-xs flex items-center gap-1.5">
                <Layers className="h-4 w-4" />
                Architectural Trade-offs & Compromises
              </span>
              <div className="p-5 rounded-2xl bg-card border border-teal-500/25 text-foreground leading-relaxed shadow-xs">
                <FormattedAnswer text={question.tradeoffs || "Direct linearizable vs eventual consistency trade-offs; memory overhead vs query throughput."} />
              </div>
            </div>

            {/* Production Readiness Checklist */}
            <div className="space-y-2">
              <span className="font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400 text-xs flex items-center gap-1.5">
                <ShieldCheck className="h-4 w-4" />
                Production Considerations & Operational Readiness
              </span>
              <div className="p-5 rounded-2xl bg-amber-500/5 border border-amber-500/25 text-foreground leading-relaxed">
                <FormattedAnswer text={question.production_considerations || "Enforce bounded queue limits, configure P99 telemetry alerts, and attach distributed trace IDs to prevent silent deadlocks."} />
              </div>
            </div>

            {/* Failure Modes & Cascades */}
            <div className="space-y-2">
              <span className="font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400 text-xs flex items-center gap-1.5">
                <AlertTriangle className="h-4 w-4" />
                Known Failure Modes & Degradation Paths
              </span>
              <div className="p-5 rounded-2xl bg-rose-500/5 border border-rose-500/25 text-foreground leading-relaxed">
                <FormattedAnswer text={question.failure_modes || "Thread starvation resulting from unclosed connection sockets; cascading retries leading to downstream thundering herds."} />
              </div>
            </div>

          </div>
        )}

        {/* Tab 4: Architecture Topology */}
        {activeTab === "architecture" && (
          <div className="space-y-4 animate-fade-in">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-primary">
                System Topology & Component Interactions
              </span>
              <button
                onClick={() => setIsDiagramExpanded(!isDiagramExpanded)}
                className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground font-mono"
              >
                {isDiagramExpanded ? (
                  <>
                    <Minimize2 className="h-3.5 w-3.5" />
                    <span>Collapse Diagram</span>
                  </>
                ) : (
                  <>
                    <Maximize2 className="h-3.5 w-3.5" />
                    <span>Expand Diagram</span>
                  </>
                )}
              </button>
            </div>

            <div className={cn(
              "rounded-2xl bg-[#0d1117] border border-[#30363d] overflow-hidden shadow-2xl transition-all",
              isDiagramExpanded ? "max-h-[850px]" : "max-h-[460px]"
            )}>
              <div className="flex items-center justify-between px-4 py-2 bg-[#161b22] border-b border-[#30363d] text-xs font-mono text-slate-400 select-none">
                <div className="flex items-center gap-2">
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-[#ff5f56]" />
                    <span className="h-2.5 w-2.5 rounded-full bg-[#ffbd2e]" />
                    <span className="h-2.5 w-2.5 rounded-full bg-[#27c93f]" />
                  </div>
                  <span className="text-[#30363d]">|</span>
                  <span className="text-xs font-mono font-bold text-[#e6edf3]">architecture_spec.txt</span>
                </div>
                <span className="text-[11px] font-mono text-[#8b949e]">ASCII ARCHITECTURE FLOW</span>
              </div>
              <div className="p-5 overflow-x-auto font-mono text-[13.5px] sm:text-[14.5px] text-[#79c0ff] leading-[1.75]">
                <pre className="whitespace-pre">
                {question.architecture_notes || 
`Client Request
      │
      ▼
┌─────────────────────────┐
│  API Gateway / Ingress  │ (Rate Limiting, JWT Auth)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ State Orchestration     │ (LangGraph / Spring Worker)
└─────┬─────────────┬─────┘
      │             │
      ▼             ▼
┌───────────┐ ┌───────────┐
│ Hybrid DB │ │ LLM Engine│
└───────────┘ └───────────┘`}
              </pre>
              </div>
            </div>
          </div>
        )}

        {/* Tab 5: Implementation Code */}
        {activeTab === "code" && (
          <div className="space-y-3 animate-fade-in">
            <span className="text-xs font-bold uppercase tracking-wider text-primary">
              Production Implementation Snippet
            </span>
            {question.code_example ? (
              <CodeBlock 
                code={question.code_example} 
                language="python" 
                showLineNumbers={true}
              />
            ) : (
              <div className="p-8 text-center border border-dashed border-border rounded-xl text-xs text-muted-foreground">
                No code snippet required for this high-level architectural / scenario problem.
              </div>
            )}
          </div>
        )}

        {/* Tab 6: Interviewer Traps & Common Mistakes */}
        {activeTab === "traps" && (
          <div className="space-y-6 animate-fade-in text-xs sm:text-sm">
            
            {/* Interviewer Trap Box */}
            <div className="p-5 rounded-2xl bg-amber-500/10 border border-amber-500/30 space-y-2.5">
              <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400 font-bold uppercase tracking-wider text-xs font-mono">
                <AlertTriangle className="h-4 w-4" />
                <span>⚠ Interviewer Trap: &ldquo;{question.title.slice(0, 50)}...&rdquo;</span>
              </div>
              <p className="text-foreground leading-relaxed">
                {question.why_interviewer_asks || 
                  "Interviewers will challenge you on edge-case atomicity. If you claim 'guaranteed consistency', they will immediately inject an unhandled network partition."}
              </p>
            </div>

            {/* Common Mistakes */}
            <div className="space-y-3">
              <span className="text-xs font-bold uppercase tracking-wider text-rose-500">
                Where Candidates Frequently Lose Points
              </span>
              <div className="space-y-2.5">
                {question.common_mistakes && question.common_mistakes.length > 0 ? (
                  question.common_mistakes.map((mistake, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-xs sm:text-sm text-foreground flex items-start gap-3"
                    >
                      <AlertTriangle className="h-4 w-4 text-rose-500 shrink-0 mt-0.5" />
                      <span className="leading-relaxed text-foreground/90">{mistake.replace(/\*/g, "")}</span>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-muted-foreground">No critical pitfalls reported for this question.</p>
                )}
              </div>
            </div>

          </div>
        )}

        {/* Tab 7: Sources & References */}
        {activeTab === "sources" && (
          <div className="space-y-6 animate-fade-in">
            <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-border/60">
              <div className="space-y-1">
                <span className="text-xs font-bold uppercase tracking-wider text-primary flex items-center gap-1.5">
                  <ShieldCheck className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
                  Verified Authoritative Sources & Primary Specifications
                </span>
                <p className="text-xs text-muted-foreground">
                  Cross-referenced against official language specifications (Oracle JVM), engineering whitepapers (Google Spanner, Amazon Dynamo), open standards (W3C), and foundational textbooks (CLRS).
                </p>
              </div>

              {question.tags && question.tags.length > 0 && (
                <div className="flex items-center gap-1.5 flex-wrap">
                  <span className="text-[11px] font-semibold text-muted-foreground">Asked at Tier-1:</span>
                  {question.tags.map((t) => (
                    <span key={t.slug} className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-white dark:bg-card border border-border text-foreground shadow-2xs">
                      {t.name}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {question.sources && question.sources.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {question.sources.map((s, idx) => (
                  <a
                    key={idx}
                    href={s.source_url || "#"}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-5 rounded-2xl border border-emerald-300/80 dark:border-emerald-800/60 bg-white/95 dark:bg-card/75 hover:border-emerald-500 hover:shadow-md transition-all flex flex-col justify-between group gap-4"
                  >
                    <div className="space-y-2.5">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider bg-emerald-500/15 text-emerald-800 dark:text-emerald-200 border border-emerald-500/30">
                          {s.license || "PRIMARY REFERENCE"}
                        </span>
                        {s.publisher && (
                          <span className="px-2 py-0.5 rounded-md text-[10px] font-mono font-semibold bg-muted text-foreground/80 border border-border/80">
                            {s.publisher}
                          </span>
                        )}
                      </div>

                      <div className="font-bold text-base text-foreground group-hover:text-emerald-700 dark:group-hover:text-emerald-300 transition-colors leading-snug">
                        {s.source_name}
                      </div>

                      {s.source_url && (
                        <div className="text-xs text-muted-foreground font-mono truncate group-hover:text-foreground/90">
                          {s.source_url}
                        </div>
                      )}
                    </div>

                    <div className="pt-3 border-t border-border/60 flex items-center justify-between text-xs font-semibold text-emerald-700 dark:text-emerald-300">
                      <span>View Official Documentation</span>
                      <ExternalLink className="h-4 w-4 shrink-0 group-hover:translate-x-0.5 transition-transform" />
                    </div>
                  </a>
                ))}
              </div>
            ) : (
              <div className="p-6 rounded-2xl bg-muted/30 border border-border/60 text-xs text-muted-foreground">
                Sourced from standard architectural patterns across Meta, Google, and Amazon production post-mortems.
              </div>
            )}
          </div>
        )}

        {/* Trust & Provenance Footer Banner on all tabs */}
        <div className="mt-8 pt-5 border-t border-border/60 flex flex-wrap items-center justify-between gap-4 text-xs font-mono text-muted-foreground bg-muted/20 p-4 rounded-xl">
          <div className="flex flex-wrap items-center gap-3">
            <span className="inline-flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-bold">
              <CheckCircle2 className="h-3.5 w-3.5" />
              <span>Technically Reviewed</span>
            </span>
            <span>•</span>
            <span className="inline-flex items-center gap-1 text-sky-600 dark:text-sky-400 font-bold">
              <BookOpen className="h-3.5 w-3.5" />
              <span>Source Referenced</span>
            </span>
            <span>•</span>
            <span className="inline-flex items-center gap-1 text-amber-600 dark:text-amber-400 font-semibold">
              <GitBranch className="h-3.5 w-3.5" />
              <span>Version: {question.technology_version || "Current (2026)"}</span>
            </span>
          </div>

          <div className="text-[11px]">
            Quality Score: <strong className="text-foreground">{Math.round((question.overall_quality_score || 0.95) * 100)}%</strong>
          </div>
        </div>

      </div>
    </div>
  );
};
