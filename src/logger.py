import sqlite3
from datetime import datetime
from config import DB_PATH


def criar_tabela_envios():
    with sqlite3.connect(DB_PATH) as conexao:
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS envios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                arquivo TEXT NOT NULL,
                pedido TEXT,
                cliente TEXT,
                hash_arquivo TEXT,
                status TEXT NOT NULL,
                mensagem TEXT,
                data_hora TEXT NOT NULL
            )
        """)

        conexao.commit()


def registrar_envio(
    arquivo,
    pedido=None,
    cliente=None,
    hash_arquivo=None,
    status="PENDENTE",
    mensagem=""
):
    with sqlite3.connect(DB_PATH) as conexao:
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO envios (
                arquivo,
                pedido,
                cliente,
                hash_arquivo,
                status,
                mensagem,
                data_hora
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            arquivo,
            pedido,
            cliente,
            hash_arquivo,
            status,
            mensagem,
            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ))

        conexao.commit()


def listar_envios():
    with sqlite3.connect(DB_PATH) as conexao:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, arquivo, pedido, cliente, hash_arquivo, status, data_hora
            FROM envios
            ORDER BY id DESC
        """)

        return cursor.fetchall()