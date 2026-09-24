"use client";

import React from "react";
import { 
  Cpu, 
  Database, 
  Terminal, 
  Binary, 
  Layers, 
  Sparkles, 
  Check, 
  Bot, 
  Coffee, 
  Server,
  Compass
} from "lucide-react";
import { prefetchReadingModeTrack } from "@/lib/api";

export interface TechTrackItem {
  id: string;
  name: string;
  slug: string;
  shortLabel?: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  activeBg: string;
  activeBorder: string;
  activeText: string;
  badgeBg: string;
}

export const KNOWN_TRACKS: TechTrackItem[] = [
  {
    id: "tech-1",
    name: "LangGraph & Agentic AI",
    shortLabel: "LangGraph / Agents",
    slug: "langgraph",
    icon: Bot,
    color: "text-purple-500",
    activeBg: "bg-purple-600 text-white shadow-purple-500/25",
    activeBorder: "border-purple-600",
    activeText: "text-white",
    badgeBg: "bg-purple-500/15 text-purple-700 dark:text-purple-300",
  },
  {
    id: "tech-2",
    name: "RAG & Vector Databases",
    shortLabel: "RAG & Vector DBs",
    slug: "rag-vector-db",
    icon: Database,
    color: "text-cyan-500",
    activeBg: "bg-cyan-600 text-white shadow-cyan-500/25",
    activeBorder: "border-cyan-600",
    activeText: "text-white",
    badgeBg: "bg-cyan-500/15 text-cyan-700 dark:text-cyan-300",
  },
  {
    id: "tech-3",
    name: "Java & JVM Concurrency",
    shortLabel: "Java & JVM Internals",
    slug: "java-backend",
    icon: Coffee,
    color: "text-orange-500",
    activeBg: "bg-orange-600 text-white shadow-orange-500/25",
    activeBorder: "border-orange-600",
    activeText: "text-white",
    badgeBg: "bg-orange-500/15 text-orange-700 dark:text-orange-300",
  },
  {
    id: "tech-4",
    name: "DSA & Algorithms",
    shortLabel: "DSA & Core Algos",
    slug: "dsa",
    icon: Binary,
    color: "text-pink-500",
    activeBg: "bg-pink-600 text-white shadow-pink-500/25",
    activeBorder: "border-pink-600",
    activeText: "text-white",
    badgeBg: "bg-pink-500/15 text-pink-700 dark:text-pink-300",
  },
  {
    id: "tech-5",
    name: "System Design",
    shortLabel: "System Design & Arch",
    slug: "system-design",
    icon: Server,
    color: "text-teal-500",
    activeBg: "bg-teal-600 text-white shadow-teal-500/25",
    activeBorder: "border-teal-600",
    activeText: "text-white",
    badgeBg: "bg-teal-500/15 text-teal-700 dark:text-teal-300",
  },
];

interface TechnologyTrackBarProps {
  selectedTech: string;
  onSelectTech: (techSlug: string) => void;
  technologies?: Array<{ id: string; name: string; slug: string }>;
  className?: string;
}

export const TechnologyTrackBar: React.FC<TechnologyTrackBarProps> = ({
  selectedTech,
  onSelectTech,
  technologies,
  className = "",
}) => {
  const isAllSelected = !selectedTech;

  return (
    <div className={`w-full space-y-3 p-4 sm:p-5 rounded-2xl bg-card/90 border border-border/80 backdrop-blur-md shadow-sm ${className}`}>
      {/* Top Header Label */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-border/40">
        <div className="flex items-center gap-2">
          <div className="h-6 w-6 rounded-lg bg-primary/10 text-primary flex items-center justify-center font-bold text-xs">
            <Compass className="h-3.5 w-3.5" />
          </div>
          <span className="text-xs font-mono font-bold uppercase tracking-wider text-foreground">
            Technology Track
          </span>
          <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-primary/10 text-primary border border-primary/20">
            5 Tracks
          </span>
        </div>

        <div className="text-xs text-muted-foreground flex items-center gap-2">
          {selectedTech ? (
            <span className="flex items-center gap-1.5 font-medium text-foreground">
              <span className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
              Active:{" "}
              <strong className="text-primary">
                {KNOWN_TRACKS.find((t) => t.slug === selectedTech)?.name || selectedTech.toUpperCase()}
              </strong>
              <button
                onClick={() => onSelectTech("")}
                className="ml-1 text-[11px] text-muted-foreground hover:text-foreground underline decoration-dotted font-semibold cursor-pointer"
              >
                Show All Tracks
              </button>
            </span>
          ) : (
            <span>All curriculum tracks combined</span>
          )}
        </div>
      </div>

      {/* Horizontal Track Selector Buttons */}
      <div className="flex items-center gap-2 overflow-x-auto scrollbar-none py-1 touch-pan-x">
        {/* All Tracks Option */}
        <button
          onClick={() => onSelectTech("")}
          className={`group flex items-center gap-2 px-3.5 py-2.5 rounded-xl text-xs sm:text-sm font-bold border transition-all duration-150 cursor-pointer shrink-0 ${
            isAllSelected
              ? "bg-primary text-primary-foreground border-primary shadow-md shadow-primary/25"
              : "bg-muted/40 hover:bg-muted/80 text-muted-foreground hover:text-foreground border-border/80"
          }`}
        >
          <Layers className={`h-4 w-4 ${isAllSelected ? "text-primary-foreground" : "text-primary"}`} />
          <span>All Tracks</span>
          {isAllSelected && <Check className="h-3.5 w-3.5 stroke-[3]" />}
        </button>

        {/* Individual Technology Track Buttons */}
        {KNOWN_TRACKS.map((t) => {
          const isSelected = selectedTech === t.slug;
          const Icon = t.icon;

          return (
            <button
              key={t.slug}
              onClick={() => onSelectTech(t.slug)}
              onMouseEnter={() => prefetchReadingModeTrack(t.slug)}
              className={`group flex items-center gap-2 px-3.5 py-2.5 rounded-xl text-xs sm:text-sm font-bold border transition-all duration-150 cursor-pointer shrink-0 ${
                isSelected
                  ? `${t.activeBg} ${t.activeBorder} shadow-md`
                  : "bg-muted/40 hover:bg-muted/80 text-muted-foreground hover:text-foreground border-border/80"
              }`}
            >
              <Icon className={`h-4 w-4 ${isSelected ? "text-white" : t.color} transition-transform group-hover:scale-110`} />
              <span>{t.name}</span>
              {isSelected && <Check className="h-3.5 w-3.5 stroke-[3]" />}
            </button>
          );
        })}
      </div>
    </div>
  );
};
