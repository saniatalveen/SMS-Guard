import { ShieldAlert, ShieldCheck, Link2, Clock, KeyRound, IndianRupee } from "lucide-react";
import type { Prediction } from "@/lib/api";
const ICON: Record<string, any> = { link: Link2, urgency: Clock, sensitive_info: KeyRound, money: IndianRupee };
export default function ResultCard({ message, result }: { message: string; result: Prediction }) {
  const scam = result.label === "scam";
  const Icon = scam ? ShieldAlert : ShieldCheck;
  return (
    <section aria-live="polite" className="card space-y-4">
      <div className={`flex items-center gap-3 rounded-md border p-4 ${scam ? "border-red-200 bg-red-50 text-red-800" : "border-emerald-200 bg-emerald-50 text-emerald-800"}`}>
        <Icon className="h-7 w-7" aria-hidden />
        <div><p className="text-lg font-semibold">{result.display_label}</p>
          <p className="text-sm">Model score {(result.scam_score * 100).toFixed(0)}%. {result.score_note}</p></div>
      </div>
      <blockquote className="rounded-md bg-slate-100 p-3 text-sm text-slate-700 break-words">{message}</blockquote>
      {result.indicators.length > 0 && (<div><h3 className="mb-2 text-sm font-semibold text-navy-900">Things worth noticing</h3>
        <ul className="space-y-2">{result.indicators.map(i => { const I = ICON[i.type] ?? Link2;
          return <li key={i.type} className="flex gap-2 text-sm"><I className="mt-0.5 h-4 w-4 shrink-0 text-amber-600" aria-hidden />{i.detail}</li>; })}</ul>
        <p className="mt-1 text-xs text-slate-500">These are simple keyword hints, separate from the model prediction.</p></div>)}
      <div><h3 className="mb-2 text-sm font-semibold text-navy-900">What to do</h3>
        <ul className="list-disc space-y-1 pl-5 text-sm">{result.guidance.map(g => <li key={g}>{g}</li>)}</ul></div>
      <p className="border-t pt-3 text-xs text-slate-500">{result.disclaimer} Model v{result.model_version}.</p>
    </section>);
}
