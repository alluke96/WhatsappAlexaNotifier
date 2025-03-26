from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time
import requests
import os

def trigger_voicemonkey():
    url = "YOUR_FLOW_ENDPOINT"  
    response = requests.get(url)
    return response.status_code

def monitor_whatsapp():
    # Configuração do Edge
    edge_options = Options()
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    
    # Define o caminho do executável do Edge - ajuste esse caminho de acordo com a instalação do Edge
    edge_binary_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    if os.path.exists(edge_binary_path):
        edge_options.binary_location = edge_binary_path
    
    # Inicializa o navegador com as opções
    driver = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()),
        options=edge_options
    )
    driver.get("https://web.whatsapp.com/")

    # Aguarda o usuário escanear o QR Code manualmente
    input("Pressione Enter após escanear o QR Code no WhatsApp Web...")

    last_unread = None
    last_unread_first_chat = None

    try:
        while True:
            # Encontra o container da lista de chats
            chat_list = driver.find_element(By.CSS_SELECTOR, 'div[role="grid"]')
            # Pega o total de chats
            total_chats = int(chat_list.get_attribute('aria-rowcount'))
            
            # Pega o primeiro chat (total_chats - 1)
            first_chat_selector = f'div[role="listitem"][style*="z-index: {total_chats - 1}"]'
            first_chat = driver.find_element(By.CSS_SELECTOR, first_chat_selector)
            
            # Procura por mensagens não lidas no primeiro chat
            unread_elements = first_chat.find_elements(By.CSS_SELECTOR, 'div._ahlk span.x1rg5ohu')
            
            if unread_elements:
                if unread_elements[0].text.isdigit():
                    first_chat_count = int(unread_elements[0].text)
                    if last_unread_first_chat is None or first_chat_count > last_unread_first_chat:
                        print(f"Nova mensagem detectada no primeiro chat! Total de mensagens não lidas: {first_chat_count}")
                        trigger_voicemonkey()  # Dispara o Voice Monkey apenas para o primeiro chat
                        last_unread_first_chat = first_chat_count
                
                # Atualiza o contador total de mensagens não lidas
                unread_count = sum(int(element.text) for element in unread_elements if element.text.isdigit())
                if last_unread is None or unread_count > last_unread:
                    last_unread = unread_count
            else:
                last_unread = 0
                last_unread_first_chat = 0

            time.sleep(5)  # Verifica a cada 5 segundos

    except KeyboardInterrupt:
        print("Monitoramento encerrado.")
    finally:
        driver.quit()

if __name__ == "__main__":
    monitor_whatsapp()