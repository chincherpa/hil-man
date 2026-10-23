<script>
  let { name, size = 16 } = $props();

  const paths = {
    bell: "M12 22a2 2 0 0 0 2-2H10a2 2 0 0 0 2 2ZM18 16v-5a6 6 0 1 0-12 0v5l-2 2v1h16v-1l-2-2Z",
    settings:
      "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm8-3a7.9 7.9 0 0 0-.14-1.5l2.11-1.65-2-3.46-2.49 1a8 8 0 0 0-2.6-1.5L14.5 2h-5l-.38 2.9a8 8 0 0 0-2.6 1.5l-2.49-1-2 3.46L3.14 10.5A7.9 7.9 0 0 0 3 12c0 .51.05 1.01.14 1.5L2.03 15.15l2 3.46 2.49-1a8 8 0 0 0 2.6 1.5L9.5 22h5l.38-2.9a8 8 0 0 0 2.6-1.5l2.49 1 2-3.46-2.11-1.65c.09-.49.14-.99.14-1.5Z",
    chat: "M4 4h16v12H7l-3 3Z",
    sun: "M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10ZM12 1v3M12 20v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M1 12h3M20 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1",
    chevronDown: "M6 9l6 6 6-6",
    check: "M5 13l4 4L19 7",
    info: "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm0 5h.01M11 11h2v6h-2Z",
    push: "M12 3v12m0 0-4-4m4 4 4-4M4 21h16",
    stop: "M6 6h12v12H6Z",
    refresh: "M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3M4 4v5h5M20 20v-5h-5",
    grid: "M4 4h7v7H4ZM13 4h7v7h-7ZM4 13h7v7H4ZM13 13h7v7h-7Z",
    download: "M12 3v12m0 0-4-4m4 4 4-4M4 19h16",
    copy: "M9 9h10v10H9ZM5 5h10v10H5V5Z",
    trash: "M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13",
    power: "M12 2v9M6.3 6.3a8 8 0 1 0 11.4 0",
    minimize: "M5 12h14",
    maximize: "M5 5h14v14H5Z",
    close: "M5 5l14 14M19 5L5 19",
  };
</script>

<svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <path d={paths[/** @type {keyof typeof paths} */ (name)] ?? ""} />
</svg>
