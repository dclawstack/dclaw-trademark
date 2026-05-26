"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { listBillingPlans, createCheckout, type BillingPlan } from "@/lib/api";

const PLAN_HIGHLIGHTS: Record<string, string[]> = {
  starter: ["50 clearance searches/mo", "Portfolio up to 25 marks", "AI class recommendations", "Email alerts"],
  pro: ["500 searches/mo", "Unlimited portfolio marks", "AI copilot", "Watch service", "API access"],
  enterprise: ["Unlimited searches", "Multi-user seats", "Custom integrations", "SLA + dedicated support"],
};

export default function BillingPage() {
  const [plans, setPlans] = useState<BillingPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [email, setEmail] = useState("");
  const [selected, setSelected] = useState<string | null>(null);
  const [checking, setChecking] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    listBillingPlans().then(setPlans).catch(() => setPlans([])).finally(() => setLoading(false));
  }, []);

  async function handleCheckout(plan: string) {
    if (!email) { setMessage("Please enter your email."); return; }
    setSelected(plan);
    setChecking(true);
    setMessage(null);
    try {
      const resp = await createCheckout(email, plan);
      if (resp.checkout_url) window.location.href = resp.checkout_url;
    } catch {
      setMessage("Checkout failed. Please try again.");
    } finally {
      setChecking(false);
    }
  }

  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Plans &amp; Pricing</h1>
        <p className="text-gray-600">
          Protect your brand with AI-powered trademark intelligence.
        </p>
      </div>

      <div className="mb-6">
        <Label htmlFor="email">Your email</Label>
        <div className="flex gap-2 mt-1 max-w-sm">
          <Input
            id="email"
            type="email"
            placeholder="you@company.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
      </div>

      {message && (
        <div className="mb-4 rounded-md bg-yellow-50 border border-yellow-200 p-3 text-yellow-800 text-sm">
          {message}
        </div>
      )}

      {loading ? (
        <div className="text-gray-500 py-8">Loading plans…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((plan) => (
            <Card key={plan.plan} className={selected === plan.plan ? "ring-2 ring-indigo-500" : ""}>
              <CardHeader>
                <CardTitle className="text-lg">{plan.label}</CardTitle>
                <p className="text-2xl font-bold text-indigo-600">
                  ${(plan.price_usd / 100).toFixed(0)}
                  <span className="text-sm font-normal text-gray-500">/mo</span>
                </p>
              </CardHeader>
              <CardContent>
                <ul className="text-sm text-gray-600 space-y-1 mb-4">
                  {(PLAN_HIGHLIGHTS[plan.plan] ?? []).map((f) => (
                    <li key={f} className="flex items-start gap-1">
                      <span className="text-green-500 mt-0.5">✓</span>
                      {f}
                    </li>
                  ))}
                </ul>
                <Button
                  className="w-full"
                  disabled={checking && selected === plan.plan}
                  onClick={() => handleCheckout(plan.plan)}
                >
                  {checking && selected === plan.plan ? "Redirecting…" : "Get Started"}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <p className="mt-8 text-xs text-gray-400 text-center">
        Payments are processed by Stripe. Cancel anytime.
      </p>
    </div>
  );
}
