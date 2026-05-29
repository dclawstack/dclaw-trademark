import Link from "next/link";
import {
  ArrowRight,
  Bell,
  CalendarClock,
  CreditCard,
  FileText,
  Gavel,
  Github,
  LayoutGrid,
  Search,
  Shield,
  Sparkles,
  Tags,
} from "lucide-react";
import DemoControls from "@/components/landing/DemoControls";

const NAV_LINKS = [
  { href: "/portfolio", label: "Portfolio" },
  { href: "/search", label: "Search" },
  { href: "/watchlist", label: "Watchlist" },
  { href: "/oppositions", label: "Oppositions" },
  { href: "/billing", label: "Billing" },
];

const FEATURES_CORE = [
  {
    icon: LayoutGrid,
    title: "Portfolio management",
    body:
      "Track every mark in one place — status, owner, jurisdiction, application and registration numbers, filing and expiry dates. Filter by status and drill into each mark's classes, deadlines, watchlist and oppositions.",
    href: "/portfolio",
  },
  {
    icon: Search,
    title: "Trademark clearance search",
    body:
      "Screen a proposed mark against existing registrations before you file. Phonetic and semantic similarity scoring surfaces conflicts with a risk level, similarity breakdown and the conflicting marks' classes.",
    href: "/search",
  },
  {
    icon: Bell,
    title: "Watchlist & monitoring",
    body:
      "Register confusingly-similar marks against your portfolio and track conflict type, similarity score and status — so you spot infringing applications while there's still time to oppose.",
    href: "/watchlist",
  },
  {
    icon: CalendarClock,
    title: "Deadline tracking",
    body:
      "Never miss a renewal, declaration of use or statement-of-use deadline. A background scheduler keeps deadline alerts current per mark, with due dates and status front and center.",
    href: "/portfolio",
  },
];

const FEATURES_MORE = [
  {
    icon: Gavel,
    title: "Oppositions & disputes",
    body:
      "Manage oppositions, cancellations and litigation through their lifecycle — stage, opposing party and counsel, filing date, response deadline and hearing date, all linked to the mark at issue.",
    href: "/oppositions",
  },
  {
    icon: Tags,
    title: "NICE classification",
    body:
      "Assign goods and services to the 45 NICE classes per mark, with AI-assisted class recommendations to make sure your application covers the right scope.",
    href: "/portfolio",
  },
  {
    icon: FileText,
    title: "AI application drafting & copilot",
    body:
      "Draft application descriptions and get answers from a trademark copilot available on every screen. Powered by OpenRouter with a local Ollama fallback.",
    href: "/portfolio",
  },
  {
    icon: CreditCard,
    title: "Billing & subscriptions",
    body:
      "Plan, subscription and usage management built in, so portfolio operations and billing live in the same place.",
    href: "/billing",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <TopNav />

      {/* ── Hero ─────────────────────────────────────────────────────── */}
      <section className="relative overflow-hidden">
        <div
          className="absolute inset-0 -z-10 opacity-40"
          style={{
            backgroundImage:
              "radial-gradient(circle at 20% 0%, #6366F1 0%, transparent 40%), radial-gradient(circle at 80% 20%, #818CF8 0%, transparent 35%)",
          }}
        />
        <div className="mx-auto max-w-6xl px-6 pb-20 pt-20 lg:pt-28">
          <div className="inline-flex items-center gap-2 rounded-full border border-indigo-200 bg-white/80 px-3 py-1 text-xs font-semibold text-indigo-700 shadow-sm backdrop-blur">
            <Sparkles className="h-3 w-3" /> DClaw vertical SaaS · Legal
          </div>
          <h1 className="mt-6 max-w-3xl text-5xl font-bold tracking-tight sm:text-6xl">
            Manage your entire trademark portfolio in one place.
          </h1>
          <p className="mt-5 max-w-2xl text-lg text-slate-600">
            DClaw Trademark brings clearance search, portfolio tracking,
            watchlist monitoring, deadline alerts, opposition management, NICE
            classification and AI drafting together — so you can search, file,
            monitor and defend your marks without juggling spreadsheets.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href="/portfolio"
              className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow hover:bg-indigo-700"
            >
              Open App <ArrowRight className="h-4 w-4" />
            </Link>
            <a
              href="#features"
              className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            >
              Explore features
            </a>
          </div>
        </div>
      </section>

      {/* DEMO CONTROLS — remove this block + the import to drop the demo feature */}
      <DemoControls />
      {/* END DEMO CONTROLS */}

      {/* ── Feature sections ─────────────────────────────────────────── */}
      <div id="features">
        <FeatureBlock
          eyebrow="Run your practice"
          title="Everything from clearance to renewal."
          items={FEATURES_CORE}
        />
        <FeatureBlock
          eyebrow="Defend & extend"
          title="Disputes, classification, AI and billing."
          items={FEATURES_MORE}
          background="bg-slate-50"
        />
      </div>

      {/* ── Final CTA ────────────────────────────────────────────────── */}
      <section className="mx-auto max-w-4xl px-6 py-24 text-center">
        <h2 className="text-4xl font-bold tracking-tight">Ready to dive in?</h2>
        <p className="mt-4 text-slate-600">
          Seed the demo portfolio above, then open the app — every screen reads
          from real endpoints.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          <Link
            href="/portfolio"
            className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow hover:bg-indigo-700"
          >
            Open App <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>

      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-6 py-6 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-indigo-600" />
            <span className="font-semibold text-slate-700">DClaw Trademark</span>
            <span>·</span>
            <span>part of the DClaw vertical SaaS stack</span>
          </div>
          <a
            href="https://github.com/dclawstack/dclaw-trademark"
            className="inline-flex items-center gap-1 hover:text-slate-900"
          >
            <Github className="h-3.5 w-3.5" /> dclawstack/dclaw-trademark
          </a>
        </div>
      </footer>
    </main>
  );
}

