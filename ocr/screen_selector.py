# ocr/screen_selector.py

import tkinter as tk
from typing import Optional
from dataclasses import dataclass


# =====================================================
# CONTRATO ÚNICO DE REGIÃO DE TELA
# =====================================================

@dataclass(frozen=True)
class ScreenRegion:
    """
    Representa uma região fixa da tela.

    Responsabilidade:
    - Armazenar coordenadas
    - Validar integridade
    - Converter para / de dict

    NÃO:
    - Captura tela
    - Executa OCR
    - Persiste dados
    """

    x: int
    y: int
    width: int
    height: int

    def is_valid(self) -> bool:
        return (
            self.x >= 0
            and self.y >= 0
            and self.width > 0
            and self.height > 0
        )

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }

    @staticmethod
    def from_dict(data: dict) -> "ScreenRegion":
        return ScreenRegion(
            x=int(data["x"]),
            y=int(data["y"]),
            width=int(data["width"]),
            height=int(data["height"]),
        )


# =====================================================
# SELETOR VISUAL DE REGIÃO
# =====================================================

class ScreenSelector:
    """
    Seletor genérico de área da tela.

    Responsabilidade ÚNICA:
    - Permitir seleção manual de uma região da tela
    - Retornar um ScreenRegion válido ou None

    NÃO:
    - Decide finalidade (OCR ou GPT)
    - Persiste dados
    - Interage com Engine, IA ou Timer
    """

    def __init__(self):
        self._root = None
        self._canvas = None

        self._start_x = 0
        self._start_y = 0
        self._end_x = 0
        self._end_y = 0

        self._rect = None
        self._selection: Optional[ScreenRegion] = None

    # =====================================================
    # API PÚBLICA
    # =====================================================

    def select_area(self) -> Optional[ScreenRegion]:
        """
        Inicia o modo de seleção visual.
        Retorna ScreenRegion ou None se cancelado.
        """
        self._root = tk.Tk()
        self._root.attributes("-fullscreen", True)
        self._root.attributes("-alpha", 0.3)
        self._root.configure(background="black")
        self._root.title("Selecione a área desejada")

        self._canvas = tk.Canvas(
            self._root,
            cursor="cross",
            bg="black",
            highlightthickness=0,
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)

        self._bind_events()
        self._root.mainloop()

        return self._selection

    # =====================================================
    # EVENTOS
    # =====================================================

    def _bind_events(self):
        self._canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self._canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self._canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
        self._root.bind("<Escape>", self._on_cancel)

    def _on_mouse_press(self, event):
        self._start_x = event.x
        self._start_y = event.y

        if self._rect:
            self._canvas.delete(self._rect)

        self._rect = self._canvas.create_rectangle(
            self._start_x,
            self._start_y,
            self._start_x,
            self._start_y,
            outline="red",
            width=2,
        )

    def _on_mouse_drag(self, event):
        self._end_x = event.x
        self._end_y = event.y

        self._canvas.coords(
            self._rect,
            self._start_x,
            self._start_y,
            self._end_x,
            self._end_y,
        )

    def _on_mouse_release(self, event):
        self._end_x = event.x
        self._end_y = event.y

        x1 = min(self._start_x, self._end_x)
        y1 = min(self._start_y, self._end_y)
        x2 = max(self._start_x, self._end_x)
        y2 = max(self._start_y, self._end_y)

        region = ScreenRegion(
            x=x1,
            y=y1,
            width=x2 - x1,
            height=y2 - y1,
        )

        self._selection = region if region.is_valid() else None
        self._close()

    def _on_cancel(self, event=None):
        self._selection = None
        self._close()

    # =====================================================
    # FINALIZAÇÃO
    # =====================================================

    def _close(self):
        if self._root:
            self._root.destroy()
            self._root = None
