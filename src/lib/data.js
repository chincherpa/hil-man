// Static placeholder data — wiring to real backend commands follows later.

export const mainProcesses = [
  { id: 1, label: "ControlDesk - Kalibrierung", checked: true, expandable: false },
  { id: 2, label: "Absturzdiagnose", checked: true, expandable: false },
  { id: 3, label: "Model Reload", checked: true, expandable: true },
  { id: 4, label: "Modulinitialisierung", checked: true, expandable: false },
  { id: 5, label: "Fahrzeuginitialisierung", checked: true, expandable: false },
  { id: 6, label: "Nachtlaufvorbereit...", checked: true, expandable: false },
];

export const extraActions = [
  { label: "Usim Start", checked: false, expandable: true },
  { label: "Flashen", checked: false, expandable: false },
  { label: "FSP lesen", checked: false, expandable: false },
  { label: "Refresh all Layouts", checked: null, expandable: true, icon: "refresh" },
  { label: "Einzelprozesse", checked: null, expandable: true, icon: "grid" },
];

export const setupPresets = [
  { id: "none", label: "Keine Auswahl" },
  { id: "default", label: "Default Setup" },
  { id: "erweitert", label: "Erweitertes Setup" },
  { id: "nachtlauf", label: "Nachtlauf Setup" },
];

export const controlModes = ["Automatisch", "Nachfragend", "Schrittweise"];

export const features = [
  { label: "Info & Hilfe", badge: "F1", icon: "info" },
  { label: "Feedback & Support", icon: "chat" },
  { label: "Push Aktiv Layout", icon: "push" },
  { label: "RuntimeAgent stoppen", icon: "stop", toggle: true, active: true },
];

export const statusItems = [
  { label: "GENERIC", kind: "badge" },
  { label: "RUNTIMEAGENT", kind: "text" },
  { label: "AKTIV", kind: "dot-ok" },
  { label: "ControlDesk", kind: "dot-ok" },
  { label: "Echtzeit", kind: "text" },
  { label: "Module", kind: "text" },
  { label: "Usim", kind: "dot-ok" },
];
