# 🧠 CONTRATO DE ENGENHARIA: CRYPTO HUNTER (v2.0)

**AVISO CRÍTICO:** Este arquivo é a LEI do projeto. Você (Claude Code) deve lê-lo no início de CADA sessão. Se uma instrução do usuário violar este contrato, você deve recusar e explicar o motivo.

---

## ⚠️ PARTE 0: GUARDA DE SISTEMA OPERACIONAL (GATEKEEPER)
Você está rodando em um ambiente **Windows PowerShell**. 
- É TERMINANTEMENTE PROIBIDO usar sintaxe Bash (grep, awk, sed, cat). 
- Use `Select-String`, `Get-Content` ou as ferramentas nativas do Claude Code (Read, Glob, Grep).
- Se um comando falhar, NÃO repita o loop. Mude a estratégia tática.
- Se o contexto estiver muito grande (acima de 50K tokens), solicite ao usuário o comando `/compact` IMEDIATAMENTE.

---

## 🏛️ PARTE 1: OS 4 PILARES DA ENGENHARIA (KARPATHY)
1. **PENSE ANTES DE CODAR**: Nunca assuma interpretações. Apresente trade-offs. Se não entendeu, diga "Não entendi X".
2. **SIMPLICIDADE PRIMEIRO**: Não crie abstrações para uso único. Escreva o mínimo necessário.
3. **MUDANÇAS CIRÚRGICAS**: Não refatore código adjacente. Remova apenas o que a sua mudança tornou órfão.
4. **EXECUÇÃO ORIENTADA A METAS**: Transforme toda tarefa em um critério verificável (ex: "Escrever teste que reproduz o bug, depois corrigir").

---

## 🧩 PARTE 2: ARQUITETURA DE CAMADAS (SKILLS vs. MCP vs. RAG)

Você deve distinguir claramente o papel de cada camada antes de agir. Não confunda ferramenta com procedimento.

### 2.1 Skills (O "Como Fazer" - Conhecimento Procedural)
Skills são manuais de instruções que você carrega sob demanda. Elas ensinam **procedimentos**.
- **Obrigatório:** Use `/tdd` antes de escrever código novo.
- **Obrigatório:** Use `/code-review` antes de commitar.
- **Obrigatório:** Use `/diagnosing-bugs` se algo quebrar.
- **Novas Skills:** Se o usuário pedir para criar uma skill, ela deve ser um diretório em `.claude/skills/` com um `SKILL.md` (frontmatter + instruções concisas, <500 linhas).

### 2.2 MCP (O "O Quê" - Ferramentas e Dados)
MCP é a camada de conexão com o mundo externo (APIs, bancos de dados). **Nunca crie um MCP se uma Skill resolver.**
- **`sequential-thinking`**: Obrigatório para cálculos de taxa, edge, lucro.
- **`context7`**: Obrigatório para consultar sintaxe de bibliotecas (`ccxt`, `pandas`). **PROIBIDO** inventar sintaxe.
- **`mt5`**: Obrigatório para validar ordens e cotações em tempo real.
- **`playwright`**: Obrigatório para testar o frontend visualmente.

### 2.3 RAG (O "Conhecimento" - Base de Dados Privada)
RAG é a camada de **conhecimento factual** que você não pode inventar. Sempre que precisar de informações sobre o projeto, consulte a base RAG (se disponível) antes de responder.
- **Fontes:** Documentos em `./docs/`, logs de trades, estratégias em PDF, histórico de decisões.
- **Pipeline:** Se o usuário pedir para implementar RAG, siga o padrão: Ingestão (Chunking 400-512 tokens, overlap 10-20%) → Embedding (via OmniRoute) → Vector DB (ChromaDB local) → Retrieval → Generation.
- **Regra de Ouro:** Use RAG para **fatos** (o que o modelo não sabe) e Fine-Tuning para **comportamento** (como o modelo responde). Não use RAG para ensinar estilo.

### 2.4 Subagents (Isolamento de Contexto)
Para tarefas de exploração pesada (ler muitos arquivos, pesquisar logs), **delegue para um subagent**. Isso mantém o contexto principal limpo e evita o `/compact` prematuro.

---

## 🛠️ PARTE 3: FERRAMENTAS OBRIGATÓRIAS (MUST USE)

| Ferramenta | Quando USAR (Gatilho) | Consequência se não usar |
| :--- | :--- | :--- |
| **`sequential-thinking`** | Cálculos de taxa, edge, lucro, ou lógica complexa. | **BLOQUEIO**: Não pode commitar sem ter usado. |
| **`context7`** | Qualquer biblioteca (`ccxt`, `pandas`, `FastAPI`). | **PROIBIDO** inventar sintaxe. |
| **`mt5`** | Validar ordens e cotações em tempo real. | Obrigatório para `arbitrage/`. |
| **`playwright`** | Testar o frontend (`web/`) no navegador. | **BLOQUEIO**: Frontend só é "pronto" após teste visual. |
| **`RAG (ChromaDB)`** | Dúvidas sobre regras de negócio, logs históricos ou documentação. | Respostas baseadas em alucinação. |

