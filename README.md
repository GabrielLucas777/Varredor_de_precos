# Price Monitor Bot - Seu Assistente de Preços

## O Que Faz Este Projeto?

Um robô automático que:
- Entra em sites de lojas (como Terabyte, Amazon, Kabum)
- Lê o preço do produto que você quer
- Compara com o valor que você deseja pagar
- Avisa quando o preço cai para seu alvo

Você configura uma vez e o robô trabalha para você!



---

## Como Funciona (Resumido)

```
1. Você cria um arquivo com: Produto → Link → Preço Alvo
2. Robô abre o navegador
3. Acessa o link
4. Lê o preço atual
5. Se preço ≤ seu alvo → ALERTA!
6. Se preço > seu alvo → Continua esperando
```

---

## Inteligência de Pasta (Caminhos Dinâmicos)

O robô foi configurado para encontrar seus próprios arquivos automaticamente.

**Como foi feito:**

```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(BASE_DIR, "precos.json")
```

**Por quê isso importa?**

Sem essa configuração, o código dependeria de um caminho fixo como:
```
D:\Desenvolvimento\automacao_ecommerce\precos.json
```

Isso quebraria se:
- Você movesse a pasta
- Usasse em outro computador
- Quisesse transformar em um .exe

**Com a configuração correta:**
- O robô funciona em qualquer lugar
- Não precisa configurar nada manualmente
- Está pronto para virar um executável (.exe) no futuro
- Funciona em Windows, Mac e Linux

---

## Técnicas de Simulação Humana

O robô não age como uma máquina fria. Ele "disfarça-se" de um humano real:

### 1. Identificação de Navegador Real
```python
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
```
O robô diz: "Sou um navegador Chrome comum" (e não "Sou um bot Playwright")

### 2. Tamanho de Tela Normal
```python
viewport={"width": 1366, "height": 768}
```
Usa resolução comum (1366x768), como a maioria dos monitores. Não aparece como mobile ou coisa estranha.

### 3. Pausas Entre Ações
```python
page.wait_for_timeout(random.randint(3000, 5000))  # Aguarda 3-5 segundos
```
Um humano lê uma página em alguns segundos. Um bot puro extrairia dados em milissegundos.
O robô deliberadamente **espera** para parecer mais humano.

### 4. Desabilitar Sinais de Automação
```python
args=["--disable-blink-features=AutomationControlled"]
```
Remove um sinalizador que denuncia automação (navigator.webdriver).

---

## Manual da 'Lista de Compras' (arquivo precos.json)

Este é o arquivo onde você adiciona os produtos que quer monitorar.

### Como Preencher

Abra o arquivo `precos.json` e adicione seus produtos:

```json
{
  "meu_monitor": {
    "nome": "Monitor Gamer 24\" Full HD",
    "url": "https://www.terabyteshop.com.br/produto/12345/monitor-gamer-...",
    "preco_referencia": 800.00
  },
  
  "meu_teclado": {
    "nome": "Teclado Mecânico RGB",
    "url": "https://www.terabyteshop.com.br/produto/67890/teclado-mecanico-...",
    "preco_referencia": 450.00
  }
}
```

### Campos Explicados

| Campo | O Que É | Exemplo |
|-------|---------|---------|
| `nome` | Um label para você reconhecer nos alertas | "Monitor Gamer 24\"" |
| `url` | Endereço completo do produto no site | https://www.terabyte...produto/12345/... |
| `preco_referencia` | O preço que você quer pagar | 800.00 |

### Passo a Passo para Adicionar

1. Abra `precos.json` com Bloco de Notas ou VSCode
2. Copie um bloco de produto (do `{` ao `}`)
3. Altere `nome`, `url` e `preco_referencia`
4. Salve o arquivo
5. Na próxima execução, o robô monitorará esse novo produto

