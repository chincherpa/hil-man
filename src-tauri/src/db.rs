use std::error::Error;
use std::path::Path;
use std::sync::Mutex;

use rusqlite::Connection;

pub struct AppDb(pub Mutex<Connection>);

/// Opens (and creates on first start) `hilman.sqlite` next to the executable.
pub fn open() -> Result<Connection, Box<dyn Error>> {
    let exe_dir = std::env::current_exe()?
        .parent()
        .ok_or("executable has no parent directory")?
        .to_path_buf();

    let conn = Connection::open(exe_dir.join("hilman.sqlite"))?;
    conn.execute_batch(
        "CREATE TABLE IF NOT EXISTS event_log (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            ts      TEXT NOT NULL,
            session TEXT NOT NULL,
            tag     TEXT NOT NULL,
            path    TEXT NOT NULL,
            label   TEXT NOT NULL,
            context TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_event_log_ts ON event_log (ts);
        CREATE TABLE IF NOT EXISTS settings (
            section TEXT NOT NULL,
            key     TEXT NOT NULL,
            value   TEXT NOT NULL,
            PRIMARY KEY (section, key)
        );",
    )?;
    migrate_old_event_log(&conn, &exe_dir)?;
    Ok(conn)
}

/// Einmalig: Zeilen aus der alten `event_log.sqlite` übernehmen.
/// `user_version` merkt sich, dass die Migration schon lief. Die alte Datei bleibt unverändert liegen.
fn migrate_old_event_log(conn: &Connection, exe_dir: &Path) -> Result<(), Box<dyn Error>> {
    const MIGRATION_VERSION: i64 = 1;

    let version: i64 = conn.query_row("PRAGMA user_version", [], |row| row.get(0))?;
    if version >= MIGRATION_VERSION {
        return Ok(());
    }

    let old = exe_dir.join("event_log.sqlite");
    if old.exists() {
        conn.execute("ATTACH DATABASE ?1 AS old", [old.to_string_lossy().as_ref()])?;
        conn.execute_batch(
            "INSERT INTO main.event_log (ts, session, tag, path, label, context)
             SELECT ts, session, tag, path, label, context FROM old.event_log ORDER BY id;
             DETACH DATABASE old;",
        )?;
    }

    conn.execute_batch(&format!("PRAGMA user_version = {MIGRATION_VERSION};"))?;
    Ok(())
}
