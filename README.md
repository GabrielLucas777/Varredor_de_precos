# Automação de E-commerce - Monitoramento de Preços

Um bot automatizado em Python para monitorar preços de produtos em lojas online, alertando quando o valor atinge seu alvo de compra. O projeto foi desenvolvido com foco em **modularização** e **camuflagem anti-bot**, aplicando boas práticas de desenvolvimento.

---

## Sobre o Projeto

Este projeto implementa um sistema inteligente de rastreamento de preços que:

- Acessa automaticamente lojas online via navegador controlado
- Extrai preços de produtos em tempo real
- Compara com valores de referência configuráveis
- Simula comportamento humano para evitar bloqueios
- Organiza a lógica em "departamentos" especializados

**Por que foi criado?** Para aplicar conhecimentos de automação web, tratamento de dados e boas práticas de arquitetura em um projeto real do cotidiano.

---

## Estrutura do Projeto: Os "Departamentos"

O código está organizado como uma empresa com departamentos especializados, cada um com sua responsabilidade:

### Almoxarifado (Parte 1 - Configuração)
Responsável pelo **armazenamento de dados** e configurações centralizadas:
- Define o caminho do arquivo JSON (`ARQUIVO_JSON`)
- Garante que todas as funções consigam acessar a fonte de dados

```python
ARQUIVO_JSON = r"D:\Desenvolvimento\automacao_ecommerce\precos.json"
```

---

### Especialistas de Dados (Parte 2 - Funções de Apoio)
Time responsável pelo **tratamento e processamento de informações**:

- **`tratar_preco()`**: Converte texto bruto em números decimais
  - Remove símbolos monetários (`R$`)
  - Normaliza pontos e vírgulas
  - Retorna um `float` pronto para cálculos

- **`carregar_dados_json()`**: Lê o arquivo de dados
  - Carrega produtos e preços de referência
  - Trata erros de leitura graciosamente

---

### Especialistas Web (Parte 3 - Ação Web)
Equipe responsável pela **navegação e extração de dados** do site:

- **`verificar_produto_no_site()`**: A função principal deste departamento
  - Navega até a URL do produto
  - Aguarda carregamento completo da página
  - **Simula comportamento humano**: delay aleatório (3-5 segundos)
  - Verifica disponibilidade do produto
  - Extrai e trata o preço via seletor CSS
  - Retorna o valor atual ou `None` em caso de erro

---

### Gerente (Parte 4 - Fluxo Principal)
Coordena todo o **orquestramento da automação**:

- **`executar_bot()`**: Função executiva que:
  1. Inicializa o navegador Playwright com camuflagem anti-bot
  2. Carrega dados do JSON
  3. Itera por cada produto
  4. Chama especialistas para verificar preço
  5. Compara e exibe alertas
  6. Finaliza o processo

**Camuflagem Anti-bot Ativa:**
```python
args=["--disable-blink-features=AutomationControlled"]
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
```

---

## O Coração de Dados: `precos.json`

O arquivo `precos.json` é o **coração de dados** do projeto. Nele você define todos os produtos a monitorar:

```json
{
  "produto_1": {
    "nome": "Monitor LG 24\"",
    "url": "https://exemplo.com/produto/monitor-lg-24",
    "preco_referencia": 800.00
  },
  "produto_2": {
    "nome": "Teclado Mecânico",
    "url": "https://exemplo.com/produto/teclado-mecanico",
    "preco_referencia": 350.00
  }
}
```

**Como funciona:**
- Cada entrada é um produto com identificador único (`produto_1`, `produto_2`)
- `nome`: Usado apenas para exibição no console
- `url`: Link direto do produto na loja
- `preco_referencia`: Seu preço-alvo (bot alertará quando preço ≤ este valor)


---

## Como Configurar

### Pré-requisitos
- Python 3.8+
- Windows, macOS ou Linux

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/automacao_ecommerce.git
cd automacao_ecommerce
```

### Passo 2: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Instalar Navegadores do Playwright
O Playwright requer que você instale os navegadores controlados:
```bash
playwright install
```

Isso baixará automaticamente o Chromium, Firefox e WebKit (você pode usar apenas `chromium` neste projeto).

### Passo 4: Configurar Seus Produtos
Edite o arquivo `precos.json` com seus produtos:

```json
{
  "samsung_tv": {
    "nome": "Smart TV Samsung 55\"",
    "url": "https://loja.com.br/samsung-tv-55",
    "preco_referencia": 2500.00
  }
}
```

### Passo 5: Executar o Bot
```bash
python automacao.py
```

O bot abrirá uma janela do navegador e começará a verificar os preços.

---

## Entendendo a Saída do Console

```
--- Verificando: Monitor LG 24" ---
Alvo atual: R$ 800.00

