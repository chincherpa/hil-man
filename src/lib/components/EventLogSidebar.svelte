<script>
  import { onMount } from "svelte";
  import { eventLog, loadEvents, startEventLog } from "$lib/eventlog.svelte.js";
  import Icon from "./Icon.svelte";

  let collapsed = $state(false);

  onMount(() => {
    loadEvents();
    return startEventLog();
  });

  /** @param {string} ts */
  function time(ts) {
    return new Date(ts).toLocaleTimeString("de-DE", { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" });
  }
</script>

<aside class="sidebar" class:collapsed data-no-log>
  <div class="panel-header">
    <button class="toggle" title={collapsed ? "Event-Log ausklappen" : "Event-Log einklappen"} onclick={() => (collapsed = !collapsed)}>
      <span class="chev" class:open={!collapsed}>
        <Icon name="chevronDown" size={14} />
      </span>
    </button>
    {#if !collapsed}
      <h2>Log</h2>
      <span class="count">{eventLog.length}</span>
    {/if}
  </div>

  {#if !collapsed}
    <ol class="list">
      {#each eventLog as ev}
        <li class="entry">
          <div class="meta">
            <span class="time">{time(ev.ts)}</span>
            <span class="tag">{ev.tag}</span>
          </div>
          <div class="label" title={ev.label}>{ev.label}</div>
          {#if ev.context}
            <div class="context">{ev.context}</div>
          {/if}
          <div class="path" title={ev.path}>{ev.path}</div>
        </li>
      {:else}
        <li class="empty">Noch keine Klicks</li>
      {/each}
    </ol>
  {/if}
</aside>

<style>
  .sidebar {
    width: 280px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
    background: var(--bg-elev-1);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 14px 12px 14px 14px;
    margin: 12px 12px 12px 0;
    min-height: 0;
  }

  .sidebar.collapsed {
    width: 44px;
    padding: 14px 0;
    align-items: center;
  }

  .panel-header {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    flex-shrink: 0;
    border: none;
    background: transparent;
    color: var(--text-faint);
    border-radius: var(--radius-sm);
  }

  .toggle:hover {
    background: var(--bg-elev-3);
    color: var(--text);
  }

  .chev {
    display: flex;
    transform: rotate(90deg);
    transition: transform 0.2s ease;
  }

  .chev.open {
    transform: rotate(-90deg);
  }

  h2 {
    margin: 0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-dim);
  }

  .count {
    margin-left: auto;
    font-size: 10.5px;
    color: var(--text-faint);
    font-variant-numeric: tabular-nums;
  }

  .list {
    flex: 1;
    min-height: 0;
    margin: 0;
    padding: 0 4px 0 0;
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
    overflow-y: auto;
  }

  .entry {
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 6px 8px;
    display: flex;
    flex-direction: column;
    gap: 2px;
    font-size: 11.5px;
  }

  .meta {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 10px;
    color: var(--text-faint);
    font-variant-numeric: tabular-nums;
  }

  .tag {
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  .label {
    color: var(--text);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .context {
    color: var(--text-dim);
    font-size: 10.5px;
  }

  .path {
    color: var(--text-faint);
    font-size: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .empty {
    color: var(--text-faint);
    font-size: 12px;
    text-align: center;
    padding: 16px 0;
  }
</style>
