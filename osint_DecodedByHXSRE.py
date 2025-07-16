import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
from urllib.parse import urlparse

def search_and_extract(query):
    results = []
    search_engines = [
        ('https://www.google.com/search?q=', 'Google'),
        ('https://www.bing.com/search?q=', 'Bing'),
        ('https://duckduckgo.com/?q=', 'DuckDuckGo'),
        ('https://www.yandex.ru/search/?text=', 'Yandex'),
        ('https://www.ecosia.org/search?q=', 'Ecosia'),
        ('https://search.yahoo.com/search?p=', 'Yahoo'),
        ('https://www.ask.com/web?q=', 'Ask'),
        ('https://www.wolframalpha.com/input/?i=', 'Wolfram Alpha'),
        ('https://www.baidu.com/s?wd=', 'Baidu'),
        ('https://www.ask.com/web?q=', 'Ask'),
        ('https://www.aol.com/search?q=', 'AOL'),
        ('https://www.excite.com/search/?q=', 'Excite'),
        ('https://www.lycos.com/web/search?q=', 'Lycos'),
        ('https://www.metacrawler.com/search?q=', 'MetaCrawler'),
        ('https://www.webcrawler.com/search?q=', 'WebCrawler'),
        ('https://www.dogpile.com/search?q=', 'Dogpile'),
        ('https://search.seznam.cz/search?q=', 'Seznam'),
        ('https://www.startpage.com/do/search?q=', 'Startpage'),
        ('https://www.qwant.com/search?q=', 'Qwant'),
        ('https://www.swisscows.com/en/search?query=', 'Swisscows'),
        ('https://www.gibiru.com/search?q=', 'Gibiru'),
        ('https://www.duckduckgo.com/?q=', 'DuckDuckGo'),
        ('https://www.aport.ru/search/', 'Aport'),
        ('https://www.rambler.ru/search/', 'Rambler'),
        ('https://www.nigma.ru/search/', 'Nigma'),
        ('https://www.sber.ru/search/', 'SberSearch')
    ]
    social_networks = [
        ('https://www.facebook.com/search/top/?q=', 'Facebook'),
        ('https://twitter.com/search?q=', 'Twitter'),
        ('https://www.instagram.com/explore/tags/', 'Instagram'),
        ('https://www.linkedin.com/in/', 'LinkedIn'),
        ('https://vk.com/search?c%5Bsection%5D=people&q=', 'VK'),
        ('https://ok.ru/dk?st.cmd=userSearch&st.q=', 'Одноклассники'),
        ('https://t.me/s/', 'Telegram'),
        ('https://www.youtube.com/results?search_query=', 'YouTube'),
        ('https://www.reddit.com/search?q=', 'Reddit'),
        ('https://www.pinterest.com/search/pins/?q=', 'Pinterest'),
        ('https://www.tiktok.com/search/', 'TikTok'),
        ('https://www.tumblr.com/search/', 'Tumblr'),
        ('https://www.myspace.com/search/', 'MySpace'),
        ('https://www.snapchat.com/add/', 'Snapchat'),
        ('https://www.discord.com/invite/', 'Discord'),
        ('https://www.livejournal.com/users/search?q=', 'LiveJournal'),
        ('https://www.mewe.com/search/', 'MeWe'),
        ('https://www.diaspora.com/directory/', 'Diaspora'),
        ('https://www.mastodon.social/web/accounts/search?q=', 'Mastodon'),
        ('https://www.gab.com/search/', 'Gab'),
        ('https://www.parler.com/search/', 'Parler'),
        ('https://www.minds.com/discover/people/', 'Minds'),
        ('https://www.telegram.me/s/', 'Telegram'),
        ('https://www.whatsapp.com/search/', 'WhatsApp'),
        ('https://www.signal.org/search/', 'Signal'),
        ('https://www.wire.com/en/search', 'Wire'),
        ('https://www.vkontakte.ru/search/', 'ВКонтакте'),
        ('https://www.odnoklassniki.ru/search/', 'Одноклассники'),
        ('https://www.moikrug.ru/search/', 'Мой Круг'),
        ('https://www.linkedin.com/sales/search/', 'LinkedIn Sales Navigator'),
        ('https://www.twitter.com/search/', 'Twitter'),
        ('https://www.facebook.com/search/', 'Facebook')
    ]
    people_search_engines = [
        ('https://www.google.com/search?q=', 'Google People Search'),
        ('https://www.pipl.com/search/?q=', 'Pipl'),
        ('https://www.spokeo.com/search/people/', 'Spokeo'),
        ('https://www.whitepages.com/people/', 'Whitepages'),
        ('https://www.truepeoplesearch.com/people/', 'TruePeopleSearch'),
        ('https://www.beenverified.com/people-search/', 'BeenVerified'),
        ('https://www.intelius.com/people-search/', 'Intelius'),
        ('https://www.zabasearch.com/people/', 'ZabaSearch'),
        ('https://www.fastpeoplesearch.com/', 'FastPeopleSearch'),
        ('https://www.radaris.com/', 'Radaris'),
        ('https://www.peekyou.com/', 'PeekYou'),
        ('https://www.peoplelookup.com/', 'PeopleLookup'),
        ('https://www.findfamily.com/', 'FindFamily'),
        ('https://www.familytreenow.com/', 'FamilyTreeNow'),
        ('https://www.whitepages.com/people/', 'Whitepages'),
        ('https://www.spokeo.com/search/', 'Spokeo')
    ]

    public_records_engines = [
        ('https://www.rusprofile.ru/search/', 'Rusprofile'),
    ]

    for engine_url, engine_name in search_engines + social_networks + people_search_engines + public_records_engines :
        url = engine_url + query
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                search_results = soup.find_all('div', 'g') + soup.find_all('li', 'b_algo') + soup.find_all('div', class_='serp-item__content') + soup.find_all('div', class_='search-result') + soup.find_all('div', class_='person-card') + soup.find_all('div', class_='people-results')

                for result in search_results:
                    link_tag = result.find('a')
                    if link_tag:
                        href = link_tag.get('href')
                        if href:
                            cleaned_url = re.findall('(https?://\\S+)', href)
                            if cleaned_url:
                                title = result.find('h3') or result.find('h2') or  result.find('div', class_='title') or result.find('div', class_='VwiC3b tZESfb r025kc hJNv6b') or result.find('div', class_='VwiC3b') or result.find('p')
                                description_tag =  result.find('span', class_='description')
                                title_text = title.text if title else 'No Title'
                                description_text = description_tag.text if description_tag else 'No Description'
                                results.append({'source': engine_name, 'link': cleaned_url[0], 'title': title_text, 'description': description_text})

        except requests.exceptions.RequestException:
            pass

    extracted_info = defaultdict(list)
    for result in results:
        text_for_extraction = f"{result['title']} {result['description']}"
        names = re.findall(r'\b[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+(?:\s[А-ЯЁ][а-яё]+)?\b', text_for_extraction)
        phones = re.findall(r'\+?\d[\d\-\(\) ]{9,}\d', text_for_extraction)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_for_extraction)
        social_media_links = re.findall(r'(https?://(?:www\.)?(?:facebook|twitter|instagram|linkedin|vk|ok\.ru|t\.me|youtube|wa\.me|tiktok\.com)/[^\\\s]+)', text_for_extraction)
        usernames = re.findall(r'@[a-zA-Z0-9_]{1,15}', text_for_extraction)
        hashtags = re.findall(r'#[a-zA-Z0-9_]{1,15}', text_for_extraction)
        addresses = re.findall(r'\b[А-Яа-я]+\s[А-Яа-я]+(?:\s[А-Яа-я]+)?\b', text_for_extraction)
        cities = re.findall(r'\b[A-ЯЁ][а-яё]+\s*[а-яё]*\s*[А-ЯЁ]?[а-яё]*\b', text_for_extraction)
        birth_dates = re.findall(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', text_for_extraction)
        passport_numbers = re.findall(r'\b[0-9]{4}\s?[0-9]{6}\b', text_for_extraction)
        car_numbers = re.findall(r'\b[AА-ЯЁ]{1}[0-9]{3}[A-ЯЁ]{2,3}\b', text_for_extraction)
        geo_locations = re.findall(r'\b-?\d{1,3}\.\d{4},?\s*-?\d{1,3}\.\d{4}\b|\b-?\d{1,3}\.\d{4}\s-?\d{1,3}\.\d{4}\b', text_for_extraction)

        extracted_info['names'].extend(names)
        extracted_info['phones'].extend(phones)
        extracted_info['emails'].extend(emails)
        extracted_info['social_media'].extend(social_media_links)
        extracted_info['usernames'].extend(usernames)
        extracted_info['hashtags'].extend(hashtags)
        extracted_info['addresses'].extend(addresses)
        extracted_info['cities'].extend(cities)
        extracted_info['birth_dates'].extend(birth_dates)
        extracted_info['passport_numbers'].extend(passport_numbers)
        extracted_info['car_numbers'].extend(car_numbers)
        extracted_info['geo_locations'].extend(geo_locations)

    print("\nНайденные результаты:")
    for result in results:
        print(f"\nИсточник: {result['source']}")
        print(f"\nСсылка: {result['link']}")
        print(f"\nЗаголовок: {result['title']}")
        print(f"\nОписание: {result['description']}\n")

    print("\n\nКлючевая информация:")
    for key, values in extracted_info.items():
        if values:
            print(f"\n{key.capitalize()}: {', '.join(values)}")

    with open('results.txt', 'w', encoding='utf-8') as f:
        f.write("Найденные результаты:\n")
        for result in results:
            f.write(f"\nИсточник: {result['source']}\n")
            f.write(f"\nСсылка: {result['link']}\n")
            f.write(f"\nЗаголовок: {result['title']}\n")
            f.write(f"\nОписание: {result['description']}\n")
        f.write("\n\nКлючевая информация:\n")
        for key, values in extracted_info.items():
            if values:
                f.write(f"\n{key.capitalize()}: {', '.join(values)}\n")


    print('Результаты были сохранены в results.txt')


if __name__ == '__main__':
    while True:
        query_type = input("Введите тип запроса (ФИО, номер, почта, и т.д.) или 'exit' для выхода: ")
        if query_type.lower() == 'exit':
            break
        search_and_extract(query_type)