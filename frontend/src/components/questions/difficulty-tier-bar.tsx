"use client";

import React from "react";
import { Layers, Sparkles, Check, Flame, Crown, ShieldAlert } from "lucide-react";

export interface DifficultyTierItem {
  tier: string;
  level: number;
  shortLabel: string;
  label: string;
  sub: string;
  dotColor: string;
  activeBg: string;
  activeRing: string;
  activeText: string;
  badgeBg: string;
}

export const DIFFICULTY_TIERS: DifficultyTierItem[] = [
  {
    tier: "BASIC",
    level: 1,
    shortLabel: "L1",
    label: "Basic",
    sub: "Fundamentals",
    dotColor: "bg-emerald-500",
    activeBg: "bg-emerald-600 text-white shadow-emerald-500/25",
    activeRing: "ring-2 ring-emerald-500",
    activeText: "text-white",
    badgeBg: "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300",
  },
  {
    tier: "MEDIUM",
    level: 2,
    shortLabel: "L2",
    label: "Medium",
    sub: "Foundations",
    dotColor: "bg-sky-500",
    activeBg: "bg-sky-600 text-white shadow-sky-500/25",
    activeRing: "ring-2 ring-sky-500",
    activeText: "text-white",
    badgeBg: "bg-sky-500/15 text-sky-700 dark:text-sky-300",
  },
  {
    tier: "HARD",
    level: 3,
    shortLabel: "L3",
    label: "Hard",
    sub: "Concurrency",
    dotColor: "bg-indigo-500",
    activeBg: "bg-indigo-600 text-white shadow-indigo-500/25",
    activeRing: "ring-2 ring-indigo-500",
    activeText: "text-white",
    badgeBg: "bg-indigo-500/15 text-indigo-700 dark:text-indigo-300",
  },
  {
    tier: "TOUGH",
    level: 4,
    shortLabel: "L4",
    label: "Tough",
    sub: "Bottlenecks",
    dotColor: "bg-amber-500",
    activeBg: "bg-amber-500 text-white shadow-amber-500/25",
    activeRing: "ring-2 ring-amber-500",
    activeText: "text-white",
    badgeBg: "bg-amber-500/15 text-amber-700 dark:text-amber-300",
  },
  {
    tier: "VERY_TOUGH",
    level: 5,
    shortLabel: "L5",
    label: "Very Tough",
    sub: "Scale & Split",
    dotColor: "bg-orange-500",
    activeBg: "bg-orange-600 text-white shadow-orange-500/25",
    activeRing: "ring-2 ring-orange-500",
    activeText: "text-white",
    badgeBg: "bg-orange-500/15 text-orange-700 dark:text-orange-300",
  },
  {
    tier: "VERY_VERY_TOUGH",
    level: 6,
    shortLabel: "L6",
    label: "Very Very Tough",
    sub: "Consensus",
    dotColor: "bg-rose-600",
    activeBg: "bg-rose-600 text-white shadow-rose-600/25",
    activeRing: "ring-2 ring-rose-500",
    activeText: "text-white",
    badgeBg: "bg-rose-500/15 text-rose-700 dark:text-rose-300",
  },
  {
    tier: "PRODUCTION_SCENARIO",
    level: 7,
    shortLabel: "L7",
    label: "Production",
    sub: "Live Incident",
    dotColor: "bg-teal-500",
    activeBg: "bg-teal-600 text-white shadow-teal-500/25",
    activeRing: "ring-2 ring-teal-500",
    activeText: "text-white",
    badgeBg: "bg-teal-500/15 text-teal-700 dark:text-teal-300",
  },
  {
    tier: "EXPERT_DEEP_DIVE",
    level: 8,
    shortLabel: "L8",
    label: "Expert",
    sub: "Staff Architect",
    dotColor: "bg-purple-600",
    activeBg: "bg-purple-600 text-white shadow-purple-500/25",
    activeRing: "ring-2 ring-purple-500",
    activeText: "text-white",
    badgeBg: "bg-purple-500/15 text-purple-700 dark:text-purple-300",
  },
];

interface DifficultyTierBarProps {
  selectedDifficulty: string;
  onSelectDifficulty: (difficulty: string) => void;
  totalFiltered?: number;
}

