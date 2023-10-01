from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
import time

def inicializar_navegador():
    service = Service(ChromeDriverManager().install())
    nav = webdriver.Chrome(service=service)
    nav.get("https://web.whatsapp.com/")
    time.sleep(35)
    return nav

def extrair_mensagens(nav):
    nav = WebDriverWait(nav, 10).until(EC.presence_of_element_located(('xpath', '//*[@class="copyable-text"]')))
    mensagens_elements = nav.find_elements('xpath', '//*[@class="copyable-text"]')
    mensagens = []
    time.sleep(2)
    for mensagem_element in mensagens_elements:
        mensagem = mensagem_element.text
        if mensagem:
            mensagens.append(mensagem)
    return mensagens

def verificar_e_salvar_mensagens_com_palavra_chave(mensagens, palavra_chave):
    mensagens_com_palavra_chave = [mensagem for mensagem in mensagens if palavra_chave in mensagem.split()]
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for mensagem in mensagens_com_palavra_chave:
        sheet.append([mensagem])
    workbook.save('mensagens_com_palavra_chave.xlsx')
    workbook.close()

def interagir_com_whatsapp(nav):
    nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div/button/div[2]/span').click()
    time.sleep(1)
    nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').send_keys("Teste script")
    time.sleep(1)
    nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').send_keys(Keys.ENTER)
    time.sleep(5)

if __name__ == "__main__":
    # Palavra-chave que você deseja identificar
    palavra_chave = 'produtos'

    # Inicializar o navegador
    nav = inicializar_navegador()

    # Interagir com o WhatsApp
    interagir_com_whatsapp(nav)

    # Extrair mensagens
    mensagens = extrair_mensagens(nav)
    time.sleep(5)

    # Verificar e salvar mensagens com a palavra-chave
    verificar_e_salvar_mensagens_com_palavra_chave(mensagens, palavra_chave)
