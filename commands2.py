import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime

integration_types = {
    discord.IntegrationType.guild_install,
    discord.IntegrationType.user_install,
}

def format_timestamp(timestamp):
    try:
        dt = datetime.strptime(timestamp, '%d.%m.%Y %H:%M:%S')
        formatted_date = dt.strftime('%d.%m.%Y')
        formatted_time = dt.strftime('%H:%M:%S')
        return f"{formatted_date} | {formatted_time}"
    except ValueError:
        return "Geçersiz Tarih/Saat Formatı"

class COMMANDS2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='wargods2', 
        description='Rapordan Bilgileri Göster Lan!!! - Örnek: https://www.wargods.ro/wcd/report.php?id=2927800',
        integration_types=integration_types
    )
    async def wargods(self, ctx, rapor_linki: str):
        # URL doğrulaması
        if not rapor_linki.startswith('https://www.wargods.ro/wcd/report.php?id='):
            await ctx.respond("Linki Adam Akıllı Tam Gir Lan!!!")
            return

        # URL'ye GET isteği gönder
        response = requests.get(rapor_linki)
        if response.status_code != 200:
            await ctx.respond(f"Bilgi çekilemedi: {response.status_code}")
            return

        # HTML içeriğini ayrıştır
        soup = BeautifulSoup(response.text, 'html.parser')

        # Hariç tutulan div'i bul ve kaldır
        excluded_div = soup.find('div', id='searchcnt')
        if excluded_div:
            excluded_div.decompose()

        # id="report" olan div'i bul
        report_div = soup.find('div', id='report')
        if not report_div:
            await ctx.respond("Rapor bulunamadı")
            return

        # Verileri çekmek için yardımcı fonksiyon
        def extract_data(tag_class):
            data = {
                'unique_id': None,
                'nick': None,
                'steam_id': None,
                'render': None,
                'cs_opened_at': None,
                'last_server_ip': None,
                'wcd_timestamp': None,
                'system_timestamp': None,
                'server_timestamp': None,
                'operating_system': None,
                'country': "Bilinmiyor",
                'processes': None,
                'report': None,
                'ip_info': None,
                'modules': None,
                'cstrike': None,
                'cfg': None,
                'resources': None
            }

            for div in report_div.find_all('div', class_=tag_class):
                text_content = div.get_text(strip=True)
                next_div = div.find_next_sibling('div', class_='reportq')
                if 'Unique ID' in text_content:
                    data['unique_id'] = next_div.get_text(strip=True)
                elif 'Nick' in text_content:
                    data['nick'] = next_div.get_text(strip=True)
                elif 'Type (Steam/NonSteam)' in text_content:
                    data['steam_id'] = next_div.get_text(strip=True)
                elif 'Render' in text_content:
                    data['render'] = next_div.get_text(strip=True)
                elif 'CS opened at' in text_content:
                    data['cs_opened_at'] = format_timestamp(next_div.get_text(strip=True))
                elif 'Last Server IP:' in text_content:
                    data['last_server_ip'] = next_div.get_text(strip=True)
                elif 'wCD TimeStamp' in text_content:
                    data['wcd_timestamp'] = format_timestamp(next_div.get_text(strip=True))
                elif 'System TimeStamp' in text_content:
                    data['system_timestamp'] = format_timestamp(next_div.get_text(strip=True))
                elif 'Server TimeStamp' in text_content:
                    data['server_timestamp'] = format_timestamp(next_div.get_text(strip=True))
                elif 'Operating System' in text_content:
                    data['operating_system'] = next_div.get_text(strip=True)
                elif 'Report' in text_content:
                    data['report'] = next_div.get_text(strip=True)
                elif 'IP:' in text_content:
                    data['ip_info'] = next_div.get_text(strip=True)

                # Ülke bilgisini çıkar
                previous_div = div.find_previous_sibling('div')
                if previous_div:
                    flag_img_tag = previous_div.find('img', {'style': 'display:inline-block;vertical-align:sub;'})
                    if flag_img_tag and 'title' in flag_img_tag.attrs:
                        data['country'] = flag_img_tag['title']

                # Processes bağlantısını çıkar
                if 'Processes:' in text_content:
                    process_link = next_div.find('a', href=True)
                    if process_link:
                        data['processes'] = f"https://www.wargods.ro/wcd/{process_link['href']}"
                    else:
                        data['processes'] = "Bilgi Yok"

                if 'Modules:' in text_content:
                    modules_link = next_div.find('a', href=True)
                    if modules_link:
                        data['modules'] = f"https://www.wargods.ro/wcd/{modules_link['href']}"
                    else:
                        data['modules'] = "Bilgi Yok"

                if 'Cstrike (dlls/executables/scripts):' in text_content:
                    cstrike_link = next_div.find('a', href=True)
                    if cstrike_link:
                        data['cstrike'] = f"https://www.wargods.ro/wcd/{cstrike_link['href']}"
                    else:
                        data['cstrike'] = "Bilgi Yok"

                if 'CFG:' in text_content:
                    cfg_link = next_div.find('a', href=True)
                    if cfg_link:
                        data['cfg'] = f"https://www.wargods.ro/wcd/{cfg_link['href']}"
                    else:
                        data['cfg'] = "Bilgi Yok"

                if 'Resources:' in text_content:
                    resources_link = next_div.find('a', href=True)
                    if resources_link:
                        data['resources'] = f"https://www.wargods.ro/wcd/{resources_link['href']}"
                    else:
                        data['resources'] = "Bilgi Yok"

            return data

        # 'reporttagcheat' ve 'reporttag' ile verileri çek
        data_cheat = extract_data('reporttagcheat')
        data_tag = extract_data('reporttag')

        # Verileri birleştir ve formatla
        combined_data = [data_cheat, data_tag]
        for entry in combined_data:
            if entry['nick']:
                # Embed rengini rapor metnine göre ayarla
                embed_color = discord.Color.dark_blue() if entry['report'] and "No Cheat Signature Detected" in entry['report'] else discord.Color.red()

                embed = discord.Embed(
                    title=f"İstediğin {entry['nick']} Adındaki Kişinin Bilgileri",
                    color=embed_color
                )

                # Kalın metin için ** işareti kullanın ve verileri alt alta ekleyin
                embed.add_field(
                    name="Bana Göre Temiz Bu Adam",
                    value=(
                        f"İSİM: **{entry['nick'] or 'Bilgi Yok'}**\n"
                        f"Unique ID: **{entry['unique_id'] or 'Bilgi Yok'}**\n"
                        f"ID: **{entry['steam_id'] or 'Bilgi Yok'}**\n"
                        f"Render: **{entry['render'] or 'Bilgi Yok'}**\n"
                        f"IP Bilgisi: **{entry['ip_info'] or 'Bilgi Yok'}**\n"
                        f"Ülke: **{entry['country'] or 'Bilgi Yok'}**\n"
                        f"Rapor: **{entry['report'] or 'Bilgi Yok'}**\n"
                        f"CS Açılma Tarihi & Zamanı: **{entry['cs_opened_at'] or 'Bilgi Yok'}**\n"
                        f"Wargods Açılma Tarihi & Zamanı: **{entry['wcd_timestamp'] or 'Bilgi Yok'}**\n"
                        f"Wargods Taratıldığı Tarih & Zamanı: **{entry['system_timestamp'] or 'Bilgi Yok'}**\n"
                        f"Wargods Serverine Sonucun Gönderdildiği Tarih & Zaman: **{entry['server_timestamp'] or 'Bilgi Yok'}**\n"
                        f"Son Oynadığı Server IP: **{entry['last_server_ip'] or 'Bilgi Yok'}**\n"
                        f"İşletim Sistemi: **{entry['operating_system'] or 'Bilgi Yok'}**\n"
                        f"Çalışan İşlemler: **{entry['processes'] or 'Bilgi Yok'}**\n"
                        f"Çalışan Modüller: **{entry['modules'] or 'Bilgi Yok'}**\n"
                        f"Çalışan Cstrike: **{entry['cstrike'] or 'Bilgi Yok'}**\n"
                        f"Çalışan Configler: **{entry['cfg'] or 'Bilgi Yok'}**\n"
                        f"Modeller/Spriteler: **{entry['resources'] or 'Bilgi Yok'}**\n"
                    ),
                    inline=False
                )

                await ctx.respond(embed=embed)
                return

        await ctx.respond("Güncel rapor bulunamadı.")

def setup(bot):
    bot.add_cog(COMMANDS2(bot))
