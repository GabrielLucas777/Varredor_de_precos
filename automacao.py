import json
import os
import random
from playwright.sync_api import sync_playwright  

# --- CONFIGURAÇÃO DE CAMINHO (Precisei apontar o caminho para evitar erro no momento da leitura do arquivo) ---
ARQUIVO_JSON = r"D:\Desenvolvimento\automacao_ecommerce\precos.json"

with sync_playwright() as p: 
    # Lançamento com camuflagem anti-bot(parametro user_agent utilizado para simular um navegador real)
    browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"]) # - parametro foi utilizado para esconder as marcas de que o navegador está sendo automátizado. tomei essa atitude pois cai em captccha diversas vezes. 
    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()  

   

   # 1. LER O DOCUMENTO (JSON)
    try:
        with open(ARQUIVO_JSON, 'r', encoding='utf-8-sig') as f:
            conteudo_bruto = f.read() # Lê o texto puro do arquivo
            print(f"--- CONTEÚDO BRUTO DO ARQUIVO NO DISCO ---\n{conteudo_bruto}\n------------------------------------------")
            
            # Agora volta pro início do arquivo para o json.load funcionar
            f.seek(0)
            dados_json = json.load(f)
    except Exception as e:
        print(f" Erro ao ler o JSON: {e}")
        dados_json = {}
    # 3. ITERAR PELOS PRODUTOS
    for item in dados_json:
        # Relendo o JSON dentro do loop para captar alterações de preço em tempo real
        with open(ARQUIVO_JSON, 'r', encoding='utf-8-sig') as f:
            produto = json.load(f)[item]

        print(f"\n--- Verificando: {produto['nome']} ---")
        print(f"Alvo atual: R$ {produto['preco_referencia']}")
        
        # Navegação
        page.goto(produto['url'], wait_until='domcontentloaded')
        
        # Timeout para carregar o site e driblar o capcha
        page.wait_for_timeout(random.randint(3000, 5000)) 

        # Lógica do seletor (Heading de Indisponível)
        aviso_indisponivel = page.get_by_role("heading", name=" Produto Indisponível")

        if not aviso_indisponivel.is_visible():
            try:
                # Localizando preço 
                elemento_preco = page.locator('#valVista').first
                elemento_preco.wait_for(state="visible", timeout=10000)
                
                texto_bruto = elemento_preco.inner_text() 
                preco_limpo = texto_bruto.replace('R$', '').replace('.', '').replace(',', '.').strip()
                preco_atual = float(preco_limpo)
                
                print(f" STATUS: Disponível | Preço Site: R$ {preco_atual:.2f}")

                if preco_atual <= produto['preco_referencia']:
                    print(" ALERTA: O PREÇO ATINGIU O SEU ALVO!")
                else:
                    print(f" Ainda caro. Diferença: R$ {preco_atual - produto['preco_referencia']:.2f}. Não recomendo comprar.")
                    
            except Exception:
                print(f" Preço não localizado (pode ser Captcha).")
        else:
            print(f" STATUS: Produto Indisponível no momento.")

        # Pausa entre produtos 
        page.wait_for_timeout(2000)

    print("\n" + "="*40)
    print("Automação concluída.")
    input("Pressione Enter para sair...")
    browser.close()