function TopNav() {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-3">
        <Link href="/" className="flex items-center gap-2">
          <Shield className="h-5 w-5 text-indigo-600" />
          <span className="text-sm font-bold text-indigo-600">
            DClaw Trademark
          </span>
        </Link>
        <nav className="hidden items-center gap-1 text-xs font-medium md:flex">
          {NAV_LINKS.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="rounded-md px-2.5 py-1 text-slate-600 hover:bg-slate-100 hover:text-slate-900"
            >
              {l.label}
            </Link>
          ))}
        </nav>
        <Link
          href="/portfolio"
          className="inline-flex items-center gap-1 rounded-md bg-indigo-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-indigo-700"
        >
          Open App <ArrowRight className="h-3 w-3" />
        </Link>
      </div>
    </header>
  );
}

function FeatureBlock({
  eyebrow,
  title,
  items,
  background = "bg-white",
}: {
  eyebrow: string;
  title: string;
  items: {
    icon: typeof Sparkles;
    title: string;
    body: string;
    href: string;
  }[];
  background?: string;
}) {
  return (
    <section className={`${background} border-t border-slate-200`}>
      <div className="mx-auto max-w-6xl px-6 py-24">
        <div className="mb-12 max-w-2xl">
          <div className="inline-flex items-center gap-1 rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-indigo-700">
            {eyebrow}
          </div>
          <h2 className="mt-3 text-3xl font-bold tracking-tight sm:text-4xl">
            {title}
          </h2>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          {items.map((f) => (
            <Link
              key={f.title}
              href={f.href}
              className="group flex flex-col rounded-2xl border border-slate-200 bg-white p-6 transition hover:-translate-y-0.5 hover:border-indigo-300 hover:shadow-lg"
            >
              <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-100">
                <f.icon className="h-5 w-5 text-indigo-600" />
              </div>
              <h3 className="text-lg font-semibold">{f.title}</h3>
              <p className="mt-2 flex-1 text-sm text-slate-600">{f.body}</p>
              <span className="mt-4 inline-flex items-center gap-1 text-xs font-semibold text-indigo-700 transition-all group-hover:gap-2">
                Explore <ArrowRight className="h-3 w-3" />
              </span>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
