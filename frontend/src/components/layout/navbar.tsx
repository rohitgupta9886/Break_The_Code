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
      <header className="sticky top-0 z-40 w-full max-w-[100vw] border-b border-border/70 bg-background/85 backdrop-blur-xl transition-colors">
        {/* Top Iridescent Gradient Energy Bar */}
        <div className="h-[2px] w-full bg-gradient-to-r from-indigo-500 via-cyan-400 to-indigo-500 opacity-80" />

        <div className="w-full flex h-16 sm:h-18 items-center justify-between px-3 sm:px-6 lg:px-8 xl:px-12 gap-2 sm:gap-4 lg:gap-6">
          
          {/* 1. Left: Enhanced Logo & Brandmark */}
          <div className="flex items-center gap-3 xl:gap-6 shrink-0">
            <Logo size="md" />

            {/* Desktop Navigation Links */}
            <nav className="hidden lg:flex items-center gap-1 xl:gap-1.5">
              {navLinks.map((link) => {
                const Icon = link.icon;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs xl:text-sm font-semibold whitespace-nowrap transition-all duration-200 ${
                      link.active
                        ? "bg-primary/10 text-primary font-bold border border-primary/25 shadow-2xs"
                        : "text-muted-foreground hover:text-foreground hover:bg-surface-elevated/80"
                    }`}
                  >
                    <Icon className={`h-4 w-4 ${link.iconColor} shrink-0`} />
                    <span>{link.label}</span>
                    {link.badge && (
                      <span className="text-[10px] font-mono px-1.5 py-0.5 rounded-full bg-surface-elevated border border-border/80 text-muted-foreground font-bold shadow-2xs">
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
              className="w-full h-9 sm:h-10 px-3.5 rounded-xl bg-surface/80 hover:bg-surface-elevated border border-border/70 hover:border-border flex items-center justify-between text-xs text-muted-foreground hover:text-foreground transition-all duration-200 shadow-2xs group cursor-pointer"
            >
              <span className="flex items-center gap-2 truncate">
                <Search className="h-4 w-4 text-primary group-hover:scale-110 transition-transform shrink-0" />
                <span className="truncate font-medium">Search 750+ questions...</span>
              </span>
              <kbd className="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-mono font-bold bg-surface-elevated border border-border/80 text-foreground/80 shadow-2xs shrink-0">
                <Command className="h-3 w-3" /> K
              </kbd>
            </button>
          </div>

          {/* 3. Right: Action Controls (Practice CTA, Theme, User Profile) */}
          <div className="flex items-center gap-2 sm:gap-2.5 shrink-0">
            {/* Theme Toggle Button */}
            <ThemeToggle />

            {/* User Authentication / Profile */}
            {user ? (
              <div className="flex items-center gap-2 sm:gap-2.5">
                {/* Streak Badge */}
                <div
                  title={`${user.streak_days} Day Streak`}
                  className="flex items-center gap-1.5 h-9 sm:h-10 px-3 rounded-xl bg-amber-500/10 border border-amber-500/25 text-amber-500 dark:text-amber-400 text-xs font-bold shadow-2xs"
                >
                  <Flame className="h-4 w-4 fill-amber-500 text-amber-500 shrink-0" />
                  <span>{user.streak_days}d</span>
                </div>

                {/* XP Level Badge */}
                <div
                  title={`Level ${user.level} (${user.xp} XP)`}
                  className="hidden md:flex items-center gap-1.5 h-9 sm:h-10 px-3 rounded-xl bg-indigo-500/10 border border-indigo-500/25 text-indigo-500 dark:text-indigo-400 text-xs font-bold shadow-2xs"
                >
                  <Zap className="h-4 w-4 fill-indigo-500 text-indigo-500 shrink-0" />
                  <span>Lvl {user.level}</span>
                </div>

                {/* User Dropdown */}
                <div className="relative">
                  <button
                    onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                    className="h-9 sm:h-10 flex items-center gap-2 px-2 rounded-xl border border-border/70 bg-surface/80 hover:bg-surface-elevated transition-colors shadow-2xs cursor-pointer"
                  >
                    <div className="h-7 w-7 rounded-lg bg-gradient-to-tr from-indigo-600 to-cyan-500 flex items-center justify-center text-white font-extrabold text-xs uppercase shadow-xs">
                      {user.full_name ? user.full_name[0] : user.email[0]}
                    </div>
                    <ChevronDown className="h-3.5 w-3.5 text-muted-foreground mr-0.5" />
                  </button>

                  {isUserMenuOpen && (
                    <div
                      className="absolute right-0 mt-2 w-64 rounded-2xl border border-border/80 bg-surface p-2 shadow-2xl z-50 animate-fade-in"
                      onMouseLeave={() => setIsUserMenuOpen(false)}
                    >
                      <div className="px-3 py-2.5 border-b border-border/60 mb-1.5 flex items-start justify-between">
                        <div className="truncate mr-2">
                          <p className="text-sm font-bold text-foreground truncate">{user.full_name || "Candidate"}</p>
                          <p className="text-xs text-muted-foreground truncate">{user.email}</p>
                        </div>
                        <span className="text-[10px] font-mono font-bold uppercase px-1.5 py-0.5 rounded-md bg-primary/10 text-primary border border-primary/20 shrink-0">
                          {user.roles?.[0]?.name || "USER"}
                        </span>
                      </div>

                      {/* Admin Links if user is an Administrator */}
                      {user.roles?.some(r => r.name === "ADMIN" || r.name === "SUPER_ADMIN") && (
                        <div className="pb-1.5 mb-1.5 border-b border-border/60">
                          <p className="px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-purple-400">
                            Administrator Controls
                          </p>
                          <Link
                            href="/admin/users"
                            onClick={() => setIsUserMenuOpen(false)}
                            className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-bold text-purple-300 bg-purple-500/10 hover:bg-purple-500/20 transition-colors"
                          >
                            <Users className="h-4 w-4 text-purple-400" />
                            User Management &amp; Export
                          </Link>
                          <Link
                            href="/admin/questions"
                            onClick={() => setIsUserMenuOpen(false)}
                            className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-foreground hover:bg-surface-elevated hover:text-primary transition-colors mt-0.5"
                          >
                            <ShieldCheck className="h-4 w-4 text-primary" />
                            Questions &amp; Quotas
                          </Link>
                        </div>
                      )}

                      <Link
                        href="/dashboard"
                        onClick={() => setIsUserMenuOpen(false)}
                        className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-foreground hover:bg-surface-elevated hover:text-primary transition-colors"
                      >
                        <LayoutDashboard className="h-4 w-4 text-primary" />
                        Dashboard Overview
                      </Link>

                      <Link
                        href="/dashboard/revision"
                        onClick={() => setIsUserMenuOpen(false)}
                        className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-foreground hover:bg-surface-elevated hover:text-sky-400 transition-colors"
                      >
                        <RotateCcw className="h-4 w-4 text-sky-400" />
                        Spaced Repetition (SRS)
                      </Link>

                      <Link
                        href="/dashboard/bookmarks"
                        onClick={() => setIsUserMenuOpen(false)}
                        className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-foreground hover:bg-surface-elevated hover:text-amber-400 transition-colors"
                      >
                        <Bookmark className="h-4 w-4 text-amber-400" />
                        Saved Bookmarks
                      </Link>

                      <Link
                        href="/dashboard/history"
                        onClick={() => setIsUserMenuOpen(false)}
                        className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-foreground hover:bg-surface-elevated hover:text-purple-400 transition-colors"
                      >
                        <History className="h-4 w-4 text-purple-400" />
                        Attempt History
                      </Link>

                      <div className="border-t border-border/60 my-1.5" />

                      <button
                        onClick={() => {
                          logout();
                          setIsUserMenuOpen(false);
                          router.push("/");
                        }}
                        className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-bold text-rose-500 hover:bg-rose-500/10 transition-colors cursor-pointer"
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
                    className="text-xs sm:text-sm font-semibold rounded-xl h-9 sm:h-10 px-3.5 shadow-2xs"
                  >
                    <LogIn className="h-4 w-4 mr-1.5 text-primary" />
                    Log in
                  </Button>
                </Link>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={handleDemoCandidateLogin}
                  className="hidden md:inline-flex text-xs sm:text-sm font-semibold border-amber-500/30 text-amber-500 dark:text-amber-300 bg-amber-500/10 hover:bg-amber-500/20 rounded-xl h-9 sm:h-10 px-3.5 shadow-2xs"
                >
                  <Sparkles className="h-4 w-4 mr-1.5 text-amber-400" />
                  Demo
                </Button>
                <Link href="/questions" className="hidden lg:inline-flex">
                  <Button
                    size="sm"
                    className="rounded-xl font-bold h-9 sm:h-10 px-4 bg-primary hover:bg-primary/90 text-primary-foreground shadow-xs shadow-primary/20"
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
