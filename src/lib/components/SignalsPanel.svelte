<script>
  import { signals } from "$lib/data.js";
</script>

<section class="panel">
  <div class="panel-header">
    <h2>Critical Signals</h2>
  </div>

  <table>
    <thead>
      <tr>
        <th>Signal</th>
        <th class="num">Soll</th>
        <th class="num">Ist</th>
        <th class="center">LED</th>
      </tr>
    </thead>
    <tbody>
      {#each signals as s}
        <tr>
          <td>{s.name}</td>
          <td class="num">{s.soll}</td>
          <td class="num">{s.ist}</td>
          <td class="center"><span class="led {s.led}"></span></td>
        </tr>
      {/each}
    </tbody>
  </table>
</section>

<style>
  .panel {
    background: var(--bg-elev-1);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    flex: 1;
    min-height: 0;
  }

  h2 {
    margin: 0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-dim);
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
  }

  th {
    text-align: left;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-faint);
    padding: 0 10px 8px;
    border-bottom: 1px solid var(--border-soft);
  }

  td {
    padding: 10px;
    color: var(--text);
    border-bottom: 1px solid var(--border-soft);
  }

  .num {
    text-align: right;
  }

  .center {
    text-align: center;
  }

  .led {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    vertical-align: middle;
  }

  .led.green {
    background: var(--led-ok);
    box-shadow: var(--led-ok-glow);
  }

  .led.red {
    background: var(--danger);
    box-shadow: 0 0 6px var(--danger);
  }
</style>
