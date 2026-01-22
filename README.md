# 🤖 Price Monitor Bot

### 🎯 Robô Inteligente de Monitoramento de Preços com Telegram

---

## 📋 O Que Este Projeto Faz?

O **Price Monitor Bot** é um sistema automatizado que monitora preços de produtos em tempo real nas principais lojas online do Brasil:

- ✅ **Amazon Brasil**
- ✅ **Mercado Livre**
- ✅ **Terabyte Shop**

### 🚀 Funcionalidades Principais:

- 🌐 Acessa os sites de forma automatizada usando Playwright
- 🧹 Remove anúncios e pop-ups automaticamente
- 💰 Extrai o preço atual do produto
- 📸 Captura screenshot da página
- 📊 Calcula a diferença entre preço atual e preço de referência
- 📱 Envia alertas completos no Telegram com foto e análise de preço

---

## ⚙️ Como Funciona? (Workflow Completo)

1. **Você preenche o arquivo `precos.json`** com os produtos que deseja monitorar
2. **O robô inicia** e carrega sua lista de compras
3. **Para cada produto:**
   - Abre o navegador de forma invisível (headless)
   - Acessa a URL do produto
   - Remove anúncios e pop-ups automaticamente
   - Extrai o preço atual da página
   - Captura uma screenshot da tela
   - Compara com o preço de referência
4. **Calcula a diferença de preço** (economia ou aumento)
5. **Envia notificação no Telegram** com:
   - Nome do produto
   - Preço atual vs. Preço de referência
   - Diferença em R$ e porcentagem
   - Screenshot da página
6. **Você recebe o alerta no celular** instantaneamente! 📲

---

## 📂 Inteligência de Pasta (Caminhos Dinâmicos)

O projeto utiliza um sistema inteligente de localização de arquivos:
```python
import os

# Detecta automaticamente onde o script está rodando
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Constrói caminhos relativos a partir da pasta raiz
json_path = os.path.join(BASE_DIR, 'precos.json')
screenshots_path = os.path.join(BASE_DIR, 'screenshots')
```

### 🤔 Por Que Isso Importa?

| Benefício | Descrição |
|-----------|-----------|
| **Portabilidade Total** | Funciona em qualquer PC (Windows, Mac, Linux) sem precisar alterar código |
| **Preparado para .exe** | Quando compilado para executável, os caminhos continuarão funcionando |
| **Zero Configuração Manual** | Não precisa editar paths manualmente ao trocar de máquina |
| **Organização Profissional** | Todos os arquivos ficam relativos à pasta do projeto |

---

## 🕵️ Disfarce Humano (Simulação Anti-Detecção)

O robô foi projetado para **parecer um usuário real**, evitando bloqueios dos sites:

### 🎭 Técnicas de Evasão Implementadas:
```python
context = await browser.new_context(
    viewport={'width': 1920, 'height': 1080},
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
)

# Remove sinais de automação
await page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
""")
```

| Técnica | Como Funciona |
|---------|---------------|
| **User-Agent Real** | Usa identificação de navegador legítimo (Chrome/Edge) |
| **Viewport 1920x1080** | Simula resolução de tela comum de desktop |
| **Remoção de `navigator.webdriver`** | Oculta o sinal que identifica automação via Selenium/Playwright |
| **Limpeza Automática de Anúncios** | Pressiona `ESC` e injeta JavaScript para fechar pop-ups |

### 🧹 Exemplo de Limpeza de Anúncios:
```python
# Fecha pop-ups automaticamente
await page.keyboard.press('Escape')

# Injeta código para remover overlays
await page.evaluate("""
    document.querySelectorAll('[class*="modal"], [class*="popup"]')
        .forEach(el => el.remove());
""")
```

---

## 📝 Diário do Robô (Sistema de Logs)

O bot mantém um registro detalhado de todas as operações:

| Prefixo | Tipo | Exemplo de Uso |
|---------|------|----------------|
| `[BUSCA]` | Informativo | `[BUSCA] Acessando Amazon: Teclado Mecânico...` |
| `[SUCESSO]` | Positivo | `[SUCESSO] Preço extraído: R$ 349,90` |
| `[ERRO]` | Crítico | `[ERRO] Não foi possível localizar preço na página` |
| `[TELEGRAM]` | Notificação | `[TELEGRAM] Alerta enviado com screenshot` |

