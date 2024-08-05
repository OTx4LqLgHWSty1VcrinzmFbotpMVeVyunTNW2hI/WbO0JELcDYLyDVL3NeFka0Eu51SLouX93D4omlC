import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

integration_types = {
    discord.IntegrationType.guild_install,
    discord.IntegrationType.user_install,
}

class COMMANDS2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='wargods2', 
        description='Güncel Hilecileri Göster Lan!!!',
        integration_types=integration_types
    )
    async def wargods(self, ctx, url: str):
        # Validate the URL
        if not url.startswith('https://www.wargods.ro/wcd/report.php?id='):
            await ctx.respond("Geçersiz URL. Lütfen doğru bir URL girin.")
            return

        # Send a GET request to the URL
        response = requests.get(url)

        if response.status_code != 200:
            await ctx.respond(f"Bilgi çekilemedi: {response.status_code}")
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and remove the excluded div (if it exists)
        excluded_div = soup.find('div', id='searchcnt')
        if excluded_div:
            excluded_div.decompose()

        # Find the div with id="report"
        report_div = soup.find('div', id='report')
        if not report_div:
            await ctx.respond("Rapor bulunamadı")
            return

        # Extract unique IDs, nicknames, Steam IDs, Render types, IPs, and other report details
        data = []
        seen = set()  # To keep track of already processed (nick, unique_id) pairs

        def extract_data(tag_class):
            unique_id = None
            nick = None
            steam_id = None
            render_type = None
            last_server_ip = None
            cs_opened_at = None
            wcd_timestamp = None
            system_timestamp = None
            server_timestamp = None
            operating_system = None

            for div in report_div.find_all('div', class_=tag_class):
                text_content = div.get_text(strip=True)
                if 'Unique ID' in text_content:
                    unique_id = div.find_next_sibling('div', class_='reportq').get_text(strip=True)
                elif 'Nick' in text_content:
                    nick = div.find_next_sibling('div', class_='reportq').get_text(strip=True)
                elif 'Type (Steam/NonSteam)' in text_content:
                    steam_id = div.find_next_sibling('div', class_='reportq').get_text(strip=True)
                elif 'Render' in text_content:
                    render_type = div.find_next_sibling('div', class_='reportq').get_text(strip=True)
                elif 'CS opened at' in text_content:
                    cs_opened_at = div.find_next_sibling('div', class_='reportq').get_text(strip=True)
                elif 'Last Server IP:' in text_content:
                    last_server_ip = div.find_next_sibling('div', class_='reportq').get_text(strip=True)
                elif 'wCD TimeStamp' in text_content:
                    wcd_timestamp = div.find_next_sibling('div', class_='reportq').get_text(strip=True)
                elif 'System TimeStamp' in text_content:
                    system_timestamp = div.find_next_sibling('div', class_='reportq').get_text(strip=True)
                elif 'Server TimeStamp' in text_content:
                    server_timestamp = div.find_next_sibling('div', class_='reportq').get_text(strip=True)
                elif 'Operating System' in text_content:
                    operating_system = div.find_next_sibling('div', class_='reportq').get_text(strip=True)

            return {
                'unique_id': unique_id,
                'nick': nick,
                'steam_id': steam_id,
                'render': render_type,
                'cs_opened_at': cs_opened_at,
                'last_server_ip': last_server_ip,
                'wcd_timestamp': wcd_timestamp,
                'system_timestamp': system_timestamp,
                'server_timestamp': server_timestamp,
                'operating_system': operating_system,
            }

        # Extract data using both 'reporttagcheat' and 'reporttag'
        data_cheat = extract_data('reporttagcheat')
        data_tag = extract_data('reporttag')

        # Combine and format the data
        combined_data = [data_cheat, data_tag]
        for entry in combined_data:
            if entry['nick'] and (entry['unique_id'] not in seen):
                seen.add(entry['unique_id'])
                embed = discord.Embed(
                    title=f"{entry['nick']} Bilgileri",
                    description="Aşağıda listelenen hilecinin bilgileri bulunmaktadır.",
                    color=discord.Color.red()
                )

                # Add fields to the embed in a vertical format
                embed.add_field(name="Unique ID", value=entry['unique_id'] or "Bilgi Yok", inline=False)
                embed.add_field(name="Nick", value=entry['nick'] or "Bilgi Yok", inline=False)
                embed.add_field(name="Steam ID", value=entry['steam_id'] or "Bilgi Yok", inline=False)
                embed.add_field(name="Render", value=entry['render'] or "Bilgi Yok", inline=False)
                embed.add_field(name="Son Bağlanılan Yer", value=entry['last_server_ip'] or "Bilgi Yok", inline=False)
                embed.add_field(name="CS Açıldığı Zaman", value=entry['cs_opened_at'] or "Bilgi Yok", inline=False)
                embed.add_field(name="wCD Zaman Damgası", value=entry['wcd_timestamp'] or "Bilgi Yok", inline=False)
                embed.add_field(name="Sistem Zaman Damgası", value=entry['system_timestamp'] or "Bilgi Yok", inline=False)
                embed.add_field(name="Server Zaman Damgası", value=entry['server_timestamp'] or "Bilgi Yok", inline=False)
                embed.add_field(name="İşletim Sistemi", value=entry['operating_system'] or "Bilgi Yok", inline=False)

                await ctx.respond(embed=embed)
                return

        await ctx.respond("Güncel rapor bulunamadı.")

def setup(bot):
    bot.add_cog(COMMANDS2(bot))
