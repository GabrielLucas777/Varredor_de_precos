import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# --- AJUSTE PARA ENCONTRAR O .ENV ---
# Isso descobre onde este arquivo comms.py está guardado
caminho_desta_pasta = Path(__file__).parent
# Isso diz para procurar o .env na mesma pasta deste arquivo
caminho_do_env = caminho_desta_pasta / ".env"

# Tenta carregar o arquivo .env específico
load_dotenv(dotenv_path=caminho_do_env)

def enviar_mensagem_telegram(mensagem):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("⚠️ Erro de configuração no .env")
        return # Sai da função sem quebrar o código principal

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    dados = {"chat_id": chat_id, "text": mensagem, "parse_mode": "Markdown"}

    try:
        # Definimos um timeout de 10 segundos para não travar o robô se a internet oscilar
        resposta = requests.post(url, data=dados, timeout=10)
        
        if resposta.status_code == 200:
            print("✅ Sucesso: Notificação enviada.")
        else:
            print(f"❌ Erro API Telegram: {resposta.status_code}")

    except Exception as e:
        # Se a internet cair, ele avisa no terminal mas NÃO trava o robô
        print(f"⚠️ Falha na rede ao enviar Telegram: {e}")