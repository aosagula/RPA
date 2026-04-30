"""
DuxUtil: clase utilitaria que expone operaciones del sistema DUX como métodos.
Centraliza login y acceso a funcionalidades, reutilizable desde cualquier script.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from varios.dux_login import DuxSession, DuxLoginError


class DuxUtil:
    """
    Interfaz de alto nivel para operar el sistema DUX.

    Uso como context manager (recomendado):
        with DuxUtil() as dux:
            dux.login()
            registros = dux.claves()

    Uso manual:
        dux = DuxUtil()
        dux.login()
        registros = dux.claves()
        dux.cerrar()
    """

    def __init__(self, headless: bool = False):
        self.headless = headless
        self._session: DuxSession = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cerrar()

    # ─── Sesión ────────────────────────────────────────────────────────────────

    def login(self):
        """Inicia el navegador y autentica en DUX."""
        self._session = DuxSession(headless=self.headless)
        self._session.start()

    def cerrar(self):
        """Cierra el navegador y libera recursos."""
        if self._session:
            self._session.close()
            self._session = None

    def _check_session(self):
        if not self._session:
            raise RuntimeError("Llamar a login() antes de usar este método.")

    # ─── Operaciones ───────────────────────────────────────────────────────────

    def claves(self) -> list[dict]:
        """
        Navega al menú Sistema > Utilitarios > Claves y retorna la tabla de claves diarias.
        Cada elemento es un dict con las columnas de la tabla.
        """
        self._check_session()
        from claves.claves import Claves
        return Claves(self._session).ejecutar()
