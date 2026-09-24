"use client";

import React, { useEffect, useState } from "react";
import { Sun, Moon } from "lucide-react";

interface ThemeToggleProps {
  className?: string;
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({ className = "" }) => {
  const [isDark, setIsDark] = useState<boolean>(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem("btc-theme");
    if (savedTheme === "dark") {
      setIsDark(true);
      document.documentElement.classList.add("dark");
    } else {
      setIsDark(false);
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

  return (
    <button
      onClick={toggleTheme}
      className={`h-11 w-11 rounded-2xl flex items-center justify-center border border-rose-200/80 dark:border-rose-900/60 bg-white/80 dark:bg-card/80 hover:bg-rose-50 dark:hover:bg-rose-950/40 text-muted-foreground hover:text-foreground transition-all duration-200 active:scale-95 shadow-2xs cursor-pointer shrink-0 ${className}`}
      aria-label="Toggle theme"
      title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
    >
      {isDark ? <Sun className="h-4 w-4 text-amber-400" /> : <Moon className="h-4 w-4 text-rose-500 dark:text-rose-400" />}
    </button>
  );
};
