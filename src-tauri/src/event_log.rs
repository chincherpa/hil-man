use rusqlite::params;
use serde::{Deserialize, Serialize};
use tauri::State;

use crate::db::AppDb;

#[derive(Deserialize)]
pub struct ClickEvent {
    pub ts: String,
    pub session: String,
    pub tag: String,
    pub path: String,
    pub label: String,
    pub context: Option<String>,
}

#[derive(Serialize)]
pub struct EventRow {
    pub id: i64,
    pub ts: String,
    pub session: String,
    pub tag: String,
    pub path: String,
    pub label: String,
    pub context: Option<String>,
}

#[tauri::command]
pub fn log_event(db: State<AppDb>, event: ClickEvent) -> Result<(), String> {
    let conn = db.0.lock().map_err(|e| e.to_string())?;
    conn.execute(
        "INSERT INTO event_log (ts, session, tag, path, label, context) VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
        params![event.ts, event.session, event.tag, event.path, event.label, event.context],
    )
    .map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
pub fn get_events(db: State<AppDb>, limit: u32) -> Result<Vec<EventRow>, String> {
    let conn = db.0.lock().map_err(|e| e.to_string())?;
    let mut stmt = conn
        .prepare("SELECT id, ts, session, tag, path, label, context FROM event_log ORDER BY id DESC LIMIT ?1")
        .map_err(|e| e.to_string())?;
    let rows = stmt
        .query_map(params![limit], |row| {
            Ok(EventRow {
                id: row.get(0)?,
                ts: row.get(1)?,
                session: row.get(2)?,
                tag: row.get(3)?,
                path: row.get(4)?,
                label: row.get(5)?,
                context: row.get(6)?,
            })
        })
        .map_err(|e| e.to_string())?;
    rows.collect::<Result<Vec<_>, _>>().map_err(|e| e.to_string())
}
