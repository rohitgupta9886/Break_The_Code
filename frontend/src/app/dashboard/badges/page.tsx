"use client";

import React, { useEffect, useState } from "react";
import {
  Trophy,
  Zap,
  Award,
  Cpu,
  Bot,
  Coffee,
  Binary,
  Flame,
  ShieldCheck,
  Lock,
  Sparkles,
  CheckCircle2
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { fetchUserBadges } from "@/lib/api";

const ICON_MAP: Record<string, any> = {
  Zap: Zap,
  Award: Award,
  Cpu: Cpu,
  Bot: Bot,
  Coffee: Coffee,
  Binary: Binary,
  Flame: Flame,
  ShieldCheck: ShieldCheck,
  Trophy: Trophy,
};

export default function BadgesPage() {
  const { token } = useAuth();
  const [badges, setBadges] = useState<any[]>([]);
  const [unlockedCount, setUnlockedCount] = useState(0);
  const [totalBadges, setTotalBadges] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      loadBadges();
    }
  }, [token]);

  const loadBadges = async () => {
    if (!token) return;
    setLoading(true);
    const data = await fetchUserBadges(token);
    setBadges(data.badges || []);
    setUnlockedCount(data.unlocked_count || 0);
    setTotalBadges(data.total_badges || 0);
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <Trophy className="h-5 w-5 text-amber-500 fill-amber-500" />
            Badges & Achievements Trophy Case
          </h2>
          <p className="text-xs text-muted-foreground mt-0.5">
            Earn engineering distinctions as you conquer technical interview problems across our AI, JVM, and DSA curricula.
          </p>
        </div>

        <div className="px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-500 text-xs font-bold">
          {unlockedCount} / {totalBadges} Unlocked
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-40 rounded-2xl bg-muted/40 animate-pulse" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {badges.map((b) => {
            const Icon = ICON_MAP[b.icon] || Trophy;
            const isUnlocked = b.is_unlocked;

            return (
              <div
                key={b.badge_key}
                className={`p-5 rounded-2xl border transition-all relative overflow-hidden flex flex-col justify-between ${
                  isUnlocked
                    ? "bg-gradient-to-br from-card via-card to-amber-500/5 border-amber-500/40 shadow-sm"
                    : "bg-card/40 border-border/70 opacity-60"
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div
                      className={`h-11 w-11 rounded-xl flex items-center justify-center ${
                        isUnlocked
                          ? "bg-gradient-to-tr from-amber-500/20 to-primary/20 text-amber-500 border border-amber-500/30 shadow-md"
                          : "bg-muted text-muted-foreground"
                      }`}
                    >
                      <Icon className="h-6 w-6" />
                    </div>

                    {isUnlocked ? (
                      <span className="flex items-center gap-1 text-[11px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                        <CheckCircle2 className="h-3 w-3" /> Unlocked
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-[11px] font-medium text-muted-foreground bg-muted px-2 py-0.5 rounded-full">
                        <Lock className="h-3 w-3" /> Locked
                      </span>
                    )}
                  </div>

                  <h3 className="font-bold text-sm text-foreground mb-1">
                    {b.badge_name}
                  </h3>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {b.badge_description}
                  </p>
                </div>

                <div className="pt-4 border-t border-border/40 mt-4 text-[11px] text-muted-foreground">
                  {isUnlocked && b.unlocked_at ? (
                    <span>Earned {new Date(b.unlocked_at).toLocaleDateString()}</span>
                  ) : (
                    <span>Solve qualifying problems to unlock</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
