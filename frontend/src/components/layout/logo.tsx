import React from "react";
import Link from "next/link";

interface LogoProps {
  size?: "sm" | "md" | "lg";
  showSubtitle?: boolean;
  className?: string;
  variant?: "badge" | "full";
}

export const Logo: React.FC<LogoProps> = ({
  size = "md",
  showSubtitle = true,
  className = "",
  variant = "badge",
}) => {
  const iconSizes = {
    sm: "h-11 w-11 rounded-2xl",
    md: "h-14 w-14 rounded-2xl",
    lg: "h-18 w-18 sm:h-20 sm:w-20 rounded-3xl",
  };

  const imageDimensions = {
    sm: 44,
    md: 56,
    lg: 80,
  };

  const textSizes = {
    sm: "text-xl",
    md: "text-2xl sm:text-3xl",
    lg: "text-3xl sm:text-4xl",
  };

  if (variant === "full") {
    return (
      <Link href="/" suppressHydrationWarning className={`inline-flex items-center group ${className}`}>
        <img
          src="/images/logo-horizontal.png"
          alt="Break The Code Logo"
          width={360}
          height={160}
          className="h-16 sm:h-20 w-auto object-contain transition-transform duration-300 group-hover:scale-105"
        />
      </Link>
    );
  }

  return (
    <Link href="/" suppressHydrationWarning className={`flex items-center gap-4 sm:gap-5 group ${className}`}>
      {/* Visual Emblem / Brandmark from new Shield */}
      <div
        suppressHydrationWarning
        className={`relative ${iconSizes[size]} p-[2px] rounded-[inherit] bg-gradient-to-tr from-rose-500 via-amber-400 to-rose-600 shadow-lg shadow-rose-500/25 group-hover:shadow-rose-500/50 group-hover:scale-105 transition-all duration-300 shrink-0 overflow-hidden`}
      >
        <img
          src="/images/logo-shield.png"
          alt="Break The Code Emblem"
          width={imageDimensions[size]}
          height={imageDimensions[size]}
          className="h-full w-full object-cover rounded-[inherit]"
          loading="eager"
        />
      </div>

      {/* Brand Text & Badge */}
      <div className="flex flex-col justify-center select-none py-1">
        <div className="flex items-center gap-3">
          <div className="flex items-baseline font-black leading-none tracking-normal">
            <span
              className="text-foreground tracking-[0.02em] font-extrabold text-2xl sm:text-3xl lg:text-[34px] transition-colors group-hover:text-amber-500/90"
              style={{ fontFamily: "'Outfit', 'Inter', sans-serif" }}
            >
              Break
            </span>
            <span
              className="mx-2 text-xl sm:text-2xl lg:text-[28px] font-semibold text-rose-500/90 italic"
              style={{ fontFamily: "'Playfair Display', Georgia, serif" }}
            >
              The
            </span>
            <span
              className="text-2xl sm:text-3xl lg:text-[34px] font-black bg-gradient-to-r from-rose-500 via-pink-500 to-amber-400 bg-clip-text text-transparent drop-shadow-[0_2px_16px_rgba(244,63,94,0.35)] tracking-[0.02em]"
              style={{ fontFamily: "'Outfit', 'Inter', sans-serif" }}
            >
              Code
            </span>
          </div>

          {/* AI LAB Glowing Neon Pill Capsule */}
          <span className="inline-flex items-center gap-1.5 text-[10.5px] px-3 py-1 font-black uppercase tracking-[0.14em] rounded-full bg-gradient-to-r from-rose-500/15 via-pink-500/10 to-amber-500/15 text-rose-600 dark:text-rose-300 border border-rose-500/35 dark:border-rose-400/40 shadow-sm shadow-rose-500/25 backdrop-blur-xs ml-1">
            <span className="h-2 w-2 rounded-full bg-rose-500 animate-pulse shadow-sm shadow-rose-500 shrink-0" />
            <span>AI LAB</span>
          </span>
        </div>

        {showSubtitle && (
          <span
            className="hidden sm:inline text-xs sm:text-[13px] text-muted-foreground/80 font-medium italic tracking-[0.06em] mt-1.5 whitespace-nowrap"
            style={{ fontFamily: "'Playfair Display', Georgia, serif" }}
          >
            Break The Code. Crack The Interview.
          </span>
        )}
      </div>
    </Link>
  );
};
