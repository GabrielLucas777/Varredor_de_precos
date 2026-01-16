import json
import random
import os  # Biblioteca necessária para caminhos dinâmicos
from playwright.sync_api import sync_playwright  

# --- PARTE 1: CONFIGURAÇÃO DE CAMINHO (Almoxarifado) ---
# Em vez de um caminho fixo (D:\...), usamos o 'os' para localizar o arquivo na mesma pasta do script.
# Isso permite que o código funcione em qualquer computador sem precisar alterar o código.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(BASE_DIR, "precos.json")

# --- PARTE 2: FUNÇÕES DE APOIO (Especialistas de Dados) ---

def tratar_preco(texto_bruto):
    """ 
    Trata o preço para formato float.
    O motivo: o Python só consegue comparar números. 'R$ 1.500,00' precisa virar 1500.00.
    """
    preco_limpo = texto_bruto.replace('R$', '').replace('.', '').replace(',', '.').strip()
    return float(preco_limpo)

def carregar_dados_json():
    """ 
    LER O DOCUMENTO (JSON)
    Carrega o arquivo de produtos com tratamento para caso o arquivo não exista.
    """
    try:
        with open(ARQUIVO_JSON, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f" ❌ Erro: O arquivo '{ARQUIVO_JSON}' não foi encontrado na pasta.")
        return {}
    except Exception as e:
        print(f" Erro ao ler o JSON: {e}")
        return {}

# --- PARTE 3: AÇÃO WEB (Especialista em Navegar) ---

def verificar_produto_no_site(page, produto):
    """ 
    VERIFICA O PRODUTO NO SITE
    Acessa a página, lida com a disponibilidade e extrai o preço.
    """
    print(f"\n--- Verificando: {produto['nome']} ---")
    print(f"preço atual: R$ {produto['preco_referencia']}")
    
    # Navegação com timeout de segurança
    page.goto(produto['url'], wait_until='domcontentloaded', timeout=60000)
    
    # Espera aleatória para simular comportamento humano (Driblar Captcha)
    page.wait_for_timeout(random.randint(3000, 5000)) 

    # Lógica do seletor de disponibilidade (Heading de Indisponível)
    aviso_indisponivel = page.get_by_role("heading", name=" Produto Indisponível")

    if not aviso_indisponivel.is_visible():
        try:
            # Localizando o preço na página
            elemento_preco = page.locator('#valVista').first
            elemento_preco.wait_for(state="visible", timeout=10000)
            
            # Chamando a função de tratamento de preço
            preco_atual = tratar_preco(elemento_preco.inner_text())
            return preco_atual

        except Exception:
            print(f" Preço não localizado (pode ser Captcha ou site mudou).")
            return None
    else:
        print(f" STATUS: Produto Indisponível no momento.")
        return None

# --- PARTE 4: FLUXO PRINCIPAL (Gerente) ---

def executar_bot():
    with sync_playwright() as p: 
        # Lançamento com camuflagem anti-bot reforçada
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"]) 
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Carrega os produtos do 'Coração de Dados'
        dados_json = carregar_dados_json()

        # Itera pela lista de produtos monitorados
        for item in dados_json:
            produto = dados_json[item]
            
            # O Gerente solicita o preço atual ao Especialista Web
            preco_site = verificar_produto_no_site(page, produto)

            # Se o preço foi capturado com sucesso, faz a comparação lógica
            if preco_site is not None:
                print(f" STATUS: Disponível | Preço Site: R$ {preco_site:.2f}")

                if preco_site <= produto['preco_referencia']:
                    print(" ✅ ALERTA: O PREÇO ATINGIU O SEU ALVO! RECOMENDO COMPRAR AGORA!")
                else:
                    diferenca = preco_site - produto['preco_referencia']
                    print(f" Ainda caro. Diferença: R$ {diferenca:.2f}. Não recomendo comprar.")

            # Pausa natural entre produtos para evitar bloqueios de IP
            page.wait_for_timeout(2000)

        print("\n" + "="*40)
        print("Automação concluída.")
        input("Pressione Enter para fechar o navegador...")
        browser.close()

# Inicia a execução se o arquivo for rodado diretamente
if __name__ == "__main__":
    executar_bot()