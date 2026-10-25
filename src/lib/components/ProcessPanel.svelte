<script>
  import DummyModal from "./DummyModal.svelte";
  import { processButtons } from "$lib/data.js";

  /** @type {string | null} */
  let openLabel = $state(null);
</script>

<section class="panel" data-no-log>
  <div class="grid">
    {#each processButtons as label}
      <button class="cell" onclick={() => (openLabel = label)}>
        <span class="label">{label}</span>
      </button>
    {/each}
  </div>
</section>

{#if openLabel}
  <DummyModal title={openLabel} onclose={() => (openLabel = null)} />
{/if}

<style>
  .panel {
    background: var(--bg-elev-1);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex-shrink: 0;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 7px;
  }

  .cell {
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: 220px;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    padding: 8px 10px;
    color: var(--text-dim);
    font-size: 12.5px;
    min-height: 34px;
  }

  .cell:hover {
    border-color: var(--text-faint);
    color: var(--text);
  }

  .label {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>
