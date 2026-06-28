import sqlite3
from config import DB_PATH


def verificar_status_arquivo(nome_arquivo, hash_arquivo):
    with sqlite3.connect(DB_PATH) as conexao:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT hash_arquivo
            FROM envios
            WHERE arquivo = ?
            AND status IN ('ENVIADO', 'REENVIADO')
            ORDER BY id DESC
            LIMIT 1
        """, (nome_arquivo,))

        resultado = cursor.fetchone()

        if not resultado:
            return "NOVO"

        ultimo_hash = resultado[0]

        if ultimo_hash == hash_arquivo:
            return "DUPLICADO"

        return "ALTERADO"