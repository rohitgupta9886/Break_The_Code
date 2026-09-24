import React from "react";
import { Hero } from "@/components/landing/hero";
import { DailyChallenge } from "@/components/landing/daily-challenge";
import { TrackGrid } from "@/components/landing/track-grid";
import { DifficultyExplorer } from "@/components/landing/difficulty-explorer";
import { ProductionHighlights } from "@/components/landing/production-highlights";
import { Features } from "@/components/landing/features";
import { FAQ } from "@/components/landing/faq";
import { fetchTechnologies } from "@/lib/api";

export const revalidate = 60; // Incremental Static Regeneration

export default async function HomePage() {
  const technologies = await fetchTechnologies();

  return (
    <div className="flex flex-col w-full">
      {/* 1. Hero with Workflow Visual & Real Database Metrics */}
      <Hero />

      {/* 2. Today's Daily Interview Challenge */}
      <DailyChallenge />

      {/* 3. Explore By Technology (Multicolor Cards) */}
      <TrackGrid technologies={technologies} />

      {/* 4. How Far Can You Go? (8-Tier Difficulty Explorer) */}
      <DifficultyExplorer />

      {/* 5. Production Incident Drill, Staff Engineer Corner & Trust Badges */}
      <ProductionHighlights />

      {/* 6. Learning System Architecture Features */}
      <Features />

      {/* 7. Frequently Asked Questions */}
      <FAQ />
    </div>
  );
}
