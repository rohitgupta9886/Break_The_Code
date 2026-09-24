import React from "react";
import { cn } from "@/lib/utils";
import { 
  CheckCircle2, 
  Sparkles, 
  Flame, 
  ShieldCheck, 
  Terminal, 
  Layers, 
  Cpu, 
  Server, 
  Database, 
  Workflow, 
  Activity, 
  Binary, 
  AlertTriangle,
  BookOpen,
  GitBranch
} from "lucide-react";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "outline" | "success" | "warning" | "destructive" | "accent" | "tech" | "violet" | "teal" | "amber";
}

export const Badge: React.FC<BadgeProps> = ({ className, variant = "default", children, ...props }) => {
  const variants = {
    default: "bg-surface-elevated text-foreground/80 border-border/70",
    outline: "bg-transparent text-foreground/90 border-border",
    success: "bg-emerald-500/10 text-emerald-500 dark:text-emerald-400 border-emerald-500/25",
    warning: "bg-amber-500/10 text-amber-500 dark:text-amber-400 border-amber-500/25",
    destructive: "bg-rose-500/10 text-rose-500 dark:text-rose-400 border-rose-500/25",
    accent: "bg-cyan-500/10 text-cyan-500 dark:text-cyan-400 border-cyan-500/25",
    tech: "bg-indigo-500/10 text-indigo-500 dark:text-indigo-400 border-indigo-500/25",
    violet: "bg-purple-500/10 text-purple-500 dark:text-purple-400 border-purple-500/25",
    teal: "bg-teal-500/10 text-teal-500 dark:text-teal-400 border-teal-500/25",
    amber: "bg-amber-500/10 text-amber-500 dark:text-amber-400 border-amber-500/25",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold tracking-wide border transition-colors shadow-2xs",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};

export const DifficultyBadge: React.FC<{ difficulty: string; size?: "sm" | "md" | "lg" }> = ({ 
  difficulty,
  size = "md"
}) => {
  const normalized = (difficulty || "").toUpperCase().replace(/\s+/g, "_");

  const sizeClasses = {
    sm: "px-2 py-0.5 text-xs font-medium",
    md: "px-2.5 py-1 text-xs font-semibold",
    lg: "px-3 py-1.5 text-sm font-semibold",
  }[size];

  // 1. BASIC - Green / Emerald
  if (normalized === "BASIC") {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-full font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/25", sizeClasses)}>
        <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 shrink-0" />
        Basic
      </span>
    );
  }

  // 2. MEDIUM - Blue / Sky
  if (normalized === "MEDIUM") {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-full font-semibold bg-sky-500/10 text-sky-600 dark:text-sky-400 border border-sky-500/25", sizeClasses)}>
        <span className="h-1.5 w-1.5 rounded-full bg-sky-500 shrink-0" />
        Medium
      </span>
    );
  }

  // 3. HARD - Indigo / Blue
  if (normalized === "HARD") {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-full font-semibold bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/25", sizeClasses)}>
        <span className="h-1.5 w-1.5 rounded-full bg-indigo-500 shrink-0" />
        Hard
      </span>
    );
  }

  // 4. TOUGH - Amber / Gold
  if (normalized === "TOUGH") {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-full font-semibold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/25", sizeClasses)}>
        <span className="h-1.5 w-1.5 rounded-full bg-amber-500 shrink-0" />
        Tough
      </span>
    );
  }

  // 5. VERY TOUGH - Orange
  if (normalized === "VERY_TOUGH") {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-full font-semibold bg-orange-500/10 text-orange-600 dark:text-orange-400 border border-orange-500/25", sizeClasses)}>
        <span className="h-1.5 w-1.5 rounded-full bg-orange-500 shrink-0" />
        Very Tough
      </span>
    );
  }

  // 6. VERY VERY TOUGH - Crimson
  if (normalized === "VERY_VERY_TOUGH") {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-full font-bold bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/30", sizeClasses)}>
        <span className="h-1.5 w-1.5 rounded-full bg-rose-500 animate-pulse shrink-0" />
        Very Very Tough
      </span>
    );
  }

  // 7. PRODUCTION SCENARIO - Real-World Engineering (Cyan / Amber)
  if (normalized === "PRODUCTION_SCENARIO") {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-full font-semibold bg-amber-500/10 text-amber-600 dark:text-amber-300 border border-amber-500/30", sizeClasses)}>
        <Activity className="h-3 w-3 text-amber-500 shrink-0" />
        Production Scenario
      </span>
    );
  }

  // 8. EXPERT DEEP DIVE - Staff / Architect (Violet)
  if (normalized === "EXPERT_DEEP_DIVE") {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-full font-bold bg-purple-500/15 text-purple-600 dark:text-purple-300 border border-purple-500/35", sizeClasses)}>
        <Sparkles className="h-3 w-3 text-purple-400 shrink-0" />
        Expert Deep Dive
      </span>
    );
  }

  return (
    <span className={cn("inline-flex items-center gap-1.5 rounded-full font-semibold bg-muted text-muted-foreground border border-border", sizeClasses)}>
      {difficulty}
    </span>
  );
};

