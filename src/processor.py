import os

from src.duplicate_checker import verificar_status_arquivo
from src.hash_utils import calcular_hash_arquivo
from src.logger import registrar_envio
from src.pdf_reader import extrair_dados_pedido
from src.file_manager import mover_para_enviados


def processar_pedido(caminho_pdf, callback_ui=None):
    nome_arquivo = os.path.basename(caminho_pdf)

    print("\n" + "=" * 60)
    print(f"Processando: {nome_arquivo}")
    print("=" * 60)

    try:
        if callback_ui:
            callback_ui("log", f"PDF encontrado: {nome_arquivo}")

        hash_arquivo = calcular_hash_arquivo(caminho_pdf)
        status_arquivo = verificar_status_arquivo(nome_arquivo, hash_arquivo)

        if status_arquivo == "DUPLICADO":
            print("Arquivo já enviado anteriormente sem alteração.")

            if callback_ui:
                callback_ui("log", "Arquivo duplicado ignorado.")

            return

        if status_arquivo == "NOVO":
            print("Pedido novo.")
            if callback_ui:
                callback_ui("log", "Pedido novo identificado.")

        if status_arquivo == "ALTERADO":
            print("Pedido alterado. O arquivo será reprocessado.")
            if callback_ui:
                callback_ui("log", "Pedido alterado identificado.")

        print("Lendo dados do PDF...")

        if callback_ui:
            callback_ui("log", "Extraindo dados do PDF...")

        dados = extrair_dados_pedido(caminho_pdf)

        print("\nDados extraídos:")
        print("-" * 60)
        print("Pedido       :", dados.get("pedido"))
        print("Cliente      :", dados.get("cliente"))
        print("CNPJ         :", dados.get("cnpj_cliente"))
        print("Cidade       :", dados.get("cidade"), "-", dados.get("uf"))
        print("Emissão      :", dados.get("emissao"))
        print("Condição     :", dados.get("condicao_pagamento"))
        print("Valor Pedido : R$", dados.get("valor_pedido"))
        print("Valor NF     : R$", dados.get("valor_nf"))
        print("Produto      :", dados.get("produto"))
        print("-" * 60)

        mensagem = montar_mensagem(dados, status_arquivo)

        print("\nMensagem gerada:")
        print("-" * 60)
        print(mensagem)
        print("-" * 60)

        status_envio = "REENVIADO" if status_arquivo == "ALTERADO" else "ENVIADO"

        registrar_envio(
            arquivo=nome_arquivo,
            pedido=dados.get("pedido"),
            cliente=dados.get("cliente"),
            hash_arquivo=hash_arquivo,
            status=status_envio,
            mensagem=mensagem
        )

        if callback_ui:
            callback_ui("log", "Registro gravado no banco SQLite.")

        destino = mover_para_enviados(caminho_pdf)

        if callback_ui:
            callback_ui("pedido", dados)
            callback_ui("log", f"Arquivo movido para: {destino}")

        print(f"Arquivo movido para: {destino}")
        print(f"Finalizado com sucesso. Status: {status_envio}")

    except Exception as erro:
        print(f"Erro ao processar o arquivo {nome_arquivo}: {erro}")

        registrar_envio(
            arquivo=nome_arquivo,
            status="ERRO",
            mensagem=str(erro)
        )

        if callback_ui:
            callback_ui("log", f"Erro ao processar {nome_arquivo}: {erro}")


def montar_mensagem(dados, status_arquivo):
    pedido = dados.get("pedido") or "Não identificado"
    cliente = dados.get("cliente") or "Não identificado"
    cidade = dados.get("cidade") or "Não identificada"
    uf = dados.get("uf") or ""
    emissao = dados.get("emissao") or "Não identificada"
    condicao = dados.get("condicao_pagamento") or "Não identificada"
    valor_pedido = dados.get("valor_pedido") or "Não identificado"
    valor_nf = dados.get("valor_nf") or "Não identificado"
    produto = dados.get("produto") or "Não identificado"

    titulo = "Pedido alterado" if status_arquivo == "ALTERADO" else "Novo pedido disponível"

    return f"""
📦 ERP ORDER MESSENGER

{titulo}.

Pedido: {pedido}
Cliente: {cliente}
Cidade: {cidade} - {uf}
Emissão: {emissao}
Condição: {condicao}

Valor do Pedido: R$ {valor_pedido}
Valor NF: R$ {valor_nf}

Produto:
{produto}

Pedido processado e disponível para acompanhamento.
""".strip()