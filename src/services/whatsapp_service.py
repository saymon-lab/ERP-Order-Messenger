import time
from pathlib import Path
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class WhatsAppService:
    def __init__(self):
        self.driver = None
        self.wait = None

    def iniciar(self):
        options = Options()

        perfil = Path.cwd() / "chrome_profile"
        perfil.mkdir(parents=True, exist_ok=True)

        options.add_argument(f"--user-data-dir={str(perfil)}")
        options.add_argument("--start-maximized")

        service = Service(ChromeDriverManager().install())

        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 60)

        self.driver.get("https://web.whatsapp.com")

        print("WhatsApp Web aberto.")
        print("Aguardando carregamento...")

        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@contenteditable='true']")
            )
        )

        print("WhatsApp Web carregado.")

    def enviar_texto(self, telefone, mensagem):
        mensagem_url = quote(mensagem)

        url = f"https://web.whatsapp.com/send?phone={telefone}&text={mensagem_url}"

        print(f"Abrindo conversa do número: {telefone}")
        self.driver.get(url)

        time.sleep(8)

        print("Tentando enviar mensagem...")

        # Tenta apertar ENTER
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()

        time.sleep(3)

        print("Comando de envio executado.")

    def enviar_pedido(self, contato, mensagem, caminho_pdf=None):
        self.enviar_texto(contato, mensagem)