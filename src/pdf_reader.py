import re
import pdfplumber


def ler_pdf(caminho_pdf):
    texto = ""

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            conteudo = pagina.extract_text()
            if conteudo:
                texto += conteudo + "\n"

    return texto


def limpar_texto(valor):
    if not valor:
        return None

    return " ".join(valor.strip().split())


def extrair_cliente(texto):
    match = re.search(
        r"Cliente\.*:\s*([0-9\.]+)\s*([A-ZÀ-Úa-zà-ú0-9\s\-\&\.]+?)\s+CNPJ:",
        texto,
        re.IGNORECASE
    )

    if not match:
        return None, None

    codigo = match.group(1).replace(".", "").strip()
    nome = limpar_texto(match.group(2)).upper()

    return codigo, nome


def extrair_dados_pedido(caminho_pdf):
    texto = ler_pdf(caminho_pdf)

    dados = {
        "pedido": None,
        "emissao": None,
        "cliente": None,
        "codigo_cliente": None,
        "cnpj_cliente": None,
        "condicao_pagamento": None,
        "cidade": None,
        "uf": None,
        "produto": None,
        "valor_nf": None,
        "valor_pedido": None,
    }

    emissao = re.search(r"EMISSÃO\.?:\s*(\d{2}/\d{2}/\d{4})", texto, re.IGNORECASE)
    if emissao:
        dados["emissao"] = emissao.group(1)

    pedido = re.search(r"PEDIDO:\s*([\d\.]+)\s*/\s*(\d+)", texto, re.IGNORECASE)
    if pedido:
        dados["pedido"] = f"{pedido.group(1).replace('.', '')}/{pedido.group(2)}"

    codigo_cliente, cliente = extrair_cliente(texto)
    dados["codigo_cliente"] = codigo_cliente
    dados["cliente"] = cliente

    cnpj_cliente = re.search(r"Cliente.*?CNPJ:\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", texto, re.IGNORECASE | re.DOTALL)
    if cnpj_cliente:
        dados["cnpj_cliente"] = cnpj_cliente.group(1)

    condicao = re.search(
        r"Cond\. Pgto\.*:\s*(.+?)(?:\n|Endereço)",
        texto,
        re.IGNORECASE
    )
    if condicao:
        dados["condicao_pagamento"] = limpar_texto(condicao.group(1))

    cidade = re.search(
        r"Cidade\.?:\s*([A-ZÀ-Ú\s]+)\s*-\s*([A-Z]{2})",
        texto,
        re.IGNORECASE
    )
    if cidade:
        dados["cidade"] = limpar_texto(cidade.group(1)).upper()
        dados["uf"] = cidade.group(2).upper()

    produto = re.search(
        r"(RECORTADO XISTO BRUTO PRETO MATRIX)",
        texto,
        re.IGNORECASE
    )
    if produto:
        dados["produto"] = limpar_texto(produto.group(1)).upper()

    totais_nf = re.search(
        r"Totais da NF R\$\s+([\d\.,]+)\s+([\d\.,]+)\s+([\d\.,]+)",
        texto,
        re.IGNORECASE
    )
    if totais_nf:
        dados["valor_nf"] = totais_nf.group(3)

    total_pedido = re.search(
        r"Total em R\$\s*([\d\.,]+)",
        texto,
        re.IGNORECASE
    )
    if total_pedido:
        dados["valor_pedido"] = total_pedido.group(1)

    if not dados["valor_pedido"]:
        total_bruto = re.search(
            r"Total Bruto em R\$\s*([\d\.,]+)",
            texto,
            re.IGNORECASE
        )
        if total_bruto:
            dados["valor_pedido"] = total_bruto.group(1)

    return dados