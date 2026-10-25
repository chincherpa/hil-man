<script>
  import Icon from "./Icon.svelte";
  import { clampItems } from "$lib/data.js";
  import { resizeFlyout, TAB_WIDTH, TAB_HEIGHT, MENU_WIDTH } from "$lib/flyout.js";

  let open = $state(false);
  let clamps = $state(clampItems.map((label) => ({ label, on: false })));
  let doorOpen = $state(false);
  /** @type {HTMLElement} */
  let panel;

  /** @param {{ on: boolean }} item */
  function press(item) {
    item.on = true;
  }

  function toggle() {
    open = !open;
    if (open) {
      resizeFlyout(MENU_WIDTH + TAB_WIDTH, Math.max(TAB_HEIGHT, panel.offsetHeight));
    } else {
      resizeFlyout(TAB_WIDTH, TAB_HEIGHT);
    }
  }
</script>

<aside class="flyout">
  <div class="panel" class:open bind:this={panel}>
    {#each clamps as item}
      <button class="row" onclick={() => press(item)}>
        <span class="led" class:on={item.on}></span>
        <span class="label">{item.label}</span>
      </button>
    {/each}

    <button class="row" class:active={doorOpen} onclick={() => (doorOpen = !doorOpen)}>
      <span class="label">{doorOpen ? "close door" : "open door"}</span>
    </button>
  </div>

  <button class="tab" title="Menü" onclick={toggle}>
    <span class="chev" class:open>
      <Icon name="chevronDown" size={14} />
    </span>
  </button>
</aside>

<style>
  .flyout {
    display: flex;
    align-items: flex-start;
    justify-content: flex-end;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
  }

  .panel {
    box-sizing: border-box;
    width: 200px;
    flex-shrink: 0;
    background: var(--bg-elev-1);
    border: 2px solid var(--text-faint);
    border-radius: var(--radius-lg);
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 7px;
    opacity: 0;
    visibility: hidden;
    transform: translateX(16px);
    transition:
      opacity 0.5s ease,
      transform 1s cubic-bezier(0.2, 0.8, 0.2, 1),
      visibility 9s;
  }

  .panel.open {
    opacity: 1;
    visibility: visible;
    transform: translateX(0);
  }

  .row {
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

  .row:hover {
    border-color: var(--text-faint);
    color: var(--text);
  }

  .row.active {
    border-color: var(--accent);
    color: var(--text);
    background: var(--accent-bg);
  }

  .label {
    flex: 1;
  }

  .led {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--bg-elev-3);
    border: 1px solid var(--border);
    flex-shrink: 0;
  }

  .led.on {
    background: var(--led-ok);
    border-color: var(--led-ok);
    box-shadow: var(--led-ok-glow);
  }

  .tab {
    flex-shrink: 0;
    width: 18px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-elev-2);
    border: 1px solid var(--text-faint);
    border-right: none;
    border-radius: var(--radius-sm) 0 0 var(--radius-sm);
    color: var(--text-dim);
  }

  .tab:hover {
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
</style>
