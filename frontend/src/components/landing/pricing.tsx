import React from "react";
import Link from "next/link";
import { Check, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

export const Pricing: React.FC = () => {
  const tiers = [
    {
      name: "Free",
      price: "$0",
      description: "Essential interview preparation for students and early-career developers.",
      features: [
        "Access to Basic & Medium questions",
        "Think Mode with live stopwatch",
        "Level 1 Conceptual hints",
        "Track progress across all domains",
        "Community discussion access",
      ],
      cta: "Get Started Free",
      highlighted: false,
    },
    {
      name: "Pro",
      price: "$29",
      period: "/month",
      description: "The complete preparation toolkit for active interview candidates.",
      features: [
        "Unlimited access to TOUGH & L5 questions",
        "Full 3-Level Progressive Hints",
        "AI Answer Evaluation with rubric grading",
        "Personalized weak area revision queue",
        "Full architecture and code walkthroughs",
        "Spaced repetition question schedule",
      ],
      cta: "Start 7-Day Trial",
      highlighted: true,
    },
    {
      name: "Premium",
      price: "$69",
      period: "/month",
      description: "Elite preparation with simulated multi-agent interviews and project defense.",
      features: [
        "Everything in Pro plan",
        "Full LangGraph AI Mock Interviews",
        "Resume-tailored question generator",
        "Project Architecture Defense simulator",
        "Priority AI evaluation speed",
        "1-on-1 performance scorecards",
      ],
      cta: "Upgrade to Premium",
      highlighted: false,
    },
  ];

  return (
    <section className="w-full py-20 bg-muted/20 border-t border-border/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-semibold uppercase tracking-wider text-primary">Transparent Pricing</span>
          <h2 className="text-3xl font-extrabold tracking-tight text-foreground">
            Invest in Your Next Senior Role
          </h2>
          <p className="text-sm text-muted-foreground">
            Choose the tier tailored to your timeline. Cancel anytime with zero friction.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch">
          {tiers.map((tier, idx) => (
            <div
              key={idx}
              className={`relative rounded-2xl p-7 flex flex-col justify-between border transition-all duration-200 ${
                tier.highlighted
                  ? "bg-card border-primary shadow-xl glow-primary scale-105 z-10"
                  : "bg-card/70 border-border/70 shadow-sm"
              }`}
            >
              {tier.highlighted && (
                <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-primary text-primary-foreground text-xs font-semibold uppercase tracking-wider flex items-center gap-1 shadow-md">
                  <Sparkles className="h-3 w-3" />
                  Most Popular
                </div>
              )}

              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-bold text-foreground">{tier.name}</h3>
                  <p className="text-xs text-muted-foreground mt-1">{tier.description}</p>
                </div>

                <div className="flex items-baseline gap-1 py-2">
                  <span className="text-4xl font-extrabold text-foreground">{tier.price}</span>
                  {tier.period && <span className="text-xs text-muted-foreground">{tier.period}</span>}
                </div>

                <ul className="space-y-2.5 pt-4 border-t border-border/40 text-xs text-muted-foreground">
                  {tier.features.map((feat, fidx) => (
                    <li key={fidx} className="flex items-start gap-2.5">
                      <Check className="h-4 w-4 text-emerald-500 shrink-0 mt-0.5" />
                      <span>{feat}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="pt-8">
                <Link href="/questions" className="w-full">
                  <Button
                    variant={tier.highlighted ? "primary" : "outline"}
                    className="w-full font-semibold"
                  >
                    {tier.cta}
                  </Button>
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
