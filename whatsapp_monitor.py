from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time
import requests
import os

def trigger_voicemonkey():
    url = "YOUR_FLOW_ENDPOINT"
    response = requests.get(url)
    return response.status_code

def monitor_whatsapp():
    # Configure Edge options
    edge_options = Options()
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    
    # Set Edge binary path - adjust this path according to your Edge installation
    edge_binary_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    if os.path.exists(edge_binary_path):
        edge_options.binary_location = edge_binary_path
    
    # Initialize the browser with options
    driver = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()),
        options=edge_options
    )
    driver.get("https://web.whatsapp.com/")

    # Aguarda o usuário escanear o QR Code manualmente
    input("Pressione Enter após escanear o QR Code no WhatsApp Web...")

    last_unread = None

    try:
        while True:
            # Procura por chats não lidos usando o seletor correto
            unread_chats = driver.find_elements(By.XPATH, '//div[contains(@class,"_ahlk")]/span[contains(@class,"x1rg5ohu")]')
            
            if unread_chats:
                current_unread = len(unread_chats)
                if last_unread is None or current_unread > last_unread:
                    print("Nova mensagem detectada!")
                    trigger_voicemonkey()  # Dispara o Voice Monkey
                last_unread = current_unread
            else:
                last_unread = 0

            time.sleep(5)  # Verifica a cada 5 segundos

    except KeyboardInterrupt:
        print("Monitoramento encerrado.")
    finally:
        driver.quit()

if __name__ == "__main__":
    monitor_whatsapp()