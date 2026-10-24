import { invoke } from "@tauri-apps/api/core";

const MAX_ROWS = 500;
const session = crypto.randomUUID();

/** @typedef {{ id: number, ts: string, session: string, tag: string, path: string, label: string, context: string | null }} EventRow */

/** Newest first. Shown in the sidebar, capped to MAX_ROWS (the SQL file keeps everything). */
/** @type {EventRow[]} */
export const eventLog = $state([]);

export async function loadEvents() {
  try {
    const rows = await invoke("get_events", { limit: MAX_ROWS });
    eventLog.splice(0, eventLog.length, ...rows);
  } catch (err) {
    console.error("get_events failed", err);
  }
}

/** @param {Element} el */
function describe(el) {
  const text = el.getAttribute("aria-label") || el.getAttribute("title") || el.textContent || "";
  return text.replace(/\s+/g, " ").trim().slice(0, 120);
}

/** Short DOM path of up to 4 ancestors, e.g. "main.content > section.panel > button.cell". */
/** @param {Element} el */
function domPath(el) {
  /** @type {string[]} */
  const parts = [];
  /** @type {Element | null} */
  let node = el;
  for (; node && node !== document.body && parts.length < 4; node = node.parentElement) {
    const cls = node.classList[0];
    parts.unshift(cls ? `${node.tagName.toLowerCase()}.${cls}` : node.tagName.toLowerCase());
  }
  return parts.join(" > ");
}

const CLICKABLE = "button, a, input, select, textarea, label, [role='button'], [role='menuitem'], [role='tab'], [role='option']";

/** @param {MouseEvent} e */
function onClick(e) {
  if (!(e.target instanceof Element)) return;
  // Klick trifft oft ein Kind (svg, span) -> auf das bedienbare Element hochgehen
  const el = e.target.closest(CLICKABLE) ?? e.target;
  if (el.closest("[data-no-log]")) return;

  const event = {
    ts: new Date().toISOString(),
    session,
    tag: el.tagName.toLowerCase(),
    path: domPath(el),
    label: describe(el) || "(ohne Text)",
    context: el.closest("[role='dialog']")?.getAttribute("aria-label") ?? null,
  };

  eventLog.unshift({ id: -1, ...event });
  if (eventLog.length > MAX_ROWS) eventLog.pop();

  invoke("log_event", { event }).catch((err) => console.error("log_event failed", err));
}

/** Logs every click in the window. Returns the cleanup function. */
export function startEventLog() {
  document.addEventListener("click", onClick, true);
  return () => document.removeEventListener("click", onClick, true);
}
