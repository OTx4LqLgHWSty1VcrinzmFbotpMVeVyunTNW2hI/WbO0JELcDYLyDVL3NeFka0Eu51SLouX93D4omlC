import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

integration_types = {
    discord.IntegrationType.guild_install,
    discord.IntegrationType.user_install,
}

# İzin verilen kanal ID'leri
ALLOWED_CHANNEL_IDS = {
    1218307973030477944, # EmmiOğlu
    1212848523683434526, # Benim GC Tek Ben Ve Yan Hesabım Var
    1269699846999380050  # Benim GC Ben Ve Ahmet Var
}

# URL doğrulama düzenli ifadesi
URL_PATTERN = re.compile(r'https://www\.wargods\.ro/wcd/report\.php\?id=\d+')

class COMMANDS1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='wargods2', 
        description='Rapordan Bilgileri Göster Lan!!! - Örnek: https://www.wargods.ro/wcd/report.php?id=2927800',
        integration_types=integration_types
    )
    async def wargods(self, ctx, rapor_linki: str):
        # İzin verilen kanalda olup olmadığını kontrol et
        if ctx.channel.id not in ALLOWED_CHANNEL_IDS:
            return

        if rapor_linki.isdigit():
            rapor_linki = f"https://www.wargods.ro/wcd/report.php?id={rapor_linki}"
            
        if not URL_PATTERN.match(rapor_linki):
            await ctx.respond("Linki Adam Akıllı Gir Yada Sayı Gir!!!")
            return

        # URL'ye GET isteği gönder
        response = requests.get(rapor_linki)
        if response.status_code != 200:
            await ctx.respond(f"Bilgi çekilemedi: {response.status_code}")
            return

        report_id = rapor_linki.split('id=')[1]
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

        def format_timestamp(timestamp):
            try:
                dt = datetime.strptime(timestamp, '%d.%m.%Y %H:%M:%S')
                formatted_date = dt.strftime('%d.%m.%Y')
                formatted_time = dt.strftime('%H:%M:%S')
                return f"{formatted_date} | {formatted_time}"
            except ValueError:
                return "Tarih ve Saat Bilgisi Çekilemedi"

        def clean_steam_id(steam_id):
            if steam_id and steam_id.startswith('Steam #'):
                return steam_id.replace('Steam # ', '')
            return steam_id
            
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
                'resources': None,
            }

            for div in report_div.find_all('div', class_=tag_class):
                text_content = div.get_text(strip=True)
                next_div = div.find_next_sibling('div', class_='reportq')
                if 'Unique ID' in text_content:
                    data['unique_id'] = next_div.get_text(strip=True)
                elif 'Nick' in text_content:
                    data['nick'] = next_div.get_text(strip=True)
                elif 'Type (Steam/NonSteam)' in text_content:
                    steam_id_text = next_div.get_text(strip=True)
                    if 'NonSteam' in steam_id_text:
                        data['steam_id'] = "Kaçak Olduğu İçin Göremiyorum 😭"
                    else:
                        data['steam_id'] = clean_steam_id(steam_id_text)
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

                country_translation = {
                    "Türkiye": "Türkiye 🇹🇷",
                    "Pakistan": "Pakistan 🇵🇰",
                    "Romania": "Romanya 🇷🇴",
                    "Greece": "Yunanistan 🇬🇷",
                    "Lithuania": "Litvanya 🇱🇹",
                    "United Kingdom": "İngiltere 🇬🇧",
                    "Russia": "Rusya 🇷🇺",
                    "Egypt": "Mısır 🇪🇬",
                    "Ukraine": "Ukrayna 🇺🇦",
                    "Algeria": "Cezayir 🇩🇿",
                    "Albania": "Arnavutluk 🇦🇱",
                    "Serbia": "Sırbistan 🇷🇸",
                    "Germany": "Almanya 🇩🇪",
                    "Bulgaria": "Bulgaristan 🇧🇬",
                    "Bosnia and Herzegovina": "Bosna Hersek 🇧🇦",
                    "Ireland": "İrlanda 🇮🇪",
                    "Sweden": "İsveç 🇸🇪",
                    "Switzerland": "İsviçre 🇨🇭",
                    "Hungary": "Macaristan 🇭🇺",
                    "Kazakhstan": "Kazakistan 🇰🇿",
                    "Uzbekistan": "Özbekistan 🇺🇿",
                    "France": "Fransa 🇫🇷",
                    "Poland": "Polonya 🇵🇱",
                    "Georgia": "Gürcistan 🇬🇪",
                    "Saudi Arabia": "Suudi Arabistan 🇸🇦",
                    "North Macedonia": "Kuzey Makedonya 🇲🇰",
                    "Kosovo": "Kosova 🇽🇰"
                }

                previous_div = div.find_previous_sibling('div')
                if previous_div:
                    flag_img_tag = previous_div.find('img', {'style': 'display:inline-block;vertical-align:sub;'})
                    if flag_img_tag and 'title' in flag_img_tag.attrs:
                        country = flag_img_tag['title']

                        data['country'] = country_translation.get(country, country)

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

        data_cheat = extract_data('reporttagcheat')
        data_tag = extract_data('reporttag')

        # Verileri birleştir ve formatla
        combined_data = [data_cheat, data_tag]
        found_data = False 

        report_messages = {
            "No Cheat Signature Detected": "ADAM TEMİZ ÇIKMIŞ DAHA NE İSTİYORSUN LAN!",
            "Found Vermillion": "Vermillion Hack Bulundu [Yıl Kaç? 👴]",
            "Found Big CFG - unknown status": "Büyük Bir CFG Var Adamda Sıkıntılı",
            "Alternative": "Alternative Hack Bulundu [Sanki Biraz Eskidi Gibi 🤔]",
            "Found Alternative": "Alternative Hack Bulundu [Sanki Biraz Eskidi Gibi 🤔]",
            "AlterNative": "Alternative Hack Bulundu [Sanki Biraz Eskidi Gibi 🤔]",
            "Generic Cheat Detection": "Wargods Daha İsim Koyamamis Nası Bi Hileyse",
            "Found Oxware Data": "Oxware Hack Bulundu [OOO Güncel Hile / İyi Hile 😈]",
            "Riscript Injector": "Dandik İnjektörlerden İyidir | Riscript Injector",
            "Found Injector": "İsimsiz Dandik İnjektor Kullanmış 🤣",
            "Cheat Model": "Karakter Modellerini Değiştirmiş 🤦‍♂️",
            "Cheat model": "Karakter Modellerini Değiştirmiş 🤦‍♂️",
            "Found Super Simple Wallhack": "Çok Basit Wallhack [Kendi Yapmış Olabilir Heee 😍]",
            "Found HPP Hack Data": "HPP Hilesinin Verisi Bulunmuş [Silememiş Herhalde 😭]",
            "Found HPP CFG Data": "HPP Hilesinin CFG Dosyası Bulunmuş [Silememiş Herhalde 😭]",
            "Found HPP Hack": "HPP Hack Bulunmuş [OOO İyi Hile 😈]",
            "Found Extreme Injector": "Extreme Injector Kullanmış",
            "Found BunnyHop CFG - unknown status": "Bunny CFG Bulunmuş [Demekki Düz Hızlanan Buymuş 😡]",
            "Found Leis": "Leis Hack Bulunmuş [FOSİLİNDE FOSİLİ 🦖]",
            "Knifebot": "Bıçak Botu Kullanmış 🤣",
            "Wallhack": "Duvardan Eren Kara'yı (Yani Beni) Görmüş 😈",
            "WallHack": "Duvardan Eren Kara'yı (Yani Beni) Görmüş 😈",
            "OpenGL32 Cheat": "OpenGL32 Hack Bulunmuş [FOSİLİNDE FOSİLİ 🦖]",
            "Aimbot": "Dandik Bir Aimbot Kullanmış 🤣",
            "Found SXE Aim": "Dandik Bir Aimbot Kullanmış 🤣",
            "Found Crystal Hack Data": "Crystal Hile Verisi Bulunmuş [Silememiş Herhalde 😭]",
            "Found Suspicious CFG apex.cfg (alias count: 384) - unknown status": "Apex Cfg Kullanmış 384 Tane Alias Varmış İçinde",
            "Psilentware": "Psilentware Hack Bulunmuş [OOO Güncel / İyi Hile 😈]",
            "Oxware": "Oxware Hack Bulundu [OOO Güncel Hile / İyi Hile 😈]",
            "Found Project-X Rage": "Project-X Rage Hack Bulundu",
            "sPwnage Cheat": "sPwnage Hilesi Bulunmuş",
        }

        for entry in combined_data:
            if entry['nick']:
                found_data = True
                # Rapor verisini kontrol et ve gerekirse değiştir
                for key, message in report_messages.items():
                    if key in entry['report']:
                        entry['report'] = entry['report'].replace(key, message)


                # Embed rengini rapor metnine göre ayarla
                embed_color = discord.Color.dark_blue() if entry['report'] and "ADAM TEMİZ ÇIKMIŞ DAHA NE İSTİYORSUN LAN!" in entry['report'] else discord.Color.red()

                embed = discord.Embed(
                    title=f"İstediğin {entry['nick']} Adındaki Kişinin Bilgileri",
                    color=embed_color
                )

                # Kalın metin için ** işareti kullanın ve verileri alt alta ekleyin
                embed.add_field(
                    name=f"Rapor Bilgileri - {report_id}",
                    value=(
                        f"👤 İSİM: **{entry['nick'] or 'Bilgi Yok'}**\n"
                        f"🆔 Wargods ID [SANSÜRLÜ]: **{entry['unique_id'] or 'Bilgi Yok'}**\n"
                        f"🎮 OYUN ID: **{entry['steam_id'] or 'Bilgi Yok'}**\n"
                        f"🎨 Video Modu: **{entry['render'] or 'Bilgi Yok'}**\n"
                        f"🌐 IP Bilgisi [SANSÜRLÜ]: **{entry['ip_info'] or 'Bilgi Yok'}**\n"
                        f"🏁 Ülke: **{entry['country'] or 'Bilgi Yok'}**\n"
                        f"📋 Rapor: **{entry['report'] or 'Bilgi Yok'}**\n"
                        f"⏰ CS Açılış Saati: **{entry['cs_opened_at'] or 'Bilgi Yok'}**\n"
                        f"🌍 Son Oynadığı Server IP: **{entry['last_server_ip'] or 'Servere Girmeden Önce WG Taratmış'}**\n"
                        f"🕒 Wargods Açılma Tarihi & Zamanı: **{entry['wcd_timestamp'] or 'Bilgi Yok'}**\n"
                        f"🔎 Taratanın Sistem Tarihi & Zamanı **{entry['system_timestamp'] or 'Bilgi Yok'}**\n"
                        f"🕒 Wargods Serverinin Tarihi & Zamanı: **{entry['server_timestamp'] or 'Bilgi Yok'}**\n"
                        f"💻 İşletim Sistemi: **{entry['operating_system'] or 'Bilgi Yok'}**\n"
                        f"📝 Arka Planda Çalışan Uygulamalar: **{entry['processes'] or 'Bilgi Yok'}**\n"
                        f"🔧 Oyun İçinde Çalışan DLL'er: **{entry['modules'] or 'Bilgi Yok'}**\n"
                        f"🗂️ Cstrike (dll/exe/scriptler): **{entry['cstrike'] or 'Bilgi Yok'}**\n"
                        f"📂 Config Dosyaları: **{entry['cfg'] or 'Bilgi Yok'}**\n"
                        f"📁 Modeller/Spriteler: **{entry['resources'] or 'Bilgi Yok'}**"
                    ),
                    inline=False
                )

                await ctx.respond(embed=embed)

        if not found_data:
            await ctx.respond("Rapor Bilgisi Bulunamadı")

def setup(bot):
    bot.add_cog(COMMANDS1(bot))
