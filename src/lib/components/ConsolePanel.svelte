<script>
  import Icon from "./Icon.svelte";

  let filter = $state("Alle");
  /** @type {string[]} */
  let lines = $state([]);
</script>

<section class="panel">
  <div class="panel-header">
    <div class="title-group">
      <span class="dot"></span>
      <h2>Konsole</h2>
    </div>
    <div class="controls">
      <span class="meta">stdout &middot; live</span>
      <button class="filter">{filter} <Icon name="chevronDown" size={12} /></button>
      <button class="icon-btn" title="Zum Ende scrollen"><Icon name="download" size={14} /></button>
      <button class="icon-btn" title="Kopieren"><Icon name="copy" size={14} /></button>
      <button class="icon-btn" title="Leeren"><Icon name="trash" size={14} /></button>
    </div>
  </div>

  <div class="body">
    {#if lines.length === 0}
      <span class="placeholder">Bereit &middot; Ausgaben erscheinen hier, sobald ein Lauf startet.</span>
    {:else}
      {#each lines as line}
        <div class="line">{line}</div>
      {/each}
    {/if}
  </div>
</section>

<style>
  .panel {
    background: var(--bg-elev-1);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 12px 16px 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-height: 0;
    flex: 1;
  }

  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .title-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--ok);
  }

  h2 {
    margin: 0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-dim);
  }

  .controls {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .meta {
    font-size: 11px;
    color: var(--text-faint);
  }

  .filter {
    display: flex;
    align-items: center;
    gap: 5px;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 4px 8px;
    color: var(--text-dim);
    font-size: 11px;
  }

  .icon-btn {
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

  .icon-btn:hover {
    background: var(--bg-elev-3);
    color: var(--text);
  }

  .body {
    flex: 1;
    min-height: 0;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 10px 12px;
    overflow-y: auto;
    font-family: "Cascadia Code", "Consolas", monospace;
    font-size: 12px;
  }

  .placeholder {
    color: var(--text-faint);
  }

  .line {
    color: var(--text-dim);
    white-space: pre-wrap;
  }
</style>
