<script>
  import { invoke } from "@tauri-apps/api/core";
  import Icon from "./Icon.svelte";
  import { processDialogButtons, controlDeskButtons, svn, diagnosisButtons, activeDiagnosis, examButtons } from "$lib/data.js";

  let { title, onclose } = $props();

  let loading = $state(false);
  /** @type {string | null} */
  let userResult = $state(null);
  /** @type {string | null} */
  let userError = $state(null);

  async function getUser() {
    loading = true;
    userResult = null;
    userError = null;
    try {
      userResult = await invoke("get_user");
    } catch (err) {
      userError = String(err);
    } finally {
      loading = false;
    }
  }

  /** @param {KeyboardEvent} e */
  function onkeydown(e) {
    if (e.key === "Escape") onclose();
  }
</script>

<svelte:window onkeydown={onkeydown} />

<div class="backdrop" role="presentation" onclick={(e) => e.target === e.currentTarget && onclose()}>
  <div class="dialog" role="dialog" aria-modal="true" aria-label={title} tabindex="-1">
    <div class="dialog-header">
      <h2>{title}</h2>
      <button class="close" title="Schließen" data-no-log onclick={onclose}>
        <Icon name="close" size={14} />
      </button>
    </div>

    {#if title === "ControlDesk"}
      <div class="grid">
        {#each controlDeskButtons as label}
          <button class="cell">{label}</button>
        {/each}
      </div>

      <section class="svn">
        <h3>SVN</h3>
        <div class="svn-row">
          <span class="svn-label">Current</span>
          <span class="svn-value">{svn.current}</span>
        </div>
        <div class="svn-row">
          <span class="svn-label">Newest revision</span>
          <span class="svn-value">{svn.newest}</span>
        </div>
        <button class="cell">Update to newest revision</button>
      </section>

      <div class="user">
        <div class="user-result">
          {#if loading}
            <span class="spinner" role="status" aria-label="Lädt"></span>
          {:else if userError}
            <span class="error">{userError}</span>
          {:else if userResult !== null}
            <span class="svn-value">{userResult}</span>
          {/if}
        </div>
        <button class="cell get-user" onclick={getUser} disabled={loading}>GET USER</button>
      </div>
    {:else if title === "Diagnosis"}
      <div class="grid">
        {#each diagnosisButtons as label}
          <button class="cell">{label}</button>
        {/each}
      </div>

      <section class="svn">
        <div class="svn-row">
          <span class="svn-label">Aktiv</span>
          <span class="status" class:on={activeDiagnosis}>
            <span class="led" class:on={activeDiagnosis}></span>
            <span class="svn-value">{activeDiagnosis ?? "keine"}</span>
          </span>
        </div>
        <button class="cell">Update NAR/RDW</button>
      </section>
    {:else if title === "EXAM"}
      <div class="grid">
        {#each examButtons as label}
          <button class="cell">{label}</button>
        {/each}
      </div>

      <section class="empty"></section>
    {:else}
      <div class="grid">
        {#each processDialogButtons as label}
          <button class="cell">{label}</button>
        {/each}
      </div>

      <section class="empty"></section>
    {/if}
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
    width: 80vw;
    height: 80vh;
    background: var(--bg-elev-1);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 14px 16px 16px;
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

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 7px;
  }

  .svn {
    display: flex;
    flex-direction: column;
    gap: 7px;
  }

  .svn h3 {
    margin: 0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-dim);
  }

  .svn-row {
    display: flex;
    justify-content: space-between;
    font-size: 12.5px;
    color: var(--text-dim);
  }

  .svn-value {
    color: var(--text);
    font-variant-numeric: tabular-nums;
  }

  .status {
    display: flex;
    align-items: center;
    gap: 7px;
  }

  .led {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--bg-elev-3);
    border: 1px solid var(--border);
  }

  .led.on {
    background: #3fb950;
    border-color: #3fb950;
    box-shadow: 0 0 6px #3fb950;
  }

  .empty {
    flex: 1;
    border: 1px dashed var(--border-soft);
    border-radius: var(--radius-sm);
  }

  .user {
    margin-top: auto;
    display: flex;
    flex-direction: column;
    gap: 7px;
  }

  .user-result {
    display: flex;
    align-items: center;
    min-height: 20px;
    font-size: 12.5px;
  }

  .get-user {
    font-weight: 700;
    letter-spacing: 0.08em;
  }

  .get-user:disabled {
    opacity: 0.6;
    cursor: wait;
  }

  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  .error {
    color: #f85149;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .cell {
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
</style>
