"""Stoppt die Real-Time-Application der Hauptplattform im aktiven ControlDesk-Experiment.

COM-Zugriff analog KI-Tools/ControlDeskHandler (Dispatch, find_main_platform,
RealTimeApplications[0].Stop()), aber ohne den kompletten Handler: dessen
__init__ liest SDF-/Experimentpfade, braucht tkinter/lxml und verschluckt Fehler.
"""

import sys

# Plattform-Typ der Hauptplattform (Multiprozessor-/Gruppenplattform), siehe KI-Tools
MAIN_PLATFORM_TYPE = 22


def connect_control_desk():
    try:
        import pythoncom
        from win32com.client import Dispatch
    except ImportError as error:
        raise RuntimeError(f"pywin32 nicht installiert ({error}).") from error

    pythoncom.CoInitialize()
    try:
        return Dispatch("ControlDeskNG.Application")
    except Exception as error:
        raise RuntimeError(f"ControlDesk nicht erreichbar: {error}") from error


def find_main_platform(application):
    try:
        experiment = application.ActiveExperiment
    except Exception:
        experiment = None
    if experiment is None:
        raise RuntimeError("Kein aktives Experiment in ControlDesk geöffnet.")

    platforms = list(experiment.Platforms)
    if not platforms:
        raise RuntimeError(f"Experiment '{experiment.Name}' hat keine Plattform.")

    for platform in platforms:
        if platform.Type == MAIN_PLATFORM_TYPE:
            return platform
    return platforms[0]


def stop_realtime_application():
    application = connect_control_desk()
    platform = find_main_platform(application)

    applications = list(platform.RealTimeApplications)
    if not applications:
        raise RuntimeError(f"Plattform '{platform.Name}' hat keine Real-Time-Application.")

    applications[0].Stop()
    return f"Modell gestoppt ({platform.Name})."


if __name__ == "__main__":
    try:
        print(stop_realtime_application())
    except Exception as error:
        print(error, file=sys.stderr)
        sys.exit(1)
