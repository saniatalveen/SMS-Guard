import "./globals.css"; import Nav from "@/components/Nav"; import Link from "next/link";
export const metadata = { title: "SMSGuard", description: "Machine-learning SMS scam detection prototype for English messages." };
export default function Root({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body className="flex min-h-screen flex-col"><Nav /><main className="flex-1">{children}</main>
    <footer className="border-t bg-navy-900 py-8 text-sm text-slate-300"><div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 md:flex-row md:justify-between">
      <p>SMSGuard is a decision-support prototype. It cannot detect every scam or guarantee a message is safe.</p>
      <p>Built with Next.js, FastAPI and scikit-learn. <Link className="underline" href="/scanner">Scanner</Link></p></div></footer></body></html>);
}
