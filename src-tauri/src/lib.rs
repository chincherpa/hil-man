mod db;
mod event_log;
mod settings;

use std::path::PathBuf;
use std::process::Command;
use std::sync::Mutex;

use db::AppDb;
use tauri::{Manager, WindowEvent};

#[tauri::command]
async fn get_user() -> Result<String, String> {
    tauri::async_runtime::spawn_blocking(|| {
        let script = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("..")
            .join("PythonScript")
            .join("wait_10sec_return_username.py");

        let output = Command::new("python")
            .arg(&script)
            .output()
            .map_err(|e| e.to_string())?;

        if output.status.success() {
            let output_str = String::from_utf8_lossy(&output.stdout);
            let lines: Vec<&str> = output_str.trim().lines().collect();
            if lines.len() >= 2 {
                Ok(lines[1].to_string())
            } else {
                Err("Invalid output from script".to_string())
            }
        } else {
            Err(String::from_utf8_lossy(&output.stderr).trim().to_string())
        }
    })
    .await
    .map_err(|e| e.to_string())?
}

#[tauri::command]
async fn stop_realtime_application() -> Result<String, String> {
    run_python_script("stop_realtime_application.py").await
}

/// Startet ein Skript aus `python/` und liefert stdout bzw. stderr als Fehler.
async fn run_python_script(name: &'static str) -> Result<String, String> {
    tauri::async_runtime::spawn_blocking(move || {
        let script = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("..")
            .join("python")
            .join(name);

        let output = Command::new("python")
            .arg(&script)
            // Umlaute in Meldungen unabhängig von der Konsolen-Codepage
            .env("PYTHONIOENCODING", "utf-8")
            .output()
            .map_err(|e| e.to_string())?;

        if output.status.success() {
            Ok(String::from_utf8_lossy(&output.stdout).trim().to_string())
        } else {
            Err(String::from_utf8_lossy(&output.stderr).trim().to_string())
        }
    })
    .await
    .map_err(|e| e.to_string())?
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .on_window_event(|window, event| {
            // Flyout hängt an Main, beim Schließen von Main mit beenden
            if let WindowEvent::CloseRequested { .. } = event {
                if window.label() == "main" {
                    if let Some(flyout) = window.app_handle().get_webview_window("flyout") {
                        let _ = flyout.destroy();
                    }
                }
            }
        })
        .setup(|app| {
            let conn = db::open()?;
            app.manage(AppDb(Mutex::new(conn)));
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            get_user,
            stop_realtime_application,
            event_log::log_event,
            event_log::get_events,
            settings::get_settings,
            settings::save_settings
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