export const TechnologyBadge: React.FC<{ 
  technology: string; 
  size?: "sm" | "md";
  showIcon?: boolean;
}> = ({ 
  technology, 
  size = "md",
  showIcon = true 
}) => {
  const t = (technology || "").toLowerCase();

  const sizeClasses = size === "sm" ? "px-2.5 py-0.5 text-xs font-semibold" : "px-3 py-1 text-xs sm:text-sm font-semibold";

  // AI / GenAI / LangGraph / RAG
  if (t.includes("ai") || t.includes("langgraph") || t.includes("rag") || t.includes("agent") || t.includes("llm")) {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-md font-semibold bg-purple-500/10 text-purple-600 dark:text-purple-300 border border-purple-500/25", sizeClasses)}>
        {showIcon && <Cpu className="h-3.5 w-3.5 text-purple-400 shrink-0" />}
        {technology}
      </span>
    );
  }

  // Java / JVM
  if (t.includes("java") || t.includes("jvm")) {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-md font-semibold bg-orange-500/10 text-orange-600 dark:text-orange-400 border border-orange-500/25", sizeClasses)}>
        {showIcon && <Terminal className="h-3.5 w-3.5 text-orange-400 shrink-0" />}
        {technology}
      </span>
    );
  }

  // Python
  if (t.includes("python")) {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-md font-semibold bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/25", sizeClasses)}>
        {showIcon && <Terminal className="h-3.5 w-3.5 text-blue-400 shrink-0" />}
        {technology}
      </span>
    );
  }

  // Spring Boot
  if (t.includes("spring")) {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-md font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/25", sizeClasses)}>
        {showIcon && <Server className="h-3.5 w-3.5 text-emerald-400 shrink-0" />}
        {technology}
      </span>
    );
  }

  // Kafka
  if (t.includes("kafka")) {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-md font-semibold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/25", sizeClasses)}>
        {showIcon && <Activity className="h-3.5 w-3.5 text-amber-400 shrink-0" />}
        {technology}
      </span>
    );
  }

  // Redis
  if (t.includes("redis")) {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-md font-semibold bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/25", sizeClasses)}>
        {showIcon && <Database className="h-3.5 w-3.5 text-rose-400 shrink-0" />}
        {technology}
      </span>
    );
  }

  // DSA
  if (t.includes("dsa") || t.includes("algorithm") || t.includes("data structure")) {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-md font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/25", sizeClasses)}>
        {showIcon && <Binary className="h-3.5 w-3.5 text-emerald-400 shrink-0" />}
        {technology}
      </span>
    );
  }

  // System Design / Distributed Systems
  if (t.includes("system") || t.includes("distributed") || t.includes("microservice") || t.includes("architecture")) {
    return (
      <span className={cn("inline-flex items-center gap-1.5 rounded-md font-semibold bg-sky-500/10 text-sky-600 dark:text-sky-400 border border-sky-500/25", sizeClasses)}>
        {showIcon && <Layers className="h-3.5 w-3.5 text-sky-400 shrink-0" />}
        {technology}
      </span>
    );
  }

  return (
    <span className={cn("inline-flex items-center gap-1.5 rounded-md font-semibold bg-secondary/80 text-foreground/80 border border-border/70", sizeClasses)}>
      {technology}
    </span>
  );
};

export const TrustBadge: React.FC<{ 
  type: "reviewed" | "source" | "version" | "production" | "original";
  label?: string;
  verified?: boolean;
}> = ({ 
  type, 
  label, 
  verified = true 
}) => {
  if (!verified) return null;

  const config = {
    reviewed: {
      defaultLabel: "Technically Reviewed",
      icon: <CheckCircle2 className="h-3 w-3 text-emerald-500 shrink-0" />,
      style: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border-emerald-500/20",
    },
    source: {
      defaultLabel: "Source Referenced",
      icon: <BookOpen className="h-3 w-3 text-sky-500 shrink-0" />,
      style: "bg-sky-500/10 text-sky-700 dark:text-sky-300 border-sky-500/20",
    },
    version: {
      defaultLabel: "Version 2026",
      icon: <GitBranch className="h-3 w-3 text-amber-500 shrink-0" />,
      style: "bg-amber-500/10 text-amber-700 dark:text-amber-300 border-amber-500/20",
    },
    production: {
      defaultLabel: "Production Focused",
      icon: <ShieldCheck className="h-3 w-3 text-teal-500 shrink-0" />,
      style: "bg-teal-500/10 text-teal-700 dark:text-teal-300 border-teal-500/20",
    },
    original: {
      defaultLabel: "Original Content",
      icon: <Sparkles className="h-3 w-3 text-purple-500 shrink-0" />,
      style: "bg-purple-500/10 text-purple-700 dark:text-purple-300 border-purple-500/20",
    },
  }[type];

  return (
    <span className={cn("inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md text-xs font-semibold border", config.style)}>
      {config.icon}
      <span>{label || config.defaultLabel}</span>
    </span>
  );
};

export const InterviewDepthBadge: React.FC<{ depth: string }> = ({ depth }) => {
  const depthLabels: Record<string, { label: string; style: string }> = {
    L1: { label: "L1 · Definition", style: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20" },
    L2: { label: "L2 · Mechanism", style: "bg-sky-500/10 text-sky-600 dark:text-sky-400 border-sky-500/20" },
    L3: { label: "L3 · Implementation", style: "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/20" },
    L4: { label: "L4 · Architecture", style: "bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/20" },
    L5: { label: "L5 · Scenario", style: "bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/20" },
  };

  const current = depthLabels[(depth || "").toUpperCase()] || {
    label: depth || "L1",
    style: "bg-primary/10 text-primary border-primary/20",
  };

  return (
    <span className={cn("inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-bold font-mono border", current.style)}>
      {current.label}
    </span>
  );
};
