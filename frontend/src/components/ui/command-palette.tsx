"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { 
  Search, 
  Terminal, 
  Cpu, 
  Server, 
  Binary, 
  Layers, 
  Sparkles, 
  Flame, 
  Bookmark, 
  LayoutDashboard, 
  X,
  ArrowRight,
  Command
} from "lucide-react";

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({ isOpen, onClose }) => {
  const router = useRouter();
  const [query, setQuery] = useState("");

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        if (isOpen) {
          onClose();
        } else {
          // Open handled by parent or toggled
        }
      }
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const quickNav = [
    { label: "Search All Questions", href: `/questions?search=${encodeURIComponent(query)}`, icon: <Search className="h-4 w-4 text-primary" />, category: "Search" },
    { label: "AI & GenAI (LangGraph, RAG, Agents)", href: "/questions?technology=langgraph", icon: <Cpu className="h-4 w-4 text-purple-500" />, category: "Technology" },
    { label: "Java & JVM Internals", href: "/questions?technology=java-backend", icon: <Terminal className="h-4 w-4 text-orange-500" />, category: "Technology" },
    { label: "High-Level & Distributed System Design", href: "/questions?technology=system-design", icon: <Layers className="h-4 w-4 text-teal-500" />, category: "Technology" },
    { label: "Data Structures & Core Algorithms", href: "/questions?technology=dsa", icon: <Binary className="h-4 w-4 text-pink-500" />, category: "Technology" },
    { label: "Browse Production Scenarios (Level 7)", href: "/questions?difficulty=PRODUCTION_SCENARIO", icon: <Flame className="h-4 w-4 text-amber-500" />, category: "Difficulty" },
    { label: "Browse Expert Deep Dives (Level 8)", href: "/questions?difficulty=EXPERT_DEEP_DIVE", icon: <Sparkles className="h-4 w-4 text-purple-600" />, category: "Difficulty" },
    { label: "8-Tier Difficulty Hub", href: "/difficulty", icon: <Layers className="h-4 w-4 text-sky-500" />, category: "Navigation" },
    { label: "Candidate Learning Dashboard", href: "/dashboard", icon: <LayoutDashboard className="h-4 w-4 text-emerald-500" />, category: "Dashboard" },
  ];

  const filtered = query.trim()
    ? quickNav.filter(item => item.label.toLowerCase().includes(query.toLowerCase()) || item.category.toLowerCase().includes(query.toLowerCase()))
    : quickNav;

  const handleSelect = (href: string) => {
    onClose();
    router.push(href);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 sm:pt-28 px-4 bg-background/80 backdrop-blur-md transition-all">
      <div 
        className="relative w-full max-w-xl rounded-2xl border border-border/80 bg-card shadow-2xl overflow-hidden animate-fade-in"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header Search Input */}
        <div className="flex items-center px-4 py-3 border-b border-border/80 bg-muted/20">
          <Search className="h-5 w-5 text-muted-foreground mr-3 shrink-0" />
          <input
            type="text"
            placeholder="Type a command, technology, or topic (LangGraph, RAG, Java, Kafka)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
            className="w-full bg-transparent text-sm sm:text-base text-foreground placeholder:text-muted-foreground focus:outline-none"
            onKeyDown={(e) => {
              if (e.key === "Enter" && filtered.length > 0) {
                handleSelect(filtered[0].href);
              }
            }}
          />
          <button 
            onClick={onClose}
            className="p-1 rounded-md text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Results List */}
        <div className="max-h-80 overflow-y-auto p-2 space-y-1">
          {filtered.length > 0 ? (
            filtered.map((item, idx) => (
              <button
                key={idx}
                onClick={() => handleSelect(item.href)}
                className="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl hover:bg-muted/60 transition-colors text-left group"
              >
                <div className="flex items-center gap-3">
                  <div className="p-1.5 rounded-lg bg-background border border-border/80">
                    {item.icon}
                  </div>
                  <div>
                    <span className="text-xs sm:text-sm font-medium text-foreground group-hover:text-primary transition-colors">
                      {item.label}
                    </span>
                    <span className="ml-2 text-[10px] uppercase font-semibold text-muted-foreground px-1.5 py-0.5 rounded bg-muted/60">
                      {item.category}
                    </span>
                  </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground/40 group-hover:text-primary group-hover:translate-x-0.5 transition-all" />
              </button>
            ))
          ) : (
            <div className="py-8 text-center">
              <p className="text-sm text-muted-foreground">
                No commands matching &ldquo;{query}&rdquo;
              </p>
              <button
                onClick={() => handleSelect(`/questions?search=${encodeURIComponent(query)}`)}
                className="mt-3 inline-flex items-center gap-1.5 text-xs font-semibold text-primary hover:underline"
              >
                Search full question database for &ldquo;{query}&rdquo; &rarr;
              </button>
            </div>
          )}
        </div>

        {/* Footer shortcuts */}
        <div className="px-4 py-2.5 bg-muted/40 border-t border-border/60 flex items-center justify-between text-[11px] text-muted-foreground font-mono">
          <div className="flex items-center gap-3">
            <span><kbd className="px-1.5 py-0.5 rounded bg-background border border-border">↵</kbd> select</span>
            <span><kbd className="px-1.5 py-0.5 rounded bg-background border border-border">esc</kbd> close</span>
          </div>
          <span className="flex items-center gap-1">
            <Command className="h-3 w-3" /> Break The Code
          </span>
        </div>
      </div>
    </div>
  );
};
