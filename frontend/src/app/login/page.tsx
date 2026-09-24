"use client";

import React, { useState, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { 
  ShieldCheck, 
  Sparkles, 
  Mail, 
  Lock, 
  User as UserIcon, 
  ArrowRight, 
  CheckCircle2, 
  AlertCircle,
  Eye,
  EyeOff,
  Terminal,
  LogIn
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Logo } from "@/components/layout/logo";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl");
  const { login, register, loginAsDemo, user } = useAuth();

  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // If already logged in, redirect
  React.useEffect(() => {
    if (user) {
      const isAdmin = user.roles?.some(r => r.name === "ADMIN" || r.name === "SUPER_ADMIN");
      if (callbackUrl) {
        router.push(callbackUrl);
      } else if (isAdmin) {
        router.push("/admin/users");
      } else {
        router.push("/dashboard");
      }
    }
  }, [user, router, callbackUrl]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setIsLoading(true);

    try {
      if (mode === "login") {
        const ok = await login(email, password);
        if (!ok) {
          setError("Invalid email or password. Please verify credentials.");
          setIsLoading(false);
          return;
        }
        // Redirect handled by useEffect
      } else {
        if (!fullName.trim()) {
          setError("Please enter your full name.");
          setIsLoading(false);
          return;
        }
        const ok = await register(email, password, fullName);
        if (!ok) {
          setError("Registration failed. The email may already be in use.");
          setIsLoading(false);
          return;
        }
        setSuccessMsg("Account created successfully! Redirecting...");
      }
    } catch (err: any) {
      setError(err?.message || "An unexpected error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickDemo = async (role: "admin" | "candidate") => {
    setError(null);
    setIsLoading(true);
    try {
      const ok = await loginAsDemo(role);
      if (!ok) {
        setError(`Failed to sign in as demo ${role}.`);
      }
    } catch (err: any) {
      setError(err?.message || "Demo login failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative">
      {/* Background ambient decorative glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-primary/10 dark:bg-primary/15 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-2/3 left-1/3 w-80 h-80 bg-accent-cyan/10 dark:bg-accent-cyan/15 rounded-full blur-3xl pointer-events-none" />

      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center relative z-10">
        <div className="inline-flex justify-center mb-4">
          <Logo size="lg" />
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-foreground">
          {mode === "login" ? "Sign in to Break The Code" : "Create your Engineer Profile"}
        </h2>
        <p className="mt-2 text-sm text-muted-foreground">
          {mode === "login" ? (
            <>
              New to the platform?{" "}
              <button
                type="button"
                onClick={() => { setMode("register"); setError(null); }}
                className="font-bold text-primary hover:text-primary/80 cursor-pointer underline underline-offset-4"
              >
                Create an account
              </button>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <button
                type="button"
                onClick={() => { setMode("login"); setError(null); }}
                className="font-bold text-primary hover:text-primary/80 cursor-pointer underline underline-offset-4"
              >
                Sign in here
              </button>
            </>
          )}
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="bg-surface/95 backdrop-blur-xl py-8 px-5 shadow-elevation-2 sm:rounded-2xl sm:px-10 border border-border/80 transition-all">
          
          {/* Quick Demo Access Bar */}
          <div className="mb-6 pb-6 border-b border-border/70">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                <Terminal className="h-3.5 w-3.5 text-primary" />
                1-Click Instant Demo Login
              </span>
              <span className="text-[10px] bg-primary/10 text-primary font-bold px-2 py-0.5 rounded-full border border-primary/20">
                Pre-configured
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2.5">
              <button
                type="button"
                onClick={() => handleQuickDemo("admin")}
                disabled={isLoading}
                className="flex items-center justify-center gap-2 p-2.5 rounded-xl border border-purple-500/30 bg-purple-500/10 hover:bg-purple-500/20 text-purple-700 dark:text-purple-300 text-xs font-bold transition-all shadow-2xs hover:scale-[1.02] cursor-pointer"
              >
                <ShieldCheck className="h-4 w-4 text-purple-500" />
                <span>Admin Login</span>
              </button>

              <button
                type="button"
                onClick={() => handleQuickDemo("candidate")}
                disabled={isLoading}
                className="flex items-center justify-center gap-2 p-2.5 rounded-xl border border-primary/30 bg-primary/10 hover:bg-primary/20 text-primary text-xs font-bold transition-all shadow-2xs hover:scale-[1.02] cursor-pointer"
              >
                <Sparkles className="h-4 w-4 text-primary" />
                <span>Candidate Demo</span>
              </button>
            </div>
          </div>

          {/* Error / Success Feedback */}
          {error && (
            <div className="mb-5 p-3.5 rounded-2xl bg-destructive/10 border border-destructive/30 text-destructive text-xs flex items-start gap-2.5 animate-shake">
              <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
              <span className="font-semibold leading-relaxed">{error}</span>
            </div>
          )}

          {successMsg && (
            <div className="mb-5 p-3.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 text-xs flex items-center gap-2.5">
              <CheckCircle2 className="h-4 w-4 shrink-0" />
              <span className="font-semibold">{successMsg}</span>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === "register" && (
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1.5">
                  Full Name
                </label>
                <Input
                  type="text"
                  required
                  placeholder="e.g. Alex Rivera"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  icon={<UserIcon className="h-4 w-4" />}
                  className="rounded-xl bg-background/90"
                />
              </div>
            )}

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1.5">
                Work Email Address
              </label>
              <Input
                type="email"
                required
                placeholder="name@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                icon={<Mail className="h-4 w-4" />}
                className="rounded-xl bg-background/90"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1.5">
                Password
              </label>
              <div className="relative">
                <Input
                  type={showPassword ? "text" : "password"}
                  required
                  placeholder="••••••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  icon={<Lock className="h-4 w-4" />}
                  className="rounded-xl bg-background/90 pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground cursor-pointer"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            {mode === "login" && (
              <div className="flex items-center justify-between text-xs pt-1">
                <label className="flex items-center gap-2 cursor-pointer text-muted-foreground hover:text-foreground">
                  <input
                    type="checkbox"
                    defaultChecked
                    className="h-3.5 w-3.5 rounded border-border text-primary focus:ring-primary"
                  />
                  <span>Remember session</span>
                </label>
                <span className="text-muted-foreground">
                  Admin: <code className="font-mono text-[10px] text-purple-600 dark:text-purple-400">admin@breakthecode.dev</code>
                </span>
              </div>
            )}

            <Button
              type="submit"
              disabled={isLoading}
              variant="primary"
              className="w-full h-11 rounded-xl font-bold text-sm shadow-sm shadow-primary/20 mt-2"
            >
              {isLoading ? (
                <span className="flex items-center gap-2">
                  <span className="h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin" />
                  Authenticating...
                </span>
              ) : mode === "login" ? (
                <span className="flex items-center gap-2">
                  <LogIn className="h-4 w-4" />
                  Sign In to Platform
                  <ArrowRight className="h-4 w-4 ml-1" />
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4" />
                  Create Free Account
                  <ArrowRight className="h-4 w-4 ml-1" />
                </span>
              )}
            </Button>
          </form>

          <div className="mt-6 text-center text-xs text-muted-foreground">
            Protected by enterprise-grade token encryption &amp; role-based access control.
          </div>
        </div>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={
      <div className="min-h-[70vh] flex items-center justify-center">
        <div className="h-8 w-8 rounded-full border-2 border-primary border-t-transparent animate-spin" />
      </div>
    }>
      <LoginForm />
    </Suspense>
  );
}
