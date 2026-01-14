# 🛒 E-Commerce Price Monitor | Automação Terabyte

Um **bot inteligente de monitoramento de preços** que rastreia produtos em tempo real na Terabyteshop, com técnicas de bypass anti-bot e notificações automáticas quando o preço atinge sua meta.

## 🎯 Visão Geral

Este projeto implementa um sistema de **web scraping automatizado** que:

- ✅ Monitora produtos em tempo real sem bloqueios
- ✅ Implementa técnicas de stealth para contornar anti-bot
- ✅ Lê configurações dinâmicas de JSON
- ✅ Verifica disponibilidade de produtos
- ✅ Compara preços com metas definidas
- ✅ Exibe alertas automáticos no terminal

## 🚀 Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **Python** | 3.8+ | Linguagem principal |
| **Playwright** | Latest | Automação de browser com headless control |
| **JSON** | - | Armazenamento de configuração de produtos |
| **Chromium** | Latest | Engine de navegação |

### Dependências Principais
```
playwright >= 1.40.0
```

## 💡 Destaques Técnicos

### 🕵️ Anti-Bot Bypass
Implementa múltiplas estratégias para evitar detecção:

```python
# User-Agent realista
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."

# Desabilitação de marcadores de automação
args=["--disable-blink-features=AutomationControlled"]

# Viewport realista
viewport={"width": 1366, "height": 768}

# Delays aleatórios para simular comportamento humano
page.wait_for_timeout(random.randint(3000, 5000))
```

### 📖 Leitura Dinâmica de JSON
O script relê o arquivo JSON a cada iteração, permitindo **atualização em tempo real** de metas de preço sem parar a execução:

```python
for item in dados_json:
    with open(ARQUIVO_JSON, 'r', encoding='utf-8-sig') as f:
        produto = json.load(f)[item]  # Captura mudanças em tempo real
```

### 🔍 Detecção de Indisponibilidade
Usa seletores de heading para detectar status do produto:

```python
aviso_indisponivel = page.get_by_role("heading", name=" Produto Indisponível")
```

### 💰 Parsing Inteligente de Preços
Remove formatação de moeda e converte para float:

```python
preco_limpo = texto_bruto.replace('R$', '').replace('.', '').replace(',', '.').strip()
preco_atual = float(preco_limpo)
```

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes)
- ~100MB de espaço em disco (para Chromium)

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/automacao_ecommerce.git
cd automacao_ecommerce
```

### Passo 2: Instalar Dependências Python
```bash
pip install -r requirements.txt
```

Ou instalar manualmente:
```bash
pip install playwright
```

### Passo 3: Instalar Browser Chromium
```bash
playwright install chromium
```

## ⚙️ Configuração

### Estrutura do `precos.json`

O arquivo `precos.json` centraliza todas as configurações de produtos a monitorar:

```json
{
    "monitor_superframe": {
        "nome": "Monitor Gamer SuperFrame 23.8\"",
        "preco_referencia": 500.0,
        "url": "https://www.terabyteshop.com.br/produto/36653/monitor-gamer-superframe...",
        "status": "ativo"
    },
    "samsung_G5": {
        "nome": "Monitor Gamer Samsung Odyssey G5 34\"",
        "preco_referencia": 1800.0,
        "url": "https://www.terabyteshop.com.br/produto/31707/monitor-gamer-samsung-odyssey...",
        "status": "indisponivel"
    },
    "seu_produto": {
        "nome": "Nome do Produto",
        "preco_referencia": 999.99,
        "url": "https://www.terabyteshop.com.br/produto/xxxxx/seu-produto...",
        "status": "ativo"
    }
}
```

### Campos Obrigatórios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nome` | String | Nome descritivo do produto |
| `preco_referencia` | Float | Preço máximo aceito (em R$) |
| `url` | String | URL completa do produto na Terabyte |
| `status` | String | `"ativo"` ou `"indisponivel"` (opcional) |

### Como Adicionar Novos Produtos

1. Acesse a Terabyteshop e encontre o produto desejado
2. Copie a URL completa
3. Adicione uma nova entrada no `precos.json`:

```json
"novo_produto": {
    "nome": "Descrição clara do produto",
    "preco_referencia": 1500.00,
    "url": "https://www.terabyteshop.com.br/produto/xxxxx/seu-produto...",
    "status": "ativo"
}
```

4. Salve o arquivo - a mudança será detectada automaticamente na próxima iteração!

## 🎮 Como Usar

### Execução Básica

