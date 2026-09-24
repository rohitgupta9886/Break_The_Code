import React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "glass" | "destructive" | "success" | "tech";
  size?: "sm" | "md" | "lg" | "icon";
  isLoading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", isLoading, children, disabled, ...props }, ref) => {
    const baseStyles =
      "inline-flex items-center justify-center font-medium transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none active:scale-[0.98] select-none cursor-pointer";

    const variants = {
      primary:
        "bg-primary text-primary-foreground hover:bg-primary-hover shadow-sm hover:shadow-md hover:shadow-primary/20",
      secondary:
        "bg-secondary text-secondary-foreground hover:bg-secondary/80 border border-border/70 hover:border-border",
      outline:
        "border border-border/80 bg-card/60 hover:bg-surface-hover hover:border-primary/40 text-foreground",
      ghost:
        "hover:bg-muted/70 text-foreground hover:text-foreground",
      glass:
        "bg-card/70 border border-border/80 text-foreground hover:bg-card/90 shadow-sm",
      destructive:
        "bg-destructive/15 text-rose-400 border border-rose-500/30 hover:bg-destructive/25 shadow-sm",
      success:
        "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/25 shadow-sm",
      tech:
        "bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 hover:bg-indigo-500/25 shadow-sm",
    };

    const sizes = {
      sm: "h-8 px-3 text-xs rounded-lg gap-1.5",
      md: "h-9.5 px-4 text-sm rounded-xl gap-2",
      lg: "h-11 px-5 text-sm sm:text-base rounded-xl gap-2.5 font-semibold",
      icon: "h-9 w-9 rounded-xl p-0",
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        {...props}
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <svg
              className="animate-spin h-4 w-4 text-current"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span>{children}</span>
          </span>
        ) : (
          children
        )}
      </button>
    );
  }
);

Button.displayName = "Button";
