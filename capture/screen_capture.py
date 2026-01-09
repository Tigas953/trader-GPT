# capture/screen_capture.py

from PIL import ImageGrab
from pathlib import Path
from datetime import datetime
from ocr.screen_selector import ScreenRegion


CAPTURE_DIR = Path("capture/screenshots")


def capture_screen(region: ScreenRegion) -> Path:
    """
    Captura uma imagem da região informada e salva em disco.

    Parâmetros:
        region (ScreenRegion): região da tela a ser capturada

    Retorna:
        Path: caminho do arquivo de imagem salvo

    Exceções:
        ValueError: se a região for inválida
        RuntimeError: se a captura falhar
    """
    if region.width <= 0 or region.height <= 0:
        raise ValueError("Região de captura inválida")

    CAPTURE_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = CAPTURE_DIR / f"capture_{timestamp}.png"

    image = ImageGrab.grab(
        bbox=(
            region.x,
            region.y,
            region.x + region.width,
            region.y + region.height,
        )
    ).convert("RGB")

    image.save(filename)

    if not filename.exists():
        raise RuntimeError("Falha ao salvar captura de tela")

    return filename
