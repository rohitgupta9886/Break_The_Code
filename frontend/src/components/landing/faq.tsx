"use client";

import React, { useState } from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

export const FAQ: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const faqs = [
    {
      q: "How does Break The Code differ from generic coding platforms?",
      a: "Most platforms focus purely on LeetCode-style algorithmic puzzles or multiple-choice trivia. Break The Code focuses on the actual verbal, architectural, and production scenario discussions that happen in modern senior software engineer interviews—especially across AI/GenAI, Concurrency, and Distributed Systems.",
    },
    {
      q: "What is Think Mode and why should I use it?",
      a: "Think Mode simulates the actual interview setting. It starts a stopwatch and hides the answer, encouraging you to draft your response in your own words. You can request progressive hints if you get stuck before revealing the model answer or submitting to AI evaluation.",
    },
    {
      q: "How does the AI Answer Evaluation work?",
      a: "We evaluate your submitted answer against multi-metric rubrics: Technical Correctness, Completeness, Architectural Depth, and Communication Clarity. The system returns concrete checklists of points you covered vs. critical edge cases you missed, along with an improved version of your answer.",
    },
    {
      q: "Is any content scraped from proprietary question banks?",
      a: "No. All questions and model answers in Break The Code are independently authored based on official framework specifications (e.g. LangGraph documentation, OpenJDK JEPs, Spring Guides) and open educational sources, with complete source and licensing attribution.",
    },
  ];

  return (
    <section className="w-full py-20 bg-background border-t border-border/60">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12 space-y-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-primary">Frequently Asked Questions</span>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">
            Everything You Need To Know
          </h2>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, idx) => {
            const isOpen = openIndex === idx;
            return (
              <div
                key={idx}
                className="rounded-xl border border-border/80 bg-card overflow-hidden transition-all duration-200"
              >
                <button
                  onClick={() => setOpenIndex(isOpen ? null : idx)}
                  className="w-full flex items-center justify-between p-5 text-left font-medium text-sm sm:text-base text-foreground hover:text-primary transition-colors gap-4"
                >
                  <span>{faq.q}</span>
                  <ChevronDown
                    className={cn(
                      "h-4 w-4 shrink-0 transition-transform duration-200 text-muted-foreground",
                      isOpen && "rotate-180 text-primary"
                    )}
                  />
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 text-xs sm:text-sm text-muted-foreground leading-relaxed border-t border-border/40 pt-3 animate-fade-in">
                    {faq.a}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
