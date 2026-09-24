"use client";

import React, { useState } from "react";
import { Filter, X, RotateCcw, Cpu, Database, Terminal, Binary, Layers } from "lucide-react";
import { Button } from "@/components/ui/button";

interface FilterSidebarProps {
  selectedTech: string;
  selectedDifficulty: string;
  selectedDepth: string;
  onFilterChange: (filters: { tech?: string; difficulty?: string; depth?: string }) => void;
  technologies: Array<{ id: string; name: string; slug: string }>;
}

export const FilterSidebar: React.FC<FilterSidebarProps> = ({
  selectedTech,
  selectedDifficulty,
  selectedDepth,
  onFilterChange,
  technologies,
}) => {
  const [mobileOpen, setMobileOpen] = useState(false);


  const depths = [
    { label: "All Depths", value: "" },
    { label: "L1 · Definition", value: "L1" },
    { label: "L2 · Mechanism", value: "L2" },
    { label: "L3 · Implementation", value: "L3" },
    { label: "L4 · Architecture", value: "L4" },
    { label: "L5 · Scenario", value: "L5" },
  ];

  const hasActiveFilters = Boolean(selectedTech || selectedDifficulty || selectedDepth);

  const filterContent = (
    <div className="space-y-6">
      <div className="flex items-center justify-between pb-3 border-b border-border/60">
        <h4 className="text-sm font-extrabold tracking-tight text-foreground flex items-center gap-1.5">
          <Filter className="h-4 w-4 text-primary" />
          Faceted Filters
        </h4>
        {hasActiveFilters && (
          <button
            onClick={() => onFilterChange({ tech: "", difficulty: "", depth: "" })}
            className="text-[11px] text-muted-foreground hover:text-foreground flex items-center gap-1 font-semibold"
          >
            <RotateCcw className="h-3 w-3" />
            Reset
          </button>
        )}
      </div>

      {/* Technology Track Filter */}
      <div className="space-y-2">
        <label className="text-xs font-mono font-bold uppercase tracking-wider text-muted-foreground">
          Technology Pillar
        </label>
        <div className="space-y-1">
          <button
            onClick={() => onFilterChange({ tech: "" })}
            className={`w-full text-left px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              !selectedTech
                ? "bg-primary text-primary-foreground shadow-sm"
                : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"
            }`}
          >
            All 5 Technology Tracks
          </button>
          {technologies.map((t) => (
            <button
              key={t.id}
              onClick={() => onFilterChange({ tech: t.slug })}
              className={`w-full text-left px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                selectedTech === t.slug
                  ? "bg-primary text-primary-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"
              }`}
            >
              {t.name}
            </button>
          ))}
        </div>
      </div>

      {/* Interview Depth Filter */}
      <div className="space-y-2 pt-3 border-t border-border/40">
        <label className="text-xs font-mono font-bold uppercase tracking-wider text-muted-foreground">
          Interview Depth
        </label>
        <div className="space-y-1">
          {depths.map((dp) => (
            <button
              key={dp.value}
              onClick={() => onFilterChange({ depth: dp.value })}
              className={`w-full text-left px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                selectedDepth === dp.value
                  ? "bg-primary text-primary-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"
              }`}
            >
              {dp.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Mobile filter toggle trigger */}
      <div className="lg:hidden w-full mb-4">
        <Button
          variant="outline"
          className="w-full flex items-center justify-between"
          onClick={() => setMobileOpen(true)}
        >
          <span className="flex items-center gap-2">
            <Filter className="h-4 w-4" />
            <span>Filter Questions</span>
          </span>
          {hasActiveFilters && (
            <span className="h-2 w-2 rounded-full bg-primary" />
          )}
        </Button>
      </div>

      {/* Desktop Sidebar Panel */}
      <aside className="hidden lg:block w-64 shrink-0 rounded-2xl border border-border/80 bg-card p-5 shadow-sm sticky top-20 self-start max-h-[calc(100vh-6rem)] overflow-y-auto">
        {filterContent}
      </aside>

      {/* Mobile Drawer Overlay */}
      {mobileOpen && (
        <div className="lg:hidden fixed inset-0 z-50 flex">
          <div
            className="fixed inset-0 bg-background/80 backdrop-blur-sm"
            onClick={() => setMobileOpen(false)}
          />
          <div className="relative ml-auto w-full max-w-xs h-full bg-card p-6 shadow-xl border-l border-border flex flex-col justify-between overflow-y-auto">
            <div>
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-border">
                <span className="font-bold text-sm">Filters</span>
                <button onClick={() => setMobileOpen(false)} className="p-1">
                  <X className="h-5 w-5" />
                </button>
              </div>
              {filterContent}
            </div>

            <Button
              variant="primary"
              className="w-full mt-6"
              onClick={() => setMobileOpen(false)}
            >
              Apply Filters
            </Button>
          </div>
        </div>
      )}
    </>
  );
};
