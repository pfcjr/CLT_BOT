import os
import discord
from openai import OpenAI

# ========================
# Variáveis de ambiente
# ========================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN não definido")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY não definido")

# ========================
# Cliente OpenAI (API nova)
# ========================
client_openai = OpenAI(api_key=OPENAI_API_KEY)

# ========================
# Configuração do Discord
# ========================
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# ========================
# Eventos
# ========================
@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")

@client.event
async def on_message(message):
    # Evita loop infinito
    if message.author == client.user:
        return

    pergunta = message.content.strip()

    if not pergunta:
        return

    try:
        resposta = client_openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um especialista na Consolidação das Leis do Trabalho (CLT) do Brasil. "
                        "Responda sempre de forma clara, objetiva e respeitosa. "
                        "Fundamente suas respostas citando, quando aplicável, os artigos relevantes da CLT. "
                        "Não invente informações e não extrapole além do texto legal."
                    )
                },
                {
                    "role": "user",
                    "content": pergunta
                }
            ]
        )

        texto_resposta = resposta.choices[0].message.content
        await message.channel.send(texto_resposta)

    except Exception as e:
        await message.channel.send(
            "Ocorreu um erro ao processar sua pergunta. Tente novamente."
        )
        print("Erro OpenAI:", e)

# ========================
# Inicialização
# ========================
client.run(DISCORD_TOKEN)

