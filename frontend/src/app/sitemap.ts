import { MetadataRoute } from "next";
import { fetchTechnologies, fetchQuestions } from "@/lib/api";

export const revalidate = 3600;

const KNOWN_TRACKS = [
  "langgraph",
  "rag-vector-db",
  "java-backend",
  "dsa",
  "system-design"
];

const DIFFICULTY_TIERS = [
  "BASIC",
  "MEDIUM",
  "HARD",
  "TOUGH",
  "VERY_TOUGH",
  "VERY_VERY_TOUGH",
  "PRODUCTION_SCENARIO",
  "EXPERT_DEEP_DIVE"
];

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = "https://breakthecode.dev";
  const now = new Date();

  // 1. Core High-Priority Landing & Hub Pages
  const routes: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: now,
      changeFrequency: "daily",
      priority: 1.0,
    },
    {
      url: `${baseUrl}/learn`,
      lastModified: now,
      changeFrequency: "daily",
      priority: 0.95,
    },
    {
      url: `${baseUrl}/questions`,
      lastModified: now,
      changeFrequency: "daily",
      priority: 0.95,
    },
    {
      url: `${baseUrl}/difficulty`,
      lastModified: now,
      changeFrequency: "weekly",
      priority: 0.90,
    },
  ];

  // 2. Fetch technologies dynamically (with fallback)
  let techSlugs = KNOWN_TRACKS;
  try {
    const techs = await fetchTechnologies();
    if (techs && techs.length > 0) {
      techSlugs = techs.map((t) => t.slug);
    }
  } catch {
    // Use fallback
  }

  // 3. Add Dedicated Q&A Reading Mode Routes (Top Google Rank Target)
  for (const slug of techSlugs) {
    routes.push({
      url: `${baseUrl}/questions-and-answers/${slug}`,
      lastModified: now,
      changeFrequency: "daily",
      priority: 0.95,
    });
    routes.push({
      url: `${baseUrl}/questions?technology=${slug}`,
      lastModified: now,
      changeFrequency: "daily",
      priority: 0.85,
    });
  }

  // 4. Add Calibrated Difficulty Tier Filter Pages
  for (const tier of DIFFICULTY_TIERS) {
    routes.push({
      url: `${baseUrl}/questions?difficulty=${tier}`,
      lastModified: now,
      changeFrequency: "weekly",
      priority: 0.80,
    });
  }

  // 5. Add Individual Questions (Deep Links)
  try {
    const questionsRes = await fetchQuestions({ limit: 100 });
    if (questionsRes && questionsRes.items) {
      for (const q of questionsRes.items) {
        routes.push({
          url: `${baseUrl}/questions/${q.slug}`,
          lastModified: now,
          changeFrequency: "weekly",
          priority: 0.75,
        });
      }
    }
  } catch {
    // If backend is not reached during static generation, graceful skip
  }

  return routes;
}
