# ui/app.py

import tkinter as tk
from tkinter import ttk

from ui.tabs.operacao_tab import OperacaoTab
from ui.tabs.ia_tab import IATab
from ui.tabs.pos_trade_tab import PosTradeTab
from ui.tabs.estatisticas_tab import EstatisticasTab
from ui.tabs.custos_logs_tab import CustosLogsTab
from ui.tabs.sistema_tab import SistemaTab
from ui.tabs.help_tab import HelpTab


class TraderGPTApp:
    """
    Interface gráfica do Trader GPT.
    Atua APENAS como espelho do estado do sistema.
    """

    def __init__(self, engine):
        self.engine = engine

        self.root = tk.Tk()
        self.root.title("Trader GPT")
        self.root.geometry("1200x800")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tabs = {}
        self._create_tabs()

        self._refresh_ui()

    # =====================================================
    # CRIAÇÃO DAS ABAS
    # =====================================================

    def _create_tabs(self):
        self.tabs["operacao"] = OperacaoTab(self.notebook, self.engine)
        self.tabs["ia"] = IATab(self.notebook, self.engine)
        self.tabs["pos_trade"] = PosTradeTab(self.notebook, self.engine)
        self.tabs["estatisticas"] = EstatisticasTab(self.notebook, self.engine)
        self.tabs["custos_logs"] = CustosLogsTab(self.notebook, self.engine)
        self.tabs["sistema"] = SistemaTab(self.notebook, self.engine)
        self.tabs["help"] = HelpTab(self.notebook)

        for name, tab in self.tabs.items():
            self.notebook.add(tab.frame, text=name.upper())

    # =====================================================
    # ATUALIZAÇÃO DA UI (ESPELHO DO SISTEMA)
    # =====================================================

    def _refresh_ui(self):
        """
        Atualiza todas as abas com base no estado real do sistema.
        """
        try:
            state_snapshot = self.engine.get_state_snapshot()
        except Exception as e:
            print(f"[UI] Erro ao obter estado do sistema: {e}")
            self.root.after(500, self._refresh_ui)
            return

        for tab in self.tabs.values():
            if hasattr(tab, "update_view"):
                try:
                    tab.update_view(state_snapshot)
                except Exception as e:
                    print(f"[UI] Erro ao atualizar aba: {e}")

        self.root.after(500, self._refresh_ui)

    # =====================================================
    # LOOP PRINCIPAL
    # =====================================================

    def run(self):
        self.root.mainloop()
