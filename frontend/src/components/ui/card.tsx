import React from "react";
import { cn } from "@/lib/utils";

export type CardVariant = 
  | "default" 
  | "elevated"
  | "interactive"
  | "genai"
  | "system"
  | "backend"
  | "dsa"
  | "production"
  // Legacy aliases mapped gracefully
  | "rose" 
  | "purple" 
  | "amber" 
  | "emerald" 
  | "sky" 
  | "orange" 
  | "fuchsia" 
  | "teal";

const cardVariantStyles: Record<CardVariant, string> = {
  default: "border-border/75 bg-card text-card-foreground shadow-sm hover:border-border transition-colors",
  elevated: "border-border/80 bg-surface-elevated text-card-foreground shadow-md hover:border-border",
  interactive: "border-border/75 bg-card text-card-foreground shadow-sm hover:border-primary/45 hover:shadow-md hover:shadow-primary/5 transition-all duration-200 cursor-pointer",
  genai: "border-purple-500/25 bg-card hover:border-purple-500/50 text-card-foreground shadow-sm transition-colors",
  system: "border-blue-500/25 bg-card hover:border-blue-500/50 text-card-foreground shadow-sm transition-colors",
  backend: "border-cyan-500/25 bg-card hover:border-cyan-500/50 text-card-foreground shadow-sm transition-colors",
  dsa: "border-emerald-500/25 bg-card hover:border-emerald-500/50 text-card-foreground shadow-sm transition-colors",
  production: "border-amber-500/25 bg-card hover:border-amber-500/50 text-card-foreground shadow-sm transition-colors",
  // Legacy mappings - elegant subtle borders
  rose: "border-rose-500/25 bg-card hover:border-rose-500/50 text-card-foreground shadow-sm transition-colors",
  purple: "border-purple-500/25 bg-card hover:border-purple-500/50 text-card-foreground shadow-sm transition-colors",
  amber: "border-amber-500/25 bg-card hover:border-amber-500/50 text-card-foreground shadow-sm transition-colors",
  emerald: "border-emerald-500/25 bg-card hover:border-emerald-500/50 text-card-foreground shadow-sm transition-colors",
  sky: "border-sky-500/25 bg-card hover:border-sky-500/50 text-card-foreground shadow-sm transition-colors",
  orange: "border-orange-500/25 bg-card hover:border-orange-500/50 text-card-foreground shadow-sm transition-colors",
  fuchsia: "border-fuchsia-500/25 bg-card hover:border-fuchsia-500/50 text-card-foreground shadow-sm transition-colors",
  teal: "border-teal-500/25 bg-card hover:border-teal-500/50 text-card-foreground shadow-sm transition-colors",
};

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: CardVariant;
  colorIndex?: number;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = "default", colorIndex, ...props }, ref) => {
    // If colorIndex is provided, map to clean semantic variant instead of harsh rainbow
    const selectedVariant = colorIndex !== undefined ? "default" : variant;

    return (
      <div
        ref={ref}
        className={cn(
          "rounded-2xl border transition-all duration-200",
          cardVariantStyles[selectedVariant] || cardVariantStyles.default,
          className
        )}
        {...props}
      />
    );
  }
);
Card.displayName = "Card";

export const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-5 sm:p-6", className)} {...props} />
  )
);
CardHeader.displayName = "CardHeader";

export const CardTitle = React.forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn("text-lg sm:text-xl font-bold tracking-tight text-foreground", className)} {...props} />
  )
);
CardTitle.displayName = "CardTitle";

export const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn("text-xs sm:text-sm text-muted-foreground leading-relaxed", className)} {...props} />
  )
);
CardDescription.displayName = "CardDescription";

export const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("p-5 sm:p-6 pt-0", className)} {...props} />
);
CardContent.displayName = "CardContent";

export const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center p-5 sm:p-6 pt-0", className)} {...props} />
  )
);
CardFooter.displayName = "CardFooter";
