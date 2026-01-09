# ocr/screen_selector.py

import tkinter as tk
from typing import Optional, Dict


class ScreenSelector:
    """
    Seletor genérico de área da tela.
    Responsabilidade ÚNICA: permitir seleção manual de uma região da tela
    e retornar suas coordenadas.

    NÃO:
    - Decide finalidade (OCR ou GPT)
    - Salva configuração
    - Interage com Engine ou IA
    """

    def __init__(self):
        self._root = None
        self._canvas = None

        self._start_x = 0
        self._start_y = 0
        self._end_x = 0
        self._end_y = 0

        self._rect = None
        self._selection: Optional[Dict[str, int]] = None

    # =====================================================
    # API PÚBLICA
    # =====================================================

    def select_area(self) -> Optional[Dict[str, int]]:
        """
        Inicia o modo de seleção.
        Retorna um dicionário com x, y, width, height
        ou None se o usuário cancelar.
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
    # EVENTOS DE MOUSE / TECLADO
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

        width = x2 - x1
        height = y2 - y1

        if width <= 0 or height <= 0:
            self._selection = None
        else:
            self._selection = {
                "x": x1,
                "y": y1,
                "width": width,
                "height": height,
            }

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
