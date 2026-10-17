import Link from "next/link"; import { ScanText, ListChecks, BarChart3, ShieldCheck } from "lucide-react";
export default function Home() {
  return (<>
  <section className="bg-navy-900 text-white"><div className="mx-auto grid max-w-6xl items-center gap-10 px-4 py-16 md:grid-cols-2">
    <div><h1 className="text-4xl font-bold leading-tight">Detect Suspicious SMS Before They Become a Threat.</h1>
      <p className="mt-4 text-lg text-slate-300">SMSGuard uses machine learning to analyze English SMS messages and help identify potential scams and phishing attempts.</p>
      <div className="mt-8 flex flex-wrap gap-3"><Link href="/scanner" className="btn btn-primary">Scan a Message</Link>
        <Link href="/about" className="btn border border-white/30 text-white hover:bg-white/10">Explore the Project</Link></div></div>
    <div className="rounded-lg bg-white p-5 text-slate-800 shadow-lg" aria-hidden>
      <p className="text-xs font-semibold text-slate-500">Scanner preview</p>
      <p className="mt-2 rounded-md bg-slate-100 p-3 text-sm">Your Northstar Bank account will be blocked today. Update your details: http://example.com/verify</p>
      <p className="mt-3 flex items-center gap-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm font-semibold text-red-800"><ShieldCheck className="h-4 w-4" />Potential Scam</p></div></div></section>
  <section className="mx-auto max-w-6xl px-4 py-14"><h2 className="text-2xl font-bold text-navy-900">The problem</h2>
    <p className="mt-3 max-w-3xl text-slate-600">Scam texts about bank accounts, KYC, UPI refunds, parcels and jobs pressure people into clicking links or sharing OTPs. They are hard to tell apart from genuine alerts, which look similar.</p>
    <div className="mt-8 grid gap-4 md:grid-cols-3">{[[ScanText,"Classify a message","Paste or pick an English SMS and get a prediction from the trained model."],[ListChecks,"See what stands out","Links, urgency, requests for PINs or OTPs and payments are pointed out as hints."],[BarChart3,"Review the evidence","The coordinator dashboard shows the dataset and the evaluation results as measured."]].map(([I, t, d]: any) =>
      <div key={t} className="card"><I className="h-6 w-6 text-brand" aria-hidden /><h3 className="mt-3 font-semibold text-navy-900">{t}</h3><p className="mt-1 text-sm text-slate-600">{d}</p></div>)}</div>
    <h2 className="mt-14 text-2xl font-bold text-navy-900">Three steps</h2>
    <ol className="mt-4 grid gap-4 md:grid-cols-3">{["Paste or choose a message","The model analyzes the text","Read the result and safety guidance"].map((s, i) => <li key={s} className="card"><span className="font-semibold text-brand">Step {i + 1}</span><p className="mt-1">{s}</p></li>)}</ol>
    <h2 className="mt-14 text-2xl font-bold text-navy-900">The machine-learning approach</h2>
    <p className="mt-3 max-w-3xl text-slate-600">Text is turned into TF-IDF features and classified by a scikit-learn model chosen from Naive Bayes, Logistic Regression and Linear SVM. The current model is trained on synthetic data, so results are a prototype demonstration.</p></section></>);
}
