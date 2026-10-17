"use client";
import Link from "next/link"; import { useState } from "react"; import { ShieldCheck, Menu, X } from "lucide-react";
const L = [["/","Home"],["/about","About"],["/features","Features"],["/how-it-works","How It Works"],["/technology","Technology"]];
export default function Nav() {
  const [open, setOpen] = useState(false);
  return (<header className="sticky top-0 z-20 border-b border-slate-200 bg-white/95 backdrop-blur">
    <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
      <Link href="/" className="flex items-center gap-2 font-bold text-navy-900"><ShieldCheck className="h-6 w-6 text-brand" aria-hidden />SMSGuard</Link>
      <nav aria-label="Main" className="hidden items-center gap-6 text-sm md:flex">
        {L.map(([h, t]) => <Link key={h} href={h} className="text-slate-600 hover:text-navy-900">{t}</Link>)}
        <Link href="/dashboard" className="text-slate-600 hover:text-navy-900">Coordinator</Link>
        <Link href="/scanner" className="btn btn-primary">Try Scanner</Link></nav>
      <button className="md:hidden" aria-label={open ? "Close menu" : "Open menu"} aria-expanded={open} onClick={() => setOpen(!open)}>{open ? <X /> : <Menu />}</button></div>
    {open && <nav aria-label="Mobile" className="flex flex-col gap-3 border-t bg-white px-4 py-4 text-sm md:hidden">
      {[...L, ["/dashboard", "Coordinator Login"], ["/scanner", "Try Scanner"]].map(([h, t]) => <Link key={h} href={h} onClick={() => setOpen(false)}>{t}</Link>)}</nav>}
  </header>);
}
