<script>
  import { onMount } from "svelte";
  import { getCurrentWindow } from "@tauri-apps/api/window";
  import TitleBar from "$lib/components/TitleBar.svelte";
  import ProcessPanel from "$lib/components/ProcessPanel.svelte";
  import SignalsPanel from "$lib/components/SignalsPanel.svelte";
  import FlyoutMenu from "$lib/components/FlyoutMenu.svelte";
  import StatusBar from "$lib/components/StatusBar.svelte";
  import EventLogSidebar from "$lib/components/EventLogSidebar.svelte";
  import { initFlyout } from "$lib/flyout.js";

  // Gleiche index.html für beide Windows, Label entscheidet welche Ansicht
  const isFlyout = getCurrentWindow().label === "flyout";

  onMount(() => {
    if (isFlyout) initFlyout();
  });
</script>

{#if isFlyout}
  <FlyoutMenu />
{:else}
  <div class="app">
    <TitleBar />

    <div class="body">
      <main class="content">
        <ProcessPanel />
        <SignalsPanel />
      </main>

      <EventLogSidebar />
    </div>

    <StatusBar />
  </div>
{/if}

<style>
  .app {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .body {
    flex: 1;
    min-height: 0;
    display: flex;
  }

  .content {
    position: relative;
    flex: 1;
    min-width: 0;
    min-height: 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 12px;
    overflow: hidden;
  }
</style>
