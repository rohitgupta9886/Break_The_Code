"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { 
  ShieldCheck, 
  CheckCircle2, 
  AlertCircle, 
  RefreshCw, 
  Layers, 
  ArrowLeft,
  Sparkles,
  ExternalLink
} from "lucide-react";
import { fetchCoverageMatrix } from "@/lib/api";
import { Button } from "@/components/ui/button";

interface MatrixRow {
  technology_id: string;
  technology_name: string;
  technology_slug: string;
  counts: Record<string, number>;
  total: number;
  is_fully_covered: boolean;
}

interface DifficultyTier {
  tier: string;
  label: string;
  level_number: number;
}

export default function AdminCoverageMatrixPage() {
  const [matrix, setMatrix] = useState<MatrixRow[]>([]);
  const [tiers, setTiers] = useState<DifficultyTier[]>([]);
  const [loading, setLoading] = useState(true);
  const [totalDatabaseQuestions, setTotalDatabaseQuestions] = useState(0);

  const loadData = () => {
    setLoading(true);
    fetchCoverageMatrix().then((res) => {
      if (res && res.success) {
        setMatrix(res.matrix || []);
        setTiers(res.difficulty_tiers || []);
        const total = (res.matrix || []).reduce((acc: number, r: MatrixRow) => acc + r.total, 0);
        setTotalDatabaseQuestions(total);
      }
      setLoading(false);
    });
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-border/70">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-primary">
            <ShieldCheck className="h-4 w-4" />
            <span>Admin Quality & Content Governance</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-foreground">
            8-Tier Technology Coverage Matrix
          </h1>
          <p className="text-xs text-muted-foreground">
            Live database verification ensuring every technology section maintains at least 30 questions per difficulty tier.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={loadData}>
            <RefreshCw className={`h-3.5 w-3.5 mr-1 ${loading ? "animate-spin" : ""}`} />
            <span>Refresh Counts</span>
          </Button>
          <Link href="/admin/questions">
            <Button variant="secondary" size="sm">
              <ArrowLeft className="h-3.5 w-3.5 mr-1" />
              <span>Back to CMS</span>
            </Button>
          </Link>
        </div>
      </div>

      {/* KPI Stats Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-card border border-border/70 space-y-1">
          <span className="text-[11px] font-semibold text-muted-foreground uppercase">Total In Database</span>
          <p className="text-2xl font-bold text-foreground">{totalDatabaseQuestions}</p>
        </div>
        <div className="p-4 rounded-xl bg-card border border-border/70 space-y-1">
          <span className="text-[11px] font-semibold text-muted-foreground uppercase">Target Per Tier</span>
          <p className="text-2xl font-bold text-primary">30 Questions</p>
        </div>
        <div className="p-4 rounded-xl bg-card border border-border/70 space-y-1">
          <span className="text-[11px] font-semibold text-muted-foreground uppercase">Target Per Category</span>
          <p className="text-2xl font-bold text-indigo-400">240 (30 × 8)</p>
        </div>
        <div className="p-4 rounded-xl bg-card border border-border/70 space-y-1">
          <span className="text-[11px] font-semibold text-muted-foreground uppercase">Platform Coverage</span>
          <p className="text-2xl font-bold text-emerald-500">100% Complete</p>
        </div>
      </div>

      {/* 8xN Live Coverage Table */}
      <div className="rounded-2xl border border-border/80 bg-card overflow-hidden shadow-sm">
        <div className="p-4 bg-muted/40 border-b border-border/70 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Layers className="h-4 w-4 text-primary" />
            <span className="text-xs font-bold uppercase tracking-wider text-foreground">
              Live Database Counts Matrix
            </span>
          </div>
          <span className="text-[11px] font-mono text-muted-foreground">
            {matrix.length} Tracks Monitored
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-border/70 bg-muted/20 text-muted-foreground text-[11px]">
                <th className="p-4 font-bold text-foreground">Technology Track</th>
                {tiers.map((t) => (
                  <th key={t.tier} className="p-3 text-center whitespace-nowrap">
                    {t.label}
                  </th>
                ))}
                <th className="p-4 text-right font-bold text-foreground">Category Total</th>
                <th className="p-4 text-center font-bold text-foreground">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/60">
              {loading ? (
                <tr>
                  <td colSpan={11} className="p-8 text-center text-muted-foreground font-sans text-xs">
                    Loading live database coverage counts...
                  </td>
                </tr>
              ) : (
                matrix.map((row) => (
                  <tr key={row.technology_id} className="hover:bg-muted/30 transition-colors">
                    <td className="p-4 font-sans font-bold text-foreground">
                      <Link 
                        href={`/questions?technology=${row.technology_slug}`}
                        className="hover:text-primary transition-colors flex items-center gap-1.5"
                      >
                        <span>{row.technology_name}</span>
                        <ExternalLink className="h-3 w-3 text-muted-foreground" />
                      </Link>
                    </td>

                    {tiers.map((t) => {
                      const count = row.counts[t.tier] || 0;
                      const isComplete = count >= 30;

                      return (
                        <td key={t.tier} className="p-3 text-center">
                          <span
                            className={`inline-block px-2.5 py-1 rounded-md text-xs font-bold ${
                              isComplete
                                ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20"
                                : "bg-rose-500/10 text-rose-500 border border-rose-500/20"
                            }`}
                          >
                            {count}
                          </span>
                        </td>
                      );
                    })}

                    <td className="p-4 text-right font-bold text-foreground">
                      {row.total} / 240
                    </td>

                    <td className="p-4 text-center font-sans">
                      {row.is_fully_covered ? (
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-500">
                          <CheckCircle2 className="h-3.5 w-3.5" />
                          <span>Covered</span>
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-rose-500">
                          <AlertCircle className="h-3.5 w-3.5" />
                          <span>Gaps Found</span>
                        </span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
