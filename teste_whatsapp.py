from config import CONTATO_WHATSAPP
from src.services.whatsapp_service import WhatsAppService


def main():
    whatsapp = WhatsAppService()

    try:
        whatsapp.iniciar()

        mensagem = """
🤖 ERP ORDER MESSENGER

Teste de comunicação.

Se você recebeu esta mensagem, a integração está funcionando.
""".strip()

        whatsapp.enviar_texto(
            contato=CONTATO_WHATSAPP,
            mensagem=mensagem
        )

    except Exception as erro:
        print("\nERRO AO TESTAR WHATSAPP:")
        print(erro)

    finally:
        input("\nPressione ENTER para encerrar...")


if __name__ == "__main__":
    main()