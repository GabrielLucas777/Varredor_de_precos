import json
import random
import os 
from playwright.sync_api import sync_playwright  
from comms import enviar_mensagem_telegram

# --- PARTE 1: CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
ARQUIVO_JSON = os.path.join(ROOT_DIR, "data", "precos.json")

# --- PARTE 2: FUNÇÕES DE APOIO ---

def tratar_preco(texto_bruto):
    """ Transforma 'R$ 1.500,00' em 1500.00 """
    preco_limpo = texto_bruto.replace('R$', '').replace('.', '').replace(',', '.').strip()
    return float(preco_limpo)

def carregar_dados_json():
    """ Lê o banco de dados de produtos """
    try:
        with open(ARQUIVO_JSON, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f" ❌ Erro: Arquivo não encontrado em {ARQUIVO_JSON}")
        return {}

# --- PARTE 3: AÇÃO WEB ---

def verificar_produto_no_site(page, produto):
    """ Navega e extrai o preço atual do seletor #valVista """
    print(f"\n--- Analisando: {produto['nome']} ---")
    
    page.goto(produto['url'], wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(random.randint(3000, 5000)) 

    aviso_indisponivel = page.get_by_role("heading", name=" Produto Indisponível")

    if not aviso_indisponivel.is_visible():
        try:
            elemento_preco = page.locator('#valVista').first
            elemento_preco.wait_for(state="visible", timeout=10000)
            return tratar_preco(elemento_preco.inner_text())
        except Exception:
            return None
    else:
        print(" STATUS: Produto Indisponível.")
        return None

# --- PARTE 4: FLUXO PRINCIPAL (Gerente) ---

def executar_bot():
    with sync_playwright() as p: 
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"]) 
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        dados_json = carregar_dados_json()

        for item in dados_json:
            try:
                produto = dados_json[item]
                preco_site = verificar_produto_no_site(page, produto)

                if preco_site is not None:
                    # CENÁRIO A: PREÇO BAIXOU (Promoção)
                    if preco_site <= produto['preco_referencia']:
                        print(" ✅ SUCESSO: Alerta de promoção enviado!")
                        msg_promo = (
                            f"🔥 *PROMOÇÃO ENCONTRADA!*\n\n"
                            f"📦 {produto['nome']}\n"
                            f"💵 Preço: R$ {preco_site:.2f}\n"
                            f"🎯 Meta: R$ {produto['preco_referencia']:.2f}\n\n"
                            f"🔗 [COMPRAR AGORA]({produto['url']})"
                        )
                        enviar_mensagem_telegram(msg_promo)

                    # CENÁRIO B: PREÇO AINDA ALTO (Apenas Status)
                    else:
                        diferenca = preco_site - produto['preco_referencia']
                        print(f" ⏳ Ainda caro. Diferença: R$ {diferenca:.2f}")
                        
                        msg_status = (
                            f"ℹ️ *Status do Monitoramento*\n"
                            f"Produto: {produto['nome']}\n"
                            f"Preço: R$ {preco_site:.2f}\n"
                            f"Faltam R$ {diferenca:.2f} para o seu alvo, recomendo esperar mais um pouco."
                        )
                        enviar_mensagem_telegram(msg_status)

                page.wait_for_timeout(2000)
            
            except Exception as e:
                enviar_mensagem_telegram(f"⚠️ Erro ao processar item: {e}")

        print("\n" + "="*40)
        print("Ciclo de verificação finalizado.")
        browser.close()

if __name__ == "__main__":
    executar_bot()