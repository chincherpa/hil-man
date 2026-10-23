<script>
  import Icon from "./Icon.svelte";
  import { mainProcesses, extraActions } from "$lib/data.js";

  let processes = $state(mainProcesses.map((p) => ({ ...p })));
  let actions = $state(extraActions.map((a) => ({ ...a })));

  let total = processes.length;
  let done = $derived(processes.filter((p) => p.checked).length);
  let percent = $derived(total ? Math.round((done / total) * 100) : 0);

  /**
   * @param {Array<{ checked: boolean | null }>} list
   * @param {{ checked: boolean | null }} item
   */
  function toggle(list, item) {
    if (item.checked === null) return;
    item.checked = !item.checked;
  }

  // left column: 1,2,4,5 ; right column: 3,6 interleaved with extraActions
  let leftCol = $derived(processes.filter((p) => [1, 2, 4, 5].includes(p.id)));
  let rightNumbered = $derived(processes.filter((p) => [3, 6].includes(p.id)));
</script>

<section class="panel">
  <div class="panel-header">
    <span class="dot-icon"></span>
    <h2>Prozesse</h2>
  </div>

  <div class="grid">
    {#each leftCol as item, i (item.id)}
      <button class="cell" class:checked={item.checked} onclick={() => toggle(processes, item)}>
        <span class="check" class:on={item.checked}>
          {#if item.checked}<Icon name="check" size={11} />{/if}
        </span>
        <span class="num">{item.id}</span>
        <span class="label">{item.label}</span>
      </button>
    {/each}

    {#each [0, 1] as rowIdx}
      {#if rightNumbered[rowIdx]}
        {@const item = rightNumbered[rowIdx]}
        <button class="cell" class:checked={item.checked} onclick={() => toggle(processes, item)}>
          <span class="check" class:on={item.checked}>
            {#if item.checked}<Icon name="check" size={11} />{/if}
          </span>
          <span class="num">{item.id}</span>
          <span class="label">{item.label}</span>
          {#if item.expandable}<span class="chev"><Icon name="chevronDown" size={14} /></span>{/if}
        </button>
      {:else}
        <span class="cell empty"></span>
      {/if}
    {/each}

    {#each actions as item (item.label)}
      <button class="cell action" onclick={() => toggle(actions, item)}>
        {#if item.checked === null}
          <span class="aux-icon"><Icon name={item.icon ?? "grid"} size={14} /></span>
        {:else}
          <span class="check" class:on={item.checked}>
            {#if item.checked}<Icon name="check" size={11} />{/if}
          </span>
        {/if}
        <span class="label">{item.label}</span>
        {#if item.expandable}<span class="chev"><Icon name="chevronDown" size={14} /></span>{/if}
      </button>
    {/each}
  </div>

  <div class="progress-row">
    <span class="progress-label">Gesamtfortschritt</span>
    <div class="track">
      <div class="fill" style="width: {percent}%"></div>
    </div>
    <span class="progress-count">{done} von {total}</span>
    <span class="progress-meta">{percent}% &nbsp;ca. 00:38</span>
  </div>
</section>

<style>
  .panel {
    background: var(--bg-elev-1);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 14px 16px 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .panel-header {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .dot-icon {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--accent);
  }

  h2 {
    margin: 0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-dim);
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 7px;
  }

  .cell {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 8px 10px;
    text-align: left;
    color: var(--text-dim);
    font-size: 12.5px;
    min-height: 34px;
  }

  .cell:hover {
    border-color: var(--text-faint);
  }

  .cell.checked {
    color: var(--text);
  }

  .cell.empty {
    background: transparent;
    border: 1px dashed var(--border-soft);
    opacity: 0.4;
  }

  .check {
    width: 15px;
    height: 15px;
    border-radius: 4px;
    border: 1.5px solid var(--border);
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--bg);
  }

  .check.on {
    background: var(--accent);
    border-color: var(--accent);
  }

  .num {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: var(--bg-elev-3);
    color: var(--text-faint);
    font-size: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .label {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .chev,
  .aux-icon {
    color: var(--text-faint);
    display: flex;
    flex-shrink: 0;
  }

  .progress-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-top: 2px;
  }

  .progress-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-faint);
    white-space: nowrap;
  }

  .track {
    flex: 1;
    height: 5px;
    background: var(--bg-elev-3);
    border-radius: 3px;
    overflow: hidden;
  }

  .fill {
    height: 100%;
    background: var(--accent);
    border-radius: 3px;
    transition: width 0.3s ease;
  }

  .progress-count {
    font-size: 11px;
    color: var(--text-dim);
    white-space: nowrap;
  }

  .progress-meta {
    font-size: 11px;
    color: var(--text-faint);
    white-space: nowrap;
  }
</style>