```bash
python automacao.py
```

O script exibirá saída como:

```
--- CONTEÚDO BRUTO DO ARQUIVO NO DISCO ---
{
    "monitor_superframe": {...},
    ...
}
------------------------------------------

--- Verificando: Monitor Gamer SuperFrame 23.8" ---
Alvo atual: R$ 500.00
 STATUS: Disponível | Preço Site: R$ 520.50
 Ainda caro. Diferença: R$ 20.50. Não recomendo comprar.

--- Verificando: Monitor Gamer Samsung Odyssey G5 34" ---
Alvo atual: R$ 1800.00
 STATUS: Produto Indisponível no momento.

========================================
Automação concluída.
```

### Cenários de Execução

#### ✅ Preço Atingiu a Meta
```
--- Verificando: Monitor Gamer SuperFrame 23.8" ---
Alvo atual: R$ 500.00
 STATUS: Disponível | Preço Site: R$ 499.99
 ALERTA: O PREÇO ATINGIU O SEU ALVO!
```

#### ❌ Preço Acima da Meta
```
 STATUS: Disponível | Preço Site: R$ 520.50
 Ainda caro. Diferença: R$ 20.50. Não recomendo comprar.
```

#### ⚠️ Produto Indisponível
```
 STATUS: Produto Indisponível no momento.
```

## 🏗️ Estrutura do Projeto

```
automacao_ecommerce/
├── automacao.py          # Script principal
├── precos.json           # Arquivo de configuração
├── requirements.txt      # Dependências Python
└── README.md            # Esta documentação
```

## 🔧 Troubleshooting

### Problema: Timeout ao carregar página
**Solução:** Aumente o tempo de espera em `page.wait_for_timeout()`:
```python
page.wait_for_timeout(random.randint(5000, 8000))  # Aumentado para 5-8s
```

### Problema: CAPTCHA persistente
**Solução:** O script usa `--disable-blink-features=AutomationControlled`, mas para casos extremos:
```python
# Adicione proxies ou aumente delays ainda mais
```

### Problema: Arquivo JSON não encontrado
**Solução:** Verifique o caminho absoluto:
```python
# Windows
ARQUIVO_JSON = r"D:\Desenvolvimento\automacao_ecommerce\precos.json"

# Linux/Mac
ARQUIVO_JSON = "/home/user/automacao_ecommerce/precos.json"
```

### Problema: Playwright não consegue encontrar Chromium
**Solução:** Reinstale o browser:
```bash
playwright install --with-deps chromium
```

## 📊 Exemplos de Uso

### Monitorar Componentes de PC
```json
{
    "placa_video_rtx": {
        "nome": "RTX 4070 SUPER",
        "preco_referencia": 4200.00,
        "url": "https://www.terabyteshop.com.br/produto/xxxxx/rtx-4070-super...",
        "status": "ativo"
    }
}
```

### Monitorar Múltiplos Produtos
Adicione quantos produtos quiser ao JSON - o script iterará automaticamente por todos!

## ⚡ Performance

- **Tempo médio por produto:** 5-10 segundos
- **Consumo de memória:** ~150MB
- **CPU:** Baixo quando ocioso, médio durante navegação

## 🔐 Segurança & Ética

⚠️ **Aviso Legal:**
- Use este script **apenas para seus próprios fins**
- Respeite os `robots.txt` e Termos de Serviço da Terabyte
- Implemente delays apropriados entre requisições
- Não distribua ou revenda dados coletados

Este projeto segue as melhores práticas de web scraping ético com:
- Delays aleatórios entre requisições
- User-Agent realista
- Respeito aos limites de taxa

## 🚀 Melhorias Futuras

- [ ] Integração com Telegram/Email para notificações
- [ ] Dashboard web em tempo real
- [ ] Suporte a múltiplos e-commerce
- [ ] Histórico de preços com gráficos
- [ ] API REST para consultar preços
- [ ] Banco de dados SQLite para persistência

## 📝 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Sobre o Desenvolvedor

Desenvolvido como projeto de automação e web scraping, demonstrando:
- Domínio de Playwright e automação de browser
- Técnicas de bypass anti-bot
- Tratamento de erros robusto
- Arquitetura escalável

## 📧 Contato & Contribuições

Para dúvidas, sugestões ou contribuições:
- Abra uma **Issue** no repositório
- Envie um **Pull Request** com melhorias
- Entre em contato via [seu email/LinkedIn]

---

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

*Última atualização: Janeiro 2026*
