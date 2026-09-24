import React from "react";
import Link from "next/link";
import { Logo } from "./logo";

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-rose-200/80 dark:border-rose-900/60 bg-white/60 dark:bg-[#140a10]/60 mt-auto pb-16 sm:pb-0 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Column */}
          <div className="space-y-3.5 md:col-span-1">
            <Logo size="md" showSubtitle={false} />
            <p className="text-xs text-muted-foreground leading-relaxed">
              AI-Powered Technical Interview Preparation Platform. Break The Code. Crack The Interview.
            </p>
          </div>

          {/* Quick Tracks */}
          <div className="space-y-2.5">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-foreground">Tracks</h4>
            <ul className="space-y-2 text-xs text-muted-foreground">
              <li>
                <Link href="/questions?technology=langgraph" className="hover:text-primary transition-colors">
                  AI / GenAI & LangGraph
                </Link>
              </li>
              <li>
                <Link href="/questions?technology=java-backend" className="hover:text-primary transition-colors">
                  Java & Concurrency
                </Link>
              </li>
              <li>
                <Link href="/questions?technology=dsa" className="hover:text-primary transition-colors">
                  Data Structures & Algorithms
                </Link>
              </li>
              <li>
                <Link href="/questions?technology=system-design" className="hover:text-primary transition-colors">
                  Distributed System Design
                </Link>
              </li>
            </ul>
          </div>

          {/* Practice & Features */}
          <div className="space-y-2.5">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-foreground">Practice</h4>
            <ul className="space-y-2 text-xs text-muted-foreground">
              <li>
                <Link href="/questions" className="hover:text-primary transition-colors">
                  Think Mode & Timer
                </Link>
              </li>
              <li>
                <Link href="/questions" className="hover:text-primary transition-colors">
                  3-Level Progressive Hints
                </Link>
              </li>
              <li>
                <Link href="/questions" className="hover:text-primary transition-colors">
                  AI Answer Evaluation
                </Link>
              </li>
              <li>
                <Link href="/admin/questions" className="hover:text-primary transition-colors">
                  Content Quality & Review
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal & Editorial */}
          <div className="space-y-2.5">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-foreground">Integrity</h4>
            <p className="text-xs text-muted-foreground leading-relaxed">
              Independently authored technical explanations, verified framework documentation, and open attribution metadata.
            </p>
            <div className="text-[11px] text-muted-foreground">
              Strict multi-stage technical review pipeline.
            </div>
          </div>
        </div>

        <div className="pt-8 border-t border-border/40 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-muted-foreground">
          <p>© {new Date().getFullYear()} Break The Code. All rights reserved.</p>
          <p className="flex items-center gap-1">
            Engineered for high-performing software engineers.
          </p>
        </div>
      </div>
    </footer>
  );
};
