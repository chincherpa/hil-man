<script>
  import { invoke } from '@tauri-apps/api/core';
  import { onMount } from 'svelte';

  let hilName = '';
  let time = '';

  async function loadHilName() {
    try {
      /** @type {{ section: string, key: string, value: string }[]} */
      const entries = await invoke('get_settings');
      hilName = entries.find((e) => e.section === 'Katana' && e.key === 'hil_name')?.value ?? '';
    } catch (err) {
      console.error('Failed to load settings:', err);
    }
  }

  onMount(async () => {
    await loadHilName();
    window.addEventListener('settings-changed', loadHilName);

    const updateTime = () => {
      const now = new Date();
      const formatter = new Intl.DateTimeFormat('de-DE', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
      time = formatter.format(now);
    };

    updateTime();
    setInterval(updateTime, 1000);
  });
</script>

<footer class="statusbar">
  <div class="left">{hilName}</div>
  <div class="right">
    <span class="badge warn">DEVELOPMENT</span>
    <span class="time">{time}</span>
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

  .left {
    flex: 0 0 auto;
  }

  .right {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .time {
    white-space: nowrap;
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
