"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";
import {
  Search,
  BookOpen,
  Layers,
  ShieldCheck,
  Sparkles,
  Flame,
  Zap,
  Bookmark,
  History,
  RotateCcw,
  Trophy,
  LayoutDashboard,
  LogOut,
  ChevronDown,
  Command,
  Play,
  Users,
  LogIn,
  Target
} from "lucide-react";
import { ThemeToggle } from "./theme-toggle";
import { Logo } from "./logo";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth-context";
import { CommandPalette } from "@/components/ui/command-palette";

export const Navbar: React.FC = () => {
  const router = useRouter();
  const pathname = usePathname();
  const { user, loginAsDemo, logout, isLoading } = useAuth();
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setIsCommandPaletteOpen((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleDemoCandidateLogin = async () => {
    await loginAsDemo("candidate");
    router.push("/dashboard");
  };

  const navLinks = [
    {
      href: "/questions",
      label: "Questions",
      icon: Target,
      iconColor: "text-amber-500",
      badge: "750+",
      active: pathname === "/questions" || pathname.startsWith("/questions/"),
    },
    {
      href: "/learn",
      label: "Tracks",
      icon: Layers,
      iconColor: "text-teal-500",
      badge: "5",
      active: pathname.startsWith("/learn"),
    },
    {
      href: "/difficulty",
      label: "Difficulty",
      icon: Sparkles,
      iconColor: "text-purple-500",
      active: pathname.startsWith("/difficulty"),
    },
    {
      href: "/dashboard",
      label: "Dashboard",
      icon: LayoutDashboard,
      iconColor: "text-emerald-500",
      active: pathname.startsWith("/dashboard"),
    },
  ];

  return (
    <>
      <header className="sticky top-0 z-40 w-full max-w-[100vw] border-b border-rose-200/90 dark:border-rose-900/60 bg-white/95 dark:bg-[#0d0610]/95 backdrop-blur-2xl shadow-[0_4px_30px_-6px_rgba(244,63,94,0.14)] dark:shadow-[0_8px_32px_rgba(0,0,0,0.7)] transition-colors">
        {/* Top Iridescent Gradient Energy Bar */}
        <div className="h-[2.5px] w-full bg-gradient-to-r from-rose-500 via-pink-500 via-amber-400 to-rose-500 opacity-90" />

        <div className="w-full flex h-20 items-center justify-between px-3 sm:px-6 lg:px-8 xl:px-12 gap-2 sm:gap-4 lg:gap-6">
          
          {/* 1. Left: Enhanced Logo & Brandmark */}
          <div className="flex items-center gap-3 xl:gap-6 shrink-0">
            <Logo size="lg" />

            {/* Desktop Navigation Links */}
            <nav className="hidden lg:flex items-center gap-1 xl:gap-1.5">
              {navLinks.map((link) => {
                const Icon = link.icon;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`flex items-center gap-1.5 px-3 py-2 rounded-2xl text-xs xl:text-sm font-semibold whitespace-nowrap transition-all duration-200 ${
                      link.active
                        ? "bg-gradient-to-r from-rose-500/15 via-pink-500/15 to-amber-500/10 text-rose-700 dark:text-rose-300 font-bold border border-rose-400/40 dark:border-rose-500/40 shadow-xs shadow-rose-500/10"
                        : "text-muted-foreground hover:text-foreground hover:bg-rose-500/8 dark:hover:bg-white/10"
                    }`}
                  >
                    <Icon className={`h-4 w-4 ${link.iconColor} shrink-0`} />
                    <span>{link.label}</span>
                    {link.badge && (
                      <span className="text-[10px] font-mono px-1.5 py-0.5 rounded-full bg-white/90 dark:bg-black/40 border border-border/80 text-muted-foreground font-bold shadow-2xs">
                        {link.badge}
                      </span>
                    )}
                  </Link>
                );
              })}
            </nav>
          </div>

          {/* 2. Center: Global Search Command Trigger */}
          <div className="flex-1 min-w-0 max-w-xs md:max-w-sm lg:max-w-md mx-1 sm:mx-2">
            <button
              onClick={() => setIsCommandPaletteOpen(true)}
              className="w-full h-10 px-3.5 rounded-2xl bg-rose-50/70 dark:bg-black/40 hover:bg-white dark:hover:bg-black/60 border border-rose-200/80 dark:border-rose-900/60 hover:border-rose-400 dark:hover:border-rose-500 flex items-center justify-between text-xs text-muted-foreground hover:text-foreground transition-all duration-200 shadow-2xs hover:shadow-xs group cursor-pointer"
            >
              <span className="flex items-center gap-2 truncate">
                <Search className="h-4 w-4 text-rose-500 group-hover:scale-110 transition-transform shrink-0" />
                <span className="truncate font-medium">Search 750+ questions...</span>
              </span>
              <kbd className="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded-lg text-[10px] font-mono font-bold bg-white dark:bg-rose-950/70 border border-rose-200/80 dark:border-rose-900/60 text-rose-700 dark:text-rose-300 shadow-2xs shrink-0">
                <Command className="h-3 w-3" /> K
              </kbd>
            </button>
          </div>


          {/* 4. Right: Action Controls (Practice CTA, Theme, User Profile) */}
          <div className="flex items-center gap-2 sm:gap-2.5 shrink-0">
            {/* Theme Toggle Button */}
            <ThemeToggle />

            {/* User Authentication / Profile */}
            {user ? (
              <div className="flex items-center gap-2 sm:gap-2.5">
                {/* Streak Badge */}
                <div
                  title={`${user.streak_days} Day Streak`}
                  className="flex items-center gap-1.5 h-11 px-3.5 rounded-2xl bg-amber-500/15 border border-amber-500/30 text-amber-700 dark:text-amber-300 text-xs font-bold shadow-2xs"
                >
                  <Flame className="h-4 w-4 fill-amber-500 text-amber-500 animate-pulse" />
                  <span>{user.streak_days}d</span>
                </div>

                {/* XP Level Badge */}
                <div
                  title={`Level ${user.level} (${user.xp} XP)`}
                  className="hidden md:flex items-center gap-1.5 h-11 px-3.5 rounded-2xl bg-rose-100/90 dark:bg-rose-950/60 border border-rose-200/90 dark:border-rose-900/60 text-rose-700 dark:text-rose-300 text-xs font-bold shadow-2xs"
                >
                  <Zap className="h-4 w-4 fill-rose-500 text-rose-500" />
                  <span>Lvl {user.level}</span>
                </div>

                {/* User Dropdown */}
                <div className="relative">
                  <button
                    onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                    className="h-11 flex items-center gap-2 px-2.5 rounded-2xl border border-rose-200/80 dark:border-rose-900/60 bg-white/80 dark:bg-card/80 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors shadow-2xs cursor-pointer"
                  >
                    <div className="h-7.5 w-7.5 rounded-xl bg-gradient-to-tr from-rose-500 via-pink-500 to-amber-500 flex items-center justify-center text-white font-extrabold text-xs uppercase shadow-xs">
                      {user.full_name ? user.full_name[0] : user.email[0]}
                    </div>
                    <ChevronDown className="h-3.5 w-3.5 text-muted-foreground mr-0.5" />
                  </button>

                  {isUserMenuOpen && (
                    <div
                      className="absolute right-0 mt-2 w-64 rounded-2xl border border-rose-200/90 dark:border-rose-900/60 bg-card p-2 shadow-2xl z-50 animate-fade-in"
                      onMouseLeave={() => setIsUserMenuOpen(false)}
                    >
                      <div className="px-3 py-2.5 border-b border-border/60 mb-1.5 flex items-start justify-between">
                        <div className="truncate mr-2">
                          <p className="text-sm font-bold text-foreground truncate">{user.full_name || "Candidate"}</p>
                          <p className="text-xs text-muted-foreground truncate">{user.email}</p>
                        </div>
                        <span className="text-[10px] font-mono font-bold uppercase px-1.5 py-0.5 rounded-md bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-900 shrink-0">
                          {user.roles?.[0]?.name || "USER"}
                        </span>
                      </div>

                      {/* Admin Links if user is an Administrator */}
                      {user.roles?.some(r => r.name === "ADMIN" || r.name === "SUPER_ADMIN") && (
                        <div className="pb-1.5 mb-1.5 border-b border-border/60">
                          <p className="px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-purple-600 dark:text-purple-400">
                            Administrator Controls
                          </p>
                          <Link
                            href="/admin/users"
                            onClick={() => setIsUserMenuOpen(false)}
                            className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-bold text-purple-700 dark:text-purple-300 bg-purple-500/10 hover:bg-purple-500/20 transition-colors"
                          >
                            <Users className="h-4 w-4 text-purple-500" />
                            User Management &amp; Export
                          </Link>
                          <Link
                            href="/admin/questions"
                            onClick={() => setIsUserMenuOpen(false)}
                            className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-foreground hover:bg-rose-50 dark:hover:bg-rose-950/30 hover:text-rose-600 transition-colors mt-0.5"
                          >
                            <ShieldCheck className="h-4 w-4 text-rose-500" />
                            Questions &amp; Quotas
                          </Link>
                        </div>
                      )}

                      <Link
                        href="/dashboard"
                        onClick={() => setIsUserMenuOpen(false)}
                        className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-foreground hover:bg-rose-50 dark:hover:bg-rose-950/30 hover:text-rose-600 transition-colors"
                      >
                        <LayoutDashboard className="h-4 w-4 text-primary" />
                        Dashboard Overview
                      </Link>

                      <Link
                        href="/dashboard/revision"
                        onClick={() => setIsUserMenuOpen(false)}
                        className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-foreground hover:bg-sky-50 dark:hover:bg-sky-950/30 hover:text-sky-600 transition-colors"
                      >
                        <RotateCcw className="h-4 w-4 text-sky-500" />
                        Spaced Repetition (SRS)
                      </Link>

                      <Link
                        href="/dashboard/bookmarks"
                        onClick={() => setIsUserMenuOpen(false)}
                        className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-foreground hover:bg-amber-50 dark:hover:bg-amber-950/30 hover:text-amber-600 transition-colors"
                      >
                        <Bookmark className="h-4 w-4 text-amber-500" />
                        Saved Bookmarks
                      </Link>

                      <Link
                        href="/dashboard/history"
                        onClick={() => setIsUserMenuOpen(false)}
                        className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-foreground hover:bg-purple-50 dark:hover:bg-purple-950/30 hover:text-purple-600 transition-colors"
                      >
                        <History className="h-4 w-4 text-purple-500" />
                        Attempt History
                      </Link>

                      <div className="border-t border-border/60 my-1.5" />

                      <button
                        onClick={() => {
                          logout();
                          setIsUserMenuOpen(false);
                          router.push("/");
                        }}
                        className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-bold text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors cursor-pointer"
                      >
                        <LogOut className="h-4 w-4" />
                        Sign Out
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-2 sm:gap-2.5">
                <Link href="/login">
                  <Button
                    size="sm"
                    variant="outline"
                    className="text-xs sm:text-sm font-bold border-rose-300/80 dark:border-rose-800 text-rose-700 dark:text-rose-300 hover:bg-rose-100/60 dark:hover:bg-rose-950/60 rounded-2xl h-11 px-4 shadow-2xs transition-all"
                  >
                    <LogIn className="h-4 w-4 mr-1.5 text-rose-500" />
                    Log in
                  </Button>
                </Link>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={handleDemoCandidateLogin}
                  className="hidden md:inline-flex text-xs sm:text-sm font-bold border-amber-300/80 dark:border-amber-800 text-amber-800 dark:text-amber-200 bg-amber-500/10 hover:bg-amber-500/20 rounded-2xl h-11 px-4 shadow-2xs transition-all"
                >
                  <Sparkles className="h-4 w-4 mr-1.5 text-amber-500" />
                  Demo
                </Button>
                <Link href="/questions" className="hidden lg:inline-flex">
                  <Button
                    size="sm"
                    className="rounded-2xl font-extrabold h-11 px-5 bg-gradient-to-r from-rose-600 via-pink-600 to-amber-600 hover:from-rose-500 hover:via-pink-500 hover:to-amber-500 text-white shadow-md shadow-rose-500/30 hover:shadow-lg hover:shadow-rose-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all"
                  >
                    Explore Bank
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Command Palette Modal */}
      <CommandPalette 
        isOpen={isCommandPaletteOpen} 
        onClose={() => setIsCommandPaletteOpen(false)} 
      />
    </>
  );
};
