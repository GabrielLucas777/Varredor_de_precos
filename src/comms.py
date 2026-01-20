import os
import requests
from dotenv import load_dotenv

# Carrega as chaves do arquivo .env que você acabou de criar
load_dotenv()

def enviar_mensagem_telegram(texto):
    """
    Função modular para enviar notificações para o Telegram.
    """
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # URL da API do Telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Dados da mensagem
    payload = {
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "Markdown" # Permite usar negrito, links, etc.
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Notificação enviada ao Telegram com sucesso!")
        else:
            print(f"❌ Erro ao enviar para o Telegram. Status: {response.status_code}")
            print(f"Resposta: {response.text}")
    except Exception as e:
        print(f"⚠️ Houve uma falha de conexão: {e}")

# Este bloco abaixo serve APENAS para testarmos agora.
# Ele só roda se você executar o arquivo 'comms.py' diretamente.
if __name__ == "__main__":
    print("Iniciando teste de envio...")
    enviar_mensagem_telegram("🚀 *Olá Gabriel!* O seu bot já está integrado com o Telegram!")