Pausa aleatória (3-5 seg) para simular humano...

STATUS: Disponível | Preço Site: R$ 750.50
ALERTA: O PREÇO ATINGIU O SEU ALVO! RECOMENDO COMPRAR AGORA!
```

**Possíveis Mensagens:**
- `ALERTA: O PREÇO ATINGIU O SEU ALVO!` → Preço ≤ seu alvo
- `Ainda caro. Diferença: R$ XX.XX` → Preço acima do alvo
- `Produto Indisponível no momento` → Sem estoque
- `Preço não localizado (pode ser Captcha)` → Possível bloqueio

---

## Camuflagem Anti-Bot Explicada

O projeto implementa técnicas para evitar ser detectado como automação:

1. **User-Agent personalizado**: Simula um navegador Chrome real
2. **Desabilitar sinais de automação**: `--disable-blink-features=AutomationControlled`
3. **Viewport realista**: 1366x768 (resolução comum)
4. **Delays aleatórios**: Aguarda 3-5 segundos entre ações
5. **Pausas entre produtos**: 2 segundos para simular navegação natural

Essas técnicas reduzem o risco de bloqueios por WAF (Web Application Firewall).

---

## Próximas Features

### Integração com Telegram (em andamento)
- Receber alertas de preço via bot do Telegram
- Notificações em tempo real para o seu celular
- Comandos para listar produtos monitorados

### Monitoramento de Múltiplas Lojas
- **Suporte para Kabum**: Especificar produtos do Kabum
- **Suporte para Amazon**: Rastrear preços na Amazon Brasil
- Sistema de priorização por loja

### Interface Gráfica (GUI)
- Dashboard com interface amigável usando PyQt5 ou Tkinter
- Gráficos de evolução de preços
- Gerenciador visual de produtos
- Histórico de alertas

---

## ⚙️ Requisitos Técnicos

| Dependência | Versão | Propósito |
|---|---|---|
| `playwright` | ≥1.40.0 | Automação de navegador |
| Python | ≥3.8 | Linguagem base |

---

## Exemplo Completo de Uso

**Arquivo `precos.json`:**
```json
{
  "notebook_dell": {
    "nome": "Notebook Dell Inspiron 15",
    "url": "https://www.amazon.com.br/notebook-dell",
    "preco_referencia": 3500.00
  },
  "mouse_logitech": {
    "nome": "Mouse Logitech MX Master 3S",
    "url": "https://www.kabum.com.br/produto/mouse-mx",
    "preco_referencia": 450.00
  }
}
```

**Executar:**
```bash
python automacao.py
```

**Resultado esperado:**
- Bot abre navegador
- Verifica notebook por R$ 3500.00
- Verifica mouse por R$ 450.00
- Exibe alertas se preços atingem os alvos

---

## Troubleshooting

### "Erro ao ler o JSON"
- Verifique se o caminho em `ARQUIVO_JSON` está correto
- Certifique-se de que `precos.json` existe no diretório

### "playwright: command not found"
- Execute: `playwright install`

### Página não carrega
- Aumente o timeout em `page.wait_for_timeout()`
- Verifique sua conexão de internet
- Verifique se a URL do produto está correta

### Muitos bloqueios de Captcha
- Aumente os delays aleatórios
- Adicione mais variação de user-agents
- Use um proxy rotativo

---

## Lições Aprendidas

Este projeto aplicou na prática:

- **Modularização**: Código dividido em funções com responsabilidades claras  
- **Tratamento de dados**: Conversão e normalização de valores monetários  
- **Automação web**: Navegação controlada via Playwright  
- **Camuflagem anti-bot**: Técnicas para evitar detecção  
- **Trabalho com JSON**: Carregamento e iteração de dados estruturados  
- **Boas práticas**: Variáveis bem nomeadas, comentários informativos, fluxo lógico  

---

## Licença

Este projeto é fornecido como-é para fins educacionais.

---

## Contribuições

Se você tem melhorias ou novas features, sinta-se livre para abrir uma issue ou PR!

---

## Contato

Desenvolvido como projeto de aprendizado em automação web.

**Última atualização:** Janeiro de 2026
