import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { fetchQuestionBySlug } from "@/lib/api";
import { QuestionDetailClient } from "./question-detail-client";

export const revalidate = 300;

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const question = await fetchQuestionBySlug(slug);

  if (!question) {
    return {
      title: "Interview Question | Break The Code",
      description: "Technical interview question and production answer.",
    };
  }

  const rawAnswer = question.interview_ready_answer || question.short_answer || question.deep_explanation || "";
  const cleanAnswer = rawAnswer.replace(/\s+/g, " ").trim();
  const summary = cleanAnswer.length > 155 ? `${cleanAnswer.slice(0, 152)}...` : cleanAnswer;

  const title = `${question.title} | ${question.technology_name} Interview Question`;
  const description = `${summary} Master this ${question.difficulty} question with model answers, Think Mode, and real company interview insights.`;

  return {
    title,
    description,
    keywords: [
      `${question.technology_name} interview question`,
      question.title,
      `${question.difficulty} technical question`,
      question.topic_name,
      ...(question.tags?.map((t) => t.name) || []),
      "break the code",
    ],
    alternates: {
      canonical: `https://breakthecode.dev/questions/${question.slug}`,
    },
    openGraph: {
      title,
      description,
      url: `https://breakthecode.dev/questions/${question.slug}`,
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

export default async function QuestionDetailPage({ params }: PageProps) {
  const { slug } = await params;
  const question = await fetchQuestionBySlug(slug);

  if (!question) {
    notFound();
  }

  const answerText =
    question.interview_ready_answer ||
    question.short_answer ||
    question.deep_explanation ||
    "Model answer available inside Break The Code platform.";

  const qaSchema = {
    "@context": "https://schema.org",
    "@type": "QAPage",
    mainEntity: {
      "@type": "Question",
      name: question.title,
      text: question.title,
      answerCount: 1,
      upvoteCount: question.upvote_count || 42,
      acceptedAnswer: {
        "@type": "Answer",
        text: answerText,
        upvoteCount: question.upvote_count || 42,
        url: `https://breakthecode.dev/questions/${question.slug}#answer`,
        author: {
          "@type": "Organization",
          name: "Break The Code Staff Editorial",
        },
      },
    },
  };

  const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      {
        "@type": "ListItem",
        position: 1,
        name: "Home",
        item: "https://breakthecode.dev",
      },
      {
        "@type": "ListItem",
        position: 2,
        name: "Questions",
        item: "https://breakthecode.dev/questions",
      },
      {
        "@type": "ListItem",
        position: 3,
        name: question.technology_name,
        item: `https://breakthecode.dev/questions?technology=${question.technology_slug}`,
      },
      {
        "@type": "ListItem",
        position: 4,
        name: question.title,
        item: `https://breakthecode.dev/questions/${question.slug}`,
      },
    ],
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([qaSchema, breadcrumbSchema]),
        }}
      />
      <QuestionDetailClient question={question} />
    </>
  );
}
