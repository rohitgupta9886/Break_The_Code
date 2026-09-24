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
      border: "border-border/70 hover:border-primary/50",
      iconBg: "bg-primary/10 text-primary border border-primary/20",
    },
    {
      border: "border-border/70 hover:border-accent-violet/50",
      iconBg: "bg-accent-violet/10 text-accent-violet border border-accent-violet/20",
    },
    {
      border: "border-border/70 hover:border-accent-amber/50",
      iconBg: "bg-accent-amber/10 text-accent-amber border border-accent-amber/20",
    },
    {
      border: "border-border/70 hover:border-accent-emerald/50",
      iconBg: "bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20",
    },
    {
      border: "border-border/70 hover:border-accent-cyan/50",
      iconBg: "bg-accent-cyan/10 text-accent-cyan border border-accent-cyan/20",
    },
    {
      border: "border-border/70 hover:border-accent-indigo/50",
      iconBg: "bg-accent-indigo/10 text-accent-indigo border border-accent-indigo/20",
    },
  ];

  return (
    <section className="w-full py-20 bg-background border-t border-border/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16 space-y-3">
          <span className="text-xs sm:text-sm font-mono font-bold uppercase tracking-wider text-primary">Active Learning Loop</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
            Engineered For True Technical Retention
          </h2>
          <p className="text-base text-muted-foreground leading-relaxed">
            Passive reading fails under high-stakes interview pressure. Break The Code forces active retrieval and architectural thinking.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          {featureList.map((feat, idx) => {
            const Icon = feat.icon;
            const color = featureColors[idx % featureColors.length];
            return (
              <div
                key={idx}
                className={`rounded-2xl border ${color.border} p-6 sm:p-7 bg-surface/80 hover:bg-surface shadow-xs hover:shadow-elevation-1 transition-all duration-200 space-y-4`}
              >
                <div className={`h-11 w-11 rounded-xl ${color.iconBg} flex items-center justify-center shadow-2xs`}>
                  <Icon className="h-5 w-5" />
                </div>
                <h3 className="text-lg font-bold text-foreground tracking-tight">{feat.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{feat.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
