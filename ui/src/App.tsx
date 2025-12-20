import { useEffect, useMemo, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-dialog";
import { getCurrentWindow } from "@tauri-apps/api/window";
import Dither from "./components/Dither";

type ApiOk<T> = {
  ok: true;
  data: T;
  error: null;
  meta: { apiVersion: number; tookMs?: number };
};

type ApiErr = {
  ok: false;
  data: null;
  error: { code: string; message: string };
  meta: { apiVersion: number; tookMs?: number };
};

type ApiResp<T> = ApiOk<T> | ApiErr;

type Program = {
  dbId: number;
  idNum: string; // "123" or "M..." or "S..."
  name: string;
  version: string | null;
  fullExePath: string;
  launchVersion: string | null;
};

async function pyCall(args: string[]) {
  const raw = (await invoke<string>("py_call", { args })).trim();
  try {
    return JSON.parse(raw);
  } catch {
    throw new Error(`Backend returned invalid JSON:\n${raw}`);
  }
}

function programKind(p: Program): "official" | "steam" | "manual" {
  const id = String(p.idNum);
  if (id.startsWith("S")) return "steam";
  if (id.startsWith("M")) return "manual";
  return "official";
}

function kindLabel(kind: ReturnType<typeof programKind>) {
  if (kind === "steam") return "Steam";
  if (kind === "manual") return "Manual";
  return "Official";
}

function DitherBackground() {
  return (
    <div style={styles.bgWrap}>
      <div style={styles.bgGradient} />

      <div style={styles.bgDither}>
        <Dither
          waveColor={[0.4, 0.4, 0.45]}
          disableAnimation={false}
          enableMouseInteraction={true}
          mouseRadius={0.35}
          colorNum={4}
          waveAmplitude={0.3}
          waveFrequency={3}
          waveSpeed={0.05}
        />
      </div>

      <div style={styles.bgVignette} />
    </div>
  );
}

export default function App() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [status, setStatus] = useState<string>("");

  const [showAdd, setShowAdd] = useState(false);
  const [manualName, setManualName] = useState("");
  const [manualPath, setManualPath] = useState("");
  const [manualLaunchVersion, setManualLaunchVersion] = useState("");

  const official = useMemo(() => {
    return [...programs]
      .filter((p) => programKind(p) === "official")
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [programs]);

  const steam = useMemo(() => {
    return [...programs]
      .filter((p) => programKind(p) === "steam")
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [programs]);

  const manual = useMemo(() => {
    return [...programs]
      .filter((p) => programKind(p) === "manual")
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [programs]);

  async function refresh(opts?: { silent?: boolean }) {
    const resp: ApiResp<Program[]> = await pyCall(["list"]);
    if (!resp.ok) {
      if (!opts?.silent) setStatus(resp.error.message);
      return;
    }
    setPrograms(resp.data);
    if (!opts?.silent) {
      setStatus(
        `Loaded ${resp.data.length} programs${
          resp.meta?.tookMs != null ? ` (${resp.meta.tookMs}ms)` : ""
        }`
      );
    }
  }

  async function scan() {
    try {
      setStatus("Scanning metadata...");
      const resp: ApiResp<{ added: number; skipped: number }> = await pyCall(["scan"]);
      if (!resp.ok) return setStatus(resp.error.message);

      setStatus(
        `Scan complete: added ${resp.data.added}, skipped ${resp.data.skipped}${
          resp.meta?.tookMs != null ? ` (${resp.meta.tookMs}ms)` : ""
        }`
      );
      await refresh({ silent: true });
    } catch (e) {
      setStatus(String(e));
    }
  }

  async function steamScan() {
    try {
      setStatus("Importing Steam games...");
      const resp: ApiResp<{ added: number; skipped: number }> = await pyCall(["steam_scan"]);
      if (!resp.ok) return setStatus(resp.error.message);

      setStatus(
        `Steam import: added ${resp.data.added}, skipped ${resp.data.skipped}${
          resp.meta?.tookMs != null ? ` (${resp.meta.tookMs}ms)` : ""
        }`
      );
      await refresh({ silent: true });
    } catch (e) {
      setStatus(String(e));
    }
  }

  async function launch(dbId: number) {
    try {
      setStatus(`Launching #${dbId}...`);
      const resp: ApiResp<{ launched: number }> = await pyCall(["launch", String(dbId)]);
      if (!resp.ok) return setStatus(resp.error.message);
      setStatus(
        `Launched #${dbId}${resp.meta?.tookMs != null ? ` (${resp.meta.tookMs}ms)` : ""}`
      );
    } catch (e) {
      setStatus(String(e));
    }
  }

  async function removeExternal(dbId: number) {
    try {
      setStatus(`Removing #${dbId}...`);
      const resp: ApiResp<{ deleted: number }> = await pyCall(["delete_external", String(dbId)]);
      if (!resp.ok) return setStatus(resp.error.message);
      setStatus(`Removed #${dbId}`);
      await refresh({ silent: true });
    } catch (e) {
      setStatus(String(e));
    }
  }

  async function browseForExecutable() {
    try {
      const result = await open({
        multiple: false,
        directory: false,
        title: "Select Program",
      });

      if (typeof result === "string") setManualPath(result);
    } catch (e) {
      setStatus(`Dialog failed: ${String(e)}`);
    }
  }

  async function addManual() {
    try {
      if (!manualName.trim() || !manualPath.trim()) {
        setStatus("Name and path are required.");
        return;
      }

      setStatus("Adding manual program...");
      const args = ["add_manual", manualName.trim(), manualPath.trim()];
      if (manualLaunchVersion.trim() !== "") args.push(manualLaunchVersion.trim());

      const resp: ApiResp<{ added: boolean; dbId: number }> = await pyCall(args);
      if (!resp.ok) return setStatus(resp.error.message);

      setStatus(`Added manual program (dbId ${resp.data.dbId})`);
      setManualName("");
      setManualPath("");
      setManualLaunchVersion("");
      setShowAdd(false);

      await refresh({ silent: true });
    } catch (e) {
      setStatus(String(e));
    }
  }

  async function closeApp() {
    await getCurrentWindow().close();
  }

  useEffect(() => {
    refresh().catch((e) => setStatus(String(e)));
  }, []);

  function Section({
    title,
    subtitle,
    rows,
    removable,
  }: {
    title: string;
    subtitle?: string;
    rows: Program[];
    removable: boolean;
  }) {
    return (
      <div style={styles.section}>
        <div style={styles.sectionHeader}>
          <div>
            <h2 style={styles.h2}>{title}</h2>
            {subtitle ? <div style={styles.muted}>{subtitle}</div> : null}
          </div>
          <div style={styles.countPill}>{rows.length}</div>
        </div>

        <div style={styles.grid}>
          {rows.map((p) => (
            <div key={p.dbId} style={styles.card} title={p.fullExePath}>
              <div style={styles.cardTop}>
                <div style={styles.badge(programKind(p))}>{kindLabel(programKind(p))}</div>
                <div style={styles.smallMono}>#{p.dbId}</div>
              </div>

              <div style={styles.cardTitle}>{p.name}</div>

              <div style={styles.cardMeta}>
                <div style={styles.metaRow}>
                  <span style={styles.metaKey}>Version</span>
                  <span style={styles.metaVal}>{p.version ?? "—"}</span>
                </div>
                <div style={styles.metaRow}>
                  <span style={styles.metaKey}>Launch</span>
                  <span style={styles.metaVal}>{p.launchVersion ?? "default"}</span>
                </div>
              </div>

              <div style={styles.cardActions}>
                <button style={styles.primaryBtn} onClick={() => launch(p.dbId)}>
                  Launch
                </button>
                {removable ? (
                  <button style={styles.secondaryBtn} onClick={() => removeExternal(p.dbId)}>
                    Remove
                  </button>
                ) : (
                  <div style={{ width: 82 }} />
                )}
              </div>
            </div>
          ))}

          {rows.length === 0 ? (
            <div style={{ ...styles.card, ...styles.emptyCard }}>
              <div style={styles.muted}>No entries.</div>
            </div>
          ) : null}
        </div>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      <DitherBackground />

      <div style={styles.chrome}>
        <div style={styles.header}>
          <div>
            <div style={styles.title}>333Arcade</div>
            <div style={styles.subtitle}>Local launcher • Python backend • Tauri + React UI</div>
          </div>

          <div style={styles.headerRight}>
            <div style={styles.headerActions}>
              <button style={styles.secondaryBtn} onClick={scan}>
                Scan metadata
              </button>
              <button style={styles.secondaryBtn} onClick={steamScan}>
                Import Steam
              </button>
              <button style={styles.secondaryBtn} onClick={() => refresh()}>
                Refresh
              </button>
              <button style={styles.secondaryBtn} onClick={() => setShowAdd(true)}>
                Add Program
              </button>
            </div>

            <button style={styles.exitBtn} onClick={closeApp} title="Exit">
              ✕
            </button>
          </div>
        </div>

        <div style={styles.statusBar}>
          <div style={styles.statusDot} />
          <div style={styles.statusText}>{status || "Ready."}</div>
        </div>

        <Section title="Official Programs" rows={official} removable={false} />
        <Section title="Steam Games" rows={steam} removable={true} />
        <Section title="Manual Entries" rows={manual} removable={true} />

        {showAdd ? (
          <div style={styles.modalOverlay} onClick={() => setShowAdd(false)}>
            <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
              <div style={styles.modalHeader}>
                <div>
                  <h2 style={styles.h2}>Add manual program</h2>
                  <div style={styles.muted}>Pick any executable/script/shortcut you want.</div>
                </div>
                <button style={styles.secondaryBtn} onClick={() => setShowAdd(false)}>
                  Close
                </button>
              </div>

              <div style={styles.modalRow}>
                <input
                  style={styles.input}
                  placeholder="Display name"
                  value={manualName}
                  onChange={(e) => setManualName(e.target.value)}
                />
              </div>

              <div style={styles.modalRow}>
                <input
                  style={{ ...styles.input, flex: 1 }}
                  placeholder="Executable path"
                  value={manualPath}
                  onChange={(e) => setManualPath(e.target.value)}
                />
                <button style={styles.secondaryBtn} onClick={browseForExecutable}>
                  Browse
                </button>
              </div>

              <div style={styles.modalRow}>
                <input
                  style={{ ...styles.input, flex: 1 }}
                  placeholder='launchVersion (optional) e.g. "python3.11" or "java"'
                  value={manualLaunchVersion}
                  onChange={(e) => setManualLaunchVersion(e.target.value)}
                />
              </div>

              <div style={styles.modalFooter}>
                <button
                  style={styles.primaryBtn}
                  onClick={addManual}
                  disabled={!manualName.trim() || !manualPath.trim()}
                >
                  Add
                </button>
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}

const styles: any = {
  page: {
    position: "relative",
    minHeight: "100vh",
    color: "#eaeaf0",
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
    overflow: "hidden",
    background: "#0b0b12",

    // IMPORTANT: prevents background canvas / webview layers doing weird stacking
    isolation: "isolate",
  },

  // IMPORTANT: explicitly above the background
  chrome: { position: "relative", zIndex: 1, padding: 18 },

  // Background layer: fixed, behind the whole app UI
  bgWrap: {
    position: "fixed",
    inset: 0,
    pointerEvents: "none",
    zIndex: 0,
  },
  bgGradient: {
    position: "absolute",
    inset: 0,
    background:
      "radial-gradient(1200px 600px at 15% 0%, rgba(70,72,170,0.50) 0%, rgba(20,20,34,0.65) 55%, rgba(10,10,18,0.85) 100%)",
  },

  // A wrapper so you can control the canvas stacking inside bgWrap
  bgDither: {
    position: "absolute",
    inset: 0,
  },

  bgVignette: {
    position: "absolute",
    inset: 0,
    background:
      "radial-gradient(1200px 700px at 50% 25%, rgba(0,0,0,0.00) 0%, rgba(0,0,0,0.40) 65%, rgba(0,0,0,0.75) 100%)",
  },

  header: {
    display: "flex",
    alignItems: "flex-end",
    justifyContent: "space-between",
    gap: 12,
    marginBottom: 14,
  },
  headerRight: {
    display: "flex",
    alignItems: "center",
    gap: 10,
  },
  headerActions: {
    display: "flex",
    gap: 8,
    flexWrap: "wrap",
  },
  title: { fontSize: 30, fontWeight: 800, letterSpacing: 0.2 },
  subtitle: { opacity: 0.75, fontSize: 13, marginTop: 4 },

  exitBtn: {
    width: 36,
    height: 36,
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.16)",
    background: "rgba(0,0,0,0.20)",
    color: "#eaeaf0",
    cursor: "pointer",
    fontWeight: 800,
    lineHeight: "36px",
    textAlign: "center",
  },

  statusBar: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "10px 12px",
    borderRadius: 12,

    background: "rgba(10, 10, 18, 0.75)",
    border: "1px solid rgba(255,255,255,0.16)",
    backdropFilter: "blur(14px)",
    WebkitBackdropFilter: "blur(14px)",

    marginBottom: 14,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 999,
    background: "#7ee787",
    boxShadow: "0 0 14px rgba(126,231,135,0.45)",
  },
  statusText: {
    fontSize: 13,
    opacity: 0.95,
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
    textShadow: "0 2px 10px rgba(0,0,0,0.65)",
  },

  section: { marginTop: 18 },
  sectionHeader: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 10,
  },
  h2: { margin: 0, fontSize: 16, fontWeight: 750 },
  muted: { opacity: 0.7, fontSize: 12, marginTop: 4 },
  countPill: {
    padding: "4px 10px",
    borderRadius: 999,
    border: "1px solid rgba(255,255,255,0.14)",
    background: "rgba(0,0,0,0.22)",
    fontSize: 12,
    opacity: 0.9,
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
    gap: 12,
  },
  card: {
    borderRadius: 16,
    padding: 12,

    background: "rgba(10, 10, 18, 0.78)",
    border: "1px solid rgba(255,255,255,0.16)",
    boxShadow: "0 10px 34px rgba(0,0,0,0.45)",

    backdropFilter: "blur(14px)",
    WebkitBackdropFilter: "blur(14px)",
  },
  emptyCard: { display: "flex", alignItems: "center", justifyContent: "center", minHeight: 120 },

  cardTop: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8 },
  smallMono: {
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
    opacity: 0.65,
    fontSize: 11,
  },
  badge: (kind: "official" | "steam" | "manual") => {
    const base = {
      fontSize: 11,
      padding: "4px 8px",
      borderRadius: 999,
      border: "1px solid rgba(255,255,255,0.14)",
      background: "rgba(0,0,0,0.22)",
      opacity: 0.95,
    } as any;
    if (kind === "steam") return { ...base, background: "rgba(76, 175, 255, 0.14)" };
    if (kind === "manual") return { ...base, background: "rgba(255, 193, 7, 0.14)" };
    return { ...base, background: "rgba(126, 231, 135, 0.12)" };
  },

  cardTitle: {
    fontWeight: 800,
    fontSize: 15,
    lineHeight: 1.2,
    marginBottom: 8,
    wordBreak: "break-word",
    textShadow: "0 2px 10px rgba(0,0,0,0.65)",
  },
  cardMeta: { marginTop: 4, borderTop: "1px solid rgba(255,255,255,0.10)", paddingTop: 10, opacity: 0.9 },
  metaRow: { display: "flex", justifyContent: "space-between", fontSize: 12, marginTop: 6 },
  metaKey: { opacity: 0.7 },
  metaVal: {
    opacity: 0.98,
    marginLeft: 8,
    textAlign: "right" as const,
    textShadow: "0 2px 10px rgba(0,0,0,0.55)",
  },
  cardActions: { display: "flex", gap: 8, marginTop: 12, alignItems: "center", justifyContent: "space-between" },

  primaryBtn: {
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.18)",
    background: "rgba(126,231,135,0.16)",
    color: "#eaeaf0",
    padding: "9px 12px",
    cursor: "pointer",
    fontWeight: 700,
    flex: 1,
  },
  secondaryBtn: {
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.14)",
    background: "rgba(0,0,0,0.18)",
    color: "#eaeaf0",
    padding: "9px 12px",
    cursor: "pointer",
    fontWeight: 650,
  },

  modalOverlay: {
    position: "fixed",
    inset: 0,
    background: "rgba(0,0,0,0.55)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 50,
  },
  modal: {
    width: "min(720px, 92vw)",
    borderRadius: 18,
    padding: 14,

    background: "rgba(12, 12, 20, 0.92)",
    border: "1px solid rgba(255,255,255,0.16)",
    boxShadow: "0 18px 50px rgba(0,0,0,0.65)",

    backdropFilter: "blur(18px)",
    WebkitBackdropFilter: "blur(18px)",
  },
  modalHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: 10,
    marginBottom: 12,
  },
  modalRow: { display: "flex", gap: 8, marginTop: 8, flexWrap: "wrap" },
  modalFooter: { display: "flex", justifyContent: "flex-end", marginTop: 14 },
  input: {
    background: "rgba(0,0,0,0.25)",
    border: "1px solid rgba(255,255,255,0.14)",
    color: "#eaeaf0",
    padding: "10px 10px",
    borderRadius: 12,
    outline: "none",
    minWidth: 180,
    flex: 1,
  },
};
