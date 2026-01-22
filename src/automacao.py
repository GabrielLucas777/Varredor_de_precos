import json
import random
import os 
import logging
import requests
from playwright.sync_api import sync_playwright  
from dotenv import load_dotenv

# --- PARTE 0: TELEGRAM (SINALIZAÇÃO) ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_mensagem_telegram(mensagem, imagem_url=None):
    """ Envia o card visual e confirma o sucesso da operação. """
    try:
        url_base = f"https://api.telegram.org/bot{TOKEN}/"
        metodo = "sendPhoto" if imagem_url else "sendMessage"
        payload = {"chat_id": CHAT_ID, "parse_mode": "Markdown"}
        
        if imagem_url:
            payload.update({"photo": imagem_url, "caption": mensagem})
        else:
            payload.update({"text": mensagem})
            
        resp = requests.post(f"{url_base}{metodo}", data=payload)
        if resp.status_code == 200:
            logger.info("  [TELEGRAM] -> Notificação enviada ao celular.")
    except Exception as e:
        logger.error(f"  [TELEGRAM] -> Erro na API: {e}")

# --- PARTE 1: ORGANIZAÇÃO E LOGS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
ARQUIVO_JSON = os.path.join(ROOT_DIR, "data", "precos.json")
PASTA_LOGS = os.path.join(ROOT_DIR, "logs")

if not os.path.exists(PASTA_LOGS): os.makedirs(PASTA_LOGS)

# Logs configurados para serem curtos e diretos
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(os.path.join(PASTA_LOGS, "auditoria.log"), mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

def tratar_preco(texto_bruto):
    """ Converte moeda em número real. Ex: 'R$ 1.500,00' -> 1500.0 """
    if not texto_bruto: return 0.0
    limpo = texto_bruto.replace('R$', '').replace('\xa0', ' ').replace('.', '').replace(',', '.').strip()
    try: return float(limpo)
    except: return 0.0

# --- PARTE 3: EXTRATORES (ESTRATÉGIA POR SITE) ---



def extrair_dados_site(page, site_tipo):
    """ Tenta capturar o preço e a foto após a limpeza agressiva da página. """
    try:
        if site_tipo == "amazon":
            page.wait_for_selector('.aok-offscreen', timeout=15000)
            preco = tratar_preco(page.locator('.aok-offscreen').first.inner_text())
            img = page.locator('#landingImage').get_attribute('src')
        elif site_tipo == "ml":
            page.wait_for_selector('.andes-money-amount__fraction', timeout=10000)
            preco = tratar_preco(page.locator('.andes-money-amount__fraction').first.inner_text())
            img = page.locator('.ui-pdp-gallery__figure__image').first.get_attribute('src')
        else: # Terabyte
            # Espera o seletor principal e garante que ele tenha um valor preenchido
            page.wait_for_selector('#valVista', timeout=15000)
            page.wait_for_function("document.querySelector('#valVista').innerText.includes('R$')", timeout=10000)
            preco = tratar_preco(page.locator('#valVista').first.inner_text())
            img = page.locator('#produto_foto img').first.get_attribute('src')
        
        return preco, img
    except Exception:
        return None, None

# --- PARTE 4: MAESTRO (DRIBILANDO DEFESAS) ---

def verificar_produto(page, produto):
    """ Executa a limpeza de overlays e extração de dados. """
    url = produto['url']
    logger.info(f"🔎 [ANÁLISE]: {produto['nome']}")
    
    try:
        # 1. Navegação básica
        page.goto(url, wait_until='domcontentloaded', timeout=60000)
        
        # 2. LIMPEZA SÊNIOR: Remove pop-ups, newsletters e camadas transparentes
        page.evaluate("""
            () => {
                const seletores = ['.newsletter', '.modal', '.popup', '.overlay', '#newsletter', '.swal2-container'];
                seletores.forEach(s => document.querySelectorAll(s).forEach(el => el.remove()));
                document.body.style.overflow = 'auto'; // Reativa o scroll se o pop-up travou
            }
        """)
        
        # 3. Tempo Humano
        page.keyboard.press("Escape")
        page.wait_for_timeout(3000) 
        page.mouse.wheel(0, 500)

        # 4. Decisão de Loja
        if "amazon.com" in url.lower(): site = "amazon"
        elif "mercadolivre.com" in url.lower(): site = "ml"
        else: site = "terabyte"

        return extrair_dados_site(page, site)
    except Exception as e:
        logger.error(f"  [ERRO]: Falha na navegação: {e}")
        return None, None

# --- PARTE 5: FLUXO DE EXECUÇÃO ---

def executar_bot():
    os.system('cls' if os.name == 'nt' else 'clear')
    logger.info("=== MONITORAMENTO ATIVADO (MODO STEALTH) ===")
    
    with sync_playwright() as p:
        # Forçamos a resolução 1080p para o robô 'enxergar' tudo
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        # O Pulo do Gato: Modifica o ambiente do navegador antes da Amazon/Terabyte carregar
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.navigator.chrome = { runtime: {} };
        """)

        with open(ARQUIVO_JSON, 'r', encoding='utf-8-sig') as f:
            produtos = json.load(f)

        for id_item, dados in produtos.items():
            preco_site, img_url = verificar_produto(page, dados)
            meta = dados['preco_referencia']

            # --- LÓGICA DE LOG E NOTIFICAÇÃO CORRIGIDA ---
            if preco_site is not None and preco_site > 0:
                logger.info(f"  [SUCESSO]: Capturado R$ {preco_site:.2f}")
                
                if preco_site <= meta:
                    status = (f"🔥 *PROMOÇÃO ENCONTRADA!*\n\n*{dados['nome']}*\n"
                              f"💰 Preço: R$ {preco_site:.2f}\n🎯 Meta: R$ {meta:.2f}\n\n"
                              f"🔗 [COMPRAR AGORA]({dados['url']})")
                else:
                    dif = preco_site - meta
                    status = (f"ℹ️ *MONITORAMENTO ATIVO*\n\n*{dados['nome']}*\n"
                              f"💰 Preço: R$ {preco_site:.2f}\n📉 Faltam: R$ {dif:.2f}\n\n"
                              f"📢 *Fica tranquilo!* O robô segue vigiando por aqui. 🚀")
                
                enviar_mensagem_telegram(status, img_url)
            else:
                # Log de Erro Real: Só dispara se o preco_site for None ou 0
                logger.error(f"  [FALHA]: Não foi possível ler o preço de {dados['nome']}")
                enviar_mensagem_telegram(f"⚠️ *FALHA*\nNão consegui ler o preço de: *{dados['nome']}*", None)

            page.wait_for_timeout(random.randint(4000, 7000))

        browser.close()
    logger.info("=== CICLO FINALIZADO ===")

if __name__ == "__main__":
    executar_bot()