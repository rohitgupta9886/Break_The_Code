"use client";

import React, { useState, useEffect } from "react";
import { Timer, Play, Pause, RotateCcw, Lightbulb, Send, Eye, CheckCircle2, XCircle, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { formatTime } from "@/lib/utils";
import { evaluateAnswer, fetchSocraticHint, AnswerEvaluationData } from "@/lib/api";

import { useAuth } from "@/lib/auth-context";

interface Hint {
  id: string;
  hint_level: number;
  hint_type: string;
  content: string;
}

interface ThinkModeProps {
  questionId: string;
  hints: Hint[];
  onRevealAnswer: () => void;
  isAnswerRevealed: boolean;
}

export const ThinkMode: React.FC<ThinkModeProps> = ({
  questionId,
  hints,
  onRevealAnswer,
  isAnswerRevealed,
}) => {
  const { token, refreshUser } = useAuth();
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [candidateAnswer, setCandidateAnswer] = useState("");
  const [unlockedHintLevel, setUnlockedHintLevel] = useState(0);
  const [evaluation, setEvaluation] = useState<any>(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [isRequestingAIHint, setIsRequestingAIHint] = useState(false);
  const [dynamicAiHints, setDynamicAiHints] = useState<Array<{ level: number; type: string; question: string; clue: string }>>([]);
  const [rewardNotice, setRewardNotice] = useState<{ xp: number; streak?: number; badges?: string[] } | null>(null);

  // Live timer effect
  useEffect(() => {
    let interval: any = null;
    if (isActive) {
      interval = setInterval(() => {
        setSeconds((s) => s + 1);
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isActive]);

  const toggleTimer = () => {
    setIsActive(!isActive);
  };

  const resetTimer = () => {
    setIsActive(false);
    setSeconds(0);
  };

  const unlockNextHint = () => {
    if (unlockedHintLevel < 3) {
      setUnlockedHintLevel((prev) => prev + 1);
    }
  };

  const handleRequestAIHint = async () => {
    setIsRequestingAIHint(true);
    const nextLevel = Math.min(3, dynamicAiHints.length + 1);
    const res = await fetchSocraticHint(questionId, candidateAnswer, nextLevel);
    if (res) {
      setDynamicAiHints((prev) => [
        ...prev,
        {
          level: res.hint_level,
          type: res.hint_type,
          question: res.socratic_question,
          clue: res.guiding_clue,
        },
      ]);
    }
    setIsRequestingAIHint(false);
  };

  const handleSubmitAnswer = async () => {
    if (!candidateAnswer.trim()) return;
    setIsEvaluating(true);
    setIsActive(false); // Stop timer on submit
    const res = await evaluateAnswer(questionId, candidateAnswer, seconds, token);
    setEvaluation(res);
    setIsEvaluating(false);

    if (res && res.xp_earned) {
      setRewardNotice({
        xp: res.xp_earned,
        streak: res.streak_days,
        badges: res.new_badges,
      });
      if (token) {
        refreshUser();
      }
    }
  };

  return (
    <div className="rounded-2xl border border-border/80 bg-surface p-6 sm:p-8 shadow-elevation-1 space-y-6">
      {/* Top Header: Think Mode Title + Live Stopwatch */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border/60">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-amber-400 animate-pulse" />
            <h3 className="font-bold text-lg sm:text-xl text-foreground tracking-tight flex items-center gap-2">
              Think Mode · Interview Simulation Cockpit
            </h3>
          </div>
          <p className="text-xs sm:text-sm text-muted-foreground">
            Formulate your response under real interview conditions before reviewing the benchmark answer.
          </p>
        </div>

        {/* Stopwatch Controller */}
        <div className="flex items-center gap-2.5 bg-surface-elevated px-4 py-2 rounded-xl border border-border/80 shadow-2xs">
          <Timer className={`h-4.5 w-4.5 ${isActive ? "text-amber-400 animate-pulse" : "text-muted-foreground"}`} />
          <span className="font-mono text-base sm:text-lg font-bold text-foreground min-w-[55px]">
            {formatTime(seconds)}
          </span>
          <div className="flex items-center gap-1.5 ml-2 border-l border-border/60 pl-2">
            <button
              onClick={toggleTimer}
              className="p-1.5 rounded-lg hover:bg-surface text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
              title={isActive ? "Pause Timer" : "Start Timer"}
            >
              {isActive ? <Pause className="h-4 w-4 text-amber-400" /> : <Play className="h-4 w-4 text-emerald-400" />}
            </button>
            <button
              onClick={resetTimer}
              className="p-1.5 rounded-lg hover:bg-surface text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
              title="Reset Timer"
            >
              <RotateCcw className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Answer Draft Input Area */}
      <div className="space-y-2">
        <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center justify-between">
          <span>Draft Your Technical Answer</span>
          <span className="text-xs font-mono font-normal lowercase">{candidateAnswer.split(/\s+/).filter(Boolean).length} words</span>
        </label>
        <textarea
          rows={5}
          value={candidateAnswer}
          onChange={(e) => {
            setCandidateAnswer(e.target.value);
            if (!isActive && seconds === 0) setIsActive(true); // Auto-start timer on typing
          }}
          placeholder="Structure your answer: 1. Core mechanism & invariants, 2. Concurrency/latency trade-offs, 3. Failure modes & mitigation..."
          className="w-full rounded-xl border border-border/80 bg-surface-elevated/70 p-4 text-sm sm:text-base text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary transition-all leading-relaxed"
        />
      </div>

      {/* Action Controls */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
        <div className="flex flex-wrap items-center gap-2">
          {/* Progressive Hint Trigger */}
          <Button
            variant="outline"
            size="sm"
            onClick={unlockNextHint}
            disabled={unlockedHintLevel >= (hints?.length || 3)}
            className="text-xs"
          >
            <Lightbulb className="h-3.5 w-3.5 text-amber-500" />
            <span>
              {unlockedHintLevel === 0
                ? "Unlock Hint 1"
                : unlockedHintLevel < (hints?.length || 3)
                ? `Unlock Hint ${unlockedHintLevel + 1}`
                : "All Hints Unlocked"}
            </span>
          </Button>

          {/* Dynamic AI Socratic Coach Trigger */}
          <Button
            variant="outline"
            size="sm"
            onClick={handleRequestAIHint}
            disabled={isRequestingAIHint || dynamicAiHints.length >= 3}
            isLoading={isRequestingAIHint}
            className="text-xs border-primary/40 text-primary hover:bg-primary/10"
          >
            <Sparkles className="h-3.5 w-3.5 mr-1" />
            <span>
              {isRequestingAIHint
                ? "Asking AI Coach..."
                : dynamicAiHints.length === 0
                ? "Ask AI Coach Hint"
                : `AI Hint (${dynamicAiHints.length}/3)`}
            </span>
          </Button>

          {/* Reveal Model Answer Button */}
          <Button
            variant="ghost"
            size="sm"
            onClick={onRevealAnswer}
            className="text-xs text-muted-foreground hover:text-foreground"
          >
            <Eye className="h-3.5 w-3.5 mr-1" />
            <span>{isAnswerRevealed ? "Hide Model Answer" : "Reveal Answer"}</span>
          </Button>
        </div>

        {/* Submit to AI Evaluation Button */}
        <Button
          variant="primary"
          size="sm"
          onClick={handleSubmitAnswer}
          disabled={!candidateAnswer.trim() || isEvaluating}
          isLoading={isEvaluating}
          className="text-xs font-semibold"
        >
          <Send className="h-3.5 w-3.5 mr-1" />
          <span>{isEvaluating ? "Evaluating with Gemini..." : "Submit to AI Evaluation"}</span>
        </Button>
      </div>

      {/* Dynamic Gemini AI Hints Drawer */}
      {dynamicAiHints.length > 0 && (
        <div className="space-y-3 pt-3 border-t border-primary/20 animate-fade-in">
          <h4 className="text-xs font-bold uppercase tracking-wider text-primary flex items-center gap-1.5">
            <Sparkles className="h-3.5 w-3.5" />
            <span>AI Socratic Coach Guidance ({dynamicAiHints.length}/3)</span>
          </h4>
          <div className="space-y-2">
            {dynamicAiHints.map((ah, i) => (
              <div
                key={i}
                className="p-3.5 rounded-xl bg-primary/10 border border-primary/20 text-xs text-foreground space-y-1.5"
              >
                <div className="flex items-center justify-between font-semibold text-[11px] text-primary uppercase tracking-wide">
                  <span>Level {ah.level} · {ah.type}</span>
                </div>
                <p className="font-medium text-foreground leading-relaxed">
                  ❓ {ah.question}
                </p>
                <p className="text-muted-foreground text-[11px] leading-relaxed italic">
                  💡 Clue: {ah.clue}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Unlocked Standard Hints Drawer */}
      {unlockedHintLevel > 0 && hints && (
        <div className="space-y-3 pt-3 border-t border-border/40 animate-fade-in">
          <h4 className="text-xs font-bold uppercase tracking-wider text-amber-500 flex items-center gap-1.5">
            <Lightbulb className="h-3.5 w-3.5" />
            <span>Progressive Hints ({unlockedHintLevel}/{hints.length})</span>
          </h4>
          <div className="space-y-2">
            {hints.slice(0, unlockedHintLevel).map((h, i) => (
              <div
                key={h.id || i}
                className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-foreground space-y-1"
              >
                <div className="flex items-center justify-between font-semibold text-[11px] text-amber-600 dark:text-amber-400 uppercase tracking-wide">
                  <span>Hint {h.hint_level} · {h.hint_type}</span>
                </div>
                <p className="leading-relaxed text-muted-foreground">{h.content}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* XP & Streak Reward Banner */}
      {rewardNotice && (
        <div className="p-4 rounded-2xl bg-gradient-to-r from-primary/20 via-emerald-500/15 to-card border border-primary/40 flex flex-col sm:flex-row sm:items-center justify-between gap-3 animate-in fade-in zoom-in-95 shadow-md">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-primary text-primary-foreground flex items-center justify-center font-bold text-lg shadow-sm">
              ⚡
            </div>
            <div>
              <div className="text-sm font-bold text-foreground flex items-center gap-2">
                <span>+{rewardNotice.xp} XP Earned!</span>
                {rewardNotice.streak && (
                  <span className="text-xs font-semibold text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/20">
                    🔥 {rewardNotice.streak} Day Streak
                  </span>
                )}
              </div>
              <p className="text-[11px] text-muted-foreground">
                Your answer was evaluated, progress recorded, and question scheduled into your Spaced Repetition queue!
              </p>
            </div>
          </div>

          {rewardNotice.badges && rewardNotice.badges.length > 0 && (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-500/20 border border-amber-500/30 text-amber-400 text-xs font-bold">
              <span>🏆 Unlocked: {rewardNotice.badges.join(", ")}</span>
            </div>
          )}
        </div>
      )}

      {/* AI Evaluation Scorecard (when returned) */}
      {evaluation && (
        <div className="mt-6 p-6 rounded-2xl bg-surface-elevated/70 border border-primary/30 space-y-5 animate-fade-in shadow-elevation-1">
          <div className="flex items-center justify-between border-b border-border/60 pb-3">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-primary" />
              <h4 className="font-bold text-sm text-foreground">Google Gemini AI Evaluation Scorecard</h4>
            </div>
            <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 border border-primary/25 text-primary font-bold text-sm">
              <span className="text-base">{evaluation.overall_score}</span>
              <span className="text-xs font-normal text-muted-foreground">/ 10</span>
            </div>
          </div>

          {/* 4 Rubric Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
            <div className="p-3.5 rounded-xl bg-surface border border-border/80 flex flex-col justify-between">
              <div>
                <span className="text-[11px] text-muted-foreground uppercase font-semibold">Correctness</span>
                <p className="text-xl font-bold text-foreground mt-1">{evaluation.correctness?.score ?? 7}/10</p>
                <div className="w-full bg-border/60 rounded-full h-1 mt-2 overflow-hidden">
                  <div className="bg-emerald-500 h-1 rounded-full" style={{ width: `${((evaluation.correctness?.score ?? 7) / 10) * 100}%` }} />
                </div>
              </div>
              {evaluation.correctness?.feedback && (
                <p className="text-[11px] text-muted-foreground mt-2 line-clamp-2">{evaluation.correctness.feedback}</p>
              )}
            </div>
            <div className="p-3.5 rounded-xl bg-surface border border-border/80 flex flex-col justify-between">
              <div>
                <span className="text-[11px] text-muted-foreground uppercase font-semibold">Completeness</span>
                <p className="text-xl font-bold text-foreground mt-1">{evaluation.completeness?.score ?? 7}/10</p>
                <div className="w-full bg-border/60 rounded-full h-1 mt-2 overflow-hidden">
                  <div className="bg-sky-500 h-1 rounded-full" style={{ width: `${((evaluation.completeness?.score ?? 7) / 10) * 100}%` }} />
                </div>
              </div>
              {evaluation.completeness?.feedback && (
                <p className="text-[11px] text-muted-foreground mt-2 line-clamp-2">{evaluation.completeness.feedback}</p>
              )}
            </div>
            <div className="p-3.5 rounded-xl bg-surface border border-border/80 flex flex-col justify-between">
              <div>
                <span className="text-[11px] text-muted-foreground uppercase font-semibold">Depth</span>
                <p className="text-xl font-bold text-foreground mt-1">{evaluation.technical_depth?.score ?? 7}/10</p>
                <div className="w-full bg-border/60 rounded-full h-1 mt-2 overflow-hidden">
                  <div className="bg-indigo-500 h-1 rounded-full" style={{ width: `${((evaluation.technical_depth?.score ?? 7) / 10) * 100}%` }} />
                </div>
              </div>
              {evaluation.technical_depth?.feedback && (
                <p className="text-[11px] text-muted-foreground mt-2 line-clamp-2">{evaluation.technical_depth.feedback}</p>
              )}
            </div>
            <div className="p-3.5 rounded-xl bg-surface border border-border/80 flex flex-col justify-between">
              <div>
                <span className="text-[11px] text-muted-foreground uppercase font-semibold">Clarity</span>
                <p className="text-xl font-bold text-foreground mt-1">{evaluation.clarity?.score ?? 8}/10</p>
                <div className="w-full bg-border/60 rounded-full h-1 mt-2 overflow-hidden">
                  <div className="bg-purple-500 h-1 rounded-full" style={{ width: `${((evaluation.clarity?.score ?? 8) / 10) * 100}%` }} />
                </div>
              </div>
              {evaluation.clarity?.feedback && (
                <p className="text-[11px] text-muted-foreground mt-2 line-clamp-2">{evaluation.clarity.feedback}</p>
              )}
            </div>
          </div>

          {/* Covered vs Missed Points */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-2">
            <div className="space-y-2 p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
              <h5 className="font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="h-4 w-4" />
                <span>Points You Covered</span>
              </h5>
              <ul className="space-y-1 text-muted-foreground">
                {(evaluation.covered_points || []).map((pt: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-1.5">
                    <span className="text-emerald-500 font-bold">✓</span>
                    <span>{pt}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="space-y-2 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20">
              <h5 className="font-bold text-rose-600 dark:text-rose-400 flex items-center gap-1.5">
                <XCircle className="h-4 w-4" />
                <span>Points You Missed</span>
              </h5>
              <ul className="space-y-1 text-muted-foreground">
                {(evaluation.missed_points || []).map((pt: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-1.5">
                    <span className="text-rose-500 font-bold">•</span>
                    <span>{pt}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Improved Answer Synthesis */}
          {evaluation.improved_answer && (
            <div className="p-4 rounded-xl bg-card border border-border/70 space-y-1.5 text-xs">
              <span className="font-bold text-foreground uppercase tracking-wider text-[11px]">
                Senior-Level Model Answer
              </span>
              <p className="text-muted-foreground leading-relaxed italic">
                "{evaluation.improved_answer}"
              </p>
            </div>
          )}

          {/* Actionable Advice */}
          {evaluation.actionable_advice && (
            <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-foreground space-y-1">
              <span className="font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wide text-[11px]">
                💡 Principal Architect Coaching Advice
              </span>
              <p className="leading-relaxed text-muted-foreground">{evaluation.actionable_advice}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
