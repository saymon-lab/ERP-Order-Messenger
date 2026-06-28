from pathlib import Path

BASE_DIR = Path(__file__).parent

PASTA_PENDENTES = BASE_DIR / "pedidos" / "pendentes"
PASTA_ENVIADOS = BASE_DIR / "pedidos_enviados"
PASTA_LOGS = BASE_DIR / "logs"
PASTA_DATABASE = BASE_DIR / "database"

DB_PATH = PASTA_DATABASE / "history.db"

CONTATO_WHATSAPP = "5533999999999"

EXTENSOES_PERMITIDAS = [".pdf"]

