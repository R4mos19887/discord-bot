import discord
from discord.ext import commands
from discord import app_commands
import requests

# =========================
# CONFIG
# =========================
TOKEN = os.getenv"TOKEN"
API_KEY = os.getenv"API_KEY"
BASE_URL = "http://bypass.anikxcheats.xyz"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# API FUNCTIONS
# =========================

def add_uid(uid, days=30, bluestack=True):
    r = requests.post(
        f"{BASE_URL}/api/uid/add",
        headers={
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "uid": uid,
            "days": days,
            "bluestack": bluestack
        }
    )
    return r.json()

def remove_uid(uid):
    r = requests.post(
        f"{BASE_URL}/api/uid/remove",
        headers={
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        },
        json={"uid": uid}
    )
    return r.json()

def list_uids():
    r = requests.get(
        f"{BASE_URL}/api/uid/list",
        headers={"X-API-KEY": API_KEY}
    )
    return r.json()

# =========================
# EVENTS
# =========================

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"✅ Slash commands sincronizados")
    except Exception as e:
        print(e)

    print(f"✅ Bot online como {bot.user}")

# =========================
# SLASH COMMANDS
# =========================

# ➕ ADD
@bot.tree.command(name="add", description="Adicionar UID")
@app_commands.describe(uid="UID do usuário", days="Dias", bluestack="BlueStack (true/false)")
async def add_slash(interaction: discord.Interaction, uid: str, days: int, bluestack: bool):
    data = add_uid(uid, days, bluestack)

    if data.get("success"):
        await interaction.response.send_message(f"✅ UID `{uid}` adicionado por {days} dias!")
    else:
        await interaction.response.send_message(f"❌ Erro: {data.get('message')}")

# ❌ REMOVE
@bot.tree.command(name="remove", description="Remover UID")
async def remove_slash(interaction: discord.Interaction, uid: str):
    data = remove_uid(uid)

    if data.get("success"):
        await interaction.response.send_message(f"🗑️ UID `{uid}` removido!")
    else:
        await interaction.response.send_message(f"❌ Erro: {data.get('message')}")

# 📋 LISTAR
@bot.tree.command(name="listar", description="Listar UIDs")
async def listar_slash(interaction: discord.Interaction):
    data = list_uids()

    if not data.get("success"):
        await interaction.response.send_message(f"❌ Erro: {data.get('message')}")
        return

    uids = data.get("data", [])

    if not uids:
        await interaction.response.send_message("📭 Nenhum UID encontrado.")
        return

    mensagem = "📋 **Lista de UIDs:**\n\n"

    for u in uids[:10]:
        tipo = "BlueStack" if u["bluestack"] else "Normal"
        mensagem += f"• `{u['uid']}` | {tipo}\n"

    await interaction.response.send_message(mensagem)

# =========================
# START
# =========================

bot.run(TOKEN)