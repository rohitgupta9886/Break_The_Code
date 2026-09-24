"use client";

import React from "react";
import { CodeBlock } from "@/components/ui/code-block";

interface FormattedAnswerProps {
  text: string;
  className?: string;
  variant?: "lead" | "body";
}

/**
 * Parses inline tokens:
 * - Highlights **keywords** with an attractive, high-contrast highlighter badge
 * - Formats `code` with styled monospace badge resembling VS Code tokens
 * - Completely strips out any stray '*' characters
 */
function parseInline(text: string): React.ReactNode[] {
  if (!text) return [];
  const parts: React.ReactNode[] = [];
  const regex = /(\*\*([^*]+)\*\*)|(`([^`]+)`)/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      const plain = text.slice(lastIndex, match.index).replace(/\*/g, "");
      if (plain) parts.push(plain);
    }

    if (match[2]) {
      // Highlighted Keyword (stripped of *)
      const cleanKeyword = match[2].replace(/\*/g, "").trim();
      parts.push(
        <mark
          key={`kw-${match.index}`}
          className="font-bold text-amber-950 dark:text-amber-100 bg-amber-300/35 dark:bg-amber-400/25 px-1.5 py-0.5 rounded-md border-b-2 border-amber-500/70 not-italic inline-block my-0.5 shadow-xs"
        >
          {cleanKeyword}
        </mark>
      );
    } else if (match[4]) {
      // Inline Code - VS Code dark chip appearance
      parts.push(
        <code
          key={`code-${match.index}`}
          className="font-mono text-[13.5px] sm:text-[14px] px-2 py-0.5 rounded-md bg-[#161b22] text-[#79c0ff] border border-[#30363d] font-bold tracking-tight shadow-2xs selection:bg-rose-500/30"
        >
          {match[4]}
        </code>
      );
    }
    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    const plain = text.slice(lastIndex).replace(/\*/g, "");
    if (plain) parts.push(plain);
  }

  return parts;
}

interface Block {
  type: "heading" | "numbered" | "bullet" | "paragraph" | "code";
  num?: string;
  heading?: string;
  body: string;
}

function parseBlocks(rawText: string): Block[] {
  if (!rawText) return [];
  const lines = rawText.split("\n");
  const blocks: Block[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i].trim();
    if (!line) {
      i++;
      continue;
    }

    // 0. Markdown Code Block (```lang ... ```)
    if (/^```/.test(line)) {
      const langMatch = line.match(/^```(\w+)?/);
      const lang = (langMatch && langMatch[1]) ? langMatch[1] : "python";
      const codeLines: string[] = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith("```")) {
        codeLines.push(lines[i]);
        i++;
      }
      if (i < lines.length && lines[i].trim().startsWith("```")) {
        i++;
      }
      blocks.push({
        type: "code",
        heading: lang,
        body: codeLines.join("\n"),
      });
      continue;
    }

    // 1. Markdown Heading (###, ##, #)
    if (/^#{1,6}\s+/.test(line)) {
      const cleanHeading = line.replace(/^#{1,6}\s+/, "").replace(/\*/g, "").trim();
      blocks.push({
        type: "heading",
        body: cleanHeading,
      });
      i++;
      continue;
    }

    // 2. Numbered list item (e.g. "1. **Title**: Body" or "1. Title: Body" or "1. Body")
    if (/^\d+\.\s+/.test(line)) {
      const withColon = line.match(/^(\d+)\.\s+(?:\*\*([^*]+)\*\*|([^:]+)):\s*(.*)$/);
      if (withColon) {
        blocks.push({
          type: "numbered",
          num: withColon[1],
          heading: (withColon[2] || withColon[3] || "").replace(/\*/g, "").trim(),
          body: withColon[4].trim(),
        });
      } else {
        const simple = line.match(/^(\d+)\.\s+(.*)$/);
        blocks.push({
          type: "numbered",
          num: simple ? simple[1] : "1",
          heading: "",
          body: simple ? simple[2].trim() : line,
        });
      }
      i++;
      continue;
    }

    // 3. Bullet list item (starts with -, *, or •)
    if (/^[-*•]\s+/.test(line)) {
      const stripped = line.replace(/^[-*•]\s+/, "");
      const withColon = stripped.match(/^(?:\*\*([^*]+)\*\*|([^:]+)):\s*(.*)$/);
      if (withColon) {
        blocks.push({
          type: "bullet",
          heading: (withColon[1] || withColon[2] || "").replace(/\*/g, "").trim(),
          body: withColon[3].trim(),
        });
      } else {
        blocks.push({
          type: "bullet",
          heading: "",
          body: stripped.replace(/\*/g, "").trim(),
        });
      }
      i++;
      continue;
    }

    // 4. Regular Paragraph
    blocks.push({
      type: "paragraph",
      body: line,
    });
    i++;
  }

  return blocks;
}

export function FormattedAnswer({
  text,
  className = "",
  variant = "body",
}: FormattedAnswerProps) {
  if (!text) return null;

  const blocks = parseBlocks(text);

  return (
    <div className={`formatted-answer-container space-y-3 ${className}`}>
      {blocks.map((block, idx) => {
        if (block.type === "heading") {
          return (
            <h4
              key={idx}
              className="text-base sm:text-lg font-black text-rose-600 dark:text-rose-400 mt-5 mb-2.5 flex items-center gap-2 tracking-tight"
            >
              <span className="h-2 w-2 rounded-full bg-rose-500 shadow-xs shrink-0" />
              <span>{block.body}</span>
            </h4>
          );
        }

        if (block.type === "numbered") {
          return (
            <div
              key={idx}
              className="flex items-start gap-3 p-3.5 sm:p-4 rounded-xl bg-white/80 dark:bg-card/70 border border-border/70 hover:border-rose-300 dark:hover:border-rose-900/60 shadow-xs transition-colors"
            >
              <span className="inline-flex items-center justify-center w-6 h-6 rounded-lg bg-rose-500/15 text-rose-700 dark:text-rose-300 font-black text-xs shrink-0 mt-0.5 border border-rose-500/25 shadow-2xs">
                {block.num}
              </span>
              <div className="space-y-1 text-[15px] sm:text-base leading-relaxed text-foreground/95 flex-1">
                {block.heading && (
                  <span className="font-extrabold text-rose-600 dark:text-rose-400 mr-2 text-[15px] sm:text-base">
                    {block.heading}:
                  </span>
                )}
                <span>{parseInline(block.body)}</span>
              </div>
            </div>
          );
        }

        if (block.type === "bullet") {
          return (
            <div
              key={idx}
              className="flex items-start gap-2.5 pl-1 text-[15px] sm:text-base leading-relaxed text-foreground/95"
            >
              <span className="mt-2.5 h-2 w-2 rounded-full bg-rose-500 shrink-0 shadow-xs" />
              <div className="flex-1">
                {block.heading && (
                  <span className="font-bold text-rose-600 dark:text-rose-400 mr-1.5">
                    {block.heading}:
                  </span>
                )}
                <span>{parseInline(block.body)}</span>
              </div>
            </div>
          );
        }

        if (block.type === "code") {
          return (
            <CodeBlock
              key={idx}
              code={block.body}
              language={block.heading || "python"}
              showLineNumbers={true}
            />
          );
        }

        // Paragraph
        return (
          <p
            key={idx}
            className={`text-[15px] sm:text-base leading-relaxed text-foreground/95 ${
              variant === "lead" ? "font-medium" : ""
            }`}
          >
            {parseInline(block.body)}
          </p>
        );
      })}
    </div>
  );
}

export default FormattedAnswer;
