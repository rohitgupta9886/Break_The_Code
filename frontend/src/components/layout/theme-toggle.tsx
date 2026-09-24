"use client";

import React, { useEffect, useState } from "react";
import { Sun, Moon } from "lucide-react";

interface ThemeToggleProps {
  className?: string;
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({ className = "" }) => {
  const [isDark, setIsDark] = useState<boolean>(true);
  const [mounted, setMounted] = useState<boolean>(false);

  useEffect(() => {
    setMounted(true);
    const savedTheme = localStorage.getItem("btc-theme");
    // Default to dark mode for developer platform experience
    const prefersDark = savedTheme ? savedTheme === "dark" : true;
    setIsDark(prefersDark);
    if (prefersDark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, []);

  const toggleTheme = () => {
    if (isDark) {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("btc-theme", "light");
      setIsDark(false);
    } else {
      document.documentElement.classList.add("dark");
      localStorage.setItem("btc-theme", "dark");
      setIsDark(true);
    }
  };

  if (!mounted) {
    return (
      <div className={`h-9 w-9 rounded-xl border border-border/70 bg-card/80 shrink-0 ${className}`} />
    );
  }

  return (
    <button
      onClick={toggleTheme}
      className={`h-9 w-9 rounded-xl flex items-center justify-center border border-border/70 bg-card/80 hover:bg-surface-hover hover:border-primary/40 text-muted-foreground hover:text-foreground transition-all duration-200 active:scale-95 shadow-sm cursor-pointer shrink-0 ${className}`}
      aria-label="Toggle theme"
      title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
    >
      {isDark ? (
        <Sun className="h-4 w-4 text-amber-400 transition-transform duration-200 hover:rotate-45" />
      ) : (
        <Moon className="h-4 w-4 text-indigo-500 transition-transform duration-200 hover:-rotate-12" />
      )}
    </button>
  );
};
