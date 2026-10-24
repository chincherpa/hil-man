use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;

use rusqlite::{params, Connection};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use tauri::State;

use crate::db::AppDb;

type Field = (String, String);

#[derive(Serialize)]
pub struct SettingEntry {
    pub section: String,
    pub key: String,
    pub default: String,
    pub value: String,
    pub overridden: bool,
}

#[derive(Deserialize)]
pub struct SettingChange {
    pub section: String,
    pub key: String,
    pub value: String,
}

fn config_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("config.json")
}

fn read_defaults() -> Result<Vec<(Field, String)>, String> {
    let content = fs::read_to_string(config_path())
        .map_err(|e| format!("Failed to read config.json: {}", e))?;
    let config: Value = serde_json::from_str(&content)
        .map_err(|e| format!("Failed to parse config.json: {}", e))?;
    let root = config
        .as_object()
        .ok_or_else(|| "config.json root must be an object".to_string())?;

    let mut fields = Vec::new();
    for (section, values) in root {
        let Some(values) = values.as_object() else {
            continue;
        };
        for (key, value) in values {
            let text = match value {
                Value::String(s) => s.clone(),
                other => other.to_string(),
            };
            fields.push(((section.clone(), key.clone()), text));
        }
    }
    Ok(fields)
}

fn load_overrides(conn: &Connection) -> Result<HashMap<Field, String>, String> {
    let mut stmt = conn
        .prepare("SELECT section, key, value FROM settings")
        .map_err(|e| e.to_string())?;
    let rows = stmt
        .query_map([], |row| {
            Ok((
                (row.get::<_, String>(0)?, row.get::<_, String>(1)?),
                row.get::<_, String>(2)?,
            ))
        })
        .map_err(|e| e.to_string())?;
    rows.collect::<Result<HashMap<Field, String>, _>>()
        .map_err(|e| e.to_string())
}

#[tauri::command]
pub fn get_settings(db: State<AppDb>) -> Result<Vec<SettingEntry>, String> {
    let defaults = read_defaults()?;
    let conn = db.0.lock().map_err(|e| e.to_string())?;
    let overrides = load_overrides(&conn)?;

    Ok(defaults
        .into_iter()
        .map(|(field, default)| match overrides.get(&field) {
            Some(value) => SettingEntry {
                section: field.0,
                key: field.1,
                default,
                value: value.clone(),
                overridden: true,
            },
            None => SettingEntry {
                section: field.0,
                key: field.1,
                value: default.clone(),
                default,
                overridden: false,
            },
        })
        .collect())
}

#[tauri::command]
pub fn save_settings(db: State<AppDb>, changes: Vec<SettingChange>) -> Result<(), String> {
    let defaults: HashMap<Field, String> = read_defaults()?.into_iter().collect();
    let mut conn = db.0.lock().map_err(|e| e.to_string())?;
    let tx = conn.transaction().map_err(|e| e.to_string())?;

    for change in changes {
        let field = (change.section, change.key);
        let default = defaults
            .get(&field)
            .ok_or_else(|| format!("Unknown setting {}.{}", field.0, field.1))?;

        let written = if *default == change.value {
            tx.execute(
                "DELETE FROM settings WHERE section = ?1 AND key = ?2",
                params![field.0, field.1],
            )
        } else {
            tx.execute(
                "INSERT INTO settings (section, key, value) VALUES (?1, ?2, ?3)
                 ON CONFLICT(section, key) DO UPDATE SET value = excluded.value",
                params![field.0, field.1, change.value],
            )
        };
        written.map_err(|e| e.to_string())?;
    }

    tx.commit().map_err(|e| e.to_string())
}
