"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Bookmark,
  BookmarkX,
  Search,
  BrainCircuit,
  Clock,
  ExternalLink,
  Layers,
  Sparkles
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { fetchUserBookmarks, toggleBookmark } from "@/lib/api";
import { Button } from "@/components/ui/button";

export default function BookmarksPage() {
  const { token } = useAuth();
  const [bookmarks, setBookmarks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchFilter, setSearchFilter] = useState("");

  useEffect(() => {
    if (token) {
      loadBookmarks();
    }
  }, [token]);

  const loadBookmarks = async () => {
    if (!token) return;
    setLoading(true);
    const items = await fetchUserBookmarks(token);
    setBookmarks(items);
    setLoading(false);
  };

  const handleRemoveBookmark = async (questionId: string) => {
    if (!token) return;
    // Optimistic removal
    setBookmarks((prev) => prev.filter((b) => b.question_id !== questionId));
    await toggleBookmark(token, questionId);
  };

  const filteredBookmarks = bookmarks.filter((b) => {
    const q = searchFilter.toLowerCase();
    return (
      b.title.toLowerCase().includes(q) ||
      b.technology_name.toLowerCase().includes(q) ||
      b.difficulty.toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <Bookmark className="h-5 w-5 text-amber-500 fill-amber-500" />
            Saved Bookmarks
          </h2>
          <p className="text-xs text-muted-foreground mt-0.5">
            Curated questions you saved for deep review and practice before your interview.
          </p>
        </div>

        {/* Filter input */}
        <div className="relative w-full sm:w-64">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
          <input
            type="text"
            placeholder="Filter saved questions..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full h-8 pl-8 pr-3 rounded-lg bg-card border border-border/80 text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 rounded-2xl bg-muted/40 animate-pulse" />
          ))}
        </div>
      ) : filteredBookmarks.length === 0 ? (
        <div className="p-12 text-center border border-dashed border-border/80 rounded-3xl bg-card/40">
          <Bookmark className="h-10 w-10 text-muted-foreground/40 mx-auto mb-3" />
          <h3 className="text-sm font-semibold text-foreground mb-1">No bookmarked questions</h3>
          <p className="text-xs text-muted-foreground max-w-sm mx-auto mb-4">
            While exploring questions or using Think Mode, click the bookmark icon to save complex problems here.
          </p>
          <Link href="/questions">
            <Button size="sm" variant="primary">
              <Sparkles className="h-3.5 w-3.5 mr-1" />
              Explore Question Directory
            </Button>
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredBookmarks.map((item) => (
            <div
              key={item.bookmark_id}
              className="p-5 rounded-2xl border border-border/80 bg-card/60 backdrop-blur-md hover:border-primary/40 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
            >
              <div className="space-y-1.5 min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-semibold text-primary px-2 py-0.5 rounded bg-primary/10">
                    {item.technology_name}
                  </span>
                  <span className="text-[10px] font-medium text-muted-foreground px-1.5 py-0.2 rounded bg-muted">
                    {item.difficulty}
                  </span>
                  {item.topic_name && (
                    <span className="text-[11px] text-muted-foreground hidden sm:inline">
                      • {item.topic_name}
                    </span>
                  )}
                </div>

                <Link
                  href={`/questions/${item.slug}`}
                  className="font-bold text-sm text-foreground hover:text-primary transition-colors block truncate"
                >
                  {item.title}
                </Link>

                <div className="flex items-center gap-3 text-[11px] text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <Clock className="h-3 w-3" /> {item.estimated_time_minutes || 15} mins
                  </span>
                  <span>•</span>
                  <span>Depth: {item.interview_depth || "L3"}</span>
                </div>
              </div>

              <div className="flex items-center gap-2 self-end sm:self-center">
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => handleRemoveBookmark(item.question_id)}
                  title="Remove from saved bookmarks"
                  className="text-muted-foreground hover:text-rose-500 hover:bg-rose-500/10 h-8 px-2"
                >
                  <BookmarkX className="h-4 w-4" />
                </Button>

                <Link href={`/questions/${item.slug}`}>
                  <Button size="sm" variant="primary" className="h-8 text-xs flex items-center gap-1.5">
                    <BrainCircuit className="h-3.5 w-3.5" />
                    Practice Think Mode
                  </Button>
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
