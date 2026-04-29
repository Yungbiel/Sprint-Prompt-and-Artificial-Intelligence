# Sprint-Prompt-and-Artificial-Intelligence
ChargeGrid Intelligence — Sprint 1:  Exploração e Planejamento do Chatbot GoodWe
1. Identificação do Projeto
Projeto: ChargeGrid Intelligence (EV Challenge 2026)
Parceria: GoodWe & FIAP
Integrantes: [NOME - RM]
2. O Problema e a Proposta do Chatbot
O Problema
A infraestrutura de eletropostos da GoodWe enfrenta o desafio de orquestrar potência de forma inteligente, registrar ciclos de recarga de forma auditável e realizar o faturamento automatizado. Atualmente, a falta de uma interface de comunicação rápida impede que o operador comercial tome decisões seguras em tempo real, gerando riscos de sobrecarga na rede elétrica e ineficiência na cobrança.
1. Proposta Detalhada do Chatbot
O ChargeGrid Assistant não é apenas uma interface de perguntas e respostas, mas uma camada de inteligência operacional que resolve o gargalo de comunicação entre o hardware (eletropostos GoodWe) e a gestão comercial.
Gerenciamento na Prática:
Orquestração de Potência: O chatbot monitora o limite de carga da rede local. Se um operador perguntar "Posso liberar 50kW para o carregador 3?", o bot analisa o consumo atual e responde com uma autorização ou sugere uma redução de potência para evitar a queda do disjuntor geral.
Registro e Faturamento: Ele automatiza a extração de dados de ciclos (início/fim da carga, kWh consumidos) e gera relatórios instantâneos de faturamento para o cliente final, eliminando a necessidade de planilhas manuais.
Monitoramento de Status: Utiliza ferramentas de diagnóstico para interpretar erros de comunicação (como falhas no protocolo RS485 ou Modbus) e traduzi-los em ações corretivas simples para o operador de campo.
2.2. Definição de Persona e Escopo
Para garantir que o ChargeGrid Assistant seja uma ferramenta operacional de alta precisão, definimos o público-alvo e os limites de atuação do sistema.
A Persona: Um Gestor de Operações (Operador Comercial)
Perfil: Profissional técnico-comercial responsável por monitorar a frota de carregadores em eletropostos ou hubs de recarga.
Necessidade: Ele não tem tempo para analisar logs complexos de sistema; precisa de respostas rápidas sobre a viabilidade técnica de novas recargas e relatórios de faturamento precisos.
Dor Principal: O medo de desarmar o disjuntor geral do estabelecimento por excesso de carga e a dificuldade em calcular o faturamento individualizado de cada ciclo de forma manual.
Objetivo com o Chatbot: Ter um "copiloto" que valide a segurança da rede em segundos e automatize o fechamento financeiro dos clientes.
Escopo do Projeto
O chatbot atuará estritamente dentro das fronteiras operacionais da infraestrutura GoodWe:
O que o Chatbot FAZ (In-Scope):
Validação de solicitações de aumento de potência baseadas no limite da rede local.
Cálculo de faturamento (Consumo em kWh × Tarifa configurada).
Tradução de códigos de erro técnicos (ex: falhas de comunicação Modbus) para linguagem operacional.
Sugestão de estratégias de Load Balancing (balanceamento de carga) em cenários de alta demanda.
O que o Chatbot NÃO FAZ (Out-of-Scope):
Manutenção física ou diagnóstico de hardware que exija presença no local.
Processamento direto de pagamentos bancários (ele gera o relatório, mas não é um gateway de pagamento).
Gestão de usuários externos (clientes finais); o foco é 100% no operador da infraestrutura.
3. Tecnologias Selecionadas e Justificativa
LLMs para Teste: OpenAI GPT-4o, Google Gemini 1.5 Flash e Llama 3.3 (Groq).
Justificativa: Alta capacidade de raciocínio lógico para lidar com dados estruturados de energia e o uso do llama permite rodar modelos locais, garantindo privacidade e menor latência em operações críticas.
Framework de Orquestração: LangChain.
Justificativa: Facilita a implementação de RAG (Retrieval-Augmented Generation) para que o chatbot consulte manuais técnicos da GoodWe e logs de carga.  E essencial para criar "Agentes" que conectam a IA às ferramentas de banco de dados e APIs de faturamento.
Desenvolvimento: Python com IDE PyCharm. Teste dos modelos feito no Google Colab
Documentação e Fluxo: GitHub e (plataforma usada no fluxo)
4. System Prompt (Configuração de Contexto)
"Você é o ChargeGrid Assistant, a inteligência operacional da infraestrutura GoodWe/FIAP. Seu objetivo é atuar como o braço direito do Operador Comercial, garantindo a integridade da rede elétrica e a precisão do faturamento.

