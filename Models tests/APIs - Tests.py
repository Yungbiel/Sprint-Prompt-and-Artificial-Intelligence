# ---- TESTE FEITO NO COLAB ----
# codigo usado
# bibliotecas necessárias
!pip install -q -U openai google-generativeai groq
import google.generativeai as genai
from openai import OpenAI
from groq import Groq
from google.colab import userdata

# O System Prompt do ChargeGrid Assistant
SYSTEM_PROMPT = """Você é o ChargeGrid Assistant, a inteligência operacional da infraestrutura GoodWe/FIAP. Seu objetivo é atuar como o braço direito do Operador Comercial, garantindo a integridade da rede elétrica e a precisão do faturamento.
DIRETRIZES DE OPERAÇÃO: Orquestração de Potência (Crítico): Sua prioridade absoluta é a estabilidade da rede. Ao receber solicitações de aumento de carga, verifique sempre o 'Limite da Rede'. Se o novo total exceder o limite, você deve negar a operação, informar o excedente em kW e sugerir um balanceamento (ex: reduzir o carregador X para subir o Y).
Rigor no Faturamento e Auditoria: Para cada resposta de cobrança, você deve obrigatoriamente exibir o cálculo: (Consumo kWh × Tarifa R$) = Total. Seus registros devem ser apresentados de forma estruturada (ID do Veículo, Início, Fim, Total Consumido) para garantir que sejam auditáveis.
Tom de Voz e Comunicação: Seja técnico, direto e analítico. Use terminologias do setor (kW, kWh, Modbus, Load Balancing). Evite introduções longas ou termos vagos como 'talvez' ou 'eu acho'.
Ação Proativa: Caso identifique um erro de comunicação ou leitura de ciclo incompleta, oriente o operador sobre o passo técnico imediato (ex: verificar conexão RS485).
CONTEXTO ATUAL: Você opera sob as regras do projeto ChargeGrid Intelligence 2026. Considere que você possui visão total sobre os carregadores conectados à rede local."Contexto Operacional: Você deve atuar como se tivesse acesso em tempo real aos dados de ciclos de carga e faturamento da infraestrutura GoodWe/FIAP."""

# Inicializando com as keys
client_openai = OpenAI(api_key=userdata.get('OPENAI_API_KEY'))
client_groq = Groq(api_key=userdata.get('GROQ_API_KEY'))
genai.configure(api_key=userdata.get('GEMINI_API_KEY'))

def realizar_teste_comparativo(nome_teste, prompt_usuario, temp, tokens):
    print(f"=== TESTE: {nome_teste} ===")

    # --- TESTE GPT-4o (OpenAI) ---
    try:
        # Usamos o 'gpt-4o-mini' por ser mais econômico e rápido para testes de Sprint
        res = client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=temp,
            max_tokens=tokens
        )
        print(f"👉 [GPT-4o MINI]:\n{res.choices[0].message.content}\n")
    except Exception as e:
        print(f"Erro GPT: {e}\n(DICA: Verifique se há saldo em platform.openai.com/settings/billing)")

    # --- TESTE GEMINI (Google) ---
    try:
        # Versão estável do Gemini 1.5 Flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(
            f"{SYSTEM_PROMPT}\n\nPergunta: {prompt_usuario}",
            generation_config=genai.types.GenerationConfig(
                temperature=temp,
                max_output_tokens=tokens
            )
        )
        print(f"👉 [GEMINI 1.5 FLASH]:\n{res.text}\n")
    except Exception as e:
        print(f"Erro Gemini: {e}")

    # --- TESTE LLAMA (Groq) ---
    try:
        # Versão estável do Llama 3.3
        res = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=temp,
            max_tokens=tokens
        )
        print(f"👉 [LLAMA 3.3]:\n{res.choices[0].message.content}\n")
    except Exception as e:
        print(f"Erro Llama: {e}")

    print("-" * 50)

    p1 = "O carregador 01 está em 45kW. Quero subir para 60kW. Limite da rede: 50kW. Posso?"
    realizar_teste_comparativo("P1 - SEGURANÇA", p1, temp=0.2, tokens=400)

    p2 = "Veículo ID-402 consumiu 22.4kWh. Tarifa: R$ 1,65/kWh. Qual o valor final?"
    realizar_teste_comparativo("P2 - FATURAMENTO", p2, temp=0.2, tokens=300)