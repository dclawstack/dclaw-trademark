"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Shield } from "lucide-react";

const NAV_LINKS = [
  { href: "/portfolio", label: "Portfolio" },
  { href: "/search", label: "Search" },
  { href: "/watchlist", label: "Watchlist" },
  { href: "/oppositions", label: "Oppositions" },
  { href: "/billing", label: "Billing" },
];

export function AppNav() {
  const pathname = usePathname();
  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-3">
        <Link href="/" className="flex items-center gap-2">
          <Shield className="h-5 w-5" style={{ color: "#6366F1" }} />
          <span className="text-sm font-bold" style={{ color: "#6366F1" }}>
            DClaw Trademark
          </span>
        </Link>
        <nav className="flex items-center gap-1 text-xs font-medium">
          {NAV_LINKS.map((l) => {
            const active =
              pathname === l.href || pathname.startsWith(l.href + "/");
            return (
              <Link
                key={l.href}
                href={l.href}
                className={
                  active
                    ? "rounded-md bg-indigo-100 px-2.5 py-1 text-indigo-700"
                    : "rounded-md px-2.5 py-1 text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }
              >
                {l.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
