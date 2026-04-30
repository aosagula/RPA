"""
Módulo de login para DUX usando Playwright.
Reutilizable por cualquier proceso que necesite autenticarse en el sistema.
"""
import sys
import os
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, BrowserContext

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as cfg


USERNAME_ID = "ctl00_ContentPlaceHolder1_txUsuario"
PASSWORD_ID = "ctl00_ContentPlaceHolder1_txPassword"
LOGIN_BTN_ID = "ctl00_ContentPlaceHolder1_cmdAceptar"


class DuxLoginError(Exception):
    pass


class DuxSession:
    """
    Gestiona una sesión autenticada en DUX usando Playwright.

    Uso como context manager:
        with DuxSession() as session:
            session.page.goto("http://...")

    Uso manual:
        session = DuxSession()
        session.start()
        # ... usar session.page ...
        session.close()
    """

    def __init__(self, url: str = None, username: str = None, password: str = None, headless: bool = False):
        self.url = url or cfg.config.dux_url
        self.username = username or cfg.config.dux_username
        self.password = password or cfg.config.dux_password
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._context: BrowserContext = None
        self.page: Page = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start(self):
        """Inicia el navegador y realiza el login."""
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.firefox.launch(headless=self.headless)
        self._context = self._browser.new_context()
        self.page = self._context.new_page()
        self._login()
        return self

    def _login(self):
        print(f"[{_now()}] Autenticando en {self.url} ...")
        self.page.goto(self.url)

        self.page.wait_for_selector(f"#{USERNAME_ID}", timeout=15000)
        self.page.fill(f"#{USERNAME_ID}", self.username)
        self.page.fill(f"#{PASSWORD_ID}", self.password)
        self.page.click(f"#{LOGIN_BTN_ID}")

        # Esperar que la navegación post-login se complete
        self.page.wait_for_load_state("networkidle", timeout=20000)

        # Verificar que el login fue exitoso (no volvió a la página de login)
        if LOGIN_BTN_ID in self.page.content():
            raise DuxLoginError("Login fallido: credenciales inválidas o error en el sistema.")

        print(f"[{_now()}] Login exitoso. URL actual: {self.page.url}")

    def get_cookies(self) -> list[dict]:
        """Retorna las cookies de sesión actuales (útil para crawl4ai u otros clientes HTTP)."""
        return self._context.cookies()

    def close(self):
        """Cierra el navegador y libera recursos."""
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        print(f"[{_now()}] Sesión cerrada.")


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
