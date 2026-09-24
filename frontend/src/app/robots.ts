import { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: [
        "/",
        "/questions",
        "/questions/*",
        "/questions-and-answers",
        "/questions-and-answers/*",
        "/learn",
        "/learn/*",
        "/difficulty",
      ],
      disallow: ["/admin", "/admin/*", "/api/*", "/dashboard", "/interview/session/*"],
    },
    sitemap: "https://breakthecode.dev/sitemap.xml",
  };
}
