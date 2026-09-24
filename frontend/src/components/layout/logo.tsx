import React from "react";
import Link from "next/link";

interface LogoProps {
  size?: "sm" | "md" | "lg";
  showSubtitle?: boolean;
  className?: string;
}

export const Logo: React.FC<LogoProps> = ({
  size = "md",
  showSubtitle = true,
  className = "",
}) => {
  const iconSizes = {
    sm: "h-8 w-8 rounded-xl",
    md: "h-10 w-10 rounded-2xl",
    lg: "h-12 w-12 rounded-2xl",
  };

  const svgSizes = {
    sm: "h-4 w-4",
    md: "h-5 w-5",
    lg: "h-6 w-6",
  };

  const textSizes = {
    sm: "text-lg",
    md: "text-xl",
    lg: "text-2xl",
  };

  return (
    <Link href="/" className={`flex items-center gap-3 group ${className}`}>
      {/* Visual Emblem / Brandmark */}
      <div
        className={`relative ${iconSizes[size]} bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 p-[1.5px] shadow-sm shadow-indigo-500/20 group-hover:shadow-indigo-500/40 group-hover:scale-105 transition-all duration-300 shrink-0`}
      >
        <div className="h-full w-full bg-[#0a0f1d] rounded-[inherit] flex items-center justify-center relative overflow-hidden">
          {/* Subtle glowing ambient layer */}
          <div className="absolute inset-0 bg-gradient-to-tr from-indigo-500/20 to-cyan-500/10 opacity-80" />

          {/* Code Break Glyph */}
          <svg
            viewBox="0 0 24 24"
            className={`${svgSizes[size]} text-indigo-400 fill-none stroke-current stroke-[2.4] stroke-linecap-round stroke-linejoin-round relative z-10 transition-transform duration-300 group-hover:rotate-[-4deg]`}
          >
            <polyline points="16 18 22 12 16 6" />
            <polyline points="8 6 2 12 8 18" />
            <line x1="14" y1="4" x2="10" y2="20" stroke="url(#logo-slash-gradient)" />
            <defs>
              <linearGradient id="logo-slash-gradient" x1="14" y1="4" x2="10" y2="20" gradientUnits="userSpaceOnUse">
                <stop stopColor="#818cf8" />
                <stop offset="1" stopColor="#22d3ee" />
              </linearGradient>
            </defs>
          </svg>
        </div>
      </div>

      {/* Brand Text & Badge */}
      <div className="flex flex-col">
        <div className="flex items-center gap-2">
          <span className={`font-black ${textSizes[size]} tracking-tight text-foreground flex items-center leading-none`}>
            <span>Break</span>
            <span className="bg-gradient-to-r from-indigo-500 via-indigo-400 to-cyan-400 bg-clip-text text-transparent ml-1 font-black">
              TheCode
            </span>
          </span>
          <span className="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 font-bold uppercase tracking-wider rounded-full bg-indigo-500/10 text-indigo-500 dark:text-indigo-400 border border-indigo-500/25 shadow-2xs">
            <span className="h-1.5 w-1.5 rounded-full bg-indigo-500 animate-pulse" />
            PRO
          </span>
        </div>
        {showSubtitle && (
          <span className="hidden xl:inline text-[11px] text-muted-foreground font-medium tracking-tight mt-0.5 whitespace-nowrap">
            Break The Code. Crack The Interview.
          </span>
        )}
      </div>
    </Link>
  );
};
