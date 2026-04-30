"""
Proceso: Claves
Accede al menú Claves del sistema DUX y extrae su contenido.

Flujo:
  1. Login con DuxSession (Playwright)
  2. Navegar al menú Claves (extrayendo href del DOM)
  3. Extraer HTML de la página con Playwright (ya autenticado)
"""
import sys
import os
from datetime import datetime
import time
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from varios.dux_login import DuxSession


# ─── Selectores del menú ────────────────────────────────────────────────────────
SEL_CLAVES = "a[href*='ZZC015P001.aspx']"   # link a Claves (en DOM aunque esté oculto)
# ────────────────────────────────────────────────────────────────────────────────


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Claves:
    """
    Proceso que accede al menú Claves del sistema DUX.
    Requiere una sesión activa de DuxSession.
    """

    def __init__(self, session: DuxSession):
        self.session = session
        self.page = session.page
        self.claves_url: str = None

    def navegar_a_claves(self) -> str:
        """
        Navega a la página de Claves extrayendo el href directamente del DOM.
        Los ítems anidados del menú ASPX están en el DOM aunque tengan display:none.
        Retorna la URL final de la página de claves.
        """
        time.sleep(5)

        print(f"[{_now()}] Buscando href de Claves en el DOM ...")

        link = self.page.locator(SEL_CLAVES).first
        href = link.get_attribute("href", timeout=10000)

        if not href:
            raise RuntimeError("No se encontró el link de Claves en el DOM.")

        base_url = self.page.url.rsplit("/", 1)[0]
        self.claves_url = href if href.startswith("http") else f"{base_url}/{href}"

        print(f"[{_now()}] Navegando a: {self.claves_url}")
        self.page.goto(self.claves_url)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self.claves_url = self.page.url
        print(f"[{_now()}] Página de claves cargada: {self.claves_url}")
        return self.claves_url

    def extraer_tabla(self) -> list[dict]:
        """
        Extrae las filas de la tabla de claves diarias.
        Parsea #ctl00_ContentPlaceHolder1_tablaGeneral del HTML de la página actual.
        Retorna lista de dicts con las columnas dinámicas de la tabla.
        """
        if not self.claves_url:
            raise ValueError("Primero llamar a navegar_a_claves()")

        print(f"[{_now()}] Parseando tabla de claves ...")
        html = self.page.content()
        soup = BeautifulSoup(html, "html.parser")

        tabla = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_tablaGeneral"})
        if not tabla:
            raise RuntimeError("No se encontró la tabla de claves en la página.")

        filas_th = tabla.find_all("tr")

        # Construir cabeceras combinando fila 1 (grupo) y fila 2 (subgrupo)
        cabecera_grupo   = [th.get_text(strip=True) for th in filas_th[0].find_all("th")]
        cabecera_subgrupo = [th.get_text(strip=True) for th in filas_th[1].find_all("th")]
        columnas = []
        for grupo, sub in zip(cabecera_grupo, cabecera_subgrupo):
            columnas.append(f"{grupo} {sub}".strip() if sub else grupo)

        # Extraer filas de datos
        registros = []
        for fila in filas_th[2:]:
            celdas = [td.get_text(strip=True) for td in fila.find_all("td")]
            if celdas:
                registros.append(dict(zip(columnas, celdas)))

        print(f"[{_now()}] {len(registros)} registros extraídos.")
        return registros

    def ejecutar(self) -> list[dict]:
        """Ejecuta el proceso completo: navegar + extraer tabla."""
        self.navegar_a_claves()
        return self.extraer_tabla()
