from config import PASTA_PENDENTES
from src.logger import criar_tabela_envios
from src.monitor import iniciar_monitoramento
from src.services.whatsapp_service import WhatsAppService


def main():
    criar_tabela_envios()

    whatsapp = WhatsAppService()
    whatsapp.iniciar()

    iniciar_monitoramento(str(PASTA_PENDENTES), whatsapp)


if __name__ == "__main__":
    main()