---

## 🎨 PARTE 4: FRONTEND BLINDADO (ANTI-GENÉRICO)

O painel de arbitragem em `web/` deve parecer um produto único.

### Proibições Absolutas (NUNCA faça isso)
- **PROIBIDO** usar fontes genéricas: `Inter`, `Roboto`, `Arial`, `Space Grotesk`.
- **PROIBIDO** usar paletas clichês de IA (fundo branco com roxo/azul).
- **PROIBIDO** usar o "SaaS-card kit" (cartões idênticos com sombra suave igual).
- **PROIBIDO** gradientes aleatórios.

### Obrigações (MUST do)
1. **Antes de codar**, invoque `/web-design-guidelines` e crie um plano de design (paleta hex, tipografia com personalidade, wireframe ASCII).
2. Use **TradingView Lightweight Charts** para candles em tempo real.
3. Conecte aos WebSockets da Binance e Bybit.
4. Use `playwright` para validar visualmente antes de dizer que está pronto.

---

## 🚨 PARTE 5: BUGS FINANCEIROS (PRIORIDADE MÁXIMA)

Bugs de cálculo têm prioridade absoluta.

### Fila Atual de Correções
| Severidade | Linha | Arquivo | Problema | Status |
| :--- | :--- | :--- | :--- | :--- |
| 🔴 **CRÍTICO** | 259 | `web/data_service.py` | `price_b = edge/1000` (deveria ser `1+edge`) | **CORRIGIR AGORA** |
| 🔴 **CRÍTICO** | 358 | `web/data_service.py` | Sem fallback se `intelligence_core` quebra | Aguardando |
| 🟠 ALTO | 238 | `web/data_service.py` | Dead code: `funding_by_pair` nunca usado | Aguardando |

### Protocolo de Correção
1. **`/tdd`**: Escreva o teste de regressão (RED). Ele deve falhar.
2. Corrija o código (GREEN). O teste deve passar.
3. Comentário obrigatório: `# CRÍTICO: linha 259 originalmente fazia edge/1000`.
4. **1 Commit por bug**: `fix(data_service): corrige price_b (CRÍTICO — subestimava 100x)`.

---

## 🛡️ PARTE 6: GATE DE QUALIDADE (BLOQUEIO DE COMMIT)

**NENHUM COMMIT É PERMITIDO** sem passar por este gate.

- [ ] **1. `/code-review` rodou e retornou OK?**
- [ ] **2. `pytest` está verde (0 falhas)?**
- [ ] **3. `git diff` mostra APENAS os arquivos esperados?**
- [ ] **4. Os 4 princípios do Karpathy foram respeitados?**
- [ ] **5. Se for frontend, as regras da Vercel foram seguidas e o `playwright` validou?**
- [ ] **6. Se a tarefa envolveu conhecimento factual, o RAG foi consultado?**

---

## ⚠️ PARTE 7: REGRAS DE CONTEXTO

- **NUNCA** leia o projeto inteiro. Leia apenas os arquivos da tarefa atual.
- Se o contexto chegar a **80%**, use `/compact` ou `/clear`.
- Evite screenshots gigantes no `playwright`.
- Use **Subagents** para exploração pesada (ex: "leia todos os logs de trades e resuma").

---

## 🧠 PARTE 8: DIRETRIZES DE EVOLUÇÃO (RAG & FINE-TUNING)

Se o usuário solicitar melhorias na inteligência do sistema, siga estas regras:

### 8.1 Implementação de RAG
- **Quando usar:** O sistema precisa responder perguntas sobre documentos internos, logs ou estratégias passadas.
- **Pipeline Obrigatório:** `LangChain` ou `LlamaIndex` + `ChromaDB` + `OpenAIEmbeddings` (via OmniRoute).
- **Chunking:** 400-512 tokens, overlap de 10-20%. Prefira `RecursiveCharacterTextSplitter`.
- **Avaliação:** Use `RAGAS` (Faithfulness, Answer Relevance, Context Precision). Nunca declare "pronto" sem métricas.

### 8.2 Fine-Tuning (LoRA/QLoRA)
- **Quando usar:** O sistema precisa gerar respostas em um **formato específico** (ex: JSON de ordem, relatório de P&L) de forma consistente.
- **Regra de Ouro:** Não use Fine-Tuning para conhecimento (use RAG). Use para **comportamento**.
- **Técnica Padrão:** QLoRA (4-bit) com `r=16`, `lora_alpha=32`, `target_modules="all-linear"`.
- **Baseline Obrigatório:** Antes de treinar, compare com o modelo base + prompt few-shot. Se o Fine-Tuning não superar o baseline, descarte.

---
**LEMBRETE FINAL:** Se você (Claude) estiver prestes a responder algo que viole este contrato, PARE. Diga: "Não posso fazer X porque viola a regra Y do CLAUDE.md. Posso fazer Z, que é compatível." O usuário prefere uma recusa honesta a uma resposta que quebre a arquitetura.