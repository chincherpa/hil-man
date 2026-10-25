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
    container-type: inline-size;
  }

  /* Feste Spaltenstufen für 7 Buttons (1 / 4+3 / 7), damit kein einzelner Button allein in der letzten Zeile steht.
     max-width deckelt die Zellbreite (220px), damit Buttons zwischen den Stufen nicht aufblähen. */
  .grid {
    --cell-max: 220px;
    --gap: 7px;
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--gap);
    max-width: var(--cell-max);
  }

  @container (min-width: 400px) {
    .grid {
      grid-template-columns: repeat(4, 1fr);
      max-width: calc(4 * var(--cell-max) + 3 * var(--gap));
    }
  }

  @container (min-width: 1300px) {
    .grid {
      grid-template-columns: repeat(7, 1fr);
      max-width: calc(7 * var(--cell-max) + 6 * var(--gap));
    }
  }

  .cell {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 0;
    background: var(--bg-elev-2);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-sm);
    /* Schmales Inline-Padding: bei 4 Spalten ab 400px (~97px/Zelle) muss "ControlDesk" auch in Monospace passen */
    padding: 8px 4px;
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
