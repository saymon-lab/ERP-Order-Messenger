import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def iniciar_driver():
    options = Options()

    # Mantém a sessão do WhatsApp Web salva
    perfil = Path.cwd() / "chrome_profile"
    options.add_argument(f"--user-data-dir={perfil}")

    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    return driver


def abrir_whatsapp(driver):
    driver.get("https://web.whatsapp.com")

    print("Abrindo WhatsApp Web...")
    print("Se for a primeira vez, escaneie o QR Code.")

    time.sleep(15)


def enviar_mensagem_whatsapp(driver, contato, mensagem, caminho_pdf):
    print(f"Procurando contato: {contato}")

    campo_pesquisa = driver.find_element(
        By.XPATH,
        "//div[@contenteditable='true'][@data-tab='3']"
    )

    campo_pesquisa.click()
    campo_pesquisa.clear()
    campo_pesquisa.send_keys(contato)
    time.sleep(2)
    campo_pesquisa.send_keys(Keys.ENTER)

    time.sleep(2)

    campo_mensagem = driver.find_element(
        By.XPATH,
        "//div[@contenteditable='true'][@data-tab='10']"
    )

    campo_mensagem.click()
    campo_mensagem.send_keys(mensagem)
    campo_mensagem.send_keys(Keys.ENTER)

    time.sleep(1)

    anexar_pdf(driver, caminho_pdf)


def anexar_pdf(driver, caminho_pdf):
    caminho_pdf = str(Path(caminho_pdf).resolve())

    print(f"Anexando PDF: {caminho_pdf}")

    botao_anexar = driver.find_element(
        By.XPATH,
        "//span[@data-icon='plus']"
    )

    botao_anexar.click()
    time.sleep(1)

    input_arquivo = driver.find_element(
        By.XPATH,
        "//input[@accept='*']"
    )

    input_arquivo.send_keys(caminho_pdf)

    time.sleep(3)

    botao_enviar = driver.find_element(
        By.XPATH,
        "//span[@data-icon='send']"
    )

    botao_enviar.click()

    print("PDF enviado com sucesso.")
    time.sleep(2)