🛒 Price Monitor Bot

Monitoramento automático de preços com alertas em tempo real via Telegram

📌 Visão Geral

O Price Monitor Bot é um sistema de automação que monitora o preço de produtos em lojas online e envia alertas para o usuário quando o valor atinge o preço desejado.

Ele simula um navegador real, lida com pop-ups e anúncios automaticamente e envia notificações no Telegram com preço, diferença até a meta, link do produto e imagem.

Lojas suportadas:

Terabyte

Amazon

Mercado Livre

🎯 Funcionalidades

Monitoramento de múltiplos produtos

Suporte a múltiplas lojas

Leitura do preço real da página

Remoção automática de anúncios e pop-ups

Simulação de comportamento humano

Envio de alertas via Telegram

Envio da imagem do produto no alerta

Cálculo da diferença até o preço desejado

Logs em tempo real no terminal

⚙️ Como Funciona

O usuário cadastra os produtos em um arquivo precos.json

O robô abre o navegador em modo oculto

Remove anúncios e janelas que bloqueiam o preço

Lê o preço atual e captura a imagem do produto

Compara com o preço de referência

Se o preço for menor ou igual → envia alerta no Telegram

Se for maior → informa quanto falta para atingir a meta

📂 Estrutura Inteligente de Caminhos

O projeto utiliza caminhos dinâmicos para localizar arquivos, permitindo que a pasta seja movida sem quebrar o sistema.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(BASE_DIR, "precos.json")


Isso garante:

Compatibilidade com Windows, Linux e macOS

Facilidade para empacotar como .exe

Portabilidade do projeto

🕵️‍♂️ Simulação de Navegador Humano

Para evitar bloqueios por automação, o robô utiliza:

User-Agent de navegador real

Resolução de tela 1920x1080

Remoção de navigator.webdriver

Fechamento automático de pop-ups via ESC

Isso reduz drasticamente o risco de detecção por automação.

📊 Sistema de Logs

O terminal exibe o estado do robô em tempo real:

Prefixo	Significado
[BUSCA]	Produto sendo analisado
[SUCESSO]	Preço encontrado com sucesso
[ERRO]	Falha ao acessar ou ler a página
[TELEGRAM]	Mensagem enviada ao usuário

O log é limpo a cada nova rodada de verificação.

📝 Cadastro de Produtos (precos.json)

Exemplo:

{
  "meu_monitor": {
    "nome": "Monitor Gamer 24 Full HD",
    "url": "https://www.terabyteshop.com.br/produto/...",
    "preco_referencia": 800.00
  }
}

Campo	Descrição
nome	Nome do produto
url	Link completo da loja
preco_referencia	Preço máximo desejado
🚀 Instalação
Requisitos

Python 3.8 ou superior

Conexão com internet

Instalação
pip install playwright requests python-dotenv
playwright install chromium

📱 Configuração do Telegram

Crie um bot com o @BotFather

Obtenha seu Token

Pegue seu Chat ID usando o @userinfobot

Crie um arquivo .env na raiz do projeto:

TELEGRAM_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui

▶️ Executando
python automacao.py

📌 Tecnologias Utilizadas
Item	Tecnologia
Linguagem	Python
Automação	Playwright
Mensageria	Telegram API
Configuração	python-dotenv
Armazenamento	JSON
🛠 Futuras implementações

 Monitoramento multi-loja

 Integração com Telegram

 Envio de imagem do produto

 Cálculo de diferença até a meta

 Limpeza automática de anúncios

 Interface gráfica (GUI)

 Geração de executável (.exe)

📅 Última atualização

Janeiro de 2026