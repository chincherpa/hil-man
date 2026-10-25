<script>
  import { getCurrentWindow } from "@tauri-apps/api/window";
  import Icon from "./Icon.svelte";
  import SettingsModal from "./SettingsModal.svelte";
  import { THEMES, readStoredTheme, applyTheme, persistTheme } from "$lib/themes.js";

  const appWindow = getCurrentWindow();

  const initialTheme = readStoredTheme();

  let theme = $state(initialTheme);
  let settingsOpen = $state(false);
  let themePickerOpen = $state(false);

  applyTheme(initialTheme);

  /** @param {string} next */
  function setTheme(next) {
    theme = next;
    applyTheme(next);
    persistTheme(next);
  }

  /** @param {KeyboardEvent} e */
  function onPickerKeydown(e) {
    if (e.key === "Escape") themePickerOpen = false;
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
      <img src="/logo.png" alt="HilManager" width="20" height="20" />
    </span>
    <span class="title">HilManager</span>
    <span class="version">v0.0.2</span>
  </div>

  <div class="actions">
    <button class="icon-btn" title="Einstellungen" data-no-log onclick={() => (settingsOpen = true)}>
      <Icon name="settings" size={16} />
    </button>

    <div class="theme-picker">
      <button class="icon-btn" title="Design wählen" data-no-log onclick={() => (themePickerOpen = !themePickerOpen)}>
        <Icon name="palette" size={16} />
      </button>

      {#if themePickerOpen}
        <div class="theme-popover-backdrop" role="presentation" onclick={() => (themePickerOpen = false)}></div>
        <div class="theme-popover" role="menu">
          {#each THEMES as t (t.id)}
            <button role="menuitem" class:selected={theme === t.id} onclick={() => { setTheme(t.id); themePickerOpen = false; }}>
              {t.label}
            </button>
          {/each}
        </div>
      {/if}
    </div>

    <span class="divider"></span>

    <button class="win-btn" title="Minimieren" onclick={minimize}><Icon name="minimize" size={14} /></button>
    <button class="win-btn" title="Maximieren" onclick={toggleMaximize}><Icon name="maximize" size={12} /></button>
    <button class="win-btn win-close" title="Schließen" onclick={close}><Icon name="close" size={14} /></button>
  </div>
</header>

{#if settingsOpen}
  <SettingsModal {theme} onthemechange={setTheme} onclose={() => (settingsOpen = false)} />
{/if}

<svelte:window onkeydown={onPickerKeydown} />

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

  .logo img {
    object-fit: contain;
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

  .theme-picker {
    position: relative;
  }

  .theme-popover-backdrop {
    position: fixed;
    inset: 0;
    z-index: 100;
  }

  .theme-popover {
    position: absolute;
    top: calc(100% + 4px);
    right: 0;
    z-index: 101;
    display: flex;
    flex-direction: column;
    min-width: 140px;
    padding: 4px;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  }

  .theme-popover button {
    text-align: left;
    padding: 6px 8px;
    border: none;
    background: transparent;
    color: var(--text-dim);
    border-radius: var(--radius-sm);
    font-size: 12px;
  }

  .theme-popover button:hover {
    background: var(--bg-elev-3);
    color: var(--text);
  }

  .theme-popover button.selected {
    color: var(--text);
    font-weight: 600;
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
