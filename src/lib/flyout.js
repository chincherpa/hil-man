import { getCurrentWindow, LogicalSize, PhysicalPosition, Window } from "@tauri-apps/api/window";
import { listen } from "@tauri-apps/api/event";
import { readStoredTheme, applyTheme, THEME_EVENT } from "$lib/themes.js";

export const TAB_WIDTH = 18;
export const MENU_WIDTH = 200;
export const TAB_HEIGHT = 48;

// Abstand Tab-Oberkante zur Oberkante des Main-Fensters (Titlebar 44 + Content-Offset 12 + Tab-Top 81)
const TAB_TOP = 137;

const self = getCurrentWindow();
/** @type {Window | null} */
let main = null;
let width = TAB_WIDTH;

/** Flyout rechts bündig an die linke Kante von Main, Tab-Höhe ausgerichtet */
async function place() {
  if (!main) return;
  // innerPosition: outerPosition enthält unsichtbaren Resize-Rand (~8px)
  const [pos, scale] = await Promise.all([main.innerPosition(), main.scaleFactor()]);
  await self.setPosition(new PhysicalPosition(pos.x - width * scale, pos.y + TAB_TOP * scale));
}

/**
 * @param {number} w
 * @param {number} h
 */
export async function resizeFlyout(w, h) {
  width = w;
  await self.setSize(new LogicalSize(w, h));
  await place();
}

/** Nur im Flyout-Window aufrufen */
export async function initFlyout() {
  document.documentElement.style.background = "transparent";
  document.body.style.background = "transparent";

  applyTheme(readStoredTheme());

  // localStorage ist nicht reaktiv zwischen Fenstern -> Theme-Wechsel kommt per Tauri-Event
  await listen(THEME_EVENT, (e) => applyTheme(/** @type {string} */ (e.payload)));

  main = await Window.getByLabel("main");
  if (!main) return;

  await main.onMoved(place);
  await main.onResized(place);
  // Windows clampt beim Erzeugen auf Mindestbreite (136px), daher Größe nachträglich setzen
  await resizeFlyout(TAB_WIDTH, TAB_HEIGHT);
  await self.show();
}
