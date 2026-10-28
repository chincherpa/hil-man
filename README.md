# Tauri + SvelteKit

This template should help get you started developing with Tauri and SvelteKit in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Svelte](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode) + [Tauri](https://marketplace.visualstudio.com/items?itemName=tauri-apps.tauri-vscode) + [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer).

## Deployment: settings.ini

Auf jedem Rechner, auf dem die gebaute Anwendung läuft (nicht im Dev-Build), muss
neben der `.exe` eine `settings.ini` liegen, die auf den freigegebenen Ordner mit
`config.json` und dem `python`-Ordner (inkl. `ContolDeskHandler.py`) zeigt, z. B.
auf einem Netzlaufwerk:

```ini
[Paths]
Root=\\server\share\hil-man
```

Unter `Root` werden erwartet:

```text
Root/
  config.json
  python/
    ContolDeskHandler.py
    wait_10sec_return_username.py
    stop_realtime_application.py
```

Fehlt `settings.ini` oder der Eintrag `Root`, bricht die Anwendung mit einer
entsprechenden Fehlermeldung ab (außer im Dev-Build via `pnpm tauri dev`, dort
wird automatisch das Projektverzeichnis verwendet).
