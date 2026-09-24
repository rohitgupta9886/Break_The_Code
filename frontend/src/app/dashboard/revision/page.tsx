"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  RotateCcw,
  Sparkles,
  CheckCircle2,
  Clock,
  Layers,
  BrainCircuit,
  Eye,
  ArrowRight,
  ShieldCheck,
  Check
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { fetchRevisionQueue, submitRevisionReview, fetchQuestionBySlug } from "@/lib/api";
import { Button } from "@/components/ui/button";

export default function SpacedRepetitionPage() {
  const { token } = useAuth();
  const [cards, setCards] = useState<any[]>([]);
  const [dueCount, setDueCount] = useState(0);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [loading, setLoading] = useState(true);
  const [questionDetail, setQuestionDetail] = useState<any>(null);
  const [reviewSuccessMsg, setReviewSuccessMsg] = useState<string | null>(null);

  useEffect(() => {
    if (token) {
      loadQueue();
    }
  }, [token]);

  const loadQueue = async () => {
    if (!token) return;
    setLoading(true);
    const data = await fetchRevisionQueue(token);
    setCards(data.items || []);
    setDueCount(data.due_count || 0);
    setCurrentIndex(0);
    setIsFlipped(false);
    setLoading(false);
  };

  const currentCard = cards[currentIndex];

  useEffect(() => {
    if (currentCard) {
      setIsFlipped(false);
      fetchQuestionBySlug(currentCard.question_slug).then((q) => {
        setQuestionDetail(q);
      });
    } else {
      setQuestionDetail(null);
    }
  }, [currentIndex, currentCard]);

  const handleRate = async (grade: number) => {
    if (!token || !currentCard) return;

    setReviewSuccessMsg(`Recorded grade ${grade}! Scheduling next review...`);
    await submitRevisionReview(token, currentCard.question_id, grade);

    setTimeout(() => {
      setReviewSuccessMsg(null);
      setIsFlipped(false);
      if (currentIndex + 1 < cards.length) {
        setCurrentIndex(currentIndex + 1);
      } else {
        // Queue finished
        loadQueue();
      }
    }, 600);
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <RotateCcw className="h-5 w-5 text-blue-500" />
            Spaced Repetition (SM-2 Engine)
          </h2>
          <p className="text-xs text-muted-foreground mt-0.5">
            Scientific recall scheduling based on the SuperMemo SM-2 algorithm to guarantee long-term retention.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-semibold">
            {cards.length} In Queue ({dueCount} Due Now)
          </span>
        </div>
      </div>

      {loading ? (
        <div className="h-96 rounded-3xl bg-muted/40 animate-pulse" />
      ) : cards.length === 0 || currentIndex >= cards.length ? (
        <div className="p-16 text-center border border-dashed border-border/80 rounded-3xl bg-card/40 space-y-4">
          <div className="h-16 w-16 mx-auto rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-500">
            <CheckCircle2 className="h-8 w-8" />
          </div>
          <h3 className="text-lg font-bold text-foreground">You are all caught up!</h3>
          <p className="text-xs text-muted-foreground max-w-sm mx-auto leading-relaxed">
            Zero flashcards due right now. Solve new interview problems in Think Mode or check back tomorrow for your next SRS review cycle.
          </p>
          <div className="pt-2 flex items-center justify-center gap-3">
            <Link href="/questions">
              <Button size="sm" variant="primary">Explore More Questions</Button>
            </Link>
            <Link href="/dashboard">
              <Button size="sm" variant="outline">Back to Dashboard</Button>
            </Link>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Progress Indicator */}
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>Card {currentIndex + 1} of {cards.length}</span>
            <span className="text-primary font-medium">Status: {currentCard.status}</span>
          </div>

          {/* Interactive Flashcard */}
          <div className="relative rounded-3xl border border-border/90 bg-gradient-to-br from-card via-card to-muted/20 p-8 shadow-xl min-h-[380px] flex flex-col justify-between transition-all">
            {/* Front info */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="px-2.5 py-0.5 rounded-full bg-primary/10 text-primary text-xs font-semibold">
                  {currentCard.technology_name}
                </span>
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <span className="px-2 py-0.5 rounded bg-muted text-[11px] font-medium">
                    {currentCard.difficulty}
                  </span>
                  <span>Interval: {currentCard.interval_days}d</span>
                </div>
              </div>

              <h3 className="text-xl font-bold text-foreground mb-4 leading-snug">
                {currentCard.question_title}
              </h3>

              {!isFlipped ? (
                <div className="p-6 rounded-2xl border border-dashed border-border/70 bg-muted/20 text-center my-6">
                  <p className="text-xs text-muted-foreground mb-3">
                    Think through your verbal answer. What is the fundamental architecture, lifecycle, and trade-off?
                  </p>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setIsFlipped(true)}
                    className="flex items-center gap-2 mx-auto"
                  >
                    <Eye className="h-4 w-4" />
                    Flip to Reveal Answer Key
                  </Button>
                </div>
              ) : (
                <div className="space-y-4 my-4 animate-in fade-in zoom-in-95 duration-200">
                  <div className="p-4 rounded-2xl bg-muted/40 border border-border/80 text-xs leading-relaxed text-foreground/95">
                    <div className="text-[11px] font-bold text-primary uppercase tracking-wider mb-1">
                      Core Concept & Architectural Mechanism
                    </div>
                    {questionDetail ? (
                      <p className="whitespace-pre-line">{questionDetail.short_answer}</p>
                    ) : (
                      <p>Loading explanation key...</p>
                    )}
                  </div>

                  {questionDetail?.interviewer_intent && (
                    <div className="p-3.5 rounded-xl bg-blue-500/10 border border-blue-500/20 text-xs text-foreground/90">
                      <span className="font-bold text-blue-400">Interviewer Intent: </span>
                      {questionDetail.interviewer_intent}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Rating Buttons on Flip */}
            {isFlipped ? (
              <div className="pt-4 border-t border-border/60">
                <div className="text-center text-xs font-semibold text-muted-foreground mb-3">
                  How well did you recall this answer?
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  <button
                    onClick={() => handleRate(1)}
                    className="p-3 rounded-xl border border-rose-500/30 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 font-semibold text-xs flex flex-col items-center gap-1 transition-all"
                  >
                    <span>Again</span>
                    <span className="text-[10px] text-muted-foreground font-normal">Reset (1d)</span>
                  </button>

                  <button
                    onClick={() => handleRate(2)}
                    className="p-3 rounded-xl border border-amber-500/30 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 font-semibold text-xs flex flex-col items-center gap-1 transition-all"
                  >
                    <span>Hard</span>
                    <span className="text-[10px] text-muted-foreground font-normal">Short (2d)</span>
                  </button>

                  <button
                    onClick={() => handleRate(4)}
                    className="p-3 rounded-xl border border-blue-500/30 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 font-semibold text-xs flex flex-col items-center gap-1 transition-all"
                  >
                    <span>Good</span>
                    <span className="text-[10px] text-muted-foreground font-normal">Expanded (4d)</span>
                  </button>

                  <button
                    onClick={() => handleRate(5)}
                    className="p-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 font-semibold text-xs flex flex-col items-center gap-1 transition-all"
                  >
                    <span>Easy</span>
                    <span className="text-[10px] text-muted-foreground font-normal">Mastered (7d+)</span>
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex justify-end pt-2">
                <Link href={`/questions/${currentCard.question_slug}`}>
                  <Button size="sm" variant="ghost" className="text-xs text-muted-foreground hover:text-foreground">
                    Open Full Question Detail →
                  </Button>
                </Link>
              </div>
            )}
          </div>

          {reviewSuccessMsg && (
            <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs text-center font-medium animate-in fade-in">
              {reviewSuccessMsg}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
