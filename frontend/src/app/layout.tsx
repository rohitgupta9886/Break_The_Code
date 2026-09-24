import type { Metadata } from "next";
import "@/styles/globals.css";
import { Navbar } from "@/components/layout/navbar";
import { MobileNav } from "@/components/layout/mobile-nav";
import { Footer } from "@/components/layout/footer";
import { AuthProvider } from "@/lib/auth-context";

export const metadata: Metadata = {
  metadataBase: new URL("https://breakthecode.dev"),
  title: {
    default: "Break The Code | AI-Powered Technical Interview Preparation Platform",
    template: "%s | Break The Code",
  },
  description:
    "Break The Code. Crack The Interview. Master AI, GenAI, Java, Backend, DSA and System Design with 1,200+ production-calibrated interview questions, 60-second verbal model answers, Think Mode stopwatch, and LangGraph evaluation.",
  keywords: [
    "technical interview preparation",
    "software engineer interview questions",
    "LangGraph interview questions",
    "RAG vector db interview questions",
    "Java backend interview questions",
    "System Design interview questions",
    "DSA interview questions",
    "staff engineer interview",
    "production outage scenarios",
    "break the code"
  ],
  authors: [{ name: "Break The Code Team" }],
  creator: "Break The Code",
  alternates: {
    canonical: "https://breakthecode.dev",
  },
  openGraph: {
    title: "Break The Code | Crack The Technical Interview",
    description:
      "Master AI, GenAI, Java, Backend, DSA and System Design with active Think Mode and LangGraph evaluation.",
    url: "https://breakthecode.dev",
    siteName: "Break The Code",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Break The Code | Crack The Technical Interview",
    description: "Production-grade technical interview preparation platform across 8 calibrated difficulty tiers.",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

const websiteSchema = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "Break The Code",
  url: "https://breakthecode.dev",
  potentialAction: {
    "@type": "SearchAction",
    target: {
      "@type": "EntryPoint",
      urlTemplate: "https://breakthecode.dev/questions?search={search_term_string}",
    },
    "query-input": "required name=search_term_string",
  },
};

const organizationSchema = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Break The Code",
  url: "https://breakthecode.dev",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="overflow-x-hidden max-w-full" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify([websiteSchema, organizationSchema]),
          }}
        />
      </head>
      <body
        className="min-h-screen flex flex-col bg-background text-foreground antialiased font-sans overflow-x-hidden max-w-full touch-pan-y"
        suppressHydrationWarning
      >
        <AuthProvider>
          <Navbar />
          <main className="flex-1 w-full">{children}</main>
          <Footer />
          <MobileNav />
        </AuthProvider>
      </body>
    </html>
  );
}
