from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time

from src.processor import processar_pedido


class MonitorPedidos(FileSystemEventHandler):

    def __init__(self, callback_ui=None):
        super().__init__()
        self.callback_ui = callback_ui
        self.arquivos_em_processamento = set()

    def on_created(self, event):
        if event.is_directory:
            return

        caminho_arquivo = event.src_path

        if not caminho_arquivo.lower().endswith(".pdf"):
            return

        if caminho_arquivo in self.arquivos_em_processamento:
            return

        self.arquivos_em_processamento.add(caminho_arquivo)

        try:
            time.sleep(2)

            processar_pedido(
                caminho_pdf=caminho_arquivo,
                callback_ui=self.callback_ui
            )

        finally:
            self.arquivos_em_processamento.discard(caminho_arquivo)


def iniciar_monitoramento(pasta, callback_ui=None):
    observer = Observer()

    observer.schedule(
        MonitorPedidos(callback_ui),
        path=pasta,
        recursive=False
    )

    observer.start()

    print("=" * 60)
    print("ERP ORDER MESSENGER")
    print("=" * 60)
    print(f"Monitorando pasta:\n{pasta}")
    print("=" * 60)

    if callback_ui:
        callback_ui("log", f"Monitorando pasta: {pasta}")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()