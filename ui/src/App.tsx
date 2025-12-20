import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-dialog";

type ApiOk<T> = { ok: true; data: T };
type ApiErr = { ok: false; error: string };
type ApiResp<T> = ApiOk<T> | ApiErr;

type Program = {
  dbId: number;
  idNum: number;
  name: string;
  version: string | null;
  fullExePath: string;
  launchVersion: string | null;
};

async function pyCall(args: string[]) {
  const raw = (await invoke<string>("py_call", { args })).trim();
  return JSON.parse(raw);
}

export default function App() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [status, setStatus] = useState("");

  const [manualName, setManualName] = useState("");
  const [manualPath, setManualPath] = useState("");
  const [manualLaunchVersion, setManualLaunchVersion] = useState("");

  /* ---------------- API actions ---------------- */

  async function refresh() {
    const resp: ApiResp<Program[]> = await pyCall(["list"]);
    if (!resp.ok) return setStatus(resp.error);
    setPrograms(resp.data);
  }

  async function scan() {
    setStatus("Scanning...");
    const resp: ApiResp<{ added: number; skipped: number }> =
      await pyCall(["scan"]);
    if (!resp.ok) return setStatus(resp.error);

    setStatus(
      `Scan complete: added ${resp.data.added}, skipped ${resp.data.skipped}`
    );
    await refresh();
  }

  async function launch(dbId: number) {
    setStatus(`Launching ${dbId}...`);
    const resp: ApiResp<{ launched: number }> =
      await pyCall(["launch", String(dbId)]);
    if (!resp.ok) return setStatus(resp.error);
    setStatus(`Launched ${dbId}`);
  }

  async function addManual() {
    if (!manualName || !manualPath) {
      setStatus("Name and path are required");
      return;
    }

    setStatus("Adding manual program...");

    const args = ["add_manual", manualName, manualPath];
    if (manualLaunchVersion.trim() !== "") {
      args.push(manualLaunchVersion.trim());
    }

    const resp: ApiResp<{ added: boolean; dbId: number }> =
      await pyCall(args);

    if (!resp.ok) return setStatus(resp.error);

    setStatus(`Added program (dbId ${resp.data.dbId})`);
    setManualName("");
    setManualPath("");
    setManualLaunchVersion("");
    await refresh();
  }

  /* ---------------- File picker ---------------- */

  async function browseForExecutable() {
    try {
      setStatus("Opening file picker...");
      const result = await open({
        multiple: false,
        directory: false,
        title: "Select Program",
      });

      console.log("Dialog result:", result);

      if (typeof result === "string") {
        setManualPath(result);
        setStatus("Selected file.");
      } else if (result === null) {
        setStatus("Picker cancelled.");
      } else {
        setStatus("Multiple selection not supported here.");
      }
    } catch (e) {
      console.error("Dialog failed:", e);
      setStatus(`Dialog failed: ${String(e)}`);
    }
  }


  /* ---------------- Lifecycle ---------------- */

  useEffect(() => {
    refresh().catch((e) => setStatus(String(e)));
  }, []);

  /* ---------------- UI ---------------- */

  return (
    <div style={{ padding: 16, fontFamily: "sans-serif" }}>
      <h1>333Arcade</h1>

      {/* Controls */}
      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <button onClick={scan}>Scan</button>
        <button onClick={refresh}>Refresh</button>
      </div>

      <div style={{ marginBottom: 12 }}>{status}</div>

      {/* Manual add */}
      <h2>Add Manual Program</h2>

      <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
        <input
          placeholder="Program name"
          value={manualName}
          onChange={(e) => setManualName(e.target.value)}
          style={{ width: 200 }}
        />

        <input
          placeholder="Executable path"
          value={manualPath}
          onChange={(e) => setManualPath(e.target.value)}
          style={{ flex: 1 }}
        />

        <button onClick={browseForExecutable}>Browse</button>
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <input
          placeholder='launchVersion (optional, e.g. "python3.11", "java")'
          value={manualLaunchVersion}
          onChange={(e) => setManualLaunchVersion(e.target.value)}
          style={{ flex: 1 }}
        />

        <button onClick={addManual}>Add</button>
      </div>

      {/* Program list */}
      <table
        cellPadding={8}
        style={{ borderCollapse: "collapse", width: "100%" }}
      >
        <thead>
          <tr>
            <th align="left">dbId</th>
            <th align="left">Name</th>
            <th align="left">Version</th>
            <th align="left">Launch</th>
          </tr>
        </thead>

        <tbody>
          {programs.map((p) => (
            <tr key={p.dbId} style={{ borderTop: "1px solid #ddd" }}>
              <td>{p.dbId}</td>
              <td>{p.name}</td>
              <td>{p.version ?? ""}</td>
              <td>
                <button onClick={() => launch(p.dbId)}>Launch</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
