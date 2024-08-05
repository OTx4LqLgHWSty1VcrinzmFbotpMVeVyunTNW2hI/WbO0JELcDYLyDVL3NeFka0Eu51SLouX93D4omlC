import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup


integration_types = {
    discord.IntegrationType.guild_install,
    discord.IntegrationType.user_install,
}

class COMMANDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='wargods', description='Güncel Hilecileri Göster Lan!!!',
    integration_types=integration_types)
    async def wargods(self, ctx):
        # Define the URL
        url = 'https://www.wargods.ro/wcd/index.php'

        # Send a GET request to the URL
        response = requests.get(url)

        if response.status_code != 200:
            await ctx.respond(f"Bilgi çekilemedi: {response.status_code}")
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table in the HTML
        table = soup.find('table')

        if not table:
            await ctx.respond("Tablo bulunamadı")
            return

        # Extract table rows
        rows = []
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) > 0:
                if 'cheat' in row.get('class', []):
                    game_img_tag = cells[0].find('img')
                    game_info = "Unknown"
                    if game_img_tag and 'src' in game_img_tag.attrs:
                        game_img_src = game_img_tag['src']
                        if 'style/images/icons/steam.png' in game_img_src:
                            game_info = 'ORİJİNAL - STEAM'
                        elif 'style/images/icons/cs.png' in game_img_src:
                            game_info = 'KAÇAK - NonSteam'

                    nick_link = cells[1].find('a')
                    nick = "Bilinmiyor"
                    report_url = "Bilinmiyor"
                    unique_id = "Bilinmiyor"
                    last_played_servers = "Servere Girmeden Önce WG Taratmış"
                    steam_idd = "Bilinmiyor"

                    if nick_link:
                        nick = nick_link.get_text(strip=True)
                        report_url = f"https://www.wargods.ro/wcd/{nick_link['href']}"
                        report_response = requests.get(report_url)
                        if report_response.status_code == 200:
                            report_soup = BeautifulSoup(report_response.text, 'html.parser')
                            report_div = report_soup.find('div', id='report')
                            if report_div:
                                unique_id_div = report_div.find('div', class_='reporttagcheat', string="Unique ID: ")
                                if unique_id_div:
                                    unique_id = unique_id_div.find_next_sibling('div', class_='reportq').get_text(strip=True)

                                last_server_ip_div = report_div.find('div', class_='reporttagcheat', string="Last Server IP:")
                                if last_server_ip_div:
                                    last_played_servers = last_server_ip_div.find_next_sibling('div', class_='reportq').get_text(strip=True)

                                steam_id_div = report_div.find('div', class_='reporttagcheat', string="Type (Steam/NonSteam):")
                                if steam_id_div:
                                    steam_idd = steam_id_div.find_next_sibling('div', class_='reportq').get_text(strip=True)

                    ip_text = cells[2].get_text(strip=True)
                    report = cells[3].get_text(strip=True)
                    timestamp_td = cells[4]
                    detection = cells[5].get_text(strip=True)

                    flag_img_tag = cells[2].find('img', {'style': 'display:inline-block;vertical-align:sub;'})
                    country = "Bilinmiyor"
                    if flag_img_tag and 'title' in flag_img_tag.attrs:
                        country = flag_img_tag['title']

                    date_part = "Bilinmiyor"
                    time_part = "Bilinmiyor"

                    if timestamp_td:
                        br_tags = timestamp_td.find_all('br')
                        if len(br_tags) == 1:
                            date_part = timestamp_td.get_text(separator='|').split('|')[0].strip()
                            time_part = timestamp_td.get_text(separator='|').split('|')[1].strip()

                    if country == "Romania":
                        country = "Romanya"
                    if country == "Greece":
                        country = "Yunanistan"
                    if country == "Lithuania":
                        country = "Litvanya"
                    if country == "United Kingdom":
                        country = "İngiltere"
                    if country == "Russia":
                        country = "Rusya"
                    if country == "Egypt":
                        country = "Mısır"
                    if country == "Ukraine":
                        country = "Ukrayna"
                    if country == "Algeria":
                        country = "Cezayir"
                    if country == "Albania":
                        country = "Arnavutluk"
                    if country == "Serbia":
                        country = "Sırbistan"
                    if country == "Germany":
                        country = "Almanya"
                    if country == "Bulgaria":
                        country = "Bulgaristan"
                    if country == "Bosnia and Herzegovina":
                        country = "Bosna Hersek"
                    if country == "Ireland":
                        country = "İrlanda"
                    if country == "Sweden":
                        country = "İsveç"
                    if country == "Switzerland":
                        country = "İsviçre"
                    if country == "Hungary":
                        country = "Macaristan"
                    if country == "Kazakhstan":
                        country = "Kazakistan"
                    if country == "Uzbekistan":
                        country = "Özbekistan"
                    if country == "France":
                        country = "Fransa"
                    if country == "Poland":
                        country = "Polonya"

                    if report == "Found Vermillion":
                        report = "Vermillion Hack Bulundu [Yıl Kaç? 👴]"
                    elif report == "Found Big CFG - unknown status":
                        report = "Büyük Bir CFG Var Adamda Sıkıntılı"
                    elif report == "Alternative" or report == "Found Alternative" or report == "AlterNative":
                        report = "Alternative Hack Bulundu [Sanki Biraz Eskidi Gibi 🤔]"
                    elif report == "Generic Cheat Detection":
                        report = "Wargods Daha İsim Koyamamis Nası Bi Hileyse"
                    elif report == "Found Oxware Data":
                        report = "Oxware Hack Bulundu [OOO Güncel Hile 😈]"
                    elif report == "Riscript Injector":
                        report = "Dandik İnjektörlerden İyidir | Riscript Injector"
                    elif report == "Found Injector":
                        report = "İsimsiz Dandik İnjektor Kullanmış 🤣"
                    elif report == "Cheat Model" or report == "Cheat model":
                        report = "Karakter Modellerini Değiştirmiş 🤦‍♂️"
                    elif report == "Found Super Simple Wallhack":
                        report = "Çok Basit Wallhack [Kendi Yapmış Olabilir Heee 😍]"
                    elif report == "Found HPP Hack Data":
                        report = "HPP Hilesinin Verisi Bulunmuş [Silememiş Herhalde 😭]"    
                    elif report == "Found HPP CFG Data":
                        report = "HPP Hilesinin CFG Dosyası Bulunmuş [Silememiş Herhalde 😭]"
                    elif report == "Found HPP Hack":
                        report = "HPP Hack Bulunmuş [OOO İyi Hile 😈]"
                    elif report == "Found Extreme Injector":
                        report = "Extreme Injector Kullanmış"
                    elif report == "Found BunnyHop CFG - unknown status":
                        report = "Bunny CFG Bulunmuş [Demekki Düz Hızlanan Buymuş 😡]"
                    elif report == "Found Leis":
                        report = "Leis Hack Bulunmuş [FOSİLİNDE FOSİLİ 🦖]"
                    elif report == "Knifebot":
                        report = "Bıçak Botu Kullanmış 🤣"
                    elif report == "Wallhack":
                        report = "Duvardan Eren Kara'yı (Yani Beni) Görmüş 😈"
                    elif report == "OpenGL32 Cheat":
                        report = "OpenGL32 Hack Bulunmuş [FOSİLİNDE FOSİLİ 🦖]"
                    elif report == "Aimbot" or report == "Found SXE Aim":
                        report = "Dandik Bir Aimbot Kullanmış 🤣"
                    elif report == "Found Crystal Hack Data":
                        report = "Crystal Hile Verisi Bulunmuş [Silememiş Herhalde 😭]"
                    elif report == "Found Suspicious CFG apex.cfg (alias count: 384) - unknown status":
                        report = "Apex Cfg Kullanmış 384 Tane Alias Varmış İçinde"
                       

                    detection_status = "belli degil"
                    if detection == "Yes":
                        detection_status = "kirli"
                    elif detection == "No":
                        detection_status = "temiz"

                    # Set ID display based on Steam/NonSteam type
                    if "NonSteam" in steam_idd:
                        id_display = "**Kaçak Olduğu için, Wargods İzin Vermiyor Bakmama 😭**"
                    else:
                        id_display = f"**{steam_idd}**"

                    rows.append({
                        'Nick': f"**{nick}**",
                        'Game': f"**{game_info}**",
                        'ID': id_display,
                        'Server': f"**{last_played_servers}**",
                        'IP': f"**{ip_text}**",
                        'Country': f"**{country}**",
                        'Report': f"**{report}**",
                        'Date': f"**{date_part}**",
                        'Time': f"**{time_part}**",
                        'Detection before': f"**{detection_status}**",
                        'Report URL': f"**{report_url}**",
                    })

        if rows:
            embed = discord.Embed(
                title="HILE SAVAR - EREN KARA",
                description="-------------------------------------------------------------------------------",
                color=discord.Color.brand_red(),
                thumbnail="https://wargods.ro/wcd/wcd.ico"
            )

            for row in rows:
                embed.add_field(
                    name=f"**İSİM**: {row['Nick']}",
                    value=(
                        f"**OYUN**: {row['Game']}\n"
                        f"**İD**: {row['ID']}\n"
                        f"**EN SON OYNADIĞI SERVER**: {row['Server']}\n"
                        f"**İP [SANSÜRLÜ]**: {row['IP']}\n"
                        f"**ÜLKE**: {row['Country']}\n"
                        f"**GÜNAHI**: {row['Report']}\n"
                        f"**TARİH**: {row['Date']}\n"
                        f"**SAAT**: {row['Time']}\n"
                        f"**SİCİLİ**: {row['Detection before']}\n"
                        f"**BÜTÜN BİLGİLERİ**: {row['Report URL']}\n"
                        "-------------------------------------------------------------------------------"
                    ),
                    inline=False
                )

            await ctx.respond(embed=embed)
        else:
            # Create an embed for when no data is found
            no_data_embed = discord.Embed(
                title="ŞUANLIK RADARIMA GIREN KIMSE YOK. SONRA GEL",
                color=discord.Color.blue(),
                image="https://pbs.twimg.com/media/CF-DYiaWMAAQCci.jpg"
            )
            await ctx.respond(embed=no_data_embed)

def setup(client):
    client.add_cog(COMMANDS(client))
