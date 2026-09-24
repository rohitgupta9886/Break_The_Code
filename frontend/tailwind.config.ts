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
        // Multicolor Technology Tokens
        tech: {
          ai: {
            DEFAULT: "#7c3aed", // Electric Violet
            light: "#a78bfa",
            dark: "#5b21b6",
            surface: "rgba(124, 58, 237, 0.08)",
            border: "rgba(124, 58, 237, 0.25)",
          },
          java: {
            DEFAULT: "#ea580c", // Deep Orange / Red-Orange
            light: "#fb923c",
            dark: "#9a3412",
            surface: "rgba(234, 88, 12, 0.08)",
            border: "rgba(234, 88, 12, 0.25)",
          },
          python: {
            DEFAULT: "#2563eb", // Blue
            light: "#60a5fa",
            dark: "#1d4ed8",
            surface: "rgba(37, 99, 235, 0.08)",
            border: "rgba(37, 99, 235, 0.25)",
          },
          spring: {
            DEFAULT: "#10b981", // Emerald
            light: "#34d399",
            dark: "#047857",
            surface: "rgba(16, 185, 129, 0.08)",
            border: "rgba(16, 185, 129, 0.25)",
          },
          kafka: {
            DEFAULT: "#f59e0b", // Amber / Orange
            light: "#fbbf24",
            dark: "#b45309",
            surface: "rgba(245, 158, 11, 0.08)",
            border: "rgba(245, 158, 11, 0.25)",
          },
          redis: {
            DEFAULT: "#ef4444", // Coral Red
            light: "#f87171",
            dark: "#b91c1c",
            surface: "rgba(239, 68, 68, 0.08)",
            border: "rgba(239, 68, 68, 0.25)",
          },
          dsa: {
            DEFAULT: "#a855f7", // Purple / Pink
            light: "#c084fc",
            dark: "#7e22ce",
            surface: "rgba(168, 85, 247, 0.08)",
            border: "rgba(168, 85, 247, 0.25)",
          },
          system: {
            DEFAULT: "#06b6d4", // Teal / Cyan
            light: "#22d3ee",
            dark: "#0e7490",
            surface: "rgba(6, 182, 212, 0.08)",
            border: "rgba(6, 182, 212, 0.25)",
          },
          cloud: {
            DEFAULT: "#3b82f6", // Slate Blue
            light: "#93c5fd",
            dark: "#1e40af",
            surface: "rgba(59, 130, 246, 0.08)",
            border: "rgba(59, 130, 246, 0.25)",
          },
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "monospace"],
      },
      animation: {
        "fade-in": "fadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1)",
        "pulse-subtle": "pulseSubtle 2s infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(6px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        pulseSubtle: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.7" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
