"use client";

import React, { useState, useMemo } from "react";
import { Check, Copy, FileCode2, Terminal, Code2, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface CodeBlockProps {
  code: string;
  language?: string;
  filename?: string;
  className?: string;
  showLineNumbers?: boolean;
}

// VS Code / Antigravity Token Categories
const KEYWORDS = new Set([
  // Python
  "def", "class", "import", "from", "return", "async", "await", "yield",
  "if", "elif", "else", "try", "except", "finally", "raise", "while",
  "for", "in", "is", "not", "and", "or", "with", "as", "pass", "break",
  "continue", "lambda", "global", "nonlocal", "assert",
  // Java / TS / C++
  "public", "private", "protected", "static", "final", "void", "new",
  "this", "super", "interface", "extends", "implements", "throw", "throws",
  "switch", "case", "default", "const", "let", "var", "function", "export",
  "package", "synchronized", "volatile", "transient", "native"
]);

const BUILTIN_TYPES = new Set([
  "int", "float", "str", "bool", "dict", "list", "set", "tuple", "bytes",
  "object", "type", "void", "boolean", "byte", "char", "short", "long", "double",
  "String", "Integer", "Long", "Boolean", "Double", "Float", "Object",
  "List", "Map", "Set", "Dict", "Any", "Optional", "Union", "Tuple",
  "TypedDict", "Annotated", "Callable", "Sequence", "Iterable", "Mapping",
  "StateGraph", "MessagesState", "BaseMessage", "HumanMessage", "AIMessage",
  "SystemMessage", "ToolMessage", "Command", "MemorySaver", "SqliteSaver",
  "CompletableFuture", "ExecutorService", "ReentrantLock", "ConcurrentHashMap",
  "Thread", "AtomicInteger", "AtomicLong", "AtomicBoolean", "AtomicReference"
]);

const BUILTIN_CONSTANTS = new Set([
  "True", "False", "None", "true", "false", "null", "undefined", "self", "cls", "this"
]);

interface Token {
  kind: "keyword" | "type" | "constant" | "decorator" | "comment" | "string" | "func" | "number" | "punct" | "text" | "space";
  text: string;
}

function tokenizeLine(line: string): Token[] {
  if (!line) return [];

  // Full-line comment check
  const trimmed = line.trimStart();
  if (trimmed.startsWith("#") || trimmed.startsWith("//")) {
    const indent = line.slice(0, line.indexOf(trimmed));
    return [
      { kind: "space", text: indent },
      { kind: "comment", text: trimmed },
    ];
  }

  const tokens: Token[] = [];
  const regex = /(#.*$|\/\/.*$)|(f?"""[\s\S]*?"""|f?'''[\s\S]*?'''|f?"(?:\\.|[^"\\])*"|f?'(?:\\.|[^'\\])*')|(@\w+)|(\b\d+(?:\.\d+)?\b)|(\b[a-zA-Z_]\w*\b)|([->:=<>&|!~+*/%]+)|(\S)/g;

  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(line)) !== null) {
    if (match.index > lastIndex) {
      tokens.push({ kind: "space", text: line.slice(lastIndex, match.index) });
    }

    const [full, comment, str, decorator, num, word, punct, other] = match;

    if (comment) {
      tokens.push({ kind: "comment", text: comment });
    } else if (str) {
      tokens.push({ kind: "string", text: str });
    } else if (decorator) {
      tokens.push({ kind: "decorator", text: decorator });
    } else if (num) {
      tokens.push({ kind: "number", text: num });
    } else if (word) {
      // Check if followed by '(' -> function call
      const after = line.slice(match.index + word.length);
      const isFuncCall = /^\s*\(/.test(after);

      if (KEYWORDS.has(word)) {
        tokens.push({ kind: "keyword", text: word });
      } else if (BUILTIN_CONSTANTS.has(word)) {
        tokens.push({ kind: "constant", text: word });
      } else if (BUILTIN_TYPES.has(word) || /^[A-Z][a-zA-Z0-9_]*$/.test(word)) {
        tokens.push({ kind: "type", text: word });
      } else if (isFuncCall) {
        tokens.push({ kind: "func", text: word });
      } else {
        tokens.push({ kind: "text", text: word });
      }
    } else if (punct) {
      tokens.push({ kind: "punct", text: punct });
    } else if (other) {
      tokens.push({ kind: "text", text: other });
    }

    lastIndex = regex.lastIndex;
  }

  if (lastIndex < line.length) {
    tokens.push({ kind: "space", text: line.slice(lastIndex) });
  }

  return tokens;
}

function renderToken(token: Token, key: string | number): React.ReactNode {
  switch (token.kind) {
    case "keyword":
      // VS Code Magenta / Red-Pink
      return <span key={key} className="text-[#ff7b72] font-semibold">{token.text}</span>;
    case "type":
      // VS Code Gold / Amber
      return <span key={key} className="text-[#ffa657] font-semibold">{token.text}</span>;
    case "constant":
      // VS Code Salmon / Cyan
      return <span key={key} className="text-[#79c0ff] font-semibold italic">{token.text}</span>;
    case "decorator":
      // VS Code Lavender
      return <span key={key} className="text-[#d2a8ff] font-medium">{token.text}</span>;
    case "func":
      // VS Code Sky Blue
      return <span key={key} className="text-[#79c0ff]">{token.text}</span>;
    case "string":
      // VS Code Fresh Mint
      return <span key={key} className="text-[#7ee787] font-normal">{token.text}</span>;
    case "number":
      // VS Code Neon Cyan
      return <span key={key} className="text-[#79c0ff]">{token.text}</span>;
    case "comment":
      // VS Code Slate Gray Italic
      return <span key={key} className="text-[#8b949e] italic">{token.text}</span>;
    case "punct":
      // VS Code Muted Blue / Coral Operator
      return <span key={key} className="text-[#ff7b72]">{token.text}</span>;
    default:
      // Crisp Off-White Identifier
      return <span key={key} className="text-[#e6edf3]">{token.text}</span>;
  }
}

export const CodeBlock: React.FC<CodeBlockProps> = ({ 
  code, 
  language = "python", 
  filename,
  className,
  showLineNumbers = true 
}) => {
  const [copied, setCopied] = useState(false);

  const cleanCode = (code || "").trimEnd();
  const lines = useMemo(() => cleanCode.split("\n"), [cleanCode]);

  const defaultFilename = useMemo(() => {
    if (filename) return filename;
    const l = language.toLowerCase();
    if (l === "java") return "Solution.java";
    if (l === "javascript" || l === "js") return "index.js";
    if (l === "typescript" || l === "ts") return "solution.ts";
    if (l === "sql") return "query.sql";
    if (l === "json") return "payload.json";
    if (l === "bash" || l === "sh") return "terminal.sh";
    return "solution.py";
  }, [filename, language]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(cleanCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy code", err);
    }
  };

  return (
    <div 
      className={cn(
        "relative rounded-2xl border border-[#30363d] overflow-hidden my-5 bg-[#0d1117] text-[#e6edf3] shadow-2xl transition-all duration-200",
        "ring-1 ring-white/5",
        className
      )}
    >
      {/* 1. VS Code / Antigravity Editor Window Titlebar */}
      <div className="flex items-center justify-between px-3.5 sm:px-4 py-2 bg-[#161b22] border-b border-[#30363d] select-none">
        
        {/* Left: macOS / IDE Window Traffic Light Controls + Active File Tab */}
        <div className="flex items-center gap-3 overflow-hidden">
          {/* Traffic Lights */}
          <div className="flex items-center gap-1.5 shrink-0 pl-0.5">
            <span className="h-3 w-3 rounded-full bg-[#ff5f56] border border-[#e0443e]/40 shadow-xs inline-block" />
            <span className="h-3 w-3 rounded-full bg-[#ffbd2e] border border-[#dea123]/40 shadow-xs inline-block" />
            <span className="h-3 w-3 rounded-full bg-[#27c93f] border border-[#1aab29]/40 shadow-xs inline-block" />
          </div>

          {/* Active File Tab */}
          <div className="flex items-center gap-2 px-3 py-1 rounded-md bg-[#0d1117] border border-[#30363d] border-b-transparent text-xs font-mono text-[#e6edf3] font-semibold shrink-0 shadow-xs">
            <FileCode2 className="h-3.5 w-3.5 text-rose-400" />
            <span>{defaultFilename}</span>
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-xs" title="Ready to execute" />
          </div>
        </div>

        {/* Right Action Bar: Language Tag + Copy Button */}
        <div className="flex items-center gap-2 shrink-0">
          <span className="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-mono font-bold uppercase tracking-wider bg-[#21262d] text-[#8b949e] border border-[#30363d]">
            <Terminal className="h-3 w-3 text-rose-400" />
            {language}
          </span>

          <button
            onClick={handleCopy}
            className={cn(
              "flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-mono font-semibold transition-all duration-150 cursor-pointer border active:scale-95",
              copied
                ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/50 shadow-sm shadow-emerald-500/20"
                : "bg-[#21262d] hover:bg-[#30363d] text-[#c9d1d9] hover:text-white border-[#30363d]"
            )}
            title="Copy code snippet to clipboard"
            aria-label="Copy code"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-emerald-400" />
                <span className="text-emerald-400 font-bold">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="h-3.5 w-3.5 text-[#8b949e] group-hover:text-white" />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* 2. Code Editor Surface with Gutter & Syntax Highlighted Lines */}
      <div 
        className="p-0 overflow-x-auto select-text font-mono text-[13.5px] sm:text-[14.5px] leading-[1.78] tracking-normal"
        style={{
          fontFamily: "'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, Monaco, Consolas, monospace",
          fontFeatureSettings: '"liga" 1, "calt" 1',
        }}
      >
        <table className="w-full border-collapse">
          <tbody>
            {lines.map((line, idx) => {
              const tokens = tokenizeLine(line);
              return (
                <tr 
                  key={idx} 
                  className="hover:bg-white/[0.04] transition-colors group"
                >
                  {/* Gutter Line Number */}
                  {showLineNumbers && (
                    <td className="w-12 sm:w-14 pl-3 pr-3 text-right select-none text-[#6e7681] group-hover:text-[#8b949e] font-mono text-xs sm:text-[13px] align-top bg-[#161b22]/50 border-r border-[#30363d]/70">
                      {String(idx + 1).padStart(2, "0")}
                    </td>
                  )}
                  {/* Code Line Content */}
                  <td className="pl-4 pr-5 py-0.5 whitespace-pre font-mono text-[#e6edf3]">
                    {tokens.length > 0 ? (
                      tokens.map((t, tIdx) => renderToken(t, tIdx))
                    ) : (
                      <span>&nbsp;</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* 3. VS Code Bottom Status Bar */}
      <div className="flex items-center justify-between px-3.5 py-1 bg-[#161b22]/90 border-t border-[#30363d] text-[11px] font-mono text-[#8b949e] select-none">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1 text-emerald-400 font-semibold">
            <Sparkles className="h-3 w-3" />
            <span>Production Calibrated</span>
          </span>
          <span className="text-[#30363d]">|</span>
          <span>{lines.length} lines</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="hidden sm:inline">UTF-8</span>
          <span className="hidden sm:inline text-[#30363d]">|</span>
          <span className="uppercase">{language}</span>
        </div>
      </div>
    </div>
  );
};

export default CodeBlock;
