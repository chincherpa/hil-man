export const THEMES = [
  { id: "dark", label: "Dunkel" },
  { id: "light", label: "Hell" },
  { id: "midnight", label: "Midnight Blue" },
  { id: "highvis", label: "High-Vis" },
  { id: "cyberpunk", label: "Cyberpunk" },
  { id: "8bit", label: "8-Bit" },
];
export const DEFAULT_THEME = "dark";
export const THEME_IDS = THEMES.map((t) => t.id);

/** @param {string | null} value */
export function normalizeTheme(value) {
  return value !== null && THEME_IDS.includes(value) ? value : DEFAULT_THEME;
}

/** @returns {string} */
export function readStoredTheme() {
  try {
    return normalizeTheme(localStorage.getItem("theme"));
  } catch {
    return DEFAULT_THEME;
  }
}

/** @param {string} id */
export function applyTheme(id) {
  document.documentElement.dataset.theme = id;
}

/** @param {string} id */
export function persistTheme(id) {
  try {
    localStorage.setItem("theme", id);
  } catch {
    // storage blocked -> theme still applies for this session
  }
}
