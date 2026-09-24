"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Sparkles, LayoutDashboard, Target, Layers } from "lucide-react";
import { cn } from "@/lib/utils";

export const MobileNav: React.FC = () => {
  const pathname = usePathname();

  const navItems = [
    { label: "Home", href: "/", icon: Home },
    { label: "Questions", href: "/questions", icon: Target },
    { label: "Tracks", href: "/learn", icon: Layers },
    { label: "Difficulty", href: "/difficulty", icon: Sparkles },
    { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  ];

  return (
    <nav className="sm:hidden fixed bottom-0 left-0 right-0 z-50 h-16 bg-white/95 dark:bg-[#140a10]/95 backdrop-blur-xl border-t border-rose-200/80 dark:border-rose-900/60 flex items-center justify-around px-2 shadow-lg shadow-rose-100/30">
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
        return (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "flex flex-col items-center justify-center gap-1 py-1 px-3 rounded-xl text-[11px] font-semibold transition-all",
              isActive 
                ? "text-rose-600 dark:text-rose-400 font-bold bg-rose-100/80 dark:bg-rose-950/50" 
                : "text-muted-foreground hover:text-foreground"
            )}
          >
            <Icon className={cn("h-4 w-4", isActive && "stroke-[2.5px] scale-110")} />
            <span>{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
};
