import tkinter as tk

from tkinter import ttk


class OperacaoTab:
    def __init__(self, notebook, engine):
        self.engine = engine
        self.frame = ttk.Frame(notebook)

        self._build_ui()

    def _build_ui(self):
        self.lbl_status = ttk.Label(self.frame, text="Estado: —")
        self.lbl_status.pack(pady=10)

        self.btn_pre_trade = ttk.Button(
            self.frame,
            text="Análise Pré-Trade",
            command=self._on_pre_trade,
        )
        self.btn_pre_trade.pack(pady=5)

        self.btn_abrir_trade = ttk.Button(
            self.frame,
            text="Abrir Trade",
            command=self._on_open_trade,
        )
        self.btn_abrir_trade.pack(pady=5)

        self.btn_encerrar_trade = ttk.Button(
            self.frame,
            text="Encerrar Trade",
            command=self._on_close_trade,
        )
        self.btn_encerrar_trade.pack(pady=5)

    # ===============================
    # AÇÕES → ENGINE
    # ===============================

    def _on_pre_trade(self):
        # IA real entra depois — aqui só valida fluxo
        print("Pré-trade solicitado")

    def _on_open_trade(self):
        try:
            self.engine.abrir_trade()
        except Exception as e:
            print(e)

    def _on_close_trade(self):
        try:
            self.engine.encerrar_trade()
        except Exception as e:
            print(e)

    # ===============================
    # ATUALIZAÇÃO VISUAL
    # ===============================

    def update_view(self, state):
        self.lbl_status.config(
            text=f"IA: {state['ia_state']} | Trade: {state['trade_state']}"
        )

        # Bloqueios visuais
        self.btn_pre_trade.config(
            state="normal" if state["trade_state"] == "INEXISTENTE" else "disabled"
        )

        self.btn_abrir_trade.config(
            state="normal" if state["trade_state"] == "INEXISTENTE" else "disabled"
        )

        self.btn_encerrar_trade.config(
            state="normal" if state["trade_state"] == "ABERTO" else "disabled"
        )
