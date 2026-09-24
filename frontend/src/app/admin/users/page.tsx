"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Users,
  UserPlus,
  Download,
  Search,
  Filter,
  ShieldCheck,
  ShieldAlert,
  Clock,
  Calendar,
  CheckCircle2,
  XCircle,
  Edit2,
  Trash2,
  RefreshCw,
  Key,
  Mail,
  UserCheck,
  UserX,
  FileSpreadsheet,
  FileCode,
  Flame,
  Zap,
  ArrowUpDown
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface AdminUserItem {
  id: string;
  email: string;
  full_name: string | null;
  avatar_url: string | null;
  is_active: boolean;
  is_verified: boolean;
  xp: number;
  streak_days: number;
  created_at: string | null;
  last_login_at: string | null;
  roles: string[];
  primary_role: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

export default function AdminUsersPage() {
  const router = useRouter();
  const { user: currentUser, token, isLoading: authLoading, loginAsDemo } = useAuth();

  const [users, setUsers] = useState<AdminUserItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [roleFilter, setRoleFilter] = useState<string>("ALL");
  const [statusFilter, setStatusFilter] = useState<string>("ALL");
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);

  // Modals state
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<AdminUserItem | null>(null);

  // Form states
  const [formName, setFormName] = useState("");
  const [formEmail, setFormEmail] = useState("");
  const [formPassword, setFormPassword] = useState("");
  const [formRole, setFormRole] = useState("USER");
  const [formIsActive, setFormIsActive] = useState(true);
  const [formLoading, setFormLoading] = useState(false);

  const showToast = (message: string, type: "success" | "error" = "success") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  const isAdmin = currentUser?.roles?.some(r => r.name === "ADMIN" || r.name === "SUPER_ADMIN");

  const fetchUsers = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/admin/users`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUsers(data.users || []);
      } else {
        showToast("Failed to fetch users list", "error");
      }
    } catch (err) {
      showToast("Network error while loading users", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading && token && isAdmin) {
      fetchUsers();
    }
  }, [authLoading, token, isAdmin]);

  // Export handlers
  const handleExport = async (format: "csv" | "json") => {
    if (!token) return;
    try {
      const res = await fetch(`${API_BASE}/admin/users/export?format=${format}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) {
        showToast(`Failed to export data as ${format.toUpperCase()}`, "error");
        return;
      }

      if (format === "csv") {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `breakthecode_users_export_${new Date().toISOString().slice(0, 10)}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        showToast("Users CSV successfully exported and downloaded!");
      } else {
        const json = await res.json();
        const blob = new Blob([JSON.stringify(json, null, 2)], { type: "application/json" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `breakthecode_users_export_${new Date().toISOString().slice(0, 10)}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        showToast("Users JSON successfully exported and downloaded!");
      }
    } catch (err) {
      showToast(`Error during ${format.toUpperCase()} export`, "error");
    }
  };

  // Create User
  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) return;
    setFormLoading(true);
    try {
      const res = await fetch(`${API_BASE}/admin/users`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          full_name: formName.trim() || undefined,
          email: formEmail.trim(),
          password: formPassword,
          role: formRole,
          is_active: formIsActive,
        }),
      });

      const data = await res.json();
      if (res.ok) {
        showToast(data.message || "User created successfully!");
        setIsCreateOpen(false);
        resetForm();
        fetchUsers();
      } else {
        showToast(data.detail || "Failed to create user", "error");
      }
    } catch (err) {
      showToast("Error creating user", "error");
    } finally {
      setFormLoading(false);
    }
  };

  // Update User
  const handleUpdateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !selectedUser) return;
    setFormLoading(true);
    try {
      const body: any = {
        full_name: formName.trim() || undefined,
        email: formEmail.trim(),
        role: formRole,
        is_active: formIsActive,
      };
      if (formPassword.trim()) {
        body.password = formPassword.trim();
      }

      const res = await fetch(`${API_BASE}/admin/users/${selectedUser.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      if (res.ok) {
        showToast(data.message || "User updated successfully!");
        setIsEditOpen(false);
        resetForm();
        fetchUsers();
      } else {
        showToast(data.detail || "Failed to update user", "error");
      }
    } catch (err) {
      showToast("Error updating user", "error");
    } finally {
      setFormLoading(false);
    }
  };

  // Toggle active status directly
  const handleToggleStatus = async (userItem: AdminUserItem) => {
    if (!token) return;
    try {
      const res = await fetch(`${API_BASE}/admin/users/${userItem.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          is_active: !userItem.is_active,
        }),
      });
      const data = await res.json();
      if (res.ok) {
        showToast(`User ${userItem.email} is now ${!userItem.is_active ? "Active" : "Suspended"}`);
        fetchUsers();
      } else {
        showToast(data.detail || "Status toggle failed", "error");
      }
    } catch (err) {
      showToast("Failed to toggle user status", "error");
    }
  };

  // Delete User
  const handleDeleteUser = async () => {
    if (!token || !selectedUser) return;
    setFormLoading(true);
    try {
      const res = await fetch(`${API_BASE}/admin/users/${selectedUser.id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (res.ok) {
        showToast(data.message || "User account deleted");
        setIsDeleteOpen(false);
        setSelectedUser(null);
        fetchUsers();
      } else {
        showToast(data.detail || "Failed to delete user", "error");
      }
    } catch (err) {
      showToast("Error deleting user", "error");
    } finally {
      setFormLoading(false);
    }
  };

  const openEditModal = (u: AdminUserItem) => {
    setSelectedUser(u);
    setFormName(u.full_name || "");
    setFormEmail(u.email);
    setFormPassword("");
    setFormRole(u.primary_role || "USER");
    setFormIsActive(u.is_active);
    setIsEditOpen(true);
  };

  const openDeleteModal = (u: AdminUserItem) => {
    setSelectedUser(u);
    setIsDeleteOpen(true);
  };

  const resetForm = () => {
    setSelectedUser(null);
    setFormName("");
    setFormEmail("");
    setFormPassword("");
    setFormRole("USER");
    setFormIsActive(true);
  };

  // Format date helper
  const formatDate = (isoString: string | null) => {
    if (!isoString) return { display: "Never", relative: "Offline", isRecent: false };
    try {
      const date = new Date(isoString);
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMins / 60);
      const diffDays = Math.floor(diffHours / 24);

      let relative = "";
      if (diffMins < 1) relative = "Just now";
      else if (diffMins < 60) relative = `${diffMins}m ago`;
      else if (diffHours < 24) relative = `${diffHours}h ago`;
      else relative = `${diffDays}d ago`;

      const display = date.toLocaleString(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });

      return { display, relative, isRecent: diffHours < 24 };
    } catch (e) {
      return { display: isoString.slice(0, 16), relative: "", isRecent: false };
    }
  };

  // Filtered users
  const filteredUsers = useMemo(() => {
    return users.filter((u) => {
      if (roleFilter !== "ALL" && !u.roles.includes(roleFilter)) return false;
      if (statusFilter === "ACTIVE" && !u.is_active) return false;
      if (statusFilter === "SUSPENDED" && u.is_active) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchesName = u.full_name && u.full_name.toLowerCase().includes(q);
        const matchesEmail = u.email.toLowerCase().includes(q);
        if (!matchesName && !matchesEmail) return false;
      }
      return true;
    });
  }, [users, roleFilter, statusFilter, searchQuery]);

  // Key metrics
  const stats = useMemo(() => {
    const total = users.length;
    const active = users.filter((u) => u.is_active).length;
    const admins = users.filter((u) => u.roles.some((r) => r === "ADMIN" || r === "SUPER_ADMIN")).length;
    const loggedInRecently = users.filter((u) => {
      if (!u.last_login_at) return false;
      const d = new Date(u.last_login_at);
      return Date.now() - d.getTime() < 24 * 3600 * 1000;
    }).length;
    return { total, active, admins, loggedInRecently };
  }, [users]);

  // Auth Guard Screen if not Admin
  if (!authLoading && (!currentUser || !isAdmin)) {
    return (
      <div className="max-w-4xl mx-auto py-16 px-4 text-center">
        <div className="h-16 w-16 mx-auto rounded-3xl bg-rose-100 dark:bg-rose-950/60 border border-rose-200 dark:border-rose-900 flex items-center justify-center text-rose-600 mb-6 shadow-xl">
          <ShieldAlert className="h-8 w-8" />
        </div>
        <h1 className="text-3xl font-extrabold text-foreground mb-3">Administrator Privileges Required</h1>
        <p className="text-muted-foreground max-w-md mx-auto mb-8">
          The User Management &amp; Export suite is restricted to verified Platform Administrators.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Button
            variant="primary"
            onClick={async () => {
              await loginAsDemo("admin");
              fetchUsers();
            }}
            className="rounded-xl font-bold shadow-md shadow-rose-500/20"
          >
            <ShieldCheck className="h-4 w-4 mr-2" />
            Sign in as Demo Admin
          </Button>
          <Link href="/login">
            <Button variant="outline" className="rounded-xl font-bold">
              Standard Login
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Toast Notification */}
      {toast && (
        <div
          className={`fixed bottom-6 right-6 z-50 px-4 py-3 rounded-2xl shadow-2xl border text-sm font-semibold flex items-center gap-2.5 transition-all ${
            toast.type === "success"
              ? "bg-emerald-500/95 text-white border-emerald-400"
              : "bg-destructive/95 text-white border-destructive"
          }`}
        >
          {toast.type === "success" ? <CheckCircle2 className="h-4 w-4" /> : <XCircle className="h-4 w-4" />}
          <span>{toast.message}</span>
        </div>
      )}

      {/* Header & Title Section */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-border/60 pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1.5">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-purple-100 dark:bg-purple-950/70 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800">
              Admin Suite
            </span>
            <span className="text-xs text-muted-foreground flex items-center gap-1 font-mono">
              <Clock className="h-3 w-3" /> Live User Telemetry
            </span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-foreground flex items-center gap-3">
            <Users className="h-8 w-8 text-rose-500" />
            User Management &amp; Login Telemetry
          </h1>
          <p className="text-sm text-muted-foreground mt-1 max-w-2xl">
            Monitor real-time candidate logins, manage credentials and roles (CRUD), and export comprehensive user telemetry across CSV and JSON.
          </p>
        </div>

        {/* Global Action Toolbar */}
        <div className="flex flex-wrap items-center gap-2.5">
          <Button
            variant="outline"
            size="sm"
            onClick={() => handleExport("csv")}
            className="rounded-xl border-emerald-500/40 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-500/10 font-bold"
          >
            <FileSpreadsheet className="h-4 w-4 mr-1.5 text-emerald-600" />
            Export CSV
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={() => handleExport("json")}
            className="rounded-xl border-blue-500/40 text-blue-700 dark:text-blue-300 hover:bg-blue-500/10 font-bold"
          >
            <FileCode className="h-4 w-4 mr-1.5 text-blue-500" />
            Export JSON
          </Button>

          <Button
            variant="primary"
            size="sm"
            onClick={() => { resetForm(); setIsCreateOpen(true); }}
            className="rounded-xl font-bold shadow-sm shadow-rose-500/20"
          >
            <UserPlus className="h-4 w-4 mr-1.5" />
            Add User
          </Button>

          <button
            onClick={fetchUsers}
            title="Refresh Users"
            className="p-2 rounded-xl border border-border/80 hover:bg-muted text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>
      </div>

      {/* Metric KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-card border border-border/80 shadow-2xs">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-bold uppercase tracking-wider">Total Accounts</span>
            <Users className="h-4 w-4 text-primary" />
          </div>
          <div className="text-2xl font-black text-foreground">{stats.total}</div>
          <div className="text-xs text-muted-foreground mt-1">Registered platform candidates</div>
        </div>

        <div className="p-5 rounded-2xl bg-card border border-emerald-500/25 shadow-2xs">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-bold uppercase tracking-wider">Active Status</span>
            <UserCheck className="h-4 w-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-black text-emerald-600 dark:text-emerald-400">{stats.active}</div>
          <div className="text-xs text-muted-foreground mt-1">Unrestricted active users</div>
        </div>

        <div className="p-5 rounded-2xl bg-card border border-purple-500/25 shadow-2xs">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-bold uppercase tracking-wider">Admin Staff</span>
            <ShieldCheck className="h-4 w-4 text-purple-500" />
          </div>
          <div className="text-2xl font-black text-purple-600 dark:text-purple-400">{stats.admins}</div>
          <div className="text-xs text-muted-foreground mt-1">Super Admin &amp; Staff roles</div>
        </div>

        <div className="p-5 rounded-2xl bg-card border border-amber-500/25 shadow-2xs">
          <div className="flex items-center justify-between text-muted-foreground mb-2">
            <span className="text-xs font-bold uppercase tracking-wider">Logged In (24h)</span>
            <Flame className="h-4 w-4 text-amber-500" />
          </div>
          <div className="text-2xl font-black text-amber-600 dark:text-amber-400">{stats.loggedInRecently}</div>
          <div className="text-xs text-muted-foreground mt-1">Recent active sessions</div>
        </div>
      </div>

      {/* Search & Filter Controls */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-card p-4 rounded-2xl border border-border/80 shadow-2xs">
        <div className="relative flex-1 max-w-md">
          <Input
            placeholder="Search users by name or email..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            icon={<Search className="h-4 w-4 text-muted-foreground" />}
            className="rounded-xl bg-background/90"
          />
        </div>

        <div className="flex items-center gap-2">
          {/* Role Filter */}
          <div className="flex items-center gap-1.5 text-xs font-semibold text-muted-foreground">
            <Filter className="h-3.5 w-3.5" />
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value)}
              className="bg-background border border-border/80 text-foreground text-xs rounded-xl px-2.5 py-2 font-medium focus:ring-1 focus:ring-primary cursor-pointer"
            >
              <option value="ALL">All Roles</option>
              <option value="SUPER_ADMIN">Super Admin</option>
              <option value="ADMIN">Admin</option>
              <option value="USER">User / Candidate</option>
            </select>
          </div>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-background border border-border/80 text-foreground text-xs rounded-xl px-2.5 py-2 font-medium focus:ring-1 focus:ring-primary cursor-pointer"
          >
            <option value="ALL">All Status</option>
            <option value="ACTIVE">Active Only</option>
            <option value="SUSPENDED">Suspended Only</option>
          </select>
        </div>
      </div>

      {/* Users Telemetry & CRUD Table */}
      <div className="bg-card rounded-2xl border border-border/80 shadow-elevation-1 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs sm:text-sm">
            <thead>
              <tr className="border-b border-border/60 bg-muted/30 text-muted-foreground font-mono text-[11px] uppercase tracking-wider">
                <th className="py-3.5 px-4 font-bold">User / Profile</th>
                <th className="py-3.5 px-4 font-bold">Role</th>
                <th className="py-3.5 px-4 font-bold">Account Status</th>
                <th className="py-3.5 px-4 font-bold">
                  <div className="flex items-center gap-1">
                    <Clock className="h-3.5 w-3.5 text-amber-500" />
                    Last Login Details
                  </div>
                </th>
                <th className="py-3.5 px-4 font-bold">Progress</th>
                <th className="py-3.5 px-4 font-bold">Joined</th>
                <th className="py-3.5 px-4 font-bold text-right">Actions (CRUD)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/60">
              {loading ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-muted-foreground">
                    <div className="inline-flex items-center gap-2 font-semibold">
                      <RefreshCw className="h-5 w-5 animate-spin text-rose-500" />
                      Loading user records and telemetry...
                    </div>
                  </td>
                </tr>
              ) : filteredUsers.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-muted-foreground">
                    <Users className="h-8 w-8 mx-auto mb-2 opacity-40" />
                    <p className="font-bold text-foreground">No users found</p>
                    <p className="text-xs">Try adjusting your search or filters.</p>
                  </td>
                </tr>
              ) : (
                filteredUsers.map((u) => {
                  const loginInfo = formatDate(u.last_login_at);
                  const isCurrentAdmin = currentUser?.id === u.id;

                  return (
                    <tr
                      key={u.id}
                      className="hover:bg-rose-500/[0.02] dark:hover:bg-rose-500/[0.04] transition-colors"
                    >
                      {/* User Column */}
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-3">
                          <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-rose-500 via-pink-500 to-amber-500 flex items-center justify-center text-white font-extrabold text-sm uppercase shadow-xs shrink-0">
                            {u.full_name ? u.full_name[0] : u.email[0]}
                          </div>
                          <div className="min-w-0">
                            <div className="font-bold text-foreground truncate flex items-center gap-1.5">
                              <span>{u.full_name || "Candidate"}</span>
                              {isCurrentAdmin && (
                                <span className="text-[10px] bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300 px-1.5 py-0.2 rounded font-mono font-bold">
                                  You
                                </span>
                              )}
                            </div>
                            <div className="text-xs text-muted-foreground font-mono truncate">{u.email}</div>
                          </div>
                        </div>
                      </td>

                      {/* Role Column */}
                      <td className="py-3.5 px-4">
                        <div className="flex flex-wrap gap-1">
                          {u.roles.map((r) => (
                            <span
                              key={r}
                              className={`text-[10px] font-mono font-extrabold px-2 py-0.5 rounded-md border ${
                                r === "SUPER_ADMIN"
                                  ? "bg-purple-100 dark:bg-purple-950/80 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800"
                                  : r === "ADMIN"
                                  ? "bg-rose-100 dark:bg-rose-950/80 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-800"
                                  : "bg-muted text-muted-foreground border-border/80"
                              }`}
                            >
                              {r}
                            </span>
                          ))}
                        </div>
                      </td>

                      {/* Status Column */}
                      <td className="py-3.5 px-4">
                        <button
                          onClick={() => handleToggleStatus(u)}
                          disabled={isCurrentAdmin}
                          title={isCurrentAdmin ? "Cannot deactivate yourself" : "Click to toggle status"}
                          className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold transition-transform hover:scale-105 cursor-pointer ${
                            u.is_active
                              ? "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/30"
                              : "bg-destructive/10 text-destructive border border-destructive/30"
                          } ${isCurrentAdmin ? "opacity-70 cursor-not-allowed hover:scale-100" : ""}`}
                        >
                          <span
                            className={`h-2 w-2 rounded-full ${
                              u.is_active ? "bg-emerald-500 animate-pulse" : "bg-destructive"
                            }`}
                          />
                          <span>{u.is_active ? "Active" : "Suspended"}</span>
                        </button>
                      </td>

                      {/* Last Login Telemetry Column */}
                      <td className="py-3.5 px-4">
                        <div>
                          <div className="font-semibold text-foreground flex items-center gap-1.5">
                            <span className={loginInfo.isRecent ? "text-emerald-600 dark:text-emerald-400 font-bold" : ""}>
                              {loginInfo.display}
                            </span>
                            {loginInfo.relative && (
                              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-muted text-muted-foreground">
                                {loginInfo.relative}
                              </span>
                            )}
                          </div>
                          <div className="text-[11px] text-muted-foreground font-mono">
                            {u.last_login_at ? "Session Authenticated" : "No recorded logins"}
                          </div>
                        </div>
                      </td>

                      {/* XP / Gamification Progress */}
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-2 text-xs font-semibold">
                          <span className="inline-flex items-center gap-1 text-rose-600 dark:text-rose-400">
                            <Zap className="h-3.5 w-3.5 fill-rose-500" />
                            {u.xp} XP
                          </span>
                          <span className="text-muted-foreground">•</span>
                          <span className="inline-flex items-center gap-1 text-amber-600 dark:text-amber-400">
                            <Flame className="h-3.5 w-3.5 fill-amber-500" />
                            {u.streak_days}d
                          </span>
                        </div>
                      </td>

                      {/* Joined Date */}
                      <td className="py-3.5 px-4 text-xs text-muted-foreground font-mono">
                        {u.created_at ? new Date(u.created_at).toLocaleDateString() : "N/A"}
                      </td>

                      {/* CRUD Actions */}
                      <td className="py-3.5 px-4 text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            onClick={() => openEditModal(u)}
                            className="p-1.5 rounded-lg border border-border/80 hover:bg-muted text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
                            title="Edit User Details"
                          >
                            <Edit2 className="h-3.5 w-3.5" />
                          </button>

                          <button
                            onClick={() => openDeleteModal(u)}
                            disabled={isCurrentAdmin}
                            className={`p-1.5 rounded-lg border border-destructive/20 text-destructive hover:bg-destructive/10 transition-colors cursor-pointer ${
                              isCurrentAdmin ? "opacity-30 cursor-not-allowed hover:bg-transparent" : ""
                            }`}
                            title={isCurrentAdmin ? "Cannot delete own admin account" : "Delete User"}
                          >
                            <Trash2 className="h-3.5 w-3.5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* CREATE USER MODAL */}
      {isCreateOpen && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-surface w-full max-w-md rounded-2xl border border-border/80 p-6 shadow-elevation-3 space-y-5">
            <div className="flex items-center justify-between border-b border-border/60 pb-3">
              <h3 className="text-lg font-bold text-foreground flex items-center gap-2">
                <UserPlus className="h-5 w-5 text-primary" />
                Add New Candidate / Admin
              </h3>
              <button
                onClick={() => setIsCreateOpen(false)}
                className="text-muted-foreground hover:text-foreground text-sm font-bold p-1 cursor-pointer"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateUser} className="space-y-4 text-xs sm:text-sm">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1">
                  Full Name
                </label>
                <Input
                  required
                  placeholder="e.g. Sarah Connor"
                  value={formName}
                  onChange={(e) => setFormName(e.target.value)}
                  className="rounded-xl"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1">
                  Email Address
                </label>
                <Input
                  type="email"
                  required
                  placeholder="user@example.com"
                  value={formEmail}
                  onChange={(e) => setFormEmail(e.target.value)}
                  className="rounded-xl"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1">
                  Initial Password
                </label>
                <Input
                  type="password"
                  required
                  placeholder="••••••••••••"
                  value={formPassword}
                  onChange={(e) => setFormPassword(e.target.value)}
                  className="rounded-xl"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1">
                    System Role
                  </label>
                  <select
                    value={formRole}
                    onChange={(e) => setFormRole(e.target.value)}
                    className="w-full bg-background border border-border/80 text-foreground rounded-xl p-2.5 font-medium"
                  >
                    <option value="USER">User / Candidate</option>
                    <option value="ADMIN">Administrator</option>
                    <option value="SUPER_ADMIN">Super Admin</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1">
                    Initial Status
                  </label>
                  <div className="flex items-center h-10 gap-2">
                    <label className="flex items-center gap-2 cursor-pointer font-semibold">
                      <input
                        type="checkbox"
                        checked={formIsActive}
                        onChange={(e) => setFormIsActive(e.target.checked)}
                        className="h-4 w-4 rounded text-primary focus:ring-primary"
                      />
                      <span>Active</span>
                    </label>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-4 border-t border-border/60">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsCreateOpen(false)}
                  className="rounded-xl"
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  disabled={formLoading}
                  className="rounded-xl font-bold"
                >
                  {formLoading ? "Creating..." : "Create User"}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* EDIT USER MODAL */}
      {isEditOpen && selectedUser && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-surface w-full max-w-md rounded-2xl border border-border/80 p-6 shadow-elevation-3 space-y-5">
            <div className="flex items-center justify-between border-b border-border/60 pb-3">
              <h3 className="text-lg font-bold text-foreground flex items-center gap-2">
                <Edit2 className="h-5 w-5 text-primary" />
                Edit User Details
              </h3>
              <button
                onClick={() => setIsEditOpen(false)}
                className="text-muted-foreground hover:text-foreground text-sm font-bold p-1 cursor-pointer"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleUpdateUser} className="space-y-4 text-xs sm:text-sm">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1">
                  Full Name
                </label>
                <Input
                  required
                  value={formName}
                  onChange={(e) => setFormName(e.target.value)}
                  className="rounded-xl"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1">
                  Email Address
                </label>
                <Input
                  type="email"
                  required
                  value={formEmail}
                  onChange={(e) => setFormEmail(e.target.value)}
                  className="rounded-xl"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1">
                  Reset Password (Leave blank to keep unchanged)
                </label>
                <Input
                  type="password"
                  placeholder="New password..."
                  value={formPassword}
                  onChange={(e) => setFormPassword(e.target.value)}
                  className="rounded-xl"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1">
                    System Role
                  </label>
                  <select
                    value={formRole}
                    onChange={(e) => setFormRole(e.target.value)}
                    className="w-full bg-background border border-border/80 text-foreground rounded-xl p-2.5 font-medium"
                  >
                    <option value="USER">User / Candidate</option>
                    <option value="ADMIN">Administrator</option>
                    <option value="SUPER_ADMIN">Super Admin</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1">
                    Account Status
                  </label>
                  <div className="flex items-center h-10 gap-2">
                    <label className="flex items-center gap-2 cursor-pointer font-semibold">
                      <input
                        type="checkbox"
                        checked={formIsActive}
                        onChange={(e) => setFormIsActive(e.target.checked)}
                        disabled={currentUser?.id === selectedUser.id}
                        className="h-4 w-4 rounded text-rose-600 focus:ring-rose-500"
                      />
                      <span>Active</span>
                    </label>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-4 border-t border-border/60">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsEditOpen(false)}
                  className="rounded-xl"
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  disabled={formLoading}
                  className="rounded-xl font-bold"
                >
                  {formLoading ? "Saving Changes..." : "Save Changes"}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* DELETE CONFIRMATION MODAL */}
      {isDeleteOpen && selectedUser && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-card w-full max-w-md rounded-3xl border border-destructive/40 p-6 shadow-2xl space-y-4">
            <div className="flex items-center gap-3 text-destructive">
              <div className="h-10 w-10 rounded-2xl bg-destructive/15 flex items-center justify-center shrink-0">
                <Trash2 className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-foreground">Permanently Delete Account?</h3>
                <p className="text-xs text-muted-foreground">This action cannot be undone.</p>
              </div>
            </div>

            <div className="p-3.5 rounded-2xl bg-muted/60 border border-border/60 text-xs space-y-1">
              <p className="font-semibold text-foreground">{selectedUser.full_name || "Unnamed Candidate"}</p>
              <p className="text-muted-foreground font-mono">{selectedUser.email}</p>
              <p className="text-muted-foreground">Role: <span className="font-mono">{selectedUser.primary_role}</span></p>
            </div>

            <div className="flex items-center justify-end gap-2 pt-3 border-t border-border/60">
              <Button
                type="button"
                variant="outline"
                onClick={() => setIsDeleteOpen(false)}
                className="rounded-xl"
              >
                Cancel
              </Button>
              <Button
                type="button"
                variant="destructive"
                disabled={formLoading}
                onClick={handleDeleteUser}
                className="rounded-xl font-bold"
              >
                {formLoading ? "Deleting..." : "Confirm Delete"}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
