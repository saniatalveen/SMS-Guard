export const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
export type Prediction = { label: "scam" | "legitimate"; display_label: string; scam_score: number; score_note: string;
  indicators: { type: string; detail: string }[]; guidance: string[]; model_version: string; disclaimer: string };
async function req<T>(path: string, init?: RequestInit): Promise<T> {
  let r: Response;
  try { r = await fetch(API + path, { ...init, headers: { "Content-Type": "application/json" }, cache: "no-store" }); }
  catch { throw new Error("Cannot reach the SMSGuard API. Start the backend (uvicorn) and check NEXT_PUBLIC_API_URL."); }
  if (!r.ok) {
    let d = "Request failed.";
    try { const j = await r.json(); d = typeof j.detail === "string" ? j.detail : j.detail?.[0]?.msg ?? d; } catch {}
    throw new Error(d);
  }
  return r.json();
}
export const predict = (message: string) => req<Prediction>("/predict", { method: "POST", body: JSON.stringify({ message }) });
export const getHealth = () => req<{ status: string; model_ready: boolean; model_version: string | null }>("/health");
export const getInfo = () => req<Record<string, any>>("/model-info");
export const getMetrics = () => req<Record<string, any>>("/metrics");
export const getDataset = () => req<Record<string, any>>("/dataset-stats");
