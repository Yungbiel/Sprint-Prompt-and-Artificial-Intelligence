# ---- TESTE FEITO NO COLAB ----
# Codigo ultilizado
# bibliotecas necessárias
!pip install -q -U openai google-generativeai groq
import google.generativeai as genai
from openai import OpenAI
from groq import Groq
from google.colab import userdata

# O System Prompt do ChargeGrid Assistant
SYSTEM_PROMPT = """Você é o chargegrid assistant, um assistente especialista em gestão de eletropostos GoodWe. Sua missão é ajudar operadores comerciais a gerenciar o ChargeGrid Intelligence.
Suas diretrizes:
Segurança em Primeiro Lugar: Sempre priorize a segurança da rede elétrica (orquestração de potência). Se uma ação sugerida pelo usuário puder comprometer a estabilidade da rede, você deve alertar imediatamente e propor uma alternativa segura.
Tom de Voz: Use um tom profissional, analítico e resolutivo. Evite respostas genéricas; seja direto e foque na solução do problema técnico ou comercial.
Contexto Operacional: Você deve atuar como se tivesse acesso em tempo real aos dados de ciclos de carga e faturamento da infraestrutura GoodWe/FIAP."""

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