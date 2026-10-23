<script>
  import TitleBar from "$lib/components/TitleBar.svelte";
  import ProcessPanel from "$lib/components/ProcessPanel.svelte";
  import ControlPanel from "$lib/components/ControlPanel.svelte";
  import FeaturesPanel from "$lib/components/FeaturesPanel.svelte";
  import ConsolePanel from "$lib/components/ConsolePanel.svelte";
  import StatusBar from "$lib/components/StatusBar.svelte";
</script>

<div class="app">
  <TitleBar />

  <main class="content">
    <ProcessPanel />

    <div class="middle-row">
      <div class="control-col"><ControlPanel /></div>
      <div class="features-col"><FeaturesPanel /></div>
    </div>

    <ConsolePanel />
  </main>

  <StatusBar />
</div>

<style>
  .app {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .content {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 12px;
    overflow: hidden;
  }

  .middle-row {
    display: flex;
    gap: 12px;
    flex-shrink: 0;
  }

  .control-col {
    flex: 2.1;
  }

  .features-col {
    flex: 1;
  }
</style>
