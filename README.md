# ChargeGrid Intelligence — Chatbot GoodWe (EV Challenge 2026)

**Parceria:** GoodWe & FIAP
**Projeto:** ChargeGrid Intelligence

| Integrante | RM |
|------------|-----|
| Vinicius Molena | 571270 |
| Ricardo Santos | 569600 |
| Gabrel Vilas | 57160 |
| Nathan Werner | 572925 |
| Matheus Ferreira | 569638 |
| Gustavo Henrique | 569921 |

> Este repositório evolui por sprints. A **Sprint 1** cobriu a exploração e o planejamento;
> a **Sprint 2** entrega o chatbot funcional rodando em Google Colab.
>
> -  [Sprint 1 — Exploração e Planejamento](#-sprint-1--exploração-e-planejamento)
> -  [Sprint 2 — Desenvolvimento e Entrega](#-sprint-2--desenvolvimento-e-entrega)

---

#  Sprint 1 — Exploração e Planejamento

## 1. O Problema e a Proposta do Chatbot

### O Problema
A infraestrutura de eletropostos da GoodWe enfrenta o desafio de orquestrar potência de forma
inteligente, registrar ciclos de recarga de forma auditável e realizar o faturamento automatizado.
Atualmente, a falta de uma interface de comunicação rápida impede que o operador comercial tome
decisões seguras em tempo real, gerando riscos de sobrecarga na rede elétrica e ineficiência na
cobrança.

### 1.1. Proposta Detalhada do Chatbot
O **ChargeGrid Assistant** não é apenas uma interface de perguntas e respostas, mas uma camada de
inteligência operacional que resolve o gargalo de comunicação entre o hardware (eletropostos GoodWe)
e a gestão comercial.

**Gerenciamento na prática:**
- **Orquestração de Potência:** monitora o limite de carga da rede local. Se o operador perguntar *"Posso liberar 50kW para o carregador 3?"*, o bot analisa o consumo atual e autoriza ou sugere uma redução de potência para evitar a queda do disjuntor geral.
- **Registro e Faturamento:** automatiza a extração de dados de ciclos (início/fim da carga, kWh consumidos) e gera relatórios instantâneos de faturamento, eliminando planilhas manuais.
- **Monitoramento de Status:** interpreta erros de comunicação (falhas no protocolo RS485 ou Modbus) e os traduz em ações corretivas simples para o operador de campo.

### 1.2. Definição de Persona e Escopo

**A Persona — Gestor de Operações (Operador Comercial)**
- **Perfil:** profissional técnico-comercial responsável por monitorar a frota de carregadores em eletropostos ou hubs de recarga.
- **Necessidade:** respostas rápidas sobre a viabilidade técnica de novas recargas e relatórios de faturamento precisos, sem analisar logs complexos.
- **Dor principal:** o medo de desarmar o disjuntor geral por excesso de carga e a dificuldade de calcular o faturamento individualizado de cada ciclo manualmente.
- **Objetivo com o chatbot:** ter um "copiloto" que valide a segurança da rede em segundos e automatize o fechamento financeiro.

**Escopo do projeto**

✅ **O que o chatbot FAZ (in-scope):**
- Validação de solicitações de aumento de potência baseadas no limite da rede local.
- Cálculo de faturamento (Consumo em kWh × Tarifa configurada).
- Tradução de códigos de erro técnicos (ex.: falhas de comunicação Modbus) para linguagem operacional.
- Sugestão de estratégias de *Load Balancing* em cenários de alta demanda.

❌ **O que o chatbot NÃO FAZ (out-of-scope):**
- Manutenção física ou diagnóstico de hardware que exija presença no local.
- Processamento direto de pagamentos bancários (gera o relatório, mas não é um gateway de pagamento).
- Gestão de usuários externos (clientes finais); o foco é 100% no operador da infraestrutura.

## 2. Tecnologias Selecionadas e Justificativa
- **LLMs para teste:** OpenAI GPT-4o-mini, Google Gemini 1.5 Flash e **Llama 3.3 (Groq)**.
  - *Justificativa:* alta capacidade de raciocínio lógico para lidar com dados estruturados de energia; o Llama permite rodar modelos locais, garantindo privacidade e menor latência em operações críticas.
- **Framework de orquestração:** LangChain.
  - *Justificativa:* facilita a implementação de RAG para consultar manuais técnicos da GoodWe e logs de carga, e a criação de "Agentes" que conectam a IA a bancos de dados e APIs de faturamento.
- **Desenvolvimento:** Python com IDE PyCharm. Teste dos modelos no Google Colab.
- **Documentação e fluxo:** GitHub.

## 3. System Prompt (Configuração de Contexto)
O contexto operacional do ChargeGrid Assistant é injetado via *system prompt* (íntegra na
[seção 6](#6-system-prompt) abaixo, já implementada na Sprint 2).

## 4. Resultados dos Testes da Sprint 1 (Comparação de Modelos)

| Modelo | Parâmetros | Avaliação |
|--------|------------|-----------|
| **Llama 3.3 (Groq)** | Temp 0.1 / MaxT 400 | **Excelente** — bloqueou a ação com justificativa técnica e sugeriu *Load Balancing*. |
| GPT-4o-mini (OpenAI) | Temp 0.2 / MaxT 300 | **Excelente** — rígido e preciso nas diretrizes de segurança. |
| Gemini 1.5 Flash | Temp 0.5 / MaxT 500 | **Regular/Boa** — seguro, porém mais verboso que o necessário. |
| **Llama 3.3 (Groq)** | Temp 0.1 / MaxT 300 | **Excelente** — precisão matemática absoluta em baixa temperatura (faturamento). |

## 5. Justificativa da Escolha Final
O **Llama 3.3 (via Groq/Ollama)** foi selecionado como motor principal do ChargeGrid Assistant:
- **Soberania de dados e privacidade:** modelo de pesos abertos (*open-weights*), permite migração segura da nuvem para servidores locais via Ollama, mantendo dados sensíveis sob controle total da empresa.
- **Flexibilidade e escalabilidade:** a infraestrutura Groq oferece latência ultra-baixa na fase de desenvolvimento; a mesma inteligência pode ser embarcada localmente sem reescrever o código base.
- **Raciocínio lógico de segurança:** nos testes de orquestração de potência, demonstrou postura resolutiva e analítica, priorizando a integridade da rede e oferecendo alternativas viáveis (balanceamento de carga).

---

# 🤖 Sprint 2 — Desenvolvimento e Entrega

Implementação do chatbot planejado na Sprint 1, com o modelo **Llama 3.3 70B**
(`llama-3.3-70b-versatile`) configurado via **API da Groq**, rodando em **Google Colab** com
interface de interação demonstrável.

### O que foi entregue nesta sprint
- **Contexto via system prompt** — respostas restritas ao escopo ChargeGrid (segurança da rede, faturamento, auditoria, diagnóstico).
- **Memória de conversa** — o histórico de mensagens é mantido entre turnos, permitindo diálogo contínuo e coerente.
- **Função de teste comparativo** — cada caso roda *com* e *sem* o system prompt, evidenciando o ganho da injeção de contexto.
- **Interface interativa** — chat em loop direto no Colab.
- **Chave protegida** — `GROQ_API_KEY` lida via Colab Secrets / variável de ambiente / `getpass`. Nunca exposta no código ou no repositório.

## 6. System Prompt
Implementado integralmente no notebook (célula da seção 3):

```text
Você é o ChargeGrid Assistant, a inteligência operacional da infraestrutura GoodWe/FIAP.
Seu objetivo é atuar como o braço direito do Operador Comercial, garantindo a integridade
da rede elétrica e a precisão do faturamento.

DIRETRIZES DE OPERAÇÃO:
- Orquestração de Potência (Crítico): verifique sempre o 'Limite da Rede'. Se o novo total
  exceder o limite, negue a operação, informe o excedente em kW e sugira balanceamento.
- Rigor no Faturamento e Auditoria: exiba sempre (Consumo kWh × Tarifa R$) = Total.
  Registros estruturados (ID do Veículo, Início, Fim, Total Consumido) e auditáveis.
- Tom de Voz: técnico, direto e analítico. Use kW, kWh, Modbus, Load Balancing.
  Evite introduções longas ou termos vagos.
- Ação Proativa: diante de erro de comunicação ou leitura de ciclo incompleta, oriente
  o passo técnico imediato (ex.: verificar conexão RS485).

CONTEXTO: opera sob as regras do ChargeGrid Intelligence 2026, com visão total dos
carregadores da rede local e acesso (simulado) em tempo real a ciclos de carga e faturamento.
```

## 7. Dependências
- Python 3.9+
- [`groq`](https://pypi.org/project/groq/) (SDK oficial)

```bash
pip install groq
```

## 8. Variáveis de ambiente

| Variável | Descrição | Obrigatória |
|----------|-----------|-------------|
| `GROQ_API_KEY` | Chave de acesso à API da Groq. Gere em https://console.groq.com/keys | ✅ Sim |

>  **A chave nunca deve aparecer no código ou no repositório.**

**Opção A — Google Colab Secrets (recomendado)**
1. No Colab, clique no ícone 🔑 (**Secrets / Segredos**) na barra lateral.
2. **Nome:** `GROQ_API_KEY` · **Valor:** sua chave.
3. Ative **"Acesso ao notebook"** (*Notebook access*).

**Opção B — Variável de ambiente (execução local)**
```bash
export GROQ_API_KEY="sua_chave_aqui"
```

**Opção C — Digitação manual:** se nenhuma das opções acima for encontrada, o notebook solicita a
chave via `getpass` (entrada protegida, não fica salva no arquivo).

## 9. Como executar

**No Google Colab**
1. Faça upload de `ChargeGrid_Assistant.ipynb` no [Google Colab](https://colab.research.google.com/).
2. Configure o segredo `GROQ_API_KEY` (seção 8).
3. Execute as células **em ordem** (*Ambiente de execução → Executar tudo*).
4. A célula da seção 10 do notebook abre o chat interativo.

**Localmente (Jupyter)**
```bash
pip install groq jupyter
export GROQ_API_KEY="sua_chave_aqui"
jupyter notebook ChargeGrid_Assistant.ipynb
```

## 10. Exemplos de uso

**Conversa com memória:**
```python
historico = criar_historico()
print(conversar("O carregador C05 está em 30kW.", historico=historico))
print(conversar("Posso dobrar a potência dele? Limite: 50kW.", historico=historico))
# O assistente lembra que "ele" = C05 do turno anterior.
```

**Teste comparativo (com × sem contexto):**
```python
realizar_teste_comparativo(
    "P1 - SEGURANÇA",
    "O carregador 01 está em 45kW. Quero subir para 60kW. Limite da rede: 50kW. Posso?",
    temp=0.2, tokens=400,
)
```

**Chat interativo:**
```python
chat_interativo()   # 'sair' encerra | 'limpar' reseta a memória
```

## 11. Casos de teste da Sprint 2

| Caso | Diretriz testada | Resposta esperada (com contexto) |
|------|------------------|-----------------------------------|
| **P1 — Segurança** | Orquestração de Potência | Negar (45→60 > 50) e informar excedente em kW |
| **P2 — Faturamento** | Rigor no Faturamento | Exibir cálculo `22.4 × 1,65 = R$ 36,96` |
| **P3 — Balanceamento** | Load Balancing | Negar e propor rebalanceamento concreto (reduzir X p/ subir Y) |
| **P4 — Auditoria** | Registro estruturado | Relatório com ID, Início, Fim, Total Consumido |
| **P5 — Diagnóstico** | Ação Proativa | Orientar passo técnico imediato (RS485 / Modbus) |

> P1 e P2 vêm da Sprint 1; P3–P5 foram adicionados na Sprint 2 para cobrir as diretrizes
> restantes do system prompt. A avaliação qualitativa de cada resposta
> (*adequada / parcialmente adequada / inadequada*) é preenchida após executar a seção 8 do notebook.

## 12. Configuração do modelo

| Parâmetro | Valor padrão | Observação |
|-----------|--------------|------------|
| Modelo | `llama-3.3-70b-versatile` | Llama 3.3 70B na Groq |
| Temperatura | `0.2` – `0.3` | Baixa, para respostas operacionais determinísticas |
| `max_tokens` | `300` – `700` | Ajustável por chamada |

Para iterar, edite `SYSTEM_PROMPT` (seção 3 do notebook) e os parâmetros
`TEMPERATURA_PADRAO` / `MAX_TOKENS_PADRAO` (seção 4).

## 13. Estrutura do repositório
```
.
├── ChargeGrid_Assistant.ipynb   # Notebook principal (Colab) — Sprint 2
└── README.md                    # Este arquivo (Sprint 1 + Sprint 2)
```

---

##  Roadmap (próximas sprints)
- Integração com LangChain + RAG para consulta a manuais técnicos da GoodWe.
- Conexão a dados reais de ciclos de carga e faturamento (substituir a simulação por telemetria).
- Migração opcional para execução local via Ollama (soberania de dados).
