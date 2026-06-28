import shutil
from pathlib import Path
from datetime import datetime

from config import PASTA_ENVIADOS


def mover_para_enviados(caminho_pdf):
    origem = Path(caminho_pdf)

    # Ex.: 2026-06
    pasta_mes = datetime.now().strftime("%Y-%m")

    destino_pasta = PASTA_ENVIADOS / pasta_mes
    destino_pasta.mkdir(parents=True, exist_ok=True)

    destino = destino_pasta / origem.name

    # Evita sobrescrever caso exista um arquivo com o mesmo nome
    if destino.exists():
        hora = datetime.now().strftime("%H%M%S")
        destino = destino_pasta / f"{origem.stem}_{hora}{origem.suffix}"

    shutil.move(str(origem), str(destino))

    return destino