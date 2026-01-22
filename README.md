# 🛒 Price Monitor Bot - Seu Assistente de Preços

## 🎯 O Que Faz Este Projeto?

Um robô automático que monitora o preço de produtos para você em tempo real:
* **Monitora Várias Lojas:** Já configurado para Terabyte, Amazon e Mercado Livre.
* **Lê o Preço Real:** Identifica o valor e compara com o que você quer pagar.
* **Limpa a Tela:** Fecha sozinho propagandas e avisos de "assine nossa lista" que tentam esconder o preço.
* **Avisa no Celular:** Quando o preço cai, ele te manda um alerta no Telegram com a **foto do produto** e o link para comprar.

---

## ⚙️ Como Funciona (Resumido)

1. Você cria um arquivo com: Produto → Link → Preço Alvo.
2. O robô abre o navegador em modo disfarçado.
3. Ele limpa qualquer propaganda ou anúncio da frente antes de ler o valor.
4. Captura o preço atual e a imagem do item.
5. **Se preço ≤ seu alvo** → ALERTA NO CELULAR COM FOTO!
6. **Se preço > seu alvo** → Ele te avisa quanto dinheiro falta para baixar.

---

## 📂 Inteligência de Pasta (Caminhos Dinâmicos)

O robô foi configurado para encontrar seus próprios arquivos automaticamente, não importa onde a pasta esteja salva no seu computador.

**Como foi feito:**
```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(BASE_DIR, "precos.json")
Por Que Isso Importa?Sem essa configuração, o código dependeria de um caminho fixo (como D:\Projetos\bot\precos.json). Isso quebraria se você movesse a pasta ou usasse em outro computador. Com os caminhos dinâmicos:O robô funciona em qualquer lugar.Não precisa configurar nada manualmente ao mudar de pasta.Está pronto para virar um programa instalável (.exe) no futuro.Funciona em Windows, Mac e Linux sem ajustes.👤 Técnicas de Simulação Humana (Disfarce)Para evitar bloqueios, o robô agora se comporta como uma pessoa real:Identidade Real: Ele se apresenta aos sites como um navegador Chrome comum e atualizado (User-Agent).Tela Cheia: Abre o site em tamanho de monitor normal (1920x1080) para "enxergar" tudo o que um humano veria.Pausas Humanas: O robô espera alguns segundos entre as ações para simular o tempo de leitura de uma pessoa.Disfarce de Automação: Removemos os sinais técnicos (como o navigator.webdriver) que os sites usam para identificar robôs.Limpeza de Propagandas: O robô aperta "Esc" e remove janelas de anúncio automaticamente antes de tentar ler o preço.📊 Diário do Robô (Logs no Terminal)O terminal avisa claramente o que está acontecendo a cada segundo para você não ficar na dúvida:PrefixoO Que Significa[BUSCA]O robô começou a analisar um item da sua lista.[SUCESSO]O preço foi encontrado e lido corretamente no site.[ERRO]Houve falha na leitura (o robô avisa qual link deu problema).[TELEGRAM]Confirmação de que o aviso foi enviado para o seu celular.Nota: O robô limpa o diário antigo toda vez que começa uma rodada nova, para você focar apenas na verificação atual.📝 Manual da 'Lista de Compras' (precos.json)Este é o arquivo onde você adiciona os produtos que quer monitorar.Como Preencher:JSON{
  "meu_monitor": {
    "nome": "Monitor Gamer 24 Full HD",
    "url": "[https://www.terabyteshop.com.br/produto/](https://www.terabyteshop.com.br/produto/)...",
    "preco_referencia": 800.00
  }
}
Campos Explicados:CampoO Que ÉExemplonomeNome para você reconhecer no alerta"Monitor Gamer 24"urlLink completo do produto no site"https://www.terabyte..."preco_referenciaO preço máximo que você quer pagar800.00✅ Progresso do ProjetoAbaixo estão as tarefas concluídas e o que ainda pretendemos desenvolver:[x] Integração com Telegram ✅Enviar alerta direto no celular quando preço atingir alvo.Novo: Enviar foto do produto junto com o aviso.Novo: Calcular e mostrar quanto dinheiro falta para chegar na meta.[x] Monitoramento de Múltiplas Lojas ✅Suporte para Amazon (links curtos e anti-bloqueio).Suporte para Terabyte (espera o preço carregar de verdade).Suporte para Mercado Livre (leitura de preços correta).[x] Limpeza Automática de Janelas e Anúncios ✅[ ] Criação do Programa Instalável (.exe) ⏳[ ] Interface Visual para Cadastro de Produtos (GUI) ⏳🚀 Como Instalar e RodarPré-requisitosPython 3.8+ instalado e conexão de internet.Instalação e ExecuçãoInstale as ferramentas necessárias:Bashpip install playwright requests python-dotenv
Instale o navegador do robô:Bashplaywright install chromium
Configure seu Telegram:Crie um arquivo .env na raiz e coloque seu Token e Chat ID conforme as instruções abaixo.Rode o robô:Bashpython automacao.py
📱 Configuração do TelegramCriar um Bot: Procure pelo @BotFather no Telegram, envie /newbot e guarde o Token.Obter Chat ID: Procure pelo @userinfobot no Telegram para descobrir seu ID numérico.Iniciar o Bot: Procure pelo bot que você criou e envie /start.Arquivo .env: Na raiz do projeto, adicione:Snippet de códigoTELEGRAM_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
⚙️ Informações Técnicas BásicasItemValorLinguagemPython 3.8+Biblioteca PrincipalPlaywrightPersistênciaJSONTempo por Produto~10 segundosÚltima atualização: 22 de Janeiro de 2026.
