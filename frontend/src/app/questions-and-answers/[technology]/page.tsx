import type { Metadata } from "next";
import { ReadingModeClient } from "./reading-mode-client";

interface PageProps {
  params: Promise<{ technology: string }>;
}

const TECH_METADATA: Record<string, { name: string; desc: string }> = {
  "langgraph": {
    name: "LangGraph & Agentic AI",
    desc: "Master LangGraph, cyclical computational graphs, checkpointing, and multi-agent workflows.",
  },
  "rag-vector-db": {
    name: "RAG & Vector Databases",
    desc: "Master hybrid search, embeddings, reranking, and semantic retrieval architectures.",
  },
  "java-backend": {
    name: "Java & JVM Concurrency",
    desc: "Master Java concurrency, Virtual Threads, memory model, GC algorithms, and Spring Boot.",
  },
  "dsa": {
    name: "DSA & Algorithms",
    desc: "Master dynamic programming, graph algorithms, monotonic structures, and algorithmic trade-offs.",
  },
  "system-design": {
    name: "System Design",
    desc: "Master distributed caching, message queues, rate limiting, and high-availability architecture.",
  },
};

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { technology: techSlug } = await params;
  const meta = TECH_METADATA[techSlug] || {
    name: techSlug.toUpperCase(),
    desc: "Comprehensive software engineering interview questions and answers.",
  };

  const title = `${meta.name} Interview Questions & Answers (2026 Guide) | Break The Code`;
  const description = `${meta.desc} 60-second verbal elevator pitches, production code, and trade-offs.`;

  return {
    title,
    description,
    keywords: [
      `${meta.name} interview questions`,
      `${meta.name} interview answers`,
      "technical interview questions and answers",
      "break the code",
    ],
    alternates: {
      canonical: `https://breakthecode.dev/questions-and-answers/${techSlug}`,
    },
    openGraph: {
      title,
      description,
      url: `https://breakthecode.dev/questions-and-answers/${techSlug}`,
      siteName: "Break The Code",
      type: "article",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
    },
  };
}

import { fetchReadingMode } from "@/lib/api";

export const revalidate = 180; // ISR cache for 3 minutes

export default async function QuestionsAndAnswersPage({ params }: PageProps) {
  const { technology: techSlug } = await params;
  const initialData = await fetchReadingMode(techSlug);
  return <ReadingModeClient techSlug={techSlug} initialData={initialData} />;
}
