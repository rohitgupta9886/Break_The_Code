import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        surface: {
          DEFAULT: "hsl(var(--card))",
          elevated: "hsl(var(--surface-elevated))",
          hover: "hsl(var(--surface-hover))",
        },
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
          hover: "hsl(var(--primary-hover))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        success: {
          DEFAULT: "hsl(var(--success))",
          foreground: "hsl(var(--success-foreground))",
        },
        warning: {
          DEFAULT: "hsl(var(--warning))",
          foreground: "hsl(var(--warning-foreground))",
        },
        // Purposeful Semantic Domain Colors (No Random Clutter)
        domain: {
          genai: {
            DEFAULT: "#8b5cf6",
            light: "#a78bfa",
            dark: "#6d28d9",
            surface: "rgba(139, 92, 246, 0.08)",
            border: "rgba(139, 92, 246, 0.22)",
          },
          system: {
            DEFAULT: "#3b82f6",
            light: "#60a5fa",
            dark: "#1d4ed8",
            surface: "rgba(59, 130, 246, 0.08)",
            border: "rgba(59, 130, 246, 0.22)",
          },
          backend: {
            DEFAULT: "#06b6d4",
            light: "#22d3ee",
            dark: "#0e7490",
            surface: "rgba(6, 182, 212, 0.08)",
            border: "rgba(6, 182, 212, 0.22)",
          },
          dsa: {
            DEFAULT: "#10b981",
            light: "#34d399",
            dark: "#047857",
            surface: "rgba(16, 185, 129, 0.08)",
            border: "rgba(16, 185, 129, 0.22)",
          },
          production: {
            DEFAULT: "#f59e0b",
            light: "#fbbf24",
            dark: "#b45309",
            surface: "rgba(245, 158, 11, 0.08)",
            border: "rgba(245, 158, 11, 0.22)",
          },
          java: {
            DEFAULT: "#f97316",
            light: "#fb923c",
            dark: "#c2410c",
            surface: "rgba(249, 115, 22, 0.08)",
            border: "rgba(249, 115, 22, 0.22)",
          },
          python: {
            DEFAULT: "#2563eb",
            light: "#3b82f6",
            dark: "#1e40af",
            surface: "rgba(37, 99, 235, 0.08)",
            border: "rgba(37, 99, 235, 0.22)",
          },
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
        xl: "calc(var(--radius) + 4px)",
        "2xl": "calc(var(--radius) + 8px)",
      },
      fontFamily: {
        sans: ["var(--font-jakarta)", "var(--font-inter)", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "monospace"],
      },
      boxShadow: {
        "subtle": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "elevation-1": "0 1px 3px 0 rgba(0, 0, 0, 0.25), 0 1px 2px -1px rgba(0, 0, 0, 0.2)",
        "elevation-2": "0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.25)",
        "elevation-3": "0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -4px rgba(0, 0, 0, 0.3)",
        "glow-primary": "0 0 24px -4px rgba(99, 102, 241, 0.25)",
        "glow-accent": "0 0 24px -4px rgba(139, 92, 246, 0.25)",
      },
      animation: {
        "fade-in": "fadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
        "slide-up": "slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1)",
        "pulse-subtle": "pulseSubtle 2.5s infinite ease-in-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(4px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        pulseSubtle: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.6" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
