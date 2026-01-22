Price Monitor Bot - Seu Assistente de Preços
O Que Faz Este Projeto?
Um robô automático que monitora o preço de produtos para você:

Entra em várias lojas: Agora ele já acessa Terabyte, Amazon e Mercado Livre.

Lê o preço real: Identifica o valor atual e compara com o que você quer pagar.

Limpa a tela: Fecha sozinho propagandas e janelas de "assine nossa lista" que tentam esconder o preço.

Avisa no celular: Quando o preço atinge o seu alvo, ele te manda um alerta no Telegram com a foto do produto e o link para comprar.

Como Funciona (Resumido)
1. Você cria uma lista com: Produto → Link → Preço Alvo
2. O robô abre o navegador em modo disfarçado
3. Ele limpa qualquer propaganda ou anúncio da frente
4. Lê o preço e captura a imagem do item
5. Se preço ≤ seu alvo → ALERTA NO CELULAR COM FOTO!
6. Se preço > seu alvo → Ele te avisa quanto falta para baixar
Inteligência de Pasta (Caminhos Dinâmicos)
O robô foi configurado para encontrar seus próprios arquivos automaticamente.

Como foi feito:

Python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(BASE_DIR, "precos.json")
Por quê isso importa? Isso garante que o robô funcione em qualquer computador ou pasta sem você precisar mudar uma linha de código. Ele já está preparado para virar um programa instalável (.exe) no futuro.

Técnicas de Simulação Humana
Para evitar ser bloqueado, o robô agora "finge" ser uma pessoa real:

Identidade Real: Ele se apresenta aos sites como um navegador Chrome comum e atualizado.

Tela Cheia: Ele abre o site em tamanho de monitor normal (1920x1080) para enxergar todos os elementos da página.

Disfarce de Automação: Removemos as marcas que denunciam para o site que o navegador está sendo controlado por um robô.

Limpeza de Propagandas: O robô aperta "Esc" e usa um comando para deletar janelas de anúncio que sobem depois que a página carrega.

Diário do Robô (Logs no Terminal)
O terminal agora é o seu painel de controle. Você verá mensagens claras sobre o que está acontecendo:

[BUSCA]: O robô começou a olhar um item da sua lista.

[SUCESSO]: O preço foi encontrado e lido corretamente.

[ERRO]: O robô avisa se não conseguiu ler o preço ou se o link caiu.

[TELEGRAM]: Confirmação de que o aviso foi enviado para o seu celular.

Dica: O robô limpa o diário antigo toda vez que começa uma rodada nova, para você focar apenas no agora.

Manual da 'Lista de Compras' (arquivo precos.json)
Este é o arquivo onde você adiciona os produtos que quer monitorar.

Como Preencher:

JSON
{
  "meu_monitor": {
    "nome": "Monitor Gamer 24 Full HD",
    "url": "https://www.terabyteshop.com.br/produto/...",
    "preco_referencia": 800.00
  }
}
Como Instalar e Rodar
Pré-requisitos
Python 3.8+ instalado

Conexão de internet

Instalação
Instalar as dependências: pip install playwright requests python-dotenv

Instalar o navegador: playwright install chromium

Configurar o .env: Coloque seu Token e Chat ID do Telegram.

Executar: python automacao.py

ESTRADA À FRENTE (Progresso do Projeto)
Checklist de coisas que já funcionam e o que falta:

[x] Integração com Telegram ✅

Enviar alerta direto no celular quando preço atingir alvo.

Novo: Enviar foto do produto junto com o aviso.

Novo: Calcular e mostrar quanto dinheiro falta para chegar na meta.

[x] Monitoramento de Múltiplas Lojas ✅

Suporte para Amazon (links curtos e anti-bloqueio).

Suporte para Terabyte (espera o preço carregar de verdade).

Suporte para Mercado Livre (leitura de preços correta).

[ ] Criação do Executável (.exe)

Transformar o script em um programa de clicar e rodar.

[ ] Interface Visual (GUI)

Criar uma janelinha para gerenciar os produtos sem abrir o arquivo JSON.

Configuração do Telegram
Crie seu bot com o @BotFather no Telegram e pegue o Token.

Pegue seu Chat ID usando o @userinfobot.

Crie um arquivo chamado .env e coloque:

TELEGRAM_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
Última atualização: 21 de Janeiro de 2026.