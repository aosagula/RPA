"""
Punto de entrada del proceso Claves.

Uso:
    cd c:\prg\RPA
    python claves/main.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from varios.dux_login import DuxSession, DuxLoginError
from claves.claves import Claves


def main():
    try:
        with DuxSession() as session:
            proceso = Claves(session)
            registros = proceso.ejecutar()
            print(f"\n--- Claves ({len(registros)} registros) ---")
            for r in registros:
                print(r)
    except DuxLoginError as e:
        print(f"ERROR de login: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        raise


if __name__ == "__main__":
    main()
