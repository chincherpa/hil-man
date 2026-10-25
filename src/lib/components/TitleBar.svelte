<script>
  import { getCurrentWindow } from "@tauri-apps/api/window";
  import Icon from "./Icon.svelte";
  import SettingsModal from "./SettingsModal.svelte";

  const appWindow = getCurrentWindow();

  /** @type {"dark" | "light"} */
  let theme = $state(readTheme());
  let settingsOpen = $state(false);

  document.documentElement.dataset.theme = theme;

  /** @returns {"dark" | "light"} */
  function readTheme() {
    try {
      return localStorage.getItem("theme") === "light" ? "light" : "dark";
    } catch {
      return "dark";
    }
  }

  /** @param {"dark" | "light"} next */
  function setTheme(next) {
    theme = next;
    document.documentElement.dataset.theme = next;
    try {
      localStorage.setItem("theme", next);
    } catch {
      // storage blocked -> theme still applies for this session
    }
  }

  function toggleTheme() {
    setTheme(theme === "dark" ? "light" : "dark");
  }

  function minimize() {
    appWindow.minimize();
  }
  function toggleMaximize() {
    appWindow.toggleMaximize();
  }
  function close() {
    appWindow.close();
  }
</script>

<header class="titlebar" data-tauri-drag-region>
  <div class="brand" data-tauri-drag-region>
    <span class="logo">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
        <circle cx="9" cy="12" r="6" stroke="#2dd9c8" stroke-width="2" />
        <circle cx="15" cy="12" r="6" stroke="#1f9d91" stroke-width="2" />
      </svg>
    </span>
    <span class="title">HilManager</span>
    <span class="version">v0.0.1</span>
  </div>

  <div class="actions">
    <button class="icon-btn" title="Einstellungen" data-no-log onclick={() => (settingsOpen = true)}>
      <Icon name="settings" size={16} />
    </button>

    <button class="icon-btn" title={theme === "dark" ? "Helles Design" : "Dunkles Design"} data-no-log onclick={toggleTheme}>
      <Icon name="sun" size={16} />
    </button>

    <span class="divider"></span>

    <button class="win-btn" title="Minimieren" onclick={minimize}><Icon name="minimize" size={14} /></button>
    <button class="win-btn" title="Maximieren" onclick={toggleMaximize}><Icon name="maximize" size={12} /></button>
    <button class="win-btn win-close" title="Schließen" onclick={close}><Icon name="close" size={14} /></button>
  </div>
</header>

{#if settingsOpen}
  <SettingsModal {theme} onthemechange={setTheme} onclose={() => (settingsOpen = false)} />
{/if}

<style>
  .titlebar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 44px;
    padding: 0 10px 0 14px;
    background: var(--bg-elev-1);
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
    user-select: none;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 9px;
  }

  .logo {
    display: flex;
    align-items: center;
  }

  .title {
    font-weight: 600;
    font-size: 14px;
    color: var(--text);
  }

  .version {
    font-size: 11px;
    color: var(--text-faint);
  }

  .dev-badge {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--warn);
    background: var(--warn-bg);
    border: 1px solid rgba(232, 162, 61, 0.3);
    border-radius: 999px;
    padding: 2px 8px;
  }

  .dev-badge .dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--warn);
  }

  .actions {
    display: flex;
    align-items: center;
    gap: 2px;
  }

  .icon-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border: none;
    background: transparent;
    color: var(--text-dim);
    border-radius: var(--radius-sm);
  }

  .icon-btn:hover {
    background: var(--bg-elev-3);
    color: var(--text);
  }

  .divider {
    width: 1px;
    height: 18px;
    background: var(--border);
    margin: 0 8px;
  }

  .win-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 30px;
    border: none;
    background: transparent;
    color: var(--text-dim);
    border-radius: var(--radius-sm);
  }

  .win-btn:hover {
    background: var(--bg-elev-3);
    color: var(--text);
  }

  .win-close:hover {
    background: var(--danger);
    color: white;
  }
</style>
