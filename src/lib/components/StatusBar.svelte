<script>
  import { statusItems } from "$lib/data.js";
</script>

<footer class="statusbar">
  <div class="left">
    {#each statusItems as item}
      {#if item.kind === "badge"}
        <span class="badge">{item.label}</span>
      {:else if item.kind === "dot-ok"}
        <span class="item"><span class="dot ok"></span>{item.label}</span>
      {:else}
        <span class="item">{item.label}</span>
      {/if}
    {/each}
  </div>
  <div class="right">
    <span class="badge warn">DEVELOPMENT</span>
  </div>
</footer>

<style>
  .statusbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 28px;
    padding: 0 14px;
    background: var(--bg-elev-1);
    border-top: 1px solid var(--border);
    font-size: 10.5px;
    color: var(--text-faint);
    flex-shrink: 0;
  }

  .left,
  .right {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .item {
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
  }

  .dot.ok {
    background: var(--ok);
    box-shadow: 0 0 4px var(--ok);
  }

  .badge {
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--text-dim);
    background: var(--bg-elev-3);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 7px;
  }

  .badge.warn {
    color: var(--warn);
    background: var(--warn-bg);
    border-color: rgba(232, 162, 61, 0.3);
  }
</style>
