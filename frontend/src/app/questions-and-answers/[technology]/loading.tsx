import React from "react";

export default function Loading() {
  return (
    <div className="min-h-screen bg-background text-foreground animate-fade-in">
      {/* 1. Header Banner Skeleton */}
      <div className="border-b border-rose-200/80 dark:border-rose-900/60 bg-gradient-to-b from-rose-100/50 via-background to-background dark:from-rose-950/20 dark:via-background dark:to-background py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="h-4 w-48 bg-muted/80 rounded-md animate-pulse" />
            <div className="h-10 w-60 bg-muted/80 rounded-2xl animate-pulse" />
          </div>

          <div className="space-y-3">
            <div className="h-9 sm:h-12 w-3/4 max-w-xl bg-muted/80 rounded-2xl animate-pulse" />
            <div className="h-4 w-full max-w-2xl bg-muted/60 rounded-md animate-pulse" />
          </div>

          {/* Quick Stats Pill Skeletons */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-16 rounded-2xl bg-card border border-border/60 animate-pulse" />
            ))}
          </div>
        </div>
      </div>

      {/* 2. Main Content Skeleton (TOC + Question Cards) */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left TOC Skeleton */}
          <aside className="hidden lg:block lg:col-span-3 space-y-4">
            <div className="p-4 rounded-2xl bg-card border border-border/80 space-y-3">
              <div className="h-4 w-32 bg-muted/80 rounded animate-pulse" />
              <div className="space-y-2 pt-2">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                  <div key={i} className="h-3 w-full bg-muted/60 rounded animate-pulse" />
                ))}
              </div>
            </div>
          </aside>

          {/* Right Question Cards Feed Skeleton */}
          <main className="lg:col-span-9 space-y-6">
            <div className="p-6 rounded-3xl bg-card border border-border/80 space-y-4">
              <div className="h-6 w-48 bg-muted/80 rounded-xl animate-pulse" />
              <div className="h-4 w-full bg-muted/50 rounded animate-pulse" />
            </div>

            {[1, 2, 3].map((i) => (
              <div key={i} className="p-6 rounded-3xl bg-card border border-border/80 space-y-4 animate-pulse">
                <div className="flex items-center gap-3">
                  <div className="h-6 w-16 bg-muted/80 rounded-full" />
                  <div className="h-6 w-24 bg-muted/60 rounded-full" />
                </div>
                <div className="h-6 w-5/6 bg-muted/80 rounded-lg" />
                <div className="h-20 w-full bg-muted/40 rounded-2xl" />
              </div>
            ))}
          </main>
        </div>
      </div>
    </div>
  );
}
