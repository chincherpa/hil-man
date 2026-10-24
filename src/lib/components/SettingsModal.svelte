<script>
  import { onMount } from "svelte";
  import { invoke } from "@tauri-apps/api/core";
  import Icon from "./Icon.svelte";

  let { theme, onthemechange, onclose } = $props();

  /**
   * @typedef {{ section: string, key: string, default: string, value: string, saved: string, overridden: boolean }} Field
   */

  /** @type {Field[]} */
  let fields = $state([]);
  /** @type {string | null} */
  let error = $state(null);
  let saving = $state(false);

  let sections = $derived([...new Set(fields.map((f) => f.section))]);
  let dirty = $derived(fields.filter((f) => f.value !== f.saved));

  onMount(async () => {
    try {
      /** @type {Omit<Field, "saved">[]} */
      const entries = await invoke("get_settings");
      fields = entries.map((e) => ({ ...e, saved: e.value }));
    } catch (err) {
      error = String(err);
    }
  });

  async function save() {
    saving = true;
    error = null;
    try {
      const changes = dirty.map(({ section, key, value }) => ({ section, key, value }));
      await invoke("save_settings", { changes });
      for (const f of dirty) {
        f.saved = f.value;
        f.overridden = f.value !== f.default;
      }
      window.dispatchEvent(new Event("settings-changed"));
    } catch (err) {
      error = String(err);
    } finally {
      saving = false;
    }
  }

  /** @param {Field} field */
  function reset(field) {
    field.value = field.default;
  }

  /** @param {KeyboardEvent} e */
  function onkeydown(e) {
    if (e.key === "Escape") onclose();
  }
</script>

<svelte:window onkeydown={onkeydown} />

<div class="backdrop" role="presentation" onclick={(e) => e.target === e.currentTarget && onclose()}>
  <div class="dialog" role="dialog" aria-modal="true" aria-label="Einstellungen" tabindex="-1" data-no-log>
    <div class="dialog-header">
      <h2>Einstellungen</h2>
      <button class="close" title="Schließen" onclick={onclose}>
        <Icon name="close" size={14} />
      </button>
    </div>

    <div class="body">
      <section class="group">
        <h3>Allgemein</h3>
        <div class="row">
          <span class="label">Erscheinungsbild</span>
          <div class="segmented">
            <button class:selected={theme === "dark"} onclick={() => onthemechange("dark")}>Dunkel</button>
            <button class:selected={theme === "light"} onclick={() => onthemechange("light")}>Hell</button>
          </div>
        </div>
      </section>

      {#each sections as section (section)}
        <section class="group">
          <h3>{section}</h3>
          {#each fields.filter((f) => f.section === section) as field}
            <div class="row" class:changed={field.value !== field.saved}>
              <div class="label">
                <span class="key">{field.key}</span>
                <span class="hint">Standard: {field.default}</span>
              </div>
              <input type="text" bind:value={field.value} />
              <button
                class="reset"
                title="Auf Standard zurücksetzen"
                disabled={field.value === field.default && field.saved === field.default}
                onclick={() => reset(field)}
              >
                Reset
              </button>
            </div>
          {/each}
        </section>
      {/each}
    </div>

    <footer class="footer">
      <span class="version">v0.0.1</span>
      {#if error}<span class="error">{error}</span>{/if}
      <button class="save" disabled={saving || dirty.length === 0} onclick={save}>
        Speichern{dirty.length > 0 ? ` (${dirty.length})` : ""}
      </button>
    </footer>
  </div>
</div>

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
  }

  .dialog {
    width: min(620px, 92vw);
    max-height: 80vh;
    background: var(--bg-elev-1);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 14px 16px 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .dialog-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  h2 {
    margin: 0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-dim);
  }

  h3 {
    margin: 0 0 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-dim);
  }

  .close {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border: none;
    background: transparent;
    color: var(--text-faint);
    border-radius: var(--radius-sm);
  }

  .close:hover {
    background: var(--bg-elev-3);
    color: var(--text);
  }

  .body {
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding-right: 4px;
  }

  .group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .row {
    display: grid;
    grid-template-columns: 1fr 1.4fr auto;
    align-items: center;
    gap: 10px;
    font-size: 12.5px;
    color: var(--text);
  }

  .row.changed .key::after {
    content: " *";
    color: var(--warn);
  }

  .label {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }

  .hint {
    font-size: 10.5px;
    color: var(--text-faint);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  input {
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 6px 8px;
    color: var(--text);
    font-size: 12.5px;
    font-family: inherit;
    min-width: 0;
  }

  input:focus {
    outline: none;
    border-color: var(--accent);
  }

  .reset,
  .save {
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 6px 10px;
    color: var(--text-dim);
    font-size: 12px;
  }

  .reset:hover:not(:disabled),
  .save:hover:not(:disabled) {
    border-color: var(--text-faint);
    color: var(--text);
  }

  .reset:disabled,
  .save:disabled {
    opacity: 0.45;
    cursor: default;
  }

  .segmented {
    display: flex;
    justify-self: start;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 2px;
  }

  .segmented button {
    border: none;
    background: transparent;
    color: var(--text-dim);
    padding: 4px 10px;
    border-radius: var(--radius-sm);
    font-size: 12px;
  }

  .segmented button.selected {
    background: var(--bg-elev-3);
    color: var(--text);
  }

  .footer {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-top: 10px;
    border-top: 1px solid var(--border);
    font-size: 11px;
  }

  .version {
    color: var(--text-faint);
  }

  .error {
    flex: 1;
    color: #f85149;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .save {
    margin-left: auto;
    font-weight: 700;
  }
</style>