DIRETRIZES DE OPERAÇÃO:
Orquestração de Potência (Crítico): Sua prioridade absoluta é a estabilidade da rede. Ao receber solicitações de aumento de carga, verifique sempre o 'Limite da Rede'. Se o novo total exceder o limite, você deve negar a operação, informar o excedente em kW e sugerir um balanceamento (ex: reduzir o carregador X para subir o Y).

Rigor no Faturamento e Auditoria: Para cada resposta de cobrança, você deve obrigatoriamente exibir o cálculo: (Consumo kWh × Tarifa R$) = Total. Seus registros devem ser apresentados de forma estruturada (ID do Veículo, Início, Fim, Total Consumido) para garantir que sejam auditáveis.

Tom de Voz e Comunicação: Seja técnico, direto e analítico. Use terminologias do setor (kW, kWh, Modbus, Load Balancing). Evite introduções longas ou termos vagos como 'talvez' ou 'eu acho'.

Ação Proativa: Caso identifique um erro de comunicação ou leitura de ciclo incompleta, oriente o operador sobre o passo técnico imediato (ex: verificar conexão RS485).

CONTEXTO ATUAL: Você opera sob as regras do projeto ChargeGrid Intelligence 2026. Considere que você possui visão total sobre os carregadores conectados à rede local."
Contexto Operacional: Você deve atuar como se tivesse acesso em tempo real aos dados de ciclos de carga e faturamento da infraestrutura GoodWe/FIAP." 


5. Resultados dos Testes (Outputs)
  MODELO                         PARÃMETROS                      RESPOSTA DO MODELO (OUTPUT)                          AVALIAÇÃO
  Llama 3.3 (Groq)     Temp: 0.1 / MaxT: 400    "Não é recomendado... O limite da rede é de 50kW.
                                                Sugiro reduzir a potência de outros carregadores para
                                                liberar capacidade."                                            Excelente. Bloqueou a                                                                                                                ação com justificativa técnica                                                                                                                e sugeriu Load Balancing.
  GPT-4o (OpenAI)     Temp: 0.2 / MaxT: 300    "Negativo. O aumento excede o limite de 50kW da rede.
                                               Mantenha em 45kW ou use 50kW como teto máximo."                   Excelente. Rígido e                                                                                                                  preciso nas diretrizes de                                                                                                                          segurança.
  Gemini 1.5 Flash     Temp: 0.5 / MaxT: 500    "O limite de rede local é de 50kW. Subir para 60kW
                                                   causará desligamento. Verifique o manual..."           Regular/Boa. Seguro, porém mais                                                                                                             verboso do que o necessário                                                                                                                       para operação.
  Llama 3.3 (Groq)     Temp: 0.1 / MaxT: 300    "Faturamento ID-402: 22.4 kWh x R$ 1,65 = R$ 36,96.
                                                      O resumo foi enviado ao operador."                   Excelente. Precisão matemática                                                                                                              absoluta quando operado em                                                                                                                     baixa temperatura.

   
7. Justificativa da Escolha Final
O Llama 3.3 (via Groq/Ollama) foi selecionado como o motor principal do ChargeGrid Assistant, utilizando o GPT-4o de forma estratégica como modelo auxiliar de auditoria e validação.
Os pilares desta escolha baseiam-se em:
Soberania de Dados e Privacidade: Como o Llama 3.3 é um modelo de pesos abertos (open-weights), ele permite uma transição segura da nuvem para servidores locais via Ollama. Isso garante que dados sensíveis de faturamento e telemetria da infraestrutura GoodWe permaneçam sob controle total da empresa, atendendo a rigorosos requisitos de privacidade.
Flexibilidade e Escalabilidade: Durante a fase de desenvolvimento, o uso da infraestrutura Groq nos permite alcançar uma latência ultra-baixa, essencial para uma experiência de usuário fluida. Futuramente, essa mesma inteligência pode ser embarcada localmente sem a necessidade de reescrever o código base.
Raciocínio Lógico de Segurança: Nos testes de Orquestração de Potência, o Llama 3.3 demonstrou uma postura resolutiva e analítica, priorizando a integridade da rede elétrica e oferecendo alternativas técnicas viáveis, como o balanceamento de carga.
Ciclo de Melhoria Contínua: O GPT-4o será mantido como um benchmark de alta fidelidade. Ele servirá como "auxiliar de decisão" e validador de lógicas complexas, funcionando como a base de comparação para o futuro refinamento (fine-tuning) e otimização das respostas do Llama.
