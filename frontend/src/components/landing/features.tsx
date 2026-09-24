import React from "react";
import { Timer, HelpCircle, Sparkles, Shield, GitBranch, Cpu } from "lucide-react";

export const Features: React.FC = () => {
  const featureList = [
    {
      icon: Timer,
      title: "Think Mode with Stopwatch",
      description: "Overcome the instinct to peek at answers immediately. Formulate your answer under a live interview timer before unveiling model solutions.",
    },
    {
      icon: HelpCircle,
      title: "3-Level Progressive Hints",
      description: "Unlock clues gradually: Level 1 provides conceptual direction, Level 2 covers implementation structure, and Level 3 explores edge-case architecture.",
    },
    {
      icon: Sparkles,
      title: "Multi-Rubric Answer Evaluation",
      description: "LangGraph grades your answers across Correctness, Completeness, Technical Depth, and Clarity with checklist of covered vs missed points.",
    },
    {
      icon: GitBranch,
      title: "Deep Question DNA",
      description: "Every question includes short elevator answers, interview-ready scripts, code snippets, architecture diagrams, and common pitfalls.",
    },
    {
      icon: Cpu,
      title: "Production Scenario Focus",
      description: "Beyond academic trivia: tackle real-world failure modes, cache stampedes, Kafka consumer rebalances, and LangGraph checkpointer crashes.",
    },
    {
      icon: Shield,
      title: "Strict Editorial Integrity",
      description: "Zero scraped content. Built upon verified framework specifications, official source attribution, and multi-stage peer review.",
    },
  ];

  const featureColors = [
    {
      cardBg: "bg-[#fff1f4] dark:bg-rose-950/25",
      border: "border-rose-200/90 dark:border-rose-900/60 hover:border-rose-400",
      iconBg: "bg-rose-100 text-rose-700 dark:bg-rose-900/60 dark:text-rose-300",
    },
    {
      cardBg: "bg-[#f5f3ff] dark:bg-purple-950/25",
      border: "border-purple-200/90 dark:border-purple-900/60 hover:border-purple-400",
      iconBg: "bg-purple-100 text-purple-700 dark:bg-purple-900/60 dark:text-purple-300",
    },
    {
      cardBg: "bg-[#fffbeb] dark:bg-amber-950/25",
      border: "border-amber-200/90 dark:border-amber-900/60 hover:border-amber-400",
      iconBg: "bg-amber-100 text-amber-700 dark:bg-amber-900/60 dark:text-amber-300",
    },
    {
      cardBg: "bg-[#ecfdf5] dark:bg-emerald-950/25",
      border: "border-emerald-200/90 dark:border-emerald-900/60 hover:border-emerald-400",
      iconBg: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/60 dark:text-emerald-300",
    },
    {
      cardBg: "bg-[#f0f9ff] dark:bg-sky-950/25",
      border: "border-sky-200/90 dark:border-sky-900/60 hover:border-sky-400",
      iconBg: "bg-sky-100 text-sky-700 dark:bg-sky-900/60 dark:text-sky-300",
    },
    {
      cardBg: "bg-[#fff7ed] dark:bg-orange-950/25",
      border: "border-orange-200/90 dark:border-orange-900/60 hover:border-orange-400",
      iconBg: "bg-orange-100 text-orange-700 dark:bg-orange-900/60 dark:text-orange-300",
    },
  ];

  return (
    <section className="w-full py-20 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16 space-y-3">
          <span className="text-xs sm:text-sm font-bold uppercase tracking-wider text-primary">Active Learning Loop</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
            Engineered For True Technical Retention
          </h2>
          <p className="text-base text-muted-foreground leading-relaxed">
            Passive reading fails under high-stakes interview pressure. Break The Code forces active retrieval and architectural thinking.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featureList.map((feat, idx) => {
            const Icon = feat.icon;
            const color = featureColors[idx % featureColors.length];
            return (
              <div
                key={idx}
                className={`rounded-3xl border ${color.border} p-7 ${color.cardBg} hover:shadow-lg transition-all duration-200 space-y-4`}
              >
                <div className={`h-12 w-12 rounded-2xl ${color.iconBg} flex items-center justify-center shadow-xs`}>
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className="text-lg sm:text-xl font-bold text-foreground tracking-tight">{feat.title}</h3>
                <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">{feat.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
