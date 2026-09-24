"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  History,
  CheckCircle2,
  XCircle,
  Clock,
  Sparkles,
  ChevronDown,
  ChevronUp,
  BrainCircuit,
  Lightbulb,
  AlertTriangle
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { fetchUserHistory } from "@/lib/api";
import { Button } from "@/components/ui/button";

export default function HistoryPage() {
  const { token } = useAuth();
  const [history, setHistory] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    if (token) {
      loadHistory();
    }
  }, [token]);

  const loadHistory = async () => {
    if (!token) return;
    setLoading(true);
    const data = await fetchUserHistory(token);
    setHistory(data.items || []);
    setTotal(data.total || 0);
    setLoading(false);
  };

  const toggleExpand = (id: string) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
          <History className="h-5 w-5 text-purple-500" />
          Attempt History & Evaluation Audit
        </h2>
        <p className="text-xs text-muted-foreground mt-0.5">
          Review your past interview submissions, time spent, detailed AI rubric scores, and recommendations.
        </p>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-28 rounded-2xl bg-muted/40 animate-pulse" />
          ))}
        </div>
      ) : history.length === 0 ? (
        <div className="p-12 text-center border border-dashed border-border/80 rounded-3xl bg-card/40">
          <History className="h-10 w-10 text-muted-foreground/40 mx-auto mb-3" />
          <h3 className="text-sm font-semibold text-foreground mb-1">No past attempts</h3>
          <p className="text-xs text-muted-foreground max-w-sm mx-auto mb-4">
            Practice a question in Think Mode and submit your answer for comprehensive AI evaluation to start tracking your audit trail.
          </p>
          <Link href="/questions">
            <Button size="sm" variant="primary">Explore Questions</Button>
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {history.map((att) => {
            const isExpanded = expandedId === att.id;
            const evalDetails = att.evaluation_details || {};
            const correctness = evalDetails.correctness?.score || 0;
            const completeness = evalDetails.completeness?.score || 0;
            const depth = evalDetails.technical_depth?.score || 0;
            const clarity = evalDetails.clarity?.score || 0;

            return (
              <div
                key={att.id}
                className="border border-border/80 rounded-2xl bg-card/60 backdrop-blur-md overflow-hidden transition-all shadow-sm"
              >
                {/* Header summary bar */}
                <div
                  onClick={() => toggleExpand(att.id)}
                  className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 cursor-pointer hover:bg-muted/30 transition-colors"
                >
                  <div className="space-y-1 min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="text-[11px] font-semibold text-primary px-2 py-0.5 rounded bg-primary/10">
                        {att.technology_name}
                      </span>
                      <span className="text-[10px] font-medium text-muted-foreground px-1.5 py-0.2 rounded bg-muted">
                        {att.difficulty}
                      </span>
                    </div>

                    <h3 className="font-bold text-sm text-foreground truncate">
                      {att.question_title}
                    </h3>

                    <div className="flex items-center gap-3 text-[11px] text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" /> {att.time_spent_seconds}s
                      </span>
                      <span>•</span>
                      <span className="text-primary font-semibold">+{att.xp_earned} XP</span>
                      <span>•</span>
                      <span>{new Date(att.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 self-end sm:self-center">
                    <div className="text-right">
                      <div className="text-base font-black text-foreground">
                        {att.score_overall.toFixed(1)} / 10
                      </div>
                      <div className="text-[10px] text-muted-foreground">AI Score</div>
                    </div>

                    <Button size="sm" variant="ghost" className="h-8 w-8 p-0 text-muted-foreground">
                      {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                    </Button>
                  </div>
                </div>

                {/* Expanded Evaluation Breakdown */}
                {isExpanded && (
                  <div className="p-5 pt-0 border-t border-border/50 space-y-5 bg-muted/10">
                    {/* Rubrics grid */}
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-4">
                      <div className="p-3 rounded-xl bg-card border border-border/60">
                        <div className="text-[10px] text-muted-foreground">Correctness</div>
                        <div className="text-sm font-bold text-foreground">{correctness} / 10</div>
                      </div>
                      <div className="p-3 rounded-xl bg-card border border-border/60">
                        <div className="text-[10px] text-muted-foreground">Completeness</div>
                        <div className="text-sm font-bold text-foreground">{completeness} / 10</div>
                      </div>
                      <div className="p-3 rounded-xl bg-card border border-border/60">
                        <div className="text-[10px] text-muted-foreground">Technical Depth</div>
                        <div className="text-sm font-bold text-foreground">{depth} / 10</div>
                      </div>
                      <div className="p-3 rounded-xl bg-card border border-border/60">
                        <div className="text-[10px] text-muted-foreground">Clarity</div>
                        <div className="text-sm font-bold text-foreground">{clarity} / 10</div>
                      </div>
                    </div>

                    {/* Candidate Answer */}
                    <div className="space-y-1.5">
                      <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                        Your Submitted Answer
                      </h4>
                      <div className="p-3.5 rounded-xl bg-muted/40 border border-border/60 text-xs font-mono text-foreground whitespace-pre-wrap leading-relaxed">
                        {att.candidate_answer}
                      </div>
                    </div>

                    {/* Covered vs Missed Points */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* Covered */}
                      <div className="space-y-2 p-3.5 rounded-xl bg-emerald-500/5 border border-emerald-500/20">
                        <h5 className="text-xs font-bold text-emerald-500 flex items-center gap-1.5">
                          <CheckCircle2 className="h-3.5 w-3.5" /> What You Got Right
                        </h5>
                        <ul className="space-y-1 text-xs text-foreground/90">
                          {(evalDetails.covered_points || []).map((cp: string, idx: number) => (
                            <li key={idx} className="flex items-start gap-1.5">
                              <span className="text-emerald-500">•</span>
                              <span>{cp}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* Missed */}
                      <div className="space-y-2 p-3.5 rounded-xl bg-rose-500/5 border border-rose-500/20">
                        <h5 className="text-xs font-bold text-rose-500 flex items-center gap-1.5">
                          <AlertTriangle className="h-3.5 w-3.5" /> Key Nuances Missed
                        </h5>
                        <ul className="space-y-1 text-xs text-foreground/90">
                          {(evalDetails.missed_points || []).map((mp: string, idx: number) => (
                            <li key={idx} className="flex items-start gap-1.5">
                              <span className="text-rose-500">•</span>
                              <span>{mp}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    {/* AI Improved Answer Recommendation */}
                    {evalDetails.improved_answer && (
                      <div className="space-y-1.5 p-3.5 rounded-xl bg-primary/5 border border-primary/20">
                        <h5 className="text-xs font-bold text-primary flex items-center gap-1.5">
                          <Lightbulb className="h-3.5 w-3.5" /> How To Answer Like A Senior / Staff Engineer
                        </h5>
                        <p className="text-xs text-foreground/90 leading-relaxed">
                          {evalDetails.improved_answer}
                        </p>
                      </div>
                    )}

                    {/* Actionable Advice */}
                    {evalDetails.actionable_advice && (
                      <div className="flex items-start gap-2 text-xs text-muted-foreground italic">
                        <span>💡 Tip:</span>
                        <span>{evalDetails.actionable_advice}</span>
                      </div>
                    )}

                    <div className="pt-2 flex justify-end">
                      <Link href={`/questions/${att.question_slug}`}>
                        <Button size="sm" variant="outline" className="text-xs flex items-center gap-1.5">
                          <BrainCircuit className="h-3.5 w-3.5" />
                          Retry In Think Mode
                        </Button>
                      </Link>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
