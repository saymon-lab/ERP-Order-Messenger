import threading

from config import PASTA_PENDENTES
from src.logger import criar_tabela_envios
from src.monitor import iniciar_monitoramento
from src.ui.main_window import MainWindow


def main():
    criar_tabela_envios()

    app = MainWindow()

    def callback_ui(tipo, dados):
        if tipo == "log":
            app.after(0, app.adicionar_log, dados)

        elif tipo == "pedido":
            app.after(0, app.atualizar_ultimo_pedido, dados)

    thread_monitor = threading.Thread(
        target=iniciar_monitoramento,
        args=(str(PASTA_PENDENTES), callback_ui),
        daemon=True
    )

    thread_monitor.start()

    app.mainloop()


if __name__ == "__main__":
    main()