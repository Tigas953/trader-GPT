# ui/tabs/operacao_tab.py
import tkinter as tk
from tkinter import ttk


class OperacaoTab:
    def __init__(self, parent, engine):
        self.engine = engine

        # Frame raiz da aba (OBRIGATÓRIO)
        self.frame = ttk.Frame(parent)

        # Conteúdo mínimo (placeholder)
        label = ttk.Label(
            self.frame,
            text="ABA OPERAÇÃO",
            font=("Arial", 14)
        )
        label.pack(padx=20, pady=20)

    def update_view(self, state_snapshot):
        """
        Atualiza a aba conforme o estado do sistema.
        (por enquanto vazio)
        """
        pass
