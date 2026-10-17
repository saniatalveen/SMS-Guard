export default function Page({ title, intro, children }: { title: string; intro: string; children: React.ReactNode }) {
  return (<div className="mx-auto max-w-3xl px-4 py-12"><h1 className="text-3xl font-bold text-navy-900">{title}</h1>
    <p className="mt-3 text-lg text-slate-600">{intro}</p><div className="mt-8 space-y-4">{children}</div></div>);
}
export const Block = ({ h, children }: { h: string; children: React.ReactNode }) =>
  <div className="card"><h2 className="font-semibold text-navy-900">{h}</h2><div className="mt-2 space-y-2 text-sm leading-6">{children}</div></div>;
