# ocr/screen_selector.py

from dataclasses import dataclass
import pyautogui


@dataclass(frozen=True)
class ScreenRegion:
    x: int
    y: int
    width: int
    height: int


def select_region() -> ScreenRegion:
    """
    Seleção manual da área da tela.
    Retorna coordenadas absolutas.
    """
    region = pyautogui.selectRegion()
    if region is None:
        raise RuntimeError("Seleção de tela cancelada pelo usuário")

    x, y, width, height = region

    if width <= 0 or height <= 0:
        raise ValueError("Região inválida selecionada")

    return ScreenRegion(x=x, y=y, width=width, height=height)
