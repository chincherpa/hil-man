// Static placeholder data — wiring to real backend commands follows later.

export const processButtons = ["ControlDesk", "Diagnosis", "EXAM", "FEA", "VR", "RSI", "Overview"];

export const processDialogButtons = ["Start", "Stopp", "Status prüfen", "Protokoll", "Konfiguration", "Export"];

export const controlDeskButtons = ["Stop modell", "Reload + start modell", "Start modell"];

export const svn = { current: 12345, newest: 12367 };

export const examButtons = ["to Prio0-TestSuite", "EX.e Prio0", "EX.e PUDIS"];

export const diagnosisButtons = ["PUDIS", "Flashen (SW, ZDC)", "Read Error Memory", "Open pDiagTA-GUI"];

/** @type {"NAR" | "RDW" | null} */
export const activeDiagnosis = null;

export const signals = [
  { name: "Signal 1", soll: 1, ist: 1, led: "green" },
  { name: "Signal 2", soll: 2, ist: 2, led: "green" },
  { name: "Signal 3", soll: 3, ist: 0, led: "red" },
  { name: "Signal 4", soll: 4, ist: 0, led: "red" },
];

export const clampItems = ["Clamp 30", "Clamp 15", "Clamp S"];
