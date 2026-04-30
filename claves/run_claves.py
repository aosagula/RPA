"""
Script: extracción de claves diarias DUX.
Usa DuxUtil para login y obtención de claves.

Uso:
    cd c:\prg\RPA
    python claves/run_claves.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from varios.dux_util import DuxUtil


def main():
    with DuxUtil() as dux:
        dux.login()
        registros = dux.claves()

    print(f"\n--- Claves ({len(registros)} registros) ---")
    for r in registros:
        print(r)


if __name__ == "__main__":
    main()
