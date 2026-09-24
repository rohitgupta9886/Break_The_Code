import React from "react";
import { cn } from "@/lib/utils";

export type CardVariant = 
  | "default" 
  | "rose" 
  | "purple" 
  | "amber" 
  | "emerald" 
  | "sky" 
  | "orange" 
  | "fuchsia" 
  | "teal";

const cardVariantStyles: Record<CardVariant, string> = {
  default: "border-border/80 bg-card text-card-foreground shadow-sm",
  rose: "border-rose-200/90 dark:border-rose-900/60 bg-[#fff2f4] dark:bg-rose-950/30 text-card-foreground shadow-sm shadow-rose-100/50 hover:border-rose-400",
  purple: "border-purple-200/90 dark:border-purple-900/60 bg-[#f5f3ff] dark:bg-purple-950/30 text-card-foreground shadow-sm shadow-purple-100/50 hover:border-purple-400",
  amber: "border-amber-200/90 dark:border-amber-900/60 bg-[#fffbeb] dark:bg-amber-950/30 text-card-foreground shadow-sm shadow-amber-100/50 hover:border-amber-400",
  emerald: "border-emerald-200/90 dark:border-emerald-900/60 bg-[#ecfdf5] dark:bg-emerald-950/30 text-card-foreground shadow-sm shadow-emerald-100/50 hover:border-emerald-400",
  sky: "border-sky-200/90 dark:border-sky-900/60 bg-[#f0f9ff] dark:bg-sky-950/30 text-card-foreground shadow-sm shadow-sky-100/50 hover:border-sky-400",
  orange: "border-orange-200/90 dark:border-orange-900/60 bg-[#fff7ed] dark:bg-orange-950/30 text-card-foreground shadow-sm shadow-orange-100/50 hover:border-orange-400",
  fuchsia: "border-fuchsia-200/90 dark:border-fuchsia-900/60 bg-[#fdf4ff] dark:bg-fuchsia-950/30 text-card-foreground shadow-sm shadow-fuchsia-100/50 hover:border-fuchsia-400",
  teal: "border-teal-200/90 dark:border-teal-900/60 bg-[#f0fdfa] dark:bg-teal-950/30 text-card-foreground shadow-sm shadow-teal-100/50 hover:border-teal-400",
};

const cardVariantCycle: CardVariant[] = [
  "rose",
  "purple",
  "amber",
  "emerald",
  "sky",
  "orange",
  "fuchsia",
  "teal",
];

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: CardVariant;
  colorIndex?: number;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = "default", colorIndex, ...props }, ref) => {
    const selectedVariant = colorIndex !== undefined 
      ? cardVariantCycle[Math.abs(colorIndex) % cardVariantCycle.length]
      : variant;

    return (
      <div
        ref={ref}
        className={cn(
          "rounded-2xl border transition-all duration-200",
          cardVariantStyles[selectedVariant],
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
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
);
CardHeader.displayName = "CardHeader";

export const CardTitle = React.forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn("text-xl font-semibold tracking-tight text-foreground", className)} {...props} />
  )
);
CardTitle.displayName = "CardTitle";

export const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
  )
);
CardDescription.displayName = "CardDescription";

export const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
);
CardContent.displayName = "CardContent";

export const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center p-6 pt-0", className)} {...props} />
  )
);
CardFooter.displayName = "CardFooter";