export const DifficultyTierBar: React.FC<DifficultyTierBarProps> = ({
  selectedDifficulty,
  onSelectDifficulty,
  totalFiltered,
}) => {
  const isAllSelected = !selectedDifficulty;

  return (
    <div className="w-full space-y-3 p-4 sm:p-5 rounded-2xl bg-card/90 border border-border/80 backdrop-blur-md shadow-sm">
      {/* Header bar with title & active filter status */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-border/40">
        <div className="flex items-center gap-2">
          <div className="h-6 w-6 rounded-lg bg-primary/10 text-primary flex items-center justify-center font-bold text-xs">
            <Layers className="h-3.5 w-3.5" />
          </div>
          <span className="text-xs font-mono font-bold uppercase tracking-wider text-foreground">
            Difficulty Progression
          </span>
          <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-600 border border-rose-500/20">
            8 Tiers
          </span>
        </div>

        <div className="text-xs text-muted-foreground flex items-center gap-2">
          {selectedDifficulty ? (
            <span className="flex items-center gap-1.5 font-medium text-foreground">
              <span className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
              Filtered:{" "}
              <strong className="text-primary">
                {DIFFICULTY_TIERS.find((t) => t.tier === selectedDifficulty)?.label}
              </strong>
              <button
                onClick={() => onSelectDifficulty("")}
                className="ml-1 text-[11px] text-muted-foreground hover:text-foreground underline decoration-dotted font-semibold"
              >
                Reset to All
              </button>
            </span>
          ) : (
            <span className="text-xs text-muted-foreground">
              Showing questions across <span className="font-semibold text-foreground">all 8 tiers</span>
            </span>
          )}
        </div>
      </div>

      {/* 8 Tiers + All Selector: Desktop Grid / Mobile Horizontal Scroll */}
      <div className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 gap-2">
        {/* All Tiers Button */}
        <button
          onClick={() => onSelectDifficulty("")}
          className={`flex flex-col items-center justify-center p-2.5 rounded-xl border text-center transition-all duration-200 group relative ${
            isAllSelected
              ? "bg-primary text-primary-foreground border-primary shadow-md shadow-rose-500/20"
              : "bg-background/60 hover:bg-muted/60 border-border/70 text-foreground hover:border-primary/40"
          }`}
        >
          <div className="flex items-center gap-1 mb-1">
            <span
              className={`h-2 w-2 rounded-full ${
                isAllSelected ? "bg-white" : "bg-muted-foreground"
              }`}
            />
            <span className="text-[11px] font-mono font-black uppercase tracking-wide opacity-80">
              ALL
            </span>
          </div>
          <span className="text-xs font-extrabold leading-tight">All Tiers</span>
          <span
            className={`text-[11px] font-semibold leading-none mt-1 ${
              isAllSelected ? "text-white/90" : "text-muted-foreground"
            }`}
          >
            All 8 Levels
          </span>
          {isAllSelected && (
            <div className="absolute top-1 right-1">
              <Check className="h-3 w-3 text-white" />
            </div>
          )}
        </button>

        {/* 8 Individual Difficulty Tiers */}
        {DIFFICULTY_TIERS.map((tier) => {
          const isSelected = selectedDifficulty === tier.tier;

          return (
            <button
              key={tier.tier}
              onClick={() => onSelectDifficulty(isSelected ? "" : tier.tier)}
              className={`flex flex-col items-center justify-center p-2.5 rounded-xl border text-center transition-all duration-200 group relative ${
                isSelected
                  ? `${tier.activeBg} border-transparent shadow-md ${tier.activeRing}`
                  : `bg-background/60 hover:bg-muted/60 border-border/70 text-foreground hover:border-border`
              }`}
            >
              {/* Level indicator & Dot */}
              <div className="flex items-center gap-1 mb-1">
                <span
                  className={`h-2 w-2 rounded-full ${
                    isSelected ? "bg-white" : tier.dotColor
                  }`}
                />
                <span
                  className={`text-[11px] font-mono font-black tracking-wide ${
                    isSelected ? "text-white/95" : "text-muted-foreground"
                  }`}
                >
                  {tier.shortLabel}
                </span>
              </div>

              {/* Tier Name */}
              <span className="text-xs font-extrabold leading-tight line-clamp-1">
                {tier.label}
              </span>

              {/* Sub-label */}
              <span
                className={`text-[11px] font-semibold leading-none mt-1 line-clamp-1 ${
                  isSelected ? "text-white/90" : "text-muted-foreground"
                }`}
              >
                {tier.sub}
              </span>

              {/* Active Checkmark */}
              {isSelected && (
                <div className="absolute top-1 right-1">
                  <Check className="h-3 w-3 text-white" />
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};
