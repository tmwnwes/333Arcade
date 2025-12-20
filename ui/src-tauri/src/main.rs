// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

#[tauri::command]
fn py_call(args: Vec<String>) -> Result<String, String> {
    use std::path::PathBuf;
    use std::process::Command;

    let src_tauri_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));

    let repo_root = src_tauri_dir
        .parent()
        .and_then(|p| p.parent())
        .ok_or("Failed to compute repo root")?
        .to_path_buf();

    let output = Command::new("python")
        .args(["-m", "client.api"])
        .args(args)
        .current_dir(&repo_root)
        .env("PYTHONPATH", &repo_root)
        .output()
        .map_err(|e| format!("Failed to start python: {e}"))?;

    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).to_string());
    }

    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}


fn main() {
  tauri::Builder::default()
    .plugin(tauri_plugin_dialog::init())
    .invoke_handler(tauri::generate_handler![py_call])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}


