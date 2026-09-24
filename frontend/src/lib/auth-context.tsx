"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";

export interface UserProfile {
  id: string;
  email: string;
  full_name: string | null;
  avatar_url: string | null;
  xp: number;
  streak_days: number;
  level: number;
  roles: Array<{ name: string; description?: string }>;
}

interface AuthContextType {
  user: UserProfile | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  register: (email: string, password: string, fullName: string) => Promise<boolean>;
  loginAsDemo: (role?: "candidate" | "admin") => Promise<boolean>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchProfile = async (authToken: string) => {
    try {
      const res = await fetch(`${API_BASE}/users/me`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        // Token expired or invalid
        localStorage.removeItem("btc_token");
        setToken(null);
        setUser(null);
      }
    } catch (err) {
      console.error("Failed to fetch user profile", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const savedToken = typeof window !== "undefined" ? localStorage.getItem("btc_token") : null;
    if (savedToken) {
      setToken(savedToken);
      fetchProfile(savedToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) return false;
      const data = await res.json();
      const accessToken = data.access_token;
      localStorage.setItem("btc_token", accessToken);
      setToken(accessToken);
      setUser(data.user);
      return true;
    } catch (err) {
      console.error("Login error", err);
      return false;
    }
  };

  const register = async (email: string, password: string, fullName: string): Promise<boolean> => {
    try {
      const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, full_name: fullName }),
      });
      if (!res.ok) return false;
      const data = await res.json();
      const accessToken = data.access_token;
      localStorage.setItem("btc_token", accessToken);
      setToken(accessToken);
      setUser(data.user);
      return true;
    } catch (err) {
      console.error("Registration error", err);
      return false;
    }
  };

  const loginAsDemo = async (role: "candidate" | "admin" = "candidate"): Promise<boolean> => {
    if (role === "admin") {
      return login("admin@breakthecode.dev", "AdminPass123!");
    }
    return login("candidate@breakthecode.dev", "CandidatePass123!");
  };

  const logout = () => {
    localStorage.removeItem("btc_token");
    setToken(null);
    setUser(null);
  };

  const refreshUser = async () => {
    if (token) {
      await fetchProfile(token);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        register,
        loginAsDemo,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
