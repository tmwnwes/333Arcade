import { useEffect, useMemo, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-dialog";

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
  idNum: string;
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

export default function App() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [status, setStatus] = useState<string>("");

  const [manualName, setManualName] = useState("");
  const [manualPath, setManualPath] = useState("");
  const [manualLaunchVersion, setManualLaunchVersion] = useState("");

  const official = useMemo(() => {
    return [...programs]
      .filter((p) => {
        const id = String(p.idNum);
        return !id.startsWith("M") && !id.startsWith("S");
      })
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [programs]);

  const steam = useMemo(() => {
    return [...programs]
      .filter((p) => String(p.idNum).startsWith("S"))
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [programs]);

  const manual = useMemo(() => {
    return [...programs]
      .filter((p) => String(p.idNum).startsWith("M"))
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [programs]);

  // IMPORTANT: refresh can be "silent" so scan messages don't get overwritten.
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
      setStatus("Scanning...");
      const resp: ApiResp<{ added: number; skipped: number }> = await pyCall(["scan"]);
      if (!resp.ok) return setStatus(resp.error.message);

      setStatus(
        `Scan complete: added ${resp.data.added}, skipped ${resp.data.skipped}${
          resp.meta?.tookMs != null ? ` (${resp.meta.tookMs}ms)` : ""
        }`
      );

      // Refresh list, but keep the scan status visible
      await refresh({ silent: true });
    } catch (e) {
      setStatus(String(e));
    }
  }

  async function steamScan() {
    try {
      setStatus("Scanning Steam libraries...");
      const resp: ApiResp<{ added: number; skipped: number }> = await pyCall(["steam_scan"]);
      if (!resp.ok) return setStatus(resp.error.message);

      setStatus(
        `Steam scan: added ${resp.data.added}, skipped ${resp.data.skipped}${
          resp.meta?.tookMs != null ? ` (${resp.meta.tookMs}ms)` : ""
        }`
      );

      // Refresh list, but keep the steam scan status visible
      await refresh({ silent: true });
    } catch (e) {
      setStatus(String(e));
    }
  }

  async function launch(dbId: number) {
    try {
      setStatus(`Launching ${dbId}...`);
      const resp: ApiResp<{ launched: number }> = await pyCall(["launch", String(dbId)]);
      if (!resp.ok) return setStatus(resp.error.message);
      setStatus(
        `Launched ${dbId}${resp.meta?.tookMs != null ? ` (${resp.meta.tookMs}ms)` : ""}`
      );
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

      if (typeof result === "string") {
        setManualPath(result);
      }
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

      // Silent refresh so the "Added ..." status stays visible
      await refresh({ silent: true });
    } catch (e) {
      setStatus(String(e));
    }
  }

  async function removeExternal(dbId: number) {
    try {
      setStatus(`Removing ${dbId}...`);
      const resp: ApiResp<{ deleted: number }> = await pyCall(["delete_external", String(dbId)]);
      if (!resp.ok) return setStatus(resp.error.message);

      setStatus(`Removed ${resp.data.deleted}`);
      await refresh({ silent: true });
    } catch (e) {
      setStatus(String(e));
    }
  }

  useEffect(() => {
    refresh().catch((e) => setStatus(String(e)));
  }, []);

  function ProgramTable({
    title,
    rows,
    showRemove,
  }: {
    title: string;
    rows: Program[];
    showRemove: boolean;
  }) {
    return (
      <div style={{ marginTop: 16 }}>
        <h2 style={{ marginBottom: 8 }}>{title}</h2>

        <table cellPadding={8} style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th align="left">dbId</th>
              <th align="left">idNum</th>
              <th align="left">Name</th>
              <th align="left">Version</th>
              <th align="left">Launch</th>
              {showRemove ? <th align="left">Remove</th> : null}
            </tr>
          </thead>
          <tbody>
            {rows.map((p) => (
              <tr key={p.dbId} style={{ borderTop: "1px solid #ddd" }}>
                <td>{p.dbId}</td>
                <td>{p.idNum}</td>
                <td title={p.fullExePath}>{p.name}</td>
                <td>{p.version ?? ""}</td>
                <td>
                  <button onClick={() => launch(p.dbId)}>Launch</button>
                </td>
                {showRemove ? (
                  <td>
                    <button onClick={() => removeExternal(p.dbId)}>Remove</button>
                  </td>
                ) : null}
              </tr>
            ))}
            {rows.length === 0 ? (
              <tr style={{ borderTop: "1px solid #ddd" }}>
                <td colSpan={showRemove ? 6 : 5} style={{ opacity: 0.7 }}>
                  No entries.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    );
  }

  return (
    <div style={{ padding: 16, fontFamily: "sans-serif" }}>
      <h1 style={{ marginTop: 0 }}>333Arcade</h1>

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <button onClick={scan}>Scan</button>
        <button onClick={steamScan}>Steam Scan</button>
        <button onClick={() => refresh()}>Refresh</button>
      </div>

      <div style={{ marginBottom: 12 }}>{status}</div>

      <div style={{ border: "1px solid #ddd", padding: 12, marginBottom: 12 }}>
        <h2 style={{ marginTop: 0, marginBottom: 8 }}>Add Manual Program</h2>

        <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
          <input
            style={{ width: 220 }}
            placeholder="Display name"
            value={manualName}
            onChange={(e) => setManualName(e.target.value)}
          />
          <input
            style={{ flex: 1 }}
            placeholder="Executable path (or Browse)"
            value={manualPath}
            onChange={(e) => setManualPath(e.target.value)}
          />
          <button onClick={browseForExecutable}>Browse</button>
        </div>

        <div style={{ display: "flex", gap: 8 }}>
          <input
            style={{ flex: 1 }}
            placeholder='launchVersion (optional, ex: "python3.11" or "java")'
            value={manualLaunchVersion}
            onChange={(e) => setManualLaunchVersion(e.target.value)}
          />
          <button onClick={addManual} disabled={!manualName.trim() || !manualPath.trim()}>
            Add
          </button>
        </div>
      </div>

      <ProgramTable title="Official Programs" rows={official} showRemove={false} />
      <ProgramTable title="Steam Games" rows={steam} showRemove={true} />
      <ProgramTable title="Manual Entries" rows={manual} showRemove={true} />
    </div>
  );
}