### 📊 Exemplo de Log Real:
```
[BUSCA] Iniciando monitoramento de 3 produtos...
[BUSCA] Acessando Mercado Livre: Mouse Gamer Logitech
[SUCESSO] Preço encontrado: R$ 189,90
[SUCESSO] Screenshot salva em ./screenshots/mouse_gamer_20250122.png
[TELEGRAM] Mensagem enviada: Produto abaixo do preço de referência!
```

---

## 🛒 Manual da Lista de Compras (Arquivo JSON)

O arquivo `precos.json` é onde você configura os produtos para monitorar:

### 📄 Exemplo de Configuração:
```json
[
  {
    "nome": "Teclado Mecânico Redragon K552",
    "url": "https://www.amazon.com.br/dp/B019O8YZ4A",
    "preco_referencia": 300.00
  },
  {
    "nome": "Mouse Gamer Logitech G203",
    "url": "https://www.mercadolivre.com.br/mouse-gamer-logitech-g203",
    "preco_referencia": 150.00
  },
  {
    "nome": "SSD Kingston 480GB",
    "url": "https://www.terabyteshop.com.br/produto/12345/ssd-kingston",
    "preco_referencia": 250.00
  }
]
```

### 📖 Campos Explicados:

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `nome` | String | Nome do produto (usado nas notificações) | `"Teclado Mecânico Redragon K552"` |
| `url` | String | Link direto da página do produto | `"https://www.amazon.com.br/dp/..."` |
| `preco_referencia` | Number | Preço que você considera bom para comprar | `300.00` |

---

## ✅ Progresso do Projeto (Checklist de Desenvolvimento)

### 🎉 Funcionalidades Concluídas:

- [x] Suporte completo para **Amazon Brasil**
- [x] Suporte completo para **Mercado Livre**
- [x] Suporte completo para **Terabyte Shop**
- [x] Envio de screenshots no Telegram
- [x] Cálculo automático de diferença de preço (R$ e %)
- [x] Sistema de limpeza de anúncios e pop-ups
- [x] Logs coloridos e organizados
- [x] Caminhos dinâmicos (portabilidade)
- [x] Anti-detecção (User-Agent + Viewport)

### 🚧 Próximas Implementações:

- [ ] **Criação de executável (.exe)** via CX-Freeze
- [ ] **Interface Gráfica (GUI)** com Tkinter/PyQt
- [ ] Agendamento automático (rodar de X em X horas)
- [ ] Histórico de preços com gráficos
- [ ] Suporte para mais lojas (Kabum, Pichau, etc.)

---

## 🔧 Instalação e Execução

### 📦 Pré-requisitos:

- Python 3.8 ou superior
- Conta no Telegram (para receber alertas)

### 🚀 Passo a Passo:

**1. Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/price-monitor-bot.git
cd price-monitor-bot
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
playwright install chromium
```

**3. Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:
```env
TELEGRAM_TOKEN=seu_token_do_botfather
TELEGRAM_CHAT_ID=seu_chat_id
```

**4. Configure seus produtos:**

Edite o arquivo `precos.json` com os produtos que deseja monitorar.

**5. Execute o bot:**
```bash
python main.py
```

---

## 🛠️ Informações Técnicas

| Especificação | Detalhes |
|---------------|----------|
| **Versão do Python** | 3.8+ |
| **Bibliotecas Principais** | `playwright`, `python-telegram-bot`, `python-dotenv` |
| **Navegador** | Chromium (via Playwright) |
| **Tempo Médio por Produto** | 5-8 segundos |
| **Modo de Execução** | Headless (invisível) |
| **Formato de Screenshots** | PNG (alta qualidade) |

### 📚 Dependências do `requirements.txt`:
```txt
playwright==1.40.0
python-telegram-bot==20.7
python-dotenv==1.0.0
```

---

## 📸 Exemplo de Notificação no Telegram
```
🛒 ALERTA DE PREÇO!

Teclado Mecânico Redragon K552

💰 Preço Atual: R$ 279,90
📊 Preço Referência: R$ 300,00
✅ Economia: R$ 20,10 (6.7%)

🔗 Link: amazon.com.br/dp/B019O8YZ4A

[Screenshot anexado]
```

---

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

## 👨‍💻 Desenvolvido Por Gabriel Santos

**Price Monitor Bot** - Automatizando suas compras inteligentes!