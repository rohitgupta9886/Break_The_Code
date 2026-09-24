"use client";

import React, { ReactNode } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  RotateCcw,
  Bookmark,
  History,
  Trophy,
  ArrowRight,
  Flame,
  Zap,
  Sparkles,
  BookOpen
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const { user, loginAsDemo, isLoading } = useAuth();

  const navItems = [
    {
      name: "Overview",
      href: "/dashboard",
      icon: LayoutDashboard,
      active: pathname === "/dashboard",
    },
    {
      name: "Spaced Repetition",
      href: "/dashboard/revision",
      icon: RotateCcw,
      active: pathname === "/dashboard/revision",
    },
    {
      name: "Saved Bookmarks",
      href: "/dashboard/bookmarks",
      icon: Bookmark,
      active: pathname === "/dashboard/bookmarks",
    },
    {
      name: "Attempt History",
      href: "/dashboard/history",
      icon: History,
      active: pathname === "/dashboard/history",
    },
    {
      name: "Badges & Trophies",
      href: "/dashboard/badges",
      icon: Trophy,
      active: pathname === "/dashboard/badges",
    },
  ];

  if (!isLoading && !user) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <div className="h-16 w-16 mx-auto mb-6 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
          <Sparkles className="h-8 w-8" />
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-foreground mb-2">
          Candidate Portal & Dashboard
        </h2>
        <p className="text-sm text-muted-foreground max-w-md mx-auto mb-6">
          Sign in or jump straight in using the instant 1-click Demo Candidate account to track your progress, XP, spaced repetition, and attempts.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Button
            variant="primary"
            onClick={() => loginAsDemo("candidate")}
            className="flex items-center gap-2"
          >
            <Sparkles className="h-4 w-4" />
            Continue as Demo Candidate
          </Button>
          <Link href="/questions">
            <Button variant="outline">Browse Questions</Button>
          </Link>
        </div>
      </div>
    );
  }

  const nextLevelXp = user ? user.level * 200 : 200;
  const currentBaseXp = user ? (user.level - 1) * 200 : 0;
  const progressPct = user
    ? Math.min(100, Math.round(((user.xp - currentBaseXp) / 200) * 100))
    : 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Sidebar */}
        <aside className="lg:col-span-3 space-y-6">
          {/* User mini profile card */}
          {user && (
            <div className="p-5 rounded-2xl border border-border/80 bg-card/60 backdrop-blur-md shadow-sm">
              <div className="flex items-center gap-3.5 mb-4">
                <div className="h-12 w-12 rounded-xl bg-gradient-to-tr from-primary to-emerald-500 flex items-center justify-center text-primary-foreground font-bold text-lg uppercase shadow-md">
                  {user.full_name ? user.full_name[0] : user.email[0]}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-bold text-foreground truncate">
                    {user.full_name || "Candidate"}
                  </h3>
                  <p className="text-xs text-muted-foreground truncate">{user.email}</p>
                </div>
              </div>

              {/* Stats badges */}
              <div className="grid grid-cols-2 gap-2 mb-4">
                <div className="p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center gap-2">
                  <Flame className="h-4 w-4 text-amber-500 fill-amber-500" />
                  <div>
                    <div className="text-xs font-bold text-amber-500">{user.streak_days} Days</div>
                    <div className="text-[10px] text-muted-foreground">Active Streak</div>
                  </div>
                </div>
                <div className="p-2.5 rounded-lg bg-primary/10 border border-primary/20 flex items-center gap-2">
                  <Zap className="h-4 w-4 text-primary fill-primary" />
                  <div>
                    <div className="text-xs font-bold text-primary">{user.xp} XP</div>
                    <div className="text-[10px] text-muted-foreground">Level {user.level}</div>
                  </div>
                </div>
              </div>

              {/* Level Progress Bar */}
              <div>
                <div className="flex items-center justify-between text-[11px] mb-1.5">
                  <span className="text-muted-foreground">Level {user.level} Progress</span>
                  <span className="font-semibold text-foreground">{progressPct}%</span>
                </div>
                <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-primary to-emerald-400 rounded-full transition-all duration-500"
                    style={{ width: `${progressPct}%` }}
                  />
                </div>
                <div className="text-right text-[10px] text-muted-foreground mt-1">
                  {user.xp} / {nextLevelXp} XP to Level {user.level + 1}
                </div>
              </div>
            </div>
          )}

          {/* Navigation Links */}
          <nav className="p-2 rounded-2xl border border-border/80 bg-card/40 backdrop-blur-md space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    item.active
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted/60"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span className="flex-1">{item.name}</span>
                </Link>
              );
            })}

            <div className="pt-2 border-t border-border/50 my-1" />

            <Link
              href="/questions"
              className="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-muted/60 transition-colors"
            >
              <BookOpen className="h-4 w-4" />
              <span>Browse Questions</span>
              <ArrowRight className="h-3.5 w-3.5 ml-auto text-muted-foreground/60" />
            </Link>
          </nav>
        </aside>

        {/* Main Content Area */}
        <main className="lg:col-span-9">{children}</main>
      </div>
    </div>
  );
}
