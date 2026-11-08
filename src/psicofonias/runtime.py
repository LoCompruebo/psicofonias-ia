"""Prioridad baja para los cálculos largos (Windows)."""
import ctypes
import sys


def prioridad_baja() -> None:
    if sys.platform == "win32":
        BELOW_NORMAL = 0x00004000
        h = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.kernel32.SetPriorityClass(h, BELOW_NORMAL)