**Dica:** Use um validador JSON se ficar com dúvida: [jsonlint.com](https://jsonlint.com)

---

## Como Instalar e Rodar

### Pré-requisitos
- Python 3.8+ instalado
- Conexão de internet

### Instalação (4 passos)

**1. Instalar as dependências do robô:**
```bash
pip install playwright
```

**2. Instalar o navegador que ele usa:**
```bash
playwright install chromium
```

**3. Editar o arquivo `precos.json`:**
Adicione seus produtos conforme a seção anterior.

**4. Executar o robô:**
```bash
python automacao.py
```

Você verá um navegador abrir e o robô começar a trabalhar!

### O Que Você Vai Ver

```
--- Verificando: Monitor Gamer 24" Full HD ---
preço atual: R$ 800.00

STATUS: Disponível | Preço Site: R$ 750.50
ALERTA: O PREÇO ATINGIU O SEU ALVO! RECOMENDO COMPRAR AGORA!

---

STATUS: Disponível | Preço Site: R$ 920.00
Ainda caro. Diferença: R$ 120.00. Não recomendo comprar.
```

---

## Problemas Comuns

### "ModuleNotFoundError: No module named 'playwright'"
Execute: `pip install playwright`

### "precos.json não encontrado"
Certifique-se de que o arquivo está na mesma pasta do script. Se não tiver, crie um vazio.

### Página não carrega
- Verifique a conexão de internet
- Teste a URL no navegador manualmente
- Espere um pouco e tente de novo

---

## Estrutura de Pastas

```
automacao_ecommerce/
├── src/
│   ├── automacao.py      ← O script principal
│   └── comms.py          ← Módulo de comunicação (Telegram)
├── data/
│   └── precos.json       ← Seus produtos (EDITE AQUI!)
├── .gitignore            ← Protege credenciais (.env, __pycache__)
├── .env                  ← Variáveis de ambiente (locais, não versionado)
├── requirements.txt      ← Dependências do projeto
└── README.md             ← Este arquivo
```

**Nota:** O projeto agora é modularizado:
- **src/** contém todo o código Python
- **data/** contém arquivos de dados (JSON)
- **.env** armazena suas credenciais (Token e Chat ID) de forma segura

---

## ESTRADA À FRENTE (Tarefas para Desenvolvimento Futuro)

Checklist de coisas que ainda precisam ser feitas:

- [x] **Integração com Telegram** ✅
  - Enviar alerta direto no celular quando preço atingir alvo
  - Usar bot do Telegram para notificações
  - Status: Concluído

- [ ] **Monitoramento de Múltiplas Lojas**
  - Adicionar suporte para Kabum
  - Adicionar suporte para Amazon
  - Adicionar suporte para outras lojas
  - Problema: Cada site tem um seletor CSS diferente para preço
  - Status: Não iniciado

- [ ] **Criação do Executável (.exe)**
  - Transformar o script Python em um programa instalável
  - Usar PyInstaller ou similar
  - Objetivo: Usuários não precisam ter Python instalado
  - Status: Não iniciado

- [ ] **Interface Visual (GUI)**
  - Criar uma janelinha para adicionar/editar produtos
  - Sem precisar mexer no arquivo precos.json
  - Mostrar status do robô em tempo real
  - Usar PyQt5 ou Tkinter
  - Status: Não iniciado

---

## Configuração do Telegram

Agora o robô pode enviar notificações direto para seu celular via Telegram!

### O Que Você Precisa

**1. Criar um Bot no Telegram:**
- Abra o Telegram e procure pelo usuário `@BotFather`
- Envie a mensagem `/newbot`
- Siga as instruções para criar seu bot
- Você receberá um **Token** (copie e guarde!)
  - Exemplo: `123456789:ABCdefGHIjklMNOpqrSTUvwxyzABCdEfG`

**2. Obter Seu Chat ID:**
- Procure pelo usuário `@userinfobot` no Telegram
- Envie qualquer mensagem
- Ele responderá com seu **Chat ID**

**3. Iniciar Seu Bot:**
- Procure pelo bot que você criou (usando o nome que escolheu)
- Envie a mensagem `/start`

**4. Configurar Variáveis de Ambiente:**
- Crie um arquivo chamado `.env` na raiz do projeto
- Adicione as seguintes linhas:

```
TELEGRAM_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
```

**Importante:** O arquivo `.env` está protegido pelo `.gitignore`, então suas credenciais **nunca serão enviadas** ao repositório Git!

---

## Notas Para Desenvolvimento

### Por Que Os Caminhos Dinâmicos São Importantes

Quando transformarmos em .exe:
```
C:\Program Files\PriceMonitorBot\automacao.exe
```

O programa ainda será capaz de encontrar `precos.json` sem problemas, não importa onde estiver instalado.

### Próxima Prioridade

Se for melhorar o código agora, a prioridade é:
1. **Telegram** (mais fácil, mais útil)
2. **Multi-site** (mais complexo, requer análise de cada site)
3. **.exe** (complexidade média, requer testes)
4. **GUI** (complexidade alta, requer UI/UX)

---

## Informações Técnicas Básicas

| Item | Valor |
|------|-------|
| **Linguagem** | Python 3.8+ |
| **Biblioteca Principal** | Playwright |
| **Persistência** | JSON |
| **Tempo por Produto** | ~10 segundos |

---

## Licença e Créditos

Desenvolvido como projeto pessoal de automação.

**Última atualização:** Janeiro de 2026
