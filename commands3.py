import discord
from discord.enums import IntegrationType
from discord.ext import commands

import requests
from io import BytesIO
from PIL import Image
import random

integration_types = {
    discord.IntegrationType.guild_install,
    discord.IntegrationType.user_install,
}

ALLOWED_CHANNEL_IDS = {
    1218307973030477944, # EmmiOğlu
    1212848523683434526, # Benim GC Tek Ben Ve Yan Hesabım Var
    1269699846999380050  # Benim GC Ben Ve Ahmet Var
}

class COMMANDS2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='sor', description='Bana Soru Sor', integration_types=integration_types)
    async def sor(self, ctx, soru: str):
        if ctx.channel.id not in ALLOWED_CHANNEL_IDS:
            return
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
        await ctx.send(f"Soru: {soru}\nYanıtım: {yanit}")

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
        await ctx.send(video_url)

    @commands.slash_command(name='kişilik', description='Kişilik Özelliğini Eren Seçer', integration_types=integration_types)
    async def kişilik(self, ctx, kişi: discord.User = None):
        if ctx.channel.id not in ALLOWED_CHANNEL_IDS:
            return
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
        await ctx.send(f"{kişi.mention}'in kişilik özelliği: {kişilik}")

    @commands.slash_command(name='cum', description='cumshot at', integration_types=integration_types)
    async def cum(self, ctx, kişi: discord.User=None):
        kişi = kişi or ctx.author
        img1 = self.get_image(kişi.display_avatar.url).convert('RGBA')
        await ctx.defer()
        img2 = self.get_image('https://raw.githubusercontent.com/OTx4LqLgHWSty1VcrinzmFbotpMVeVyunTNW2hI/WbO0JELcDYLyDVL3NeFka0Eu51SLouX93D4omlC/main/cum.png').convert('RGBA').resize(img1.size)
        img1.paste(img2, (0, 0), img2)
        img1 = img1.convert('RGB')

        b = BytesIO()
        img1.save(b, format='png')
        b.seek(0)
        await ctx.respond(file=discord.File(b, 'erencumshotatti.png'))

    def get_image(self, url):
        raw = requests.get(url, stream=True).raw
        return Image.open(raw)

def setup(client):
    client.add_cog(COMMANDS2(client))
