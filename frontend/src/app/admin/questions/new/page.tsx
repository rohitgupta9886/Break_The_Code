"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowLeft, Save, Sparkles, CheckCircle2, Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import { fetchTechnologies, TechnologyData, createAdminQuestion } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

export default function NewQuestionPage() {
  const router = useRouter();
  const { token } = useAuth();
  const [technologies, setTechnologies] = useState<TechnologyData[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    title: "",
    technology_id: "",
    topic_id: "",
    difficulty: "TOUGH",
    interview_depth: "L4",
    question_type: "ARCHITECTURE",
    role_target: "Senior Software Engineer",
    experience_level: "3-7 years",
    estimated_time_minutes: 5,
    short_answer: "",
    interview_ready_answer: "",
    deep_explanation: "",
    architecture_notes: "",
    code_example: "",
    interviewer_intent: "",
    status: "PUBLISHED",
    content_origin: "ORIGINAL",
    source_name: "Official Framework Documentation",
    source_url: "https://breakthecode.dev",
    hint1: "",
    hint2: "",
    hint3: "",
  });

  useEffect(() => {
    fetchTechnologies().then((techs) => {
      setTechnologies(techs);
      if (techs.length > 0) {
        setFormData((prev) => ({ ...prev, technology_id: techs[0].id }));
      }
    });
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    const payload = {
      title: formData.title,
      technology_id: formData.technology_id,
      difficulty: formData.difficulty,
      interview_depth: formData.interview_depth,
      question_type: formData.question_type,
      role_target: formData.role_target,
      experience_level: formData.experience_level,
      estimated_time_minutes: Number(formData.estimated_time_minutes),
      short_answer: formData.short_answer,
      interview_ready_answer: formData.interview_ready_answer,
      deep_explanation: formData.deep_explanation,
      architecture_notes: formData.architecture_notes,
      code_example: formData.code_example,
      interviewer_intent: formData.interviewer_intent,
      status: formData.status,
      content_origin: formData.content_origin,
      hints: [
        { hint_level: 1, hint_type: "CONCEPTUAL", content: formData.hint1 || "Focus on the foundational data flow." },
        { hint_level: 2, hint_type: "IMPLEMENTATION", content: formData.hint2 || "Think about state mutation and locks." },
        { hint_level: 3, hint_type: "ARCHITECTURE", content: formData.hint3 || "Consider partition failure and recovery." },
      ],
      sources: [
        {
          source_name: formData.source_name,
          source_url: formData.source_url,
          license: "Attribution-NonCommercial",
          attribution_required: 1,
        },
      ],
    };

    try {
      setErrorMsg(null);
      await createAdminQuestion(payload, token || undefined);
      setSuccessMsg("Question created successfully!");
      setTimeout(() => {
        router.push("/admin/questions");
      }, 1500);
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.message || "Failed to create question");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-10 space-y-8">
      {/* Top Header */}
      <div className="flex items-center justify-between gap-4 pb-6 border-b border-border/70">
        <div className="space-y-1">
          <Link
            href="/admin/questions"
            className="text-xs text-muted-foreground hover:text-foreground flex items-center gap-1.5 transition-colors"
          >
            <ArrowLeft className="h-3.5 w-3.5" />
            <span>Back to Question Directory</span>
          </Link>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-foreground">
            Author New Interview Question
          </h1>
        </div>
      </div>

      {successMsg && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-600 dark:text-emerald-400 flex items-center gap-2 font-medium animate-fade-in">
          <CheckCircle2 className="h-4 w-4" />
          <span>{successMsg}</span>
        </div>
      )}

      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-xs text-rose-600 dark:text-rose-400 flex items-center gap-2 font-medium animate-fade-in">
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Editor Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Title */}
        <div className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Question Title *
          </label>
          <input
            type="text"
            name="title"
            required
            value={formData.title}
            onChange={handleChange}
            placeholder="e.g. How does checkpointing work in LangGraph under distributed workers?"
            className="w-full h-11 px-4 rounded-xl bg-card border border-border/80 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>

        {/* Metadata Selectors */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="space-y-2">
            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Technology Track *
            </label>
            <select
              name="technology_id"
              value={formData.technology_id}
              onChange={handleChange}
              className="w-full h-11 px-3 rounded-xl bg-card border border-border/80 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            >
              {technologies.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Difficulty *
            </label>
            <select
              name="difficulty"
              value={formData.difficulty}
              onChange={handleChange}
              className="w-full h-11 px-3 rounded-xl bg-card border border-border/80 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="BASIC">BASIC</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="TOUGH">TOUGH</option>
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Interview Depth *
            </label>
            <select
              name="interview_depth"
              value={formData.interview_depth}
              onChange={handleChange}
              className="w-full h-11 px-3 rounded-xl bg-card border border-border/80 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="L1">L1 · Definition</option>
              <option value="L2">L2 · Explanation</option>
              <option value="L3">L3 · Implementation</option>
              <option value="L4">L4 · Architecture</option>
              <option value="L5">L5 · Production Scenario</option>
            </select>
          </div>
        </div>

        {/* Short Answer */}
        <div className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Short Answer (30-second Elevator Pitch)
          </label>
          <textarea
            name="short_answer"
            rows={2}
            value={formData.short_answer}
            onChange={handleChange}
            placeholder="Brief 2-3 sentence overview..."
            className="w-full p-3 rounded-xl bg-card border border-border/80 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>

        {/* Interview-Ready Answer */}
        <div className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Interview-Ready Model Answer (2-Minute Spoken Response) *
          </label>
          <textarea
            name="interview_ready_answer"
            required
            rows={4}
            value={formData.interview_ready_answer}
            onChange={handleChange}
            placeholder="Comprehensive verbal answer expected in a senior interview..."
            className="w-full p-3 rounded-xl bg-card border border-border/80 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>

        {/* Code Snippet */}
        <div className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Code Example
          </label>
          <textarea
            name="code_example"
            rows={4}
            value={formData.code_example}
            onChange={handleChange}
            placeholder="Runnable snippet demonstrating pattern..."
            className="w-full p-3 rounded-xl bg-card border border-border/80 text-xs font-mono text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>

        {/* Progressive Hints */}
        <div className="space-y-3 pt-3 border-t border-border/60">
          <h4 className="text-xs font-bold uppercase tracking-wider text-foreground">
            3-Level Progressive Hints
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <input
              type="text"
              name="hint1"
              value={formData.hint1}
              onChange={handleChange}
              placeholder="Hint 1: Conceptual"
              className="h-10 px-3 rounded-lg bg-card border border-border/80 text-xs text-foreground"
            />
            <input
              type="text"
              name="hint2"
              value={formData.hint2}
              onChange={handleChange}
              placeholder="Hint 2: Implementation"
              className="h-10 px-3 rounded-lg bg-card border border-border/80 text-xs text-foreground"
            />
            <input
              type="text"
              name="hint3"
              value={formData.hint3}
              onChange={handleChange}
              placeholder="Hint 3: Architecture"
              className="h-10 px-3 rounded-lg bg-card border border-border/80 text-xs text-foreground"
            />
          </div>
        </div>

        {/* Source Attribution */}
        <div className="space-y-3 pt-3 border-t border-border/60">
          <h4 className="text-xs font-bold uppercase tracking-wider text-foreground">
            Source & Attribution Metadata
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <input
              type="text"
              name="source_name"
              value={formData.source_name}
              onChange={handleChange}
              placeholder="Source Name (e.g. Official Documentation)"
              className="h-10 px-3 rounded-lg bg-card border border-border/80 text-xs text-foreground"
            />
            <input
              type="url"
              name="source_url"
              value={formData.source_url}
              onChange={handleChange}
              placeholder="Source URL"
              className="h-10 px-3 rounded-lg bg-card border border-border/80 text-xs text-foreground"
            />
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-4 flex justify-end">
          <Button
            type="submit"
            variant="primary"
            size="lg"
            isLoading={isSubmitting}
            className="font-semibold"
          >
            <Save className="h-4 w-4 mr-1.5" />
            <span>Save & Publish Question</span>
          </Button>
        </div>
      </form>
    </div>
  );
}
