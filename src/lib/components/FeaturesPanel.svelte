<script>
  import Icon from "./Icon.svelte";
  import { features } from "$lib/data.js";

  let items = $state(features.map((f) => ({ ...f })));

  /** @param {{ toggle?: boolean, active?: boolean }} item */
  function toggle(item) {
    if (!item.toggle) return;
    item.active = !item.active;
  }
</script>

<section class="panel">
  <div class="panel-header">
    <h2>Features</h2>
  </div>

  <div class="list">
    {#each items as item}
      <button class="row" onclick={() => toggle(item)}>
        <span class="icon"><Icon name={item.icon} size={14} /></span>
        <span class="label">{item.label}</span>
        {#if item.badge}
          <span class="badge">{item.badge}</span>
        {:else if item.toggle}
          <span class="toggle-dot" class:on={item.active}></span>
        {/if}
      </button>
    {/each}
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
    gap: 12px;
    height: 100%;
  }

  h2 {
    margin: 0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-dim);
  }

  .list {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .row {
    display: flex;
    align-items: center;
    gap: 10px;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 9px 10px;
    color: var(--text-dim);
    font-size: 12px;
    text-align: left;
  }

  .row:hover {
    border-color: var(--text-faint);
    color: var(--text);
  }

  .icon {
    color: var(--text-faint);
    display: flex;
  }

  .label {
    flex: 1;
  }

  .badge {
    font-size: 10px;
    color: var(--text-faint);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 6px;
  }

  .toggle-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--border);
  }

  .toggle-dot.on {
    background: var(--accent);
    box-shadow: 0 0 6px var(--accent);
  }
</style>
