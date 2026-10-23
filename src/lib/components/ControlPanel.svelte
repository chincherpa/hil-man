<script>
  import Icon from "./Icon.svelte";
  import { setupPresets, controlModes } from "$lib/data.js";

  let activeMode = $state("Nachfragend");
  let activePreset = $state("nachtlauf");
  let running = $state(false);

  function start() {
    running = true;
  }
  function abort() {
    running = false;
  }
  function closeDesk() {
    running = false;
  }
</script>

<section class="panel">
  <div class="panel-header">
    <h2>Steuerung</h2>
    <div class="mode-tabs">
      {#each controlModes as mode}
        <button class="tab" class:active={activeMode === mode} onclick={() => (activeMode = mode)}>
          {mode}
        </button>
      {/each}
    </div>
  </div>

  <div class="columns">
    <div class="col">
      <span class="col-label">Setup-Preset</span>
      <div class="preset-list">
        {#each setupPresets as preset}
          <button class="preset" class:active={activePreset === preset.id} onclick={() => (activePreset = preset.id)}>
            <span class="radio" class:on={activePreset === preset.id}></span>
            {preset.label}
          </button>
        {/each}
      </div>

      <button class="scenario">
        <Icon name="refresh" size={13} />
        <span class="scenario-label">Change Szenario</span>
        <span class="scenario-warn">
          <span class="warn-dot">⚠</span>
          Szenario nicht gefunden
          <Icon name="chevronDown" size={13} />
        </span>
      </button>
    </div>

    <div class="col">
      <span class="col-label">Aktionen</span>
      <button class="start-btn" onclick={start}>
        <Icon name="maximize" size={12} />
        Start
      </button>
      <button class="ghost-btn" onclick={closeDesk}>ControlDesk schließen</button>
      <button class="ghost-btn disabled" disabled={!running} onclick={abort}>Abbruch</button>
    </div>
  </div>
</section>

<style>
  .panel {
    background: var(--bg-elev-1);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    height: 100%;
  }

  .panel-header {
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

  .mode-tabs {
    display: flex;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 2px;
    gap: 2px;
  }

  .tab {
    border: none;
    background: transparent;
    color: var(--text-faint);
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 5px;
  }

  .tab.active {
    background: var(--bg-elev-3);
    color: var(--text);
  }

  .columns {
    display: flex;
    gap: 14px;
    flex: 1;
  }

  .col {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 7px;
  }

  .col-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-faint);
    margin-bottom: 2px;
  }

  .preset-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .preset {
    display: flex;
    align-items: center;
    gap: 9px;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 9px 10px;
    color: var(--text-dim);
    font-size: 12px;
    text-align: left;
  }

  .preset:hover {
    border-color: var(--text-faint);
  }

  .preset.active {
    border-color: var(--accent);
    color: var(--text);
    background: var(--accent-bg);
  }

  .radio {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    border: 1.5px solid var(--text-faint);
    flex-shrink: 0;
  }

  .radio.on {
    background: var(--accent);
    border-color: var(--accent);
  }

  .scenario {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 7px 10px;
    color: var(--text-dim);
    font-size: 11px;
    margin-top: 4px;
  }

  .scenario-label {
    flex-shrink: 0;
  }

  .scenario-warn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 6px;
    background: var(--warn-bg);
    border: 1px solid rgba(232, 162, 61, 0.3);
    color: var(--warn);
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 10.5px;
    white-space: nowrap;
  }

  .warn-dot {
    font-size: 10px;
  }

  .start-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: var(--accent);
    color: var(--text);
    border: none;
    border-radius: var(--radius-sm);
    padding: 10px;
    font-weight: 700;
    font-size: 12.5px;
    letter-spacing: 0.03em;
  }

  .start-btn:hover {
    background: var(--accent-dim);
  }

  .ghost-btn {
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 9px;
    color: var(--text-dim);
    font-size: 12px;
  }

  .ghost-btn:hover:not(:disabled) {
    border-color: var(--text-faint);
    color: var(--text);
  }

  .ghost-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
</style>
