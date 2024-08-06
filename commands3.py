import discord
from discord.ext import commands
import random

integration_types = {
    discord.IntegrationType.guild_install,
    discord.IntegrationType.user_install,
}

class COMMANDS3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='sor', description='Bana Soru Sor', integration_types=integration_types)
    async def sor(self, ctx, soru: str):
        # Yanıt seçenekleri
        yanitlar = [
            "Evet",
            "Hayır",
            "Belki",
            "Kesinlikle",
            "Kesinlikle değil",
            "Bilmiyorum",
            "Muhtemelen",
            "Asla",
            "Kesinlikle evet",
            "Kesinlikle hayır",
            "Olabilir",
            "Düşünülebilir",
            "Şu an kesin değil",
            "Zamanla göreceğiz",
            "Belki ileride",
            "Şu an için uygun değil",
            "İhtimal var",
            "Uygun olabilir",
            "Belki evet, belki hayır",
            "Hiçbir fikrim yok",
            "Karar veremedim",
            "Çok karmaşık",
            "Bunu değerlendirmeliyim",
            "Daha fazla bilgi gerekli",
            "Sana katılmıyorum",
            "Neden olmasın?",
            "Olanaklı",
            "Her şey olabilir"
        ]

        # Rastgele yanıt seç
        yanit = random.choice(yanitlar)

        # Yanıtı gönder
        await ctx.respond(f"Soru: {soru}\nYanıtım: {yanit}")

    @commands.slash_command(name='video', description='Rastgele bir video gönderir', integration_types=integration_types)
    async def video(self, ctx):
        # Video URL'leri
        videolar = [
            "https://cdn.discordapp.com/attachments/1270335595302096951/1270377104122449984/361807693_6463251553723359_129813083509844646_n.mp4",
            "https://cdn.discordapp.com/attachments/1270335595302096951/1270377135189528576/361791034_6786518214714626_7264071351127900550_n.mp4",
            "https://cdn.discordapp.com/attachments/1270335595302096951/1270377343508021298/421368668_24531764226471104_3911977699595297928_n.mp4",
            "https://cdn.discordapp.com/attachments/1270335595302096951/1270377385497329837/363446197_7213485575333300_3214501604565230307_n.mp4"
        ]

        # Rastgele video seç
        video_url = random.choice(videolar)

        # Video'yu gönder
        await ctx.respond(video_url)

    @commands.slash_command(name='kişilik', description='Kişilik Özelliğini Eren Seçer', integration_types=integration_types)
    async def kişilik(self, ctx, kişi: discord.User = None):
        # Kişilik özellikleri
        kişilikler = [
            "Dışa dönük",
            "İçsel",
            "Yardımsever",
            "Sakin",
            "Yaratıcı",
            "Analitik",
            "Kararlı",
            "Duygusal",
            "Pratik",
            "Macera sever",
            "Sorumlu",
            "Hassas",
            "Esprili",
            "Girişken",
            "Öz disiplinli",
            "Kendine güvenen",
            "Sabırlı",
            "Gözlemci",
            "Organize",
            "Hikaye anlatıcı",
            "Etkileyici"
        ]

        if kişi is None:
            kişi = ctx.author

        # Rastgele kişilik seç
        kişilik = random.choice(kişilikler)

        # Kullanıcıya kişilik özelliği bildir
        await ctx.respond(f"{kişi.mention}'in kişilik özelliği: {kişilik}")

def setup(client):
    client.add_cog(COMMANDS3(